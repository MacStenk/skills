#!/usr/bin/env python3
"""kanalbeitrag.py: einen Beitragstext für einen Telegram-Kanal prüfen, rendern, senden, gegenlesen.

Ohne Konto nutzbar: Rendern und Prüfen laufen lokal, das Gegenlesen holt die öffentliche
Vorschau des Kanals (t.me/s/). Senden, Berichtigen und Löschen brauchen einen Bot, also einen
Schlüssel (TELEGRAM_BOT_TOKEN), und das Ziel (TELEGRAM_CHANNEL oder --kanal).

Aufrufe:
    kanalbeitrag.py beitrag.md                       rendern und prüfen (kein Konto nötig)
    kanalbeitrag.py beitrag.md --gegenlesen @kanal   öffentliche Vorschau prüfen (kein Konto nötig)
    kanalbeitrag.py beitrag.md --senden              über den Bot senden
    kanalbeitrag.py beitrag.md --bearbeiten 42       Beitrag 42 durch den neuen Text ersetzen
    kanalbeitrag.py beitrag.md --loeschen 42         Beitrag 42 entfernen
    kanalbeitrag.py bild.png --bild bild.png         Kanalbild setzen
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

GRENZE_NACHRICHT = 4096
GRENZE_KOPFZEILE = 120
GRENZE_BILD_BYTE = 5 * 1024 * 1024
ERLAUBTE_TAGS = {
    "b", "strong", "i", "em", "u", "ins", "s", "strike", "del",
    "a", "code", "pre", "blockquote", "span", "tg-spoiler", "tg-emoji",
}
URL_MUSTER = re.compile(r"https?://[^\s)>\]]+")


def html_flucht(text: str) -> str:
    """Im HTML-Modus von Telegram müssen nur diese drei Zeichen maskiert werden."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linkifizieren(text: str) -> str:
    """Nackte Adressen zu echten Links machen, sichtbar bleibt die Adresse ohne Schema."""
    def ersatz(treffer: re.Match) -> str:
        adresse = treffer.group(0)
        sichtbar = re.sub(r"^https?://(?:www\.)?", "", adresse)
        return f'<a href="{adresse}">{sichtbar}</a>'

    return URL_MUSTER.sub(ersatz, text)


def inhalt_ohne_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def rendern(rohtext: str) -> str:
    """Aus einer Notiz einen Beitrag bauen: Kopfzeile fett, Einordnung kursiv, Quellen verlinkt.

    Erwartete Form: erste Zeile ist die Kopfzeile, danach der Text, am Ende eine Zeile, die mit
    "Quelle" beginnt. Absätze werden durch Leerzeilen getrennt. Der letzte Absatz vor der
    Quellzeile gilt als Einordnung und wird kursiv gesetzt. Die Kopfzeile bleibt auch dann
    allein, wenn direkt darunter ohne Leerzeile weitergetextet wurde.
    """
    zeilen = rohtext.strip().split("\n")
    kopf = " ".join(zeilen[0].split())
    rest = "\n".join(zeilen[1:])
    if not kopf:
        return ""

    absaetze = [" ".join(a.split()) for a in re.split(r"\n\s*\n", rest) if a.strip()]
    teile = [f"<b>{html_flucht(kopf)}</b>"]

    quelle = None
    if absaetze and re.match(r"^quelle\b", absaetze[-1], re.IGNORECASE):
        quelle = absaetze[-1]
        absaetze = absaetze[:-1]

    for i, absatz in enumerate(absaetze):
        inhalt = linkifizieren(html_flucht(absatz))
        if (len(absaetze) > 1 or quelle) and i == len(absaetze) - 1:
            inhalt = f"<i>{inhalt}</i>"
        teile.append(inhalt)

    if quelle:
        teile.append(linkifizieren(html_flucht(quelle)))
    return "\n\n".join(teile)


