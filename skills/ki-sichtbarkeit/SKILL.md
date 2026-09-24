---
name: ki-sichtbarkeit
description: Herausfinden, bei welchen Fragen die eigene Website in KI-Antworten und Suchtreffern nicht vorkommt, und daraus eine Liste fehlender Beiträge machen. Verwenden, wenn jemand sagt „warum werde ich von ChatGPT nicht genannt", „KI-Sichtbarkeit", „AI Overviews", „werde ich zitiert", „welche Inhalte fehlen mir", oder wenn aus einer Content-Lücke ein Artikel entstehen soll. Braucht keine Konten und keine kostenpflichtigen Werkzeuge.
---

# KI-Sichtbarkeit messen und Lücken schließen

Wer bei einer Sachfrage nicht in den Suchtreffern steht, wird auch von keinem KI-Assistenten zitiert. Assistenten suchen, bevor sie antworten. Was die Suche nicht findet, kann in der Antwort nicht vorkommen.

Dieser Ablauf misst das, statt es zu vermuten, und macht aus dem Ergebnis eine Arbeitsliste.

Nötig sind nur Websuche und Schreibzugriff auf einen Ordner. Keine Anmeldung, keine Schlüssel, keine laufenden Kosten.

## Der Ablauf

1. Fragenliste bauen
2. Messen, bei welchen Fragen die eigene Seite fehlt
3. Lückenliste schreiben
4. Zu einer Lücke Material sammeln
5. Den Artikel schreiben
6. Nach einigen Wochen erneut messen

Schritt 1 ist der einzige, der Urteilsvermögen braucht. Alles andere ist Handwerk.

## 1. Die Fragenliste

Das ist der Hebel. Eine schlechte Liste macht die ganze Messung wertlos.

**Wonach suchen, was die Person wirklich kann.** Frag sie nach dem, was sie in den letzten Wochen gebaut, entschieden oder herausgefunden hat. Nicht nach ihrer Positionierung, nicht nach ihrer Selbstbeschreibung. Wer eine Seite über sich hat, beschreibt dort oft, was er einmal war.

**Die Fragen so formulieren, wie ein Mensch sie einem Assistenten stellt.** Ganze Sätze, keine Stichwörter. „Wann reicht SQLite statt PostgreSQL in Produktion?" statt „sqlite postgres vergleich".

**Fünfzehn bis zwanzig Stück.** Weniger misst zu wenig, mehr wird zur Fleißarbeit.

**Nicht nach Domain trennen.** Gemessen wird das Thema. Auf welcher Seite der Beitrag später liegt, ist eine andere Frage.

Speichere die Liste als JSON neben den Ergebnissen, zusammen mit den eigenen Domains:

```json
{
  "marke": "beispiel.de",
  "domains": ["beispiel.de", "www.beispiel.de"],
  "fragen": ["Erste Frage?", "Zweite Frage?"]
}
```

## 2. Messen

Für jede Frage eine Websuche. Dann zwei getrennte Prüfungen, und die Reihenfolge ist wichtig:

**Erst nachzählen, dann urteilen.** Ob eine der eigenen Domains in der Trefferliste steht, ist ein Textabgleich. Diese Frage nie an ein Sprachmodell geben. Ein Modell, das eine lange Trefferliste durchsehen soll, meldet bei Unsicherheit Treffer, die es nicht gibt.

**Nur wenn eine eigene Domain vorkommt**, lohnt die zweite Frage: auf welchem Platz, und beantwortet die Seite die Frage wirklich.

Halte je Frage fest: Zahl der Treffer, Platz der eigenen Seiten falls vorhanden, und die ersten drei fremden Treffer. Die fremden Treffer sind später das Material.

Schreib jeden Lauf als JSON mit Datum weg. Erst der Vergleich über die Zeit zeigt, ob sich etwas bewegt.

> [!NOTE]
> Eine Gegenprobe gehört zum ersten Lauf: Such einmal nach dem eigenen Namen oder der Marke. Tauchen die eigenen Seiten dort auf, arbeitet die Erkennung korrekt, und ein Ergebnis von null bei den Sachfragen ist ein echter Befund. Tauchen sie auch dort nicht auf, stimmt etwas mit der Suche oder den hinterlegten Domains nicht.

## 3. Die Lückenliste

