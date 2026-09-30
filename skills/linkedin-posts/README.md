# linkedin-posts

Skill für Claude Code und andere Agenten: schreibt LinkedIn-Posts auf Deutsch in drei Versionen, zu einem Angebot oder als Fakten-Post zu deinem Fachthema. Jede Version wird per Skript nachgezählt und von einem unabhängigen Prüfer gegen deine Fakten gelesen, dann als Datei gespeichert.

## Installation

```bash
npx skills add MacStenk/skills
```

Nur diesen Skill:

```bash
npx skills add https://github.com/MacStenk/skills/tree/main/skills/linkedin-posts
```

Voraussetzung: `python3` (nur Standardbibliothek). Kein Konto, kein Schlüssel.

Beim ersten Aufruf legt der Skill den Arbeitsordner `~/linkedin-posts` an und fragt nach Name, Anrede und Kontakt-Link. Anderer Ordner: Umgebungsvariable `LINKEDIN_POSTS_DIR` setzen.

## Benutzung

Angebote:
- `/linkedin-posts neu <name>` legt ein Angebot an. Der Skill fragt die Inhalte ab.
- `/linkedin-posts <name>` schreibt, prüft und speichert drei Posts nach `posts/`.

Fakten-Posts:
- `/linkedin-posts thema neu <name>` legt ein Thema an. Du gibst die Fakten vor, jeweils mit Quelle, Jahr und Link, oder lässt dir welche vorschlagen: Ein Recherche-Agent sucht Primärquellen und zitiert jede Zahl wörtlich, der Skill prüft die Zitate auf der Quellseite nach, und du wählst aus. Nur was du auswählst, kommt in die Themendatei.
- `/linkedin-posts thema <name>` schreibt, prüft und speichert drei Fakten-Posts. Die Quelle steht kurz im Text, der Link in der Datei zum Einfügen als ersten Kommentar.

Übersicht: `/linkedin-posts` zeigt Angebote, Themen und die letzten Posts.

## Was geprüft wird

Das Skript `scripts/check_posts.py` zählt nach: Länge des Hooks, Wortzahl, Floskeln, Gegenüberstellungen wie „nicht X, sondern Y“, Gedankenstriche, Fragezeichen, Fett, Hashtags, Emoji und die letzte Zeile. Bei Fakten-Posts (`--art fakten`) muss jede Version eine Jahreszahl enthalten, und deine Kontaktzeile aus den Angebots-Posts darf nicht drinstehen.

Danach liest ein zweiter Agent, der den Text nicht geschrieben hat, jede Version gegen deine Angebots- oder Themendatei. Er meldet Aussagen, die dort nicht stehen, und Fakten, die in der falschen Version gelandet sind. In Claude Code läuft er als eigener Subagent. Bei Agenten ohne Subagenten liest der schreibende Agent selbst in einem getrennten Durchgang gegen, und der Skill sagt dir, dass diese Prüfung schwächer ist.

## Anpassen

- Schreibregeln: `references/regeln.md` (Angebote), `references/regeln-fakten.md` (Fakten-Posts)
- Verbotene Wörter, Längen, Grenzwerte: Konstanten oben in `scripts/check_posts.py`
- Schlusszeile für Fakten-Posts: Feld `schluss_fakten` in deiner `profil.json`, leer lassen für keine