def pruefen(html: str, rohtext: str) -> tuple[list[str], list[str]]:
    """Nachzählen statt urteilen: Länge, Tags, Maskierung sind Fehler; Form ist Hinweis.

    Fehler blockieren das Senden, weil die Schnittstelle den Beitrag sonst ganz abweist.
    Hinweise sind Geschmack und Form und halten niemanden auf.
    """
    fehler: list[str] = []
    hinweise: list[str] = []
    sichtbar = inhalt_ohne_tags(html)

    if len(sichtbar) > GRENZE_NACHRICHT:
        fehler.append(f"Zu lang: {len(sichtbar)} Zeichen sichtbar, erlaubt sind {GRENZE_NACHRICHT}.")
    if not sichtbar.strip():
        fehler.append("Der Beitrag ist leer.")

    unbekannt = {
        t.split()[0].lower().lstrip("/")
        for t in re.findall(r"<(/?[A-Za-z][^>]*)>", html)
        if t.split()[0].lower().lstrip("/") not in ERLAUBTE_TAGS
    }
    if unbekannt:
        fehler.append(
            "Nicht erlaubte Auszeichnung: " + ", ".join(sorted(f"<{t}>" for t in unbekannt))
            + ". Telegram kennt nur: " + ", ".join(sorted(ERLAUBTE_TAGS)) + "."
        )

    # Alles, was wie ein Tag aussieht, muss auch eines der erlaubten sein. Sonst wurde
    # entweder nicht maskiert oder ein Tag falsch geschrieben, und die API weist den
    # ganzen Beitrag mit "can't parse entities" ab.
    if re.search(r"<(?!/?(?:%s)[\s>/])" % "|".join(sorted(ERLAUBTE_TAGS)), html):
        fehler.append(
            "Unmaskierte spitze Klammer oder unbekanntes Tag im Text. Im HTML-Modus müssen "
            "< als &lt; und > als &gt; geschrieben werden."
        )

    if re.search(r"</?[A-Za-z]", rohtext):
        fehler.append(
            "Im Rohtext stehen spitze Klammern. Die Datei enthält Klartext, die Auszeichnung setzt "
            "dieses Skript. Ein mitgebrachtes Tag erscheint sonst als Text im Beitrag."
        )

    kopf = inhalt_ohne_tags(html.split("\n")[0])
    if len(kopf) > GRENZE_KOPFZEILE:
        hinweise.append(
            f"Kopfzeile {len(kopf)} Zeichen. In Benachrichtigungen wird sie abgeschnitten, "
            f"halte sie unter {GRENZE_KOPFZEILE}."
        )

    zeilen = rohtext.strip().split("\n")
    if len(zeilen) < 2 or not "\n".join(zeilen[1:]).strip():
        hinweise.append("Nur eine Kopfzeile, kein Text darunter. Ein Beitrag braucht einen Satz dazu.")
    if not re.search(r"^quelle\b", rohtext, re.IGNORECASE | re.MULTILINE):
        hinweise.append("Keine Quellzeile gefunden. Bei Funden gehören Quelle und Datum in den Beitrag.")
    return fehler, hinweise


def bild_messen(pfad: str) -> list[str]:
    """Maße und Größe des Kanalbildes nachzählen. Was gemessen wird, muss niemand schätzen."""
    befunde: list[str] = []
    groesse = os.path.getsize(pfad)
    if groesse > GRENZE_BILD_BYTE:
        befunde.append(
            f"Bild {groesse // 1024} KB. Telegram nimmt Chatbilder nur bis "
            f"{GRENZE_BILD_BYTE // (1024 * 1024)} MB."
        )
    try:
        from PIL import Image  # nur wenn vorhanden, sonst bleibt es beim Byte-Vergleich

        with Image.open(pfad) as bild:
            breite, hoehe = bild.size
            print(f"Bild: {breite} x {hoehe} px, {groesse // 1024} KB, {bild.mode}")
            if breite != hoehe:
                befunde.append(
                    f"Bild ist {breite} x {hoehe}, nicht quadratisch. Telegram schneidet rund zu, "
                    "der Rand verschwindet."
                )
            if breite < 512:
                befunde.append(f"Nur {breite} px breit. Unter 512 px wird das Bild im Kanal unscharf.")
    except ImportError:
        print(f"Bild: {groesse // 1024} KB (Pillow fehlt, Maße ungeprüft)")
    except Exception as fehler:
        befunde.append(f"Bild konnte nicht gelesen werden: {fehler}")
    return befunde


def vorschau_holen(kanal: str) -> str:
    name = kanal.lstrip("@")
    adresse = f"https://t.me/s/{urllib.parse.quote(name)}"
    anfrage = urllib.request.Request(adresse, headers={"User-Agent": "Mozilla/5.0 (kanalbeitrag)"})
    with urllib.request.urlopen(anfrage, timeout=30) as antwort:
        return antwort.read().decode("utf-8", errors="ignore")


