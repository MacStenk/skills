---
name: telegram-kanal
description: "Einen Telegram-Kanal über die Bot-Schnittstelle bespielen: Beiträge in Telegram-HTML setzen, Länge und Auszeichnungen nachzählen, senden, berichtigen und über die öffentliche Vorschau gegenlesen. Verwenden, wenn ein Text in einen Kanal soll, ein veröffentlichter Beitrag geändert werden muss oder ein Kanalbild gesetzt wird. / Post to a Telegram channel through the Bot API: render a post as Telegram HTML, count length and tags, send, correct and verify it through the public web preview. Use when a text should go into a channel, a published post needs a correction, or a channel picture has to be set."
---

# Einen Telegram-Kanal bespielen

Ein Kanal ist der billigste eigene Verteiler. Keine Gebühren, keine Reihenfolge, die ein
Verfahren festlegt, und über `t.me/s/<name>` auch ohne Telegram-Konto lesbar.

Was ihn in der Praxis killt, ist die Form. Ein Beitrag, dessen Auszeichnung die Schnittstelle
nicht annimmt, erscheint überhaupt nicht. Ein Beitrag, der wie ein Textblock aussieht, wird
nicht gelesen. Beides lässt sich nachzählen, bevor etwas rausgeht.

## Was du brauchst

Zum Schreiben, Rendern, Prüfen und Gegenlesen nichts außer Dateizugriff. Das Gegenlesen holt
die öffentliche Vorschau, dafür braucht es kein Konto.

Zum Senden einen Bot von @BotFather und diesen Bot als Administrator im Kanal. Das steht unten
in der Ausbaustufe, weil die Grundstufe ohne Konto schon vollständig arbeitet.

## Der Ablauf

1. Text schreiben. Die erste Zeile ist die Kopfzeile. Danach der Beitrag, Absätze durch
   Leerzeilen getrennt. Am Ende eine Zeile, die mit `Quelle` beginnt, mit Datum und Adresse.
2. Rendern und prüfen: `python3 kanalbeitrag.py beitrag.md`
3. Senden: `python3 kanalbeitrag.py beitrag.md --senden`
4. Gegenlesen: `python3 kanalbeitrag.py beitrag.md --gegenlesen @kanalname`

Schritt 2 und 4 zusammen sind der Unterschied zwischen abgeschickt und nachgesehen.

Das Skript liegt neben dieser Anleitung. Es braucht keine Fremdpakete, nur Python 3.

## Die Form

**Kopfzeile unter 120 Zeichen.** Sie ist das Einzige, was in der Benachrichtigung zu sehen ist.
Ein Satz, der dort abgeschnitten wird, erklärt nichts. Was länger ist, gehört in den ersten
Absatz.

**Ein Gedanke je Absatz.** Leerzeilen trennen sie. Der letzte Absatz vor der Quellzeile wird
kursiv gesetzt und trägt die Einordnung: warum das den Leser betrifft.

**Quelle und Datum in die letzte Zeile.** Ein Fund ohne Quelle ist eine Behauptung. Das Skript
erkennt die Zeile am Wortanfang `Quelle` und macht Adressen darin zu echten Links.

**Nichts mitbringen.** Die Datei ist Klartext, die Auszeichnung setzt das Skript. Ein selbst
geschriebenes `<b>` erscheint sonst als Text im Beitrag.

**Kürzer als du denkst.** Ein Beitrag von 400 bis 800 Zeichen wird gelesen, einer von 4000
selten. Die harte Grenze der Schnittstelle liegt bei 4096 Zeichen nach dem Auszählen der
Auszeichnungen, Bildunterschriften bei 1024.

## Auszeichnung: HTML, nicht MarkdownV2

Telegram nimmt zwei Formate. Nimm HTML. Der Grund ist die Maskierung: in MarkdownV2 müssen
`_ * [ ] ( ) ~ \` > # + - = | { } . !` alle maskiert werden. Ein einziger unmaskierter Punkt
in der Quellzeile, und die API weist den ganzen Beitrag ab mit `can't parse entities`. Dasselbe
in HTML kostet nur drei Zeichen: `&`, `<`, `>`.

Verfügbar sind: `b`, `strong`, `i`, `em`, `u`, `ins`, `s`, `strike`, `del`, `a href`, `code`,
`pre`, `blockquote` (auch `expandable`), `span class="tg-spoiler"`, `tg-emoji`.

Nicht verfügbar: Überschriften, Tabellen, Aufzählungszeichen als Element, `br`. Zeilenumbrüche
sind echte Zeilenumbrüche, Leerzeilen trennen Absätze. Ein Linkvorschaubild erzeugt Telegram
selbst aus der ersten Adresse.

## Fehler und Hinweise sind getrennt

Das Skript zählt zwei Dinge getrennt:

