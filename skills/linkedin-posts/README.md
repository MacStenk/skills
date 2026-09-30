# linkedin-posts

Claude-Code-Skill: schreibt LinkedIn-Posts auf Deutsch in drei Versionen zu einem Angebot, prüft sie per Skript und per unabhängigem Review und speichert sie als Datei.

## Installation
1. Diesen Ordner nach `~/.claude/skills/linkedin-posts/` kopieren.
2. Claude Code starten und `/linkedin-posts` eingeben. Beim ersten Aufruf legt der Skill den Arbeitsordner `~/linkedin-posts` an und fragt nach Name, Anrede und Kontakt-Link.

Voraussetzung: `python3` (nur Standardbibliothek).

## Benutzung
- `/linkedin-posts neu <name>` legt ein Angebot an. Der Skill fragt die Inhalte ab.
- `/linkedin-posts <name>` schreibt, prüft und speichert drei Posts nach `~/linkedin-posts/posts/`.
- `/linkedin-posts` zeigt Angebote und letzte Posts.

Anderer Arbeitsordner: Umgebungsvariable `LINKEDIN_POSTS_DIR` setzen.

## Anpassen
- Schreibregeln: `references/regeln.md`
- Verbotene Wörter, Längen, Grenzwerte: Konstanten oben in `scripts/check_posts.py`
