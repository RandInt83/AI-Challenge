# Multiplayer Pacman AI-Challenge

## Konzept
Es treten zwei Bots gegeneinander an. Es sind Beispiele ethalten, eigene Bots können als Klassen in bot.py implementiert werden.
Das Spielfeld ist wie ein Pacman-Labyrinth aufgebaut. Die Bots treten mit ein oder zwei Figuren gegeneinander an.
Es wird abwechselnd um jeweils ein Feld weitergezogen. Es gibt die Möglichkeit, nicht zu ziehen.
Derjenige Bot gewinnt, dessen Punktzahl am Ende des Spiels die höchste ist.

Aufwendige Grafik             |  Einfache Grafik
:-------------------------:|:-------------------------:
![Aufwendige Grafik](media/demo_higraphics_2_demobots.gif)  |  ![Einfache Grafik](media/demo_lowgraphics_2_demobots.gif)

## Nutzung

0. Repository herunterladen <br>
Es gibt zwei Entwicklungszweige: den offiziellen *master* und den gemeinschaftlich entwickeltelten *development* <br>
Lade nun das Repository als ZIP-Archiv herunter oder clone es mit git. <br> `git clone https://github.com/RandInt83/AI-Challenge.git`

1. Instaliere Abhängigkeiten <br>
Zum Ausführen werden Numpy und Pygame benötigt.
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

## Beiragen
In CONTRIBUTE.md befindet sich ein [Workflow](CONTRIBUTE.md) zur Mitarbeit an diesem Projekt.
