# Multiplayer Pacman AI-Challenge

## Konzept
Es treten zwei Bots gegeneinander an. Es sind Beispiele ethalten und Eigene können als Klassen in bot.py geschrieben werden.
Das Spielfend ist wie ein Pacman Labyrinth aufgebaut und zwei Bots treten mit ein oder Zwei Figuren gegeneinander an.
Die Bots ziehen ihre Figuren abwechsend ein Feld weiter. Es gibt die Möglichkeit nicht zu ziehen.
Es gewinnt der jenige Bot, dessen Punktzahl am Ende des Spiels die Höchste ist.

Aufwendige Grafik             |  Einfache Grafik
:-------------------------:|:-------------------------:
![Aufwendige Grafik](media/demo_higraphics_2_demobots.gif)  |  ![Einfache Grafik](media/demo_lowgraphics_2_demobots.gif)

## Nutzung

0. Repository herunterladen <br>
Es gibt zwei Entwicklungszweige den offiziellen *master* und den gemeinschaftlich entwickeltelten *development* <br>
Lade nun das Repository als ZIP-Archiv herunter oder clone es mit git. <br> `git clone https://github.com/RandInt83/AI-Challenge.git`

1. Instaliere Abhängigkeiten <br>
Das Projekt ist abhängig von Numpy und Pygame.
Instaliere sie mit pip <br> `pip3 install numpy pygame`

2. Programm starten <br>
Starte das Programm mit Python 3.x <br> `python3 main.py`

## Steuerung
Taste | Funktion
:---:|:---:
`0` | Spiel starten
`6` | Pausieren
`r` | Spiel neustarten
`t` | Grafik von Einfach auf Aufwendig schalten
`1` | Bildwiederholrate auf 1 FPS
`2` | Bildwiederholrate auf 3 FPS
`3` | Bildwiederholrate auf 10 FPS
`4` | Bildwiederholrate auf 20 FPS
`5` | Bildwiederholrate auf 40 FPS