def gegenlesen(kanal: str, sucher: list[str]) -> list[str]:
    """Die öffentliche Vorschau prüfen: greifen die Auszeichnungen, und wurde nicht doppelt maskiert?"""
    befunde: list[str] = []
    seite = vorschau_holen(kanal)
    if "<b>" not in seite and "<strong>" not in seite:
        befunde.append("Keine fette Auszeichnung in der Vorschau: entweder kein Beitrag da oder ohne HTML gesendet.")
    if "<a href" not in seite:
        befunde.append("Kein echter Link in der Vorschau: die Adresse steht als Text, nicht als Link.")
    if "&lt;b&gt;" in seite or "&lt;a href" in seite:
        befunde.append("Auszeichnungen stehen als Text in der Vorschau: zweimal maskiert, das war ein Fehler.")
    for wort in sucher:
        if wort and wort not in seite:
            befunde.append(f"„{wort}“ steht nicht in der Vorschau. Beitrag noch nicht sichtbar oder Text weicht ab.")
    return befunde


def _antwort(adresse: str, daten: bytes, kopfzeilen: dict) -> dict:
    anfrage = urllib.request.Request(adresse, data=daten, headers=kopfzeilen)
    try:
        with urllib.request.urlopen(anfrage, timeout=60) as antwort:
            return json.loads(antwort.read().decode())
    except urllib.error.HTTPError as fehler:
        try:
            return json.loads(fehler.read().decode())
        except Exception:
            return {"ok": False, "description": f"HTTP {fehler.code}"}
    except Exception as fehler:  # Netz weg, Zeitüberschreitung
        return {"ok": False, "description": f"Netzfehler: {fehler}"}


def bot_aufruf(token: str, methode: str, **felder) -> dict:
    daten = urllib.parse.urlencode({k: v for k, v in felder.items() if v is not None}).encode()
    return _antwort(f"https://api.telegram.org/bot{token}/{methode}", daten, {})


def bot_datei(token: str, methode: str, feldname: str, pfad: str, **felder) -> dict:
    """Datei hochladen. Ohne Fremdpaket wird der mehrteilige Körper von Hand gebaut."""
    grenze = "kanalbeitrag" + uuid.uuid4().hex
    teile: list[bytes] = []
    for name, wert in felder.items():
        if wert is None:
            continue
        teile.append(f'--{grenze}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{wert}\r\n'.encode())
    dateiname = os.path.basename(pfad)
    teile.append(
        f'--{grenze}\r\nContent-Disposition: form-data; name="{feldname}"; filename="{dateiname}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n".encode()
    )
    with open(pfad, "rb") as datei:
        teile.append(datei.read())
    teile.append(f"\r\n--{grenze}--\r\n".encode())
    return _antwort(
        f"https://api.telegram.org/bot{token}/{methode}",
        b"".join(teile),
        {"Content-Type": f"multipart/form-data; boundary={grenze}"},
    )


def ziel_und_schluessel(argument: str | None) -> tuple[str | None, str | None]:
    return os.environ.get("TELEGRAM_BOT_TOKEN"), argument or os.environ.get("TELEGRAM_CHANNEL")


