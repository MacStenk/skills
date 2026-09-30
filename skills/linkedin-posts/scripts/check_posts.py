#!/usr/bin/env python3
"""Mechanische Prüfung der LinkedIn-Posts aus dem Skill linkedin-posts.

Aufruf:
    python3 check_posts.py entwurf.txt --profil ~/linkedin-posts/profil.json
    pbpaste | python3 check_posts.py --profil ~/linkedin-posts/profil.json

    python3 check_posts.py entwurf.txt --art fakten

Ohne --profil wird $LINKEDIN_POSTS_DIR/profil.json gesucht, sonst
~/linkedin-posts/profil.json. Die CTA-Zeile kommt aus dem Feld "cta".
Mit --art fakten kommt die Schlusszeile aus dem Feld "schluss_fakten"
(leer = keine Schlusszeile), und jede Version braucht eine Jahreszahl.

Exit-Code 0 = alles OK, 1 = mindestens eine Version fällt durch.
"""
import argparse
import json
import os
import re
import sys

CTA = None  # wird aus profil.json gesetzt
ART = "angebot"  # oder "fakten", per --art
EXPECTED_BLOCKS = 3
WORD_BUDGET = (125, 155)
MAX_CHARS = 1200
MAX_HOOK_CHARS = 120
MAX_HOOK_WORDS = 16
MAX_BOLD = 3
MAX_HASHTAGS = 3

# Wortanfänge: "krise" trifft auch "Krisen", "Krisenmodus"
ESCALATION = ["krise", "bedroh", "abgehängt", "weckruf", "überleb", "kollaps",
              "zusammenbruch", "krieg"]

FLOSKELN = ["in der heutigen zeit", "entscheidend", "bahnbrechend", "wertvoll",
            "nahtlos", "transformativ", "gamechanger", "game changer",
            "revolutionär", "lass uns eintauchen", "lassen sie uns eintauchen",
            "abschließend", "in diesem beitrag", "in diesem post"]

REFRAMES = [
    (r"\bnicht\b[^.!?\n]{0,60}\bsondern\b", "„nicht X, sondern Y“"),
    (r"\bes geht nicht (um|darum)\b", "„es geht nicht um X“"),
    (r"\bweniger\b[^.!?\n]{0,40}\bmehr\b", "„weniger X, mehr Y“"),
]

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]")
HASHTAG = re.compile(r"(?<![\w/])#\w+")
BOLD = re.compile(r"\*\*(.+?)\*\*")
DASH = re.compile(r"—| – ")
YEAR = re.compile(r"\b(19|20)\d{2}\b")


def parse(text):
    """Liefert Liste von (version, body)."""
    blocks, version, active, buf = [], "?", False, []

    def flush():
        if active and buf:
            blocks.append((version, "\n".join(buf).strip()))

    for line in text.splitlines():
        s = line.strip()
        if s.upper().startswith("VERSION"):
            flush()
            version, active, buf = s, False, []
        elif s == "DE":
            flush()
            active, buf = True, []
        elif active:
            buf.append(line)
    flush()
    return blocks


