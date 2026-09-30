---
name: linkedin-posts
description: Schreibt LinkedIn-Posts auf Deutsch in drei Versionen, zu einem Angebot oder als Fakten-Post zu einem Fachthema mit Quellen, prüft sie mechanisch per Skript und inhaltlich per unabhängigem Review und legt die fertigen Posts als Datei ab. Verwenden, wenn LinkedIn-Posts, eine Post-Serie, ein neues Angebot oder ein neues Thema für Posts angelegt werden sollen, oder bei /linkedin-posts. Writes German LinkedIn posts in three versions, either for an offer or as fact-based posts on a topic with cited sources, checks them with a script and an independent review, and saves them as files. Use for LinkedIn posts, post series, new offers or topics, or /linkedin-posts.
---

# LinkedIn-Posts

Dieser Skill schreibt drei LinkedIn-Posts zu einem Angebot oder zu einem Fachthema, prüft sie in zwei Stufen und speichert das Ergebnis.

## Arbeitsordner

Die persönlichen Daten liegen außerhalb des Skills im Arbeitsordner. Standard: `~/linkedin-posts`. Wenn die Umgebungsvariable `LINKEDIN_POSTS_DIR` gesetzt ist, gilt dieser Ordner.

```
<Arbeitsordner>/
├── profil.json          Name, Anrede, CTA-Zeile, Schlusszeile für Fakten-Posts
├── angebote/<name>.md   ein Angebot pro Datei
├── themen/<name>.md     ein Thema für Fakten-Posts pro Datei
└── posts/               fertige Posts
```

Wenn der Arbeitsordner oder `profil.json` fehlt: Lege den Ordner an, kopiere `vorlagen/profil-vorlage.json` als `profil.json` hinein und frage den Nutzer nach Name, Anrede (Sie oder du), Kontakt-URL und ob Fakten-Posts mit einer eigenen Schlusszeile enden sollen (z. B. `→ Mehr dazu: <Link>`, leer ist erlaubt). Trage die Antworten ein, die Schlusszeile als `schluss_fakten`. Erst danach weitermachen.

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

Ohne Werkzeug für Subagenten (andere Agenten als Claude Code): den Review selbst in einem getrennten Durchgang ausführen, nur mit diesem Prompt als Grundlage, und dem Nutzer sagen, dass ein Review durch den Schreiber selbst schwächer ist.

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

Vorhandene Angebote und Themen (Dateinamen in `angebote/` und `themen/` ohne `.md`) und die letzten 5 Dateien in `posts/` auflisten, dazu die Befehle aus Ablauf A, B, D und E.

## Ablauf D: Neues Thema anlegen (`/linkedin-posts thema neu <name>`)

1. Existiert `themen/<name>.md` schon: abbrechen und Bescheid geben.
2. `<skill>/vorlagen/thema-vorlage.md` nach `themen/<name>.md` kopieren.
3. Den Nutzer nach der Zielgruppe fragen, dann: „Haben Sie Fakten mit Quelle, oder soll ich welche vorschlagen?“ (Anrede aus `profil.json`).
   - Eigene Fakten: jeweils Aussage, Quelle als Kurzname, Jahr und Link abfragen.
   - Vorschlagen: Schritt 4.
   Danach für jede der drei Versionen Lesergruppe, Blickwinkel, Fakt-Nummer und Einordnung (ein Satz, was der Fakt für die Leser bedeutet) abfragen. Pro Nachricht höchstens drei Fragen.
4. Recherche (nur wenn der Nutzer Vorschläge will):
   1. Einen Subagenten starten (Agent-Tool, Typ general-purpose). Der Prompt besteht nur aus dem Inhalt von `<skill>/references/recherche-prompt.md` bis einschließlich der Zeile `# THEMA`, dann dem Themennamen und dem Abschnitt ZIELGRUPPE aus der Themendatei. Ohne Werkzeug für Subagenten: die Recherche selbst nach diesem Prompt ausführen.
   2. Jede vorgeschlagene Quelle selbst aufrufen und das Beleg-Zitat dort suchen. Gefunden: „geprüft“. Nicht gefunden oder Seite nicht lesbar: „nicht bestätigt“. Nicht bestätigte Fakten nur mit diesem Vermerk zeigen.
   3. Dem Nutzer die Liste mit Aussage, Quelle, Link, Hinweis und Prüfvermerk zeigen. Ihn bitten, die Quellen selbst anzusehen, und drei Fakten auswählen lassen.
   4. Nur die ausgewählten Fakten eintragen, jeweils mit der Zeile `Beleg: „…“ (abgerufen <Datum>)` eingerückt darunter. Die Aussage nicht umformulieren.
