# B1I – Functional Design

## Feature: Sudoku-Hinweisfunktion verbessern

### 1. Kontext und Ziel

In Sudoku Studio können Spieler einen Hinweis anfordern, wenn sie nicht weiterkommen. Die Anwendung sucht dann ein Feld, das leer ist oder eine falsche Zahl enthält, und zeigt die richtige Zahl an.

Momentan wird die Auswahl des Hinweisfeldes direkt in der Flask-Route durchgeführt.

Mein Ziel ist es, diese Berechnung in eine eigene Funktion auszulagern. Dadurch soll die Flask-Route übersichtlicher werden und die Berechnung unabhängig von der Webseite funktionieren.

### 2. Deklarative Anforderungen

Die Anwendung soll folgende Anforderungen erfüllen:

* Ein Hinweis darf nur für ein Feld gegeben werden, das im ursprünglichen Sudoku leer war.
* Die vorgegebenen Zahlen dürfen nicht verändert werden.
* Wenn der Spieler ein geeignetes Feld ausgewählt hat, soll dieses bevorzugt werden.
* Wenn kein geeignetes Feld ausgewählt wurde, soll automatisch ein passendes Feld gefunden werden.
* Die Berechnung darf das bestehende Sudoku nicht verändern.
* Wenn kein Hinweis mehr nötig ist, soll die Funktion kein Feld zurückgeben.
* Bei denselben Eingaben muss immer dasselbe Ergebnis entstehen.

Diese Anforderungen beschreiben, was die Funktion machen soll. Die einzelnen Programmierschritte werden erst bei der Implementierung festgelegt.

### 3. Geplanter Datenfluss

1. Der Benutzer klickt auf «Hinweis anzeigen».
2. JavaScript sendet das aktuelle Sudoku und das ausgewählte Feld an Flask.
3. Flask überprüft die erhaltenen Daten.
4. Die Eingaben werden in unveränderbare Daten umgewandelt.
5. Eine Pure Function sucht ein geeignetes Hinweisfeld.
6. Die Funktion gibt die Position des Feldes zurück.
7. Flask liest den richtigen Wert aus der gespeicherten Lösung.
8. Flask gibt die Position und den Wert als JSON zurück.
9. JavaScript trägt die Zahl im Sudoku ein.

### 4. Geplante Datenstrukturen

Für das Sudoku verwende ich ein Tuple of Tuples.

So kann die Berechnung keine vorhandenen Zahlen verändern.

Die Position eines Feldes wird als Tuple mit zwei Zahlen dargestellt. Die erste Zahl steht für die Zeile und die zweite für die Spalte.

Wenn kein geeignetes Feld vorhanden ist, wird `None` zurückgegeben.

### 5. Geplante Operatoren

**filter():** Damit können geeignete Felder anhand bestimmter Bedingungen ausgewählt werden.

**tuple():** Damit lassen sich unveränderbare Daten erstellen.

**Generator Expressions:** Damit können die möglichen Positionen durchsucht werden, ohne zuerst eine zusätzliche veränderbare Liste aufzubauen.

**Funktionskomposition:** Die Flask-Route kann die Prüfung der Eingaben und die Auswahl des Hinweisfeldes miteinander verbinden.

### 6. Geplante Funktionen

**choose_hint_cell(original, current, solution, selected)**

Diese Funktion erhält das ursprüngliche Sudoku, den aktuellen Spielstand, die Lösung und die ausgewählte Position.

Sie gibt die Position eines geeigneten Hinweisfeldes oder `None` zurück.

Die Funktion soll keine Dateien öffnen, keine HTTP-Anfragen verarbeiten und keine vorhandenen Daten verändern.

### 7. Geplante Tests

**Test 1: Ausgewähltes leeres Feld**

Eingabe: Ein unvollständiges Sudoku und die Position eines leeren Feldes.

Erwartetes Ergebnis: Die Funktion gibt die Position dieses Feldes zurück.

**Test 2: Kein Feld ausgewählt**

Eingabe: Ein unvollständiges Sudoku ohne ausgewählte Position.

Erwartetes Ergebnis: Die Funktion gibt die erste geeignete Position zurück.

**Test 3: Sudoku vollständig**

Eingabe: Ein vollständig und korrekt gelöstes Sudoku.

Erwartetes Ergebnis: Die Funktion gibt `None` zurück.

### 8. Warum dieses Design?

Ich möchte die Berechnung von der Flask-Route trennen, weil beide unterschiedliche Aufgaben haben.

Die Flask-Route ist für die Kommunikation mit dem Browser zuständig. Die Pure Function soll nur Daten erhalten und ein Ergebnis berechnen.

Dadurch kann ich die Berechnung einfacher mit Pytest überprüfen. Ausserdem kann ich die Funktion später an einer anderen Stelle der Anwendung wiederverwenden.

Eine mögliche Alternative wäre, die ganze Logik in der Flask-Route zu lassen. Das benötigt zunächst weniger Funktionen, macht die Route aber länger und die Berechnung stärker von Flask abhängig.

Deshalb plane ich, die Auswahl des Hinweisfeldes in eine eigene Pure Function auszulagern.