**Fehler** blockieren das Senden, weil die Schnittstelle den Beitrag sonst ganz abweist: zu
lang, leere Nachricht, unbekannte Auszeichnung, unmaskierte Klammer.

**Hinweise** halten niemanden auf: Kopfzeile zu lang, keine Quellzeile, nur eine Kopfzeile ohne
Text. Das ist Form, und Form entscheidet der Mensch.

## Nachsehen statt annehmen

`--gegenlesen @kanalname` liest `t.me/s/<name>`, also genau das, was ein Leser ohne App sieht,
und prüft drei Dinge: kommt fette Auszeichnung an, sind die Adressen echte Links, und steht
nirgends `&lt;b&gt;`. Das letzte wäre der Beweis, dass zweimal maskiert wurde.

Nützlich beim ersten Beitrag eines neuen Kanals und nach jeder Änderung an der Formatierung.
Im Alltag reicht die Prüfung vor dem Senden.

## Berichtigen statt löschen

`--bearbeiten <ID>` ersetzt den Text eines veröffentlichten Beitrags, `--loeschen <ID>` nimmt
ihn weg. Die ID ist die `message_id` aus der Antwort auf das Senden.

Ein Tippfehler wird berichtigt, nicht gelöscht. Ein gelöschter und neu gesendeter Beitrag
verliert seine Reihenfolge, und Leser sehen zweimal dasselbe. Löschen ist der Notausgang, nicht
die Korrektur.

## Ausbaustufe: mit Bot und Konto

Schlüssel und Ziel kommen aus der Umgebung, nie aus der Kommandozeile. Was in der
Befehlshistorie steht, ist veröffentlicht.

```bash
export TELEGRAM_BOT_TOKEN=...        # von @BotFather
export TELEGRAM_CHANNEL=@kanalname   # oder die numerische Kennung
python3 kanalbeitrag.py beitrag.md --senden
```

Ein Kanalbild setzt du mit `--bild`. Es muss quadratisch sein, mindestens 512 px, und der Bot
braucht das Recht, die Info zu ändern, sonst antwortet die API mit `not enough rights`. Das
Skript misst das Bild vorher und bricht bei krummen Maßen ab.

Wer den Ablauf regelmäßig fahren will, hängt ihn an einen Zeitplan und lässt nur senden, wenn es
wirklich etwas Neues gibt.

## Fallstricke

**Kein Kanal per API.** Ein Bot kann keinen Kanal anlegen, das geht nur aus einem Konto. Danach
den Bot als Administrator hinzufügen.

**`Forbidden: bot is not a member of the channel chat`** heißt genau das. Bot hinzufügen, meist
als Administrator mit Schreibrecht.

**`not enough rights`** beim Kanalbild: Dem Bot fehlt das Recht, die Kanalinfo zu ändern.

**Neu ausgelieferte Bilder können kurzfristig 404 liefern.** Ein Zwischenspeicher hat die alte
Antwort noch. Zweite Anfrage mit anderem Abfrageparameter prüft das.

**Kanalbilder werden rund zugeschnitten.** Was im Quadrat am Rand steht, verschwindet im Kreis.
Das Motiv gehört in den inneren Bereich.

**Prüfe die Bildmaße, nicht den Augenschein.** Ein Entwurf, der auf dem Rechner gut aussieht,
kann 2048 px groß sein und trotzdem nicht mittig sitzen.

**Ein Kanal ist öffentlich.** Er ist über die Webvorschau lesbar und wird von Suchmaschinen
gefunden. Was nicht öffentlich sein soll, gehört nicht hinein.

## Der Rückholknopf

Jeder Beitrag lässt sich berichtigen oder löschen, das Kanalbild lässt sich austauschen, und der
Kanal lässt sich auf privat stellen. Wenn etwas versehentlich rausgeht, ist die Reihenfolge:
berichtigen, löschen, Kanal schließen.

## Erprobter Fall

Gebaut für einen Nachrichtenkanal, der drei Mal am Tag prüft und nur sendet, wenn ein Fund durch
ein Frische-Gate gefallen ist. Beitragslänge im Betrieb rund 400 Zeichen, Kanalbild 512 mal 512
px, im Einsatz seit September 2026.

Zwei Fehler aus dem Aufbau stehen oben unter Fallstricke, weil sie beide nicht offensichtlich
waren: Der erste Sendeversuch endete mit `Forbidden: bot is not a member`, weil der Bot zwar
Mitglied, aber nicht Administrator war. Und die erste Fassung des Kanalbildes kam mit 2048 px
und ohne mittiges Motiv zurück, obwohl sie auf dem Bildschirm passend aussah.

Ohne das Gegenlesen wäre eine doppelte Maskierung wochenlang unbemerkt geblieben: In der App
sieht der Beitrag mit `&lt;b&gt;` fast normal aus, in der Vorschau steht es schwarz auf weiß.
