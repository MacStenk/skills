# Skills

Werkzeuge für KI-Agenten, auf Deutsch. Jeder Skill hier löst eine Aufgabe, die
oft genug wiederkehrt, dass sie eine Anleitung verdient.

Gebaut und im Alltag benutzt von [Steven Noack](https://stevennoack.de).
Weitere Werkzeuge, Baupläne und Prompts: [stevennoack.de/werkzeuge](https://stevennoack.de/werkzeuge).

## Installieren

```bash
npx skills add MacStenk/skills
```

Einen einzelnen Skill:

```bash
npx skills add https://github.com/MacStenk/skills/tree/main/skills/ki-sichtbarkeit
```

Läuft mit Claude Code, OpenCode, Codex, Cursor und weiteren Agenten.

## Was drin ist

### ki-sichtbarkeit

Herausfinden, bei welchen Fragen die eigene Website in KI-Antworten und
Suchtreffern nicht vorkommt, und daraus eine Liste fehlender Beiträge machen.

Misst in zwei Schritten: Findet die Websuche die eigene Seite überhaupt, und
wenn nicht, wer steht stattdessen dort. Aus den Treffern leitet sich ab, womit
man an dieser Stelle ankommt: Wo Videos dominieren, hilft kein weiterer Text.
Wo Foren stehen, gewinnt eine vollständige Antwort. Wo Herstellerseiten stehen,
muss die Frage enger gefasst werden.

**Braucht kein Konto und kein kostenpflichtiges Werkzeug.** Websuche und
Schreibzugriff auf einen Ordner genügen. Wer Zugänge hat, kann den Ablauf
günstiger und schärfer fahren; das steht am Ende der Anleitung.

### telegram-kanal

Einen Telegram-Kanal über die Bot-Schnittstelle bespielen: Beiträge in Telegram-HTML setzen,
Länge und Auszeichnungen nachzählen, senden und über die öffentliche Vorschau gegenlesen.

Rendern, Prüfen und Gegenlesen laufen ohne Konto. Wer senden will, braucht einen Bot von
@BotFather. Vor dem Absenden zählt das Skript nach: sichtbare Zeichen, unbekannte
Auszeichnungen, unmaskierte Klammern, Länge der Kopfzeile. Ohne diese Zählung weist die
Schnittstelle einen Beitrag mit `can't parse entities` komplett ab, und niemand merkt, warum.

## Warum auf Deutsch

Die Beispiele, Suchbegriffe und Bewertungen in vergleichbaren Werkzeugen sind
englisch. Wer für den deutschsprachigen Raum arbeitet, misst damit das Falsche:
andere Fragen, andere Konkurrenz, andere Trefferlisten. Diese Skills sind für
deutschsprachige Arbeit gebaut.

## Mitmachen

Fehler gefunden oder eine Anleitung, die bei dir anders läuft? Issue oder Pull
Request sind willkommen. Bei Skills zählt vor allem, ob die Schritte in der
Praxis tragen.

## Lizenz

MIT
