## Name
slotfinder

## Description
Ein Raspberry Pi auf einer 8-fach Relaiskarte, etwas Software zur Datenspeicherung und Visualisierung und Python-Skripte zur Auswertung einer Konfigurationsdatei und Einlesen von
stündlichen Strompreisen über die aWATTar API.

![slotfinder negative stock price](/media/slotfinder_guteZeiten.png "negative stock price")

aWATTar bietet einen Stromtarif mit stündlichen Preisen an. Die Preise orientieren sich am Börsenpreis plus diversen Aufschlägen. Die Herausforderung besteht darin, die jeden Tag anders liegenden Preistäler für stromhungrige Geräte zu finden und über Relais dann Freigaben zu schaffen.

Eine Konfigurationsdatei erlaubt es beliebige Aufgaben (Tasks) zu definieren. Darin enthalten
sind Angaben, ob der Task gerade benutzt werden soll, wie lange er aktiv sein soll und in welchem Zeitraum ein Preistal gesucht werden soll. Jedem Task ist eine Kommandodatei zugeordnet für das Einschalten und das Ausschalten.

![slotfinder data flow](/media/slotfinder_Datenfluss.png "data flow")

Das Python-Skript schreibt eine ToDo-Liste für das Betriebssystem (Crontab) mit den Uhrzeiten
für den Aufruf der Kommandodateien. Diese Crontab wird täglich neu erstellt.
Der Aufruf der Python-Skripte zur Preisabfrage und zur Slot-Findung stehen auch in einer
Crontab und werden jeden Tag gestartet. Die Preisabfrage startet um 23.00 Uhr und die Slot-
Findung um 23.50 Uhr.

![slotfinder Ergebnis](/media/slotfinder_Preistalkaufen.png "decided well")
Die gepunktete Linie ist der stündliche Preis auf aWATTar. Darunter ist in rot die bezogene Energie aufgezeigt. Hier lässt sich erkennen, dass der Strombezug steigt wenn der Preis fällt. Das ist das Ziel des slotfinders: möglichst viele Lasten in günstige Zeiträume verlegen.



## Visuals



# Inbetriebnahme

Es handelt sich um keine Fertiglösung sondern um einen Bausatz.

Der Raspberry Pi muss mit der Oberseite auf die Relaiskarte gesetzt werden. Die 40polige
Stiftleiste passt in die 40polige Buchenleiste.
Die Relaiskarte wird auf eine Hutschiene gesteckt. Davor werden die Seitenteile mit den beiliegenden Schrauben fixiert.

Die SD-Karte muss in den Slot gesteckt werden, so, dass die Kontakte zur Platinenseite zeigen.
Ein Ethernet-Kabel wird vom Switch zum Port am Raspberry geführt und eingesteckt.

**Die Relais werden von der Elektrofachkraft verdrahtet.**

Das Netzkabel wird eingesteckt und der RaspberryPi wird eingeschaltet.







# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2 
###### This is a Heading h6

## Emphasis

*This text will be italic*  
_This will also be italic_

**This text will be bold**  
__This will also be bold__

_You **can** combine them_

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b

### Ordered

1. Item 1
1. Item 2
1. Item 3
  1. Item 3a
  1. Item 3b

## Images

![This is a alt text.](/image/sample.png "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
>> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Tables

| Left columns  | Right columns |
| ------------- |:-------------:|
| left foo      | right foo     |
| left bar      | right bar     |
| left baz      | right baz     |

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