Schreib eine Markdown-Notiz mit allen Fragen, bei denen keine eigene Seite vorkam. Je Frage:

- die Frage als Überschrift
- der Treffer, der sie heute am ehesten sachlich beantwortet
- die übrigen Treffer als Liste
- ein Kästchen zum Abhaken

**Schreib die Bedienungsanleitung in die Notiz hinein**, nicht daneben. Wer sie in vier Wochen öffnet, weiß sonst nicht, was er tun soll. Drei Sätze reichen: Frage aussuchen, Material sammeln, Artikel schreiben.

## 4. Material sammeln

Für eine ausgewählte Frage. Anders als bei einer Faktenrecherche sind hier die Seiten der anderen selbst die Quelle.

Sammle:

- **Wer die Frage heute beantwortet.** Acht bis zwölf Quellen, deutsch und englisch. Je Quelle: was steht dort konkret, wie tief, wie alt.
- **Was überall gleich steht.** Die Ratschläge, die sich wiederholen. Das ist der Allgemeinplatz, der im eigenen Text nicht nochmal breit ausgeführt werden muss.
- **Was fehlt, sich widerspricht oder veraltet ist.** Softwarethemen altern in Monaten. Verbreitete Zahlen gegen die Primärquelle prüfen.
- **Belegbare Zahlen** mit Quelle, Datum und Geltungsbereich. Was sich nicht belegen lässt, wird als unbelegt gekennzeichnet.
- **Eigene Fälle.** Durchsuche die Notizen, Projektdateien und Protokolle der Person nach konkreten Erlebnissen zum Thema. Das ist das Material, das die anderen Seiten nicht haben.

## 5. Den Artikel schreiben

Zwei Fassungen sind möglich, und sie schließen sich fast aus. Kläre vorher, welche gebraucht wird.

**Die sachliche Fassung** beantwortet die Frage allgemeingültig. Kein Ich, keine Anekdote. Eigene Erfahrung wird zur Regel verallgemeinert: Aus „bei mir lag die Datei auf dem falschen Zweig" wird „ein häufiger Fehler: die Datei liegt auf einem Arbeitszweig statt auf dem Hauptzweig". Jede Überschrift ist eine Antwort, die für sich stehen kann, weil Modelle Abschnitte zitieren und nicht Texte. Diese Fassung wird eher zitiert.

**Die persönliche Fassung** erzählt den eigenen Fall. Sie ist schwerer als maschinell erkennbar und taugt für Newsletter und soziale Netze. Sie beantwortet aber keine Frage und wird deshalb selten als Quelle herangezogen.

Was beide brauchen: Die Widersprüche im Feld offen stehen lassen statt sie zu glätten, und veraltete verbreitete Angaben ausdrücklich richtigstellen. Das ist der Teil, den austauschbare Ratgeberseiten nicht haben.

## 6. Nachmessen

Nach vier bis acht Wochen denselben Lauf wiederholen. Wandert die Frage von „offen" zu „gefunden", hat der Beitrag gewirkt. Passiert nichts, liegt es selten am Text und meistens daran, dass die Seite nicht auffindbar ist: fehlende interne Verlinkung, keine Sitemap, kein Verweis von außen.

## Ausbaustufe, falls Konten vorhanden

Der Ablauf oben braucht nichts weiter. Mit Zugängen wird er billiger und schärfer:

- **Ein Werkzeug-Proxy mit kostenloser Websuche** spart Suchabfragen und liefert saubere Trefferlisten samt Seiteninhalt.
- **Ein kleines Entscheidungsmodell** trifft die Auswahl aus vorsortierten Kandidaten typisiert und mit Sicherheitswert, für Bruchteile eines Cents. Dafür gilt dieselbe Regel wie oben: Es bekommt nur Kandidaten, die sich wirklich unterscheiden, und niemals eine Frage, die sich nachzählen lässt.
- **Abfragen echter Modellantworten mit Websuche** zeigen zusätzlich, ob die eigene Seite in der fertigen Antwort genannt wird. Das kostet pro Frage und lohnt nur für wenige Kernfragen.

Prüfe bei kostenpflichtigen Diensten immer den tatsächlichen Verbrauch vor und nach einem Aufruf. Preisangaben in Katalogen sind nicht immer verlässlich.