def main() -> int:
    p = argparse.ArgumentParser(description="Beitragstext für einen Telegram-Kanal prüfen, rendern, senden")
    p.add_argument("datei", help="Textdatei mit dem Beitrag; beim Kanalbild die Bilddatei")
    p.add_argument("--gegenlesen", metavar="@kanal", help="öffentliche Vorschau prüfen (kein Konto nötig)")
    p.add_argument("--senden", action="store_true", help="über den Bot senden (braucht Schlüssel)")
    p.add_argument("--bearbeiten", type=int, metavar="ID", help="bestehenden Beitrag durch den neuen Text ersetzen")
    p.add_argument("--loeschen", type=int, metavar="ID", help="bestehenden Beitrag entfernen")
    p.add_argument("--bild", metavar="DATEI", help="Kanalbild setzen; ein Textbeitrag wird dazu nicht gebraucht")
    p.add_argument("--kanal", help="Ziel, Vorgabe aus TELEGRAM_CHANNEL")
    p.add_argument("--titel", help="Textbaustein, der in der Vorschau vorkommen muss, wenn vorhanden")
    p.add_argument("--trocken", action="store_true", help="nur zeigen, was geschehen würde")
    args = p.parse_args()

    if args.bild:
        print("=== Kanalbild ===")
        befunde = bild_messen(args.bild)
        for befund in befunde:
            print(f"Fehler: {befund}")
        if args.trocken:
            print("Trockenlauf: nichts gesetzt.")
            return 0 if not befunde else 4
        if befunde:
            print("Nicht gesetzt. Erst das Bild berichtigen.")
            return 4
        token, ziel = ziel_und_schluessel(args.kanal)
        if not token or not ziel:
            print("Zum Setzen fehlen TELEGRAM_BOT_TOKEN und TELEGRAM_CHANNEL.")
            return 3
        antwort = bot_datei(token, "setChatPhoto", "photo", args.bild, chat_id=ziel)
        if not antwort.get("ok"):
            print(f"Setzen fehlgeschlagen: {antwort.get('description')}")
            if "not enough rights" in str(antwort.get("description", "")):
                print("Dem Bot fehlt im Kanal das Recht, die Info zu ändern.")
            return 5
        print("Kanalbild gesetzt.")
        return 0

    rohtext = open(args.datei, encoding="utf-8").read()
    html = rendern(rohtext)
    if not html:
        print("Der Beitrag ist leer. Nichts zu tun.")
        return 2

    print("=== Gerenderter Beitrag ===")
    print(html)
    print()
    print("=== Nachgezählt ===")
    sichtbar = inhalt_ohne_tags(html)
    print(f"{len(sichtbar)} Zeichen sichtbar (erlaubt {GRENZE_NACHRICHT}), {len(html)} Zeichen mit Auszeichnung")

    fehler, hinweise = pruefen(html, rohtext)
    for befund in fehler:
        print(f"Fehler: {befund}")
    for befund in hinweise:
        print(f"Hinweis: {befund}")
    if not fehler and not hinweise:
        print("Keine Beanstandung.")

    if args.gegenlesen:
        print()
        print(f"=== Vorschau von {args.gegenlesen} ===")
        sucher = [args.titel] if args.titel else []
        beanstandungen = gegenlesen(args.gegenlesen, sucher)
        for befund in beanstandungen:
            print(f"Achtung: {befund}")
        if not beanstandungen:
            print("Vorschau sieht gut aus: fette Auszeichnung und echte Links sind da.")

    if args.trocken:
        print()
        print(f"Trockenlauf: nichts gesendet. Ziel wäre {args.kanal or os.environ.get('TELEGRAM_CHANNEL') or '(kein Ziel gesetzt)'}.")
        return 0 if not fehler else 4

    if args.senden or args.bearbeiten or args.loeschen:
        token, ziel = ziel_und_schluessel(args.kanal)
        if not token or not ziel:
            print()
            print("Dafür fehlen TELEGRAM_BOT_TOKEN und TELEGRAM_CHANNEL. Ohne Schlüssel bleibt es beim Prüfen.")
            return 3
        if fehler and not args.loeschen:
            print()
            print("Nicht gesendet, solange Fehler offen sind. Erst den Text berichtigen.")
            return 4

        if args.loeschen:
            antwort = bot_aufruf(token, "deleteMessage", chat_id=ziel, message_id=args.loeschen)
            if not antwort.get("ok"):
                print(f"Löschen fehlgeschlagen: {antwort.get('description')}")
                return 5
            print(f"Beitrag {args.loeschen} entfernt.")
            return 0

        if args.bearbeiten:
            antwort = bot_aufruf(
                token, "editMessageText",
                chat_id=ziel, message_id=args.bearbeiten, text=html, parse_mode="HTML",
            )
            if not antwort.get("ok"):
                print(f"Berichtigen fehlgeschlagen: {antwort.get('description')}")
                if "message to edit not found" in str(antwort.get("description", "")):
                    print("Diese Nummer gibt es im Ziel nicht. Nachsehen: getChat, dann die Vorschau lesen.")
                return 5
            print(f"Beitrag {args.bearbeiten} ersetzt, {len(antwort.get('result', {}).get('text', ''))} Zeichen laut Antwort.")
            print(f"Nächster Schritt: gegenlesen mit --gegenlesen {ziel}")
            return 0

        antwort = bot_aufruf(token, "sendMessage", chat_id=ziel, text=html, parse_mode="HTML")
        if not antwort.get("ok"):
            print(f"Senden fehlgeschlagen: {antwort.get('description')}")
            if "not a member" in str(antwort.get("description", "")):
                print("Der Bot ist nicht im Kanal. Aus dem eigenen Konto als Administrator hinzufügen.")
            return 5
        ergebnis = antwort.get("result", {})
        print()
        print(f"Gesendet: message_id {ergebnis.get('message_id')} an {ergebnis.get('chat', {}).get('title') or ziel}")
        print(f"Nächster Schritt: Vorschau gegenlesen: kanalbeitrag.py {args.datei} --gegenlesen {ziel}")
        return 0

    print()
    if fehler:
        print("Nächster Schritt: Fehler berichtigen, dann erneut prüfen.")
    elif hinweise:
        print("Nächster Schritt: Hinweise abwägen, dann senden mit --senden (Schlüssel nötig)")
        print("oder erst öffentlich gegenlesen mit --gegenlesen @kanalname.")
    else:
        print("Nächster Schritt: senden mit --senden (Schlüssel nötig) oder erst öffentlich gegenlesen")
        print("mit --gegenlesen @kanalname.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
