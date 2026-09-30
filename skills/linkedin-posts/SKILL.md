---
name: linkedin-posts
description: Schreibt LinkedIn-Posts auf Deutsch in drei Versionen zu einem Angebot, prüft sie mechanisch per Skript und inhaltlich per unabhängigem Review und legt die fertigen Posts als Datei ab. Verwenden, wenn LinkedIn-Posts, eine Post-Serie oder ein neues Angebot für Posts angelegt werden sollen, oder bei /linkedin-posts <angebot>.
---

# LinkedIn-Posts

Dieser Skill schreibt drei LinkedIn-Posts zu einem Angebot, prüft sie in zwei Stufen und speichert das Ergebnis.

## Arbeitsordner

Die persönlichen Daten liegen außerhalb des Skills im Arbeitsordner. Standard: `~/linkedin-posts`. Wenn die Umgebungsvariable `LINKEDIN_POSTS_DIR` gesetzt ist, gilt dieser Ordner.

```
<Arbeitsordner>/
├── profil.json          Name, Anrede, CTA-Zeile
├── angebote/<name>.md   ein Angebot pro Datei
└── posts/               fertige Posts
```

Wenn der Arbeitsordner oder `profil.json` fehlt: Lege den Ordner an, kopiere `vorlagen/profil-vorlage.json` als `profil.json` hinein und frage den Nutzer nach Name, Anrede (Sie oder du) und Kontakt-URL. Trage die Antworten ein. Erst danach weitermachen.

Die Skill-Dateien liegen im Ordner dieser SKILL.md. Im Folgenden ist `<skill>` dieser Ordner.

## Ablauf A: Posts schreiben (`/linkedin-posts <angebot>`)

### 1. Vorbereiten
- `profil.json` und `angebote/<angebot>.md` lesen.
- Fehlt das Angebot: vorhandene Angebote auflisten (Dateinamen in `angebote/` ohne `.md`) und nachfragen.
- Enthält die Angebotsdatei noch `[BITTE AUSFÜLLEN` : die offenen Stellen dem Nutzer nennen und nach den Werten fragen. Nicht raten, nichts erfinden. Die Antworten in die Angebotsdatei eintragen, dann weiter.
- `<skill>/references/regeln.md` vollständig lesen. Diese Regeln gelten für das Schreiben ohne Ausnahme.

### 2. Schreiben
Die drei Versionen nach `regeln.md` schreiben. Name, Anrede und CTA-Zeile kommen aus `profil.json`, Zielgruppe, Fakten und Zuordnung aus der Angebotsdatei.
Ergebnis im Ausgabeformat aus `regeln.md` als `<Arbeitsordner>/posts/entwurf.txt` speichern.

### 3. Mechanisch prüfen
```bash
python3 <skill>/scripts/check_posts.py <Arbeitsordner>/posts/entwurf.txt --profil <Arbeitsordner>/profil.json
```
Bei Exit-Code 1: nur die gemeldeten Punkte in den betroffenen Versionen korrigieren, Datei überschreiben, erneut prüfen. Höchstens 4 Runden. Wenn danach noch Fehler bleiben, die offenen Punkte dem Nutzer zeigen und fragen, wie weiter.

### 4. Inhaltlich prüfen (unabhängiger Review)
Einen Subagenten starten (Agent-Tool, Typ general-purpose). Er darf den Schreibprozess nicht kennen. Der Prompt an ihn besteht nur aus:
1. dem Inhalt von `<skill>/references/review-prompt.md` bis einschließlich der Zeile `# ANGEBOTSDATEI`,
2. dem Inhalt der Angebotsdatei,
3. der Zeile `# POSTS` und dem Inhalt von `entwurf.txt`.

Keine eigenen Erklärungen, Absichten oder Hinweise dazuschreiben.

Meldet der Review Verstöße: nur die gemeldeten Stellen korrigieren, danach Schritt 3 erneut ausführen und einen neuen Review-Subagenten starten. Höchstens 2 Review-Runden. Bleiben Verstöße, dem Nutzer den Review-Bericht zeigen und fragen.

### 5. Speichern und übergeben
Wenn Skript und Review ohne Befund sind, `<Arbeitsordner>/posts/<JJJJ-MM-TT>-<angebot>.md` schreiben:

```
# <Angebot>, <Datum>

## Version 1: <Blickwinkel>
<Text, fertig zum Kopieren, ohne die Zeilen VERSION und DE>

## Version 2: <Blickwinkel>
...

## Version 3: <Blickwinkel>
...
```

Danach `entwurf.txt` löschen. Dem Nutzer den Dateipfad nennen und die drei Hooks zeigen. Keine Zusammenfassung des Ablaufs.

## Ablauf B: Neues Angebot anlegen (`/linkedin-posts neu <name>`)

1. Existiert `angebote/<name>.md` schon: abbrechen und Bescheid geben.
2. `<skill>/vorlagen/angebot-vorlage.md` nach `angebote/<name>.md` kopieren.
3. Den Nutzer der Reihe nach fragen: Zielgruppe, Leistung und Preis, Belege (jeweils mit Status online oder in Arbeit), dann die drei Blickwinkel mit Lesergruppe, Risikoanker, Beleg und Rahmenangabe. Pro Nachricht höchstens drei Fragen.
4. Nur eintragen, was der Nutzer sagt. Keine Belege, Zahlen oder Kunden ergänzen.
5. Die fertige Datei zeigen und fragen, ob Posts dazu geschrieben werden sollen.

## Ablauf C: Übersicht (`/linkedin-posts` ohne Argument)

Vorhandene Angebote und die letzten 5 Dateien in `posts/` auflisten, dazu die beiden Befehle aus Ablauf A und B.

## Grenzen
- Nichts posten, nichts versenden. Der Skill erzeugt nur Dateien.
- `references/`, `scripts/` und `vorlagen/` nicht verändern.
- Nur Fakten aus der Angebotsdatei verwenden. Belege mit `[in Arbeit]` nie verwenden.