def check(body):
    problems = []
    lines = [l for l in body.splitlines() if l.strip()]
    if not lines:
        return ["Version ist leer"], 0, 0

    hook = lines[0].strip()
    if len(hook.split()) > MAX_HOOK_WORDS:
        problems.append(f"Hook {len(hook.split())} Wörter (max. {MAX_HOOK_WORDS})")
    if len(hook) > MAX_HOOK_CHARS:
        problems.append(f"Hook {len(hook)} Zeichen (max. {MAX_HOOK_CHARS})")

    if len(body) > MAX_CHARS:
        problems.append(f"{len(body)} Zeichen (max. {MAX_CHARS})")

    # Wortzahl ohne CTA-Zeile und reine Hashtag-Zeilen
    content = [l for l in lines
               if not l.strip().startswith("→")
               and not all(HASHTAG.fullmatch(t) for t in l.split())]
    words = len(" ".join(content).split())
    lo, hi = WORD_BUDGET
    if not lo <= words <= hi:
        problems.append(f"{words} Wörter (Budget {lo}–{hi})")

    text = body.replace(CTA, "") if CTA else body
    low = text.lower()

    if ART == "fakten" and not YEAR.search(text):
        problems.append("Keine Jahreszahl gefunden (Quelle mit Jahr nennen)")

    for term in ESCALATION:
        if re.search(r"\b" + re.escape(term), low):
            problems.append(f"Eskalationswort: „{term}“")

    for term in FLOSKELN:
        if re.search(r"\b" + re.escape(term), low):
            problems.append(f"Floskel: „{term}“")

    for pattern, name in REFRAMES:
        m = re.search(pattern, low)
        if m:
            problems.append(f"Gegenüberstellung {name}: „{m.group(0)}“")

    if DASH.search(text):
        problems.append("Langer Gedankenstrich im Text")

    if "?" in text:
        problems.append("Fragezeichen gefunden (Risikoanker prüfen)")

    bold = BOLD.findall(body)
    if len(bold) > MAX_BOLD:
        problems.append(f"{len(bold)} Fett-Begriffe (max. {MAX_BOLD}): {bold}")

    tags = HASHTAG.findall(body)
    if len(tags) > MAX_HASHTAGS:
        problems.append(f"{len(tags)} Hashtags (max. {MAX_HASHTAGS})")

    emoji = EMOJI.findall(body)
    if emoji:
        problems.append(f"Emoji gefunden: {''.join(emoji)}")

    if CTA and lines[-1].strip() != CTA:
        name = "Schlusszeile" if ART == "fakten" else "CTA"
        problems.append(f"{name} fehlt oder weicht ab (muss letzte Zeile sein)")

    return problems, len(body), words


def load_profil(path, art="angebot"):
    if not path:
        base = os.environ.get("LINKEDIN_POSTS_DIR",
                              os.path.expanduser("~/linkedin-posts"))
        path = os.path.join(base, "profil.json")
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            profil = json.load(f)
    except FileNotFoundError:
        sys.exit(f"profil.json nicht gefunden: {path}")
    if art == "fakten":
        schluss = (profil.get("schluss_fakten") or "").strip()
        if "[BITTE AUSFÜLLEN" in schluss:
            sys.exit(f"schluss_fakten in {path} ist noch nicht ausgefüllt")
        return schluss or None
    cta = (profil.get("cta") or "").strip()
    if not cta:
        sys.exit(f"Feld \"cta\" fehlt oder ist leer in {path}")
    if "[BITTE AUSFÜLLEN" in cta:
        sys.exit(f"CTA in {path} ist noch nicht ausgefüllt")
    return cta


def main():
    global CTA, ART
    ap = argparse.ArgumentParser(description="LinkedIn-Posts mechanisch prüfen")
    ap.add_argument("datei", nargs="?", help="Entwurf (ohne Angabe: stdin)")
    ap.add_argument("--profil", help="Pfad zu profil.json")
    ap.add_argument("--art", choices=["angebot", "fakten"], default="angebot",
                    help="angebot (Standard) oder fakten")
    args = ap.parse_args()
    ART = args.art
    CTA = load_profil(args.profil, args.art)
    text = open(args.datei, encoding="utf-8").read() if args.datei \
        else sys.stdin.read()
    blocks = parse(text)
    if len(blocks) != EXPECTED_BLOCKS:
        print(f"Warnung: {len(blocks)} Versionen gefunden, erwartet {EXPECTED_BLOCKS}")

    failed = 0
    for version, body in blocks:
        problems, chars, words = check(body)
        status = "OK" if not problems else "FEHLER"
        print(f"{version[:9]:9}  {chars:5} Zeichen  {words:3} Wörter  {status}")
        for p in problems:
            print(f"    - {p}")
        failed += bool(problems)

    print(f"\n{len(blocks) - failed} von {len(blocks)} Versionen OK")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