5. Nur eintragen, was der Nutzer sagt oder aus der Recherche ausgewählt hat. Keine Fakten, Zahlen, Quellen oder Links ergänzen. Fehlt bei einem Fakt Quelle, Jahr oder Link, nachfragen.
6. Hat `profil.json` kein Feld `schluss_fakten`: einmal fragen, ob Fakten-Posts mit einer eigenen Schlusszeile enden sollen (z. B. `→ Mehr dazu: <Link>`), und die Antwort als `schluss_fakten` eintragen. Leer ist erlaubt.
7. Die fertige Datei zeigen und fragen, ob Posts dazu geschrieben werden sollen.

## Ablauf E: Fakten-Posts schreiben (`/linkedin-posts thema <name>`)

### 1. Vorbereiten
- `profil.json` und `themen/<name>.md` lesen.
- Fehlt das Thema: vorhandene Themen auflisten (Dateinamen in `themen/` ohne `.md`) und nachfragen.
- Enthält die Themendatei noch `[BITTE AUSFÜLLEN` : die offenen Stellen dem Nutzer nennen und nach den Werten fragen. Nicht raten, nichts erfinden. Die Antworten in die Themendatei eintragen, dann weiter.
- `<skill>/references/regeln-fakten.md` vollständig lesen. Diese Regeln gelten für das Schreiben ohne Ausnahme.

### 2. Schreiben
Die drei Versionen nach `regeln-fakten.md` schreiben. Name, Anrede und Schlusszeile (`schluss_fakten`) kommen aus `profil.json`, Zielgruppe, Fakten und Zuordnung aus der Themendatei.
Ergebnis im Ausgabeformat aus `regeln-fakten.md` als `<Arbeitsordner>/posts/entwurf.txt` speichern.

### 3. Mechanisch prüfen
```bash
python3 <skill>/scripts/check_posts.py <Arbeitsordner>/posts/entwurf.txt --profil <Arbeitsordner>/profil.json --art fakten
```
Bei Exit-Code 1: nur die gemeldeten Punkte in den betroffenen Versionen korrigieren, Datei überschreiben, erneut prüfen. Höchstens 4 Runden. Wenn danach noch Fehler bleiben, die offenen Punkte dem Nutzer zeigen und fragen, wie weiter.

### 4. Inhaltlich prüfen (unabhängiger Review)
Einen Subagenten starten (Agent-Tool, Typ general-purpose). Er darf den Schreibprozess nicht kennen. Der Prompt an ihn besteht nur aus:
1. dem Inhalt von `<skill>/references/review-prompt-fakten.md` bis einschließlich der Zeile `# THEMENDATEI`,
2. dem Inhalt der Themendatei,
3. der Zeile `# POSTS` und dem Inhalt von `entwurf.txt`.

Keine eigenen Erklärungen, Absichten oder Hinweise dazuschreiben.

Ohne Werkzeug für Subagenten (andere Agenten als Claude Code): den Review selbst in einem getrennten Durchgang ausführen, nur mit diesem Prompt als Grundlage, und dem Nutzer sagen, dass ein Review durch den Schreiber selbst schwächer ist.

Meldet der Review Verstöße: nur die gemeldeten Stellen korrigieren, danach Schritt 3 erneut ausführen und einen neuen Review-Subagenten starten. Höchstens 2 Review-Runden. Bleiben Verstöße, dem Nutzer den Review-Bericht zeigen und fragen.

### 5. Speichern und übergeben
Wenn Skript und Review ohne Befund sind, `<Arbeitsordner>/posts/<JJJJ-MM-TT>-thema-<name>.md` schreiben:

```
# Thema <Name>, <Datum>

## Version 1: <Blickwinkel>
<Text, fertig zum Kopieren, ohne die Zeilen VERSION und DE>

Erster Kommentar: <Link des verwendeten Fakts aus der Themendatei>

## Version 2: <Blickwinkel>
...

## Version 3: <Blickwinkel>
...

## So geht es weiter
1. Eine Version auswählen und auf LinkedIn posten.
2. Den Link unter „Erster Kommentar“ direkt als ersten Kommentar unter den Post setzen.
3. Nächste Posts zum selben Thema: in der Themendatei die ZUORDNUNG ändern und `/linkedin-posts thema <name>` erneut aufrufen.
```

Danach `entwurf.txt` löschen. Dem Nutzer den Dateipfad nennen und die drei Hooks zeigen. Keine Zusammenfassung des Ablaufs.

## Grenzen
- Nichts posten, nichts versenden. Der Skill erzeugt nur Dateien.
- `references/`, `scripts/` und `vorlagen/` nicht verändern.
- Angebote: Nur Fakten aus der Angebotsdatei verwenden. Belege mit `[in Arbeit]` nie verwenden.
- Themen: Nur Fakten aus der Themendatei verwenden, jeweils mit Quelle und Jahr. Recherche nur in Ablauf D und nur mit Auswahl durch den Nutzer. Keine Fakten aus dem Gedächtnis.
