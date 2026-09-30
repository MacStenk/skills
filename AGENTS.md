# AGENTS.md

Werkzeuge für KI-Agenten, auf Deutsch. Jedes davon löst eine Aufgabe, die im
eigenen Alltag oft genug wiederkehrt, dass sie eine Anleitung verdient.

## Was dieses Repo ist

Eine Sammlung von Skills, installierbar mit `npx skills add MacStenk/skills`.
Kein Anwendungscode, kein Paketmanifest, kein Build. Was hier liegt, wird von
Agenten gelesen und ausgeführt, nicht kompiliert.

Der Unterschied zu vergleichbaren Sammlungen ist die Sprache. Beispiele,
Suchbegriffe und Bewertungen in englischen Werkzeugen messen für den
deutschsprachigen Raum das Falsche: andere Fragen, andere Konkurrenz, andere
Trefferlisten.

## Aufbau

```
skills/<name>/SKILL.md     die Anleitung, Pflicht
skills/<name>/<skript>     Hilfsskripte, nur wenn wirklich gebraucht
README.md                  Einstieg für Menschen
```

Ein Werkzeug lebt vollständig in seinem Ordner. Wer einen Skill einzeln
installiert, bekommt alles, was er braucht.

## Sprache

- Der Text der Anleitung ist **deutsch**.
- Die `description` im Kopf ist **zweisprachig**: erst der deutsche Satz, dann
  eine englische Fassung im selben Feld. Agenten finden den Skill damit auch
  bei englischen Anfragen.
- Der Feldname `name` bleibt technisch (klein, mit Bindestrichen, ohne Umlaute).

## Regeln für einen Skill

**Reife.** Ein Skill kommt erst ins Repo, wenn du ihn selbst angewendet hast
und mindestens ein konkreter Fall mit Zahlen dahintersteht. Das ist der
Maßstab, der diese Sammlung von maschinell erzeugten Ratgeberseiten trennt.
Eine Anleitung, die nur plausibel klingt, gehört nicht hierher.

**Ohne Konten lauffähig.** Die Grundstufe jedes Skills läuft mit dem, was ein
Agent ohnehin mitbringt: Websuche, Lesen, Schreiben. Zugänge, die es billiger
oder schärfer machen, stehen als Ausbaustufe am Ende, nie als Voraussetzung.
Ein Werkzeug, das erst zwei Anmeldungen verlangt, wird weggeklickt.

**Erst nachzählen, dann urteilen lassen.** Was sich prüfen lässt, prüft Code:
ob ein Wert in einer Liste steht, ob eine Datei da ist, ob eine Zahl über einer
Grenze liegt. Ein Modell entscheidet erst danach und nur über das, was wirklich
Ermessen braucht. Ein Modell, das eine lange Liste durchsehen soll, meldet bei
Unsicherheit Treffer, die es nicht gibt.

**Kandidaten müssen unterscheidbar sein.** Legt man einem Entscheidungsmodell
Varianten desselben Begriffs vor, stimmt es allem zu, mit hoher Sicherheit.
Der Sicherheitswert verrät das nicht.

**Die Bedienung gehört ins Ergebnis.** Wird ein Werkzeug selten benutzt, weiß
niemand nach vier Wochen mehr, was der nächste Schritt ist. Die Anleitung
schreibt deshalb in die erzeugte Datei hinein, wie es weitergeht, nicht
daneben.

**Doku wandert mit.** Bekommt ein Skill eine neue Funktion oder ändert sich seine
Bedienung, gehören die README im Skill-Ordner und sein Abschnitt in der README der
Sammlung in denselben Commit. Vor jedem Pull Request beide gegen die `SKILL.md` lesen.
Nichts davon aktualisiert sich von selbst.

**Was nicht belegt ist, wird so genannt.** Zahlen bekommen Quelle und Datum.
Ungeprüftes bleibt als ungeprüft markiert, auch wenn es die Aussage schwächt.

## Schreibweise

Deutsch, normal reden: Webseite, Server, Skript. Buzzwords übersetzen.
Keine Gedankenstriche. Keine Metaphern als Dauerton. Kurze Sätze.

Den Leser mit `du` ansprechen, als Kollege, nicht als Anleitung von oben.

## Build approach

Skateboard: zuerst die dünnste Fassung, die ganz durchläuft, danach jedes
Teilstück verbessern. Die Planung dazu wird lokal geführt und ist nicht Teil
dieses Repos.

## Git

- integration: `on`
- branch prefix: `feat/`
- commit: `per-milestone`

Ein Zweig je Werkzeug, Commit wenn ein Stück fertig ist. Pushen und Pull
Requests bestätigst du immer selbst.

## Was hier nicht hingehört

Persönliche Pfade, Schlüssel, eigene Domains, Kontonummern. Alles, was nur auf
einem Rechner gilt, bleibt lokal. Ein Skill, der ohne deinen Vault nicht läuft,
ist kein Skill für dieses Repo.

## Context files

Noch keine weiteren. Sobald ein Bereich eigene Regeln bekommt, kommt hier ein
Verweis darauf.
