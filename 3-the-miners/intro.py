from __future__ import division
from builtins import range
import copy
import math
from asciimatics.effects import Cycle, Print, Stars
from asciimatics.renderers import SpeechBubble, FigletText, Box
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import Path
from asciimatics.exceptions import ResizeScreenError
from asciimatics.effects import RandomNoise
from asciimatics.renderers import FigletText, Rainbow
import sys


def _speak(screen, text, pos, start):
    return Print(
        screen,
        SpeechBubble(text, "L", uni=screen.unicode_aware),
        x=pos[0] + 4, y=pos[1] - 4,
        colour=Screen.COLOUR_WHITE,
        clear=True,
        start_frame=start,
        stop_frame=start+60)

def _speak2(screen, text, pos, start):
    return Print(
        screen,
        SpeechBubble(text, "L", uni=screen.unicode_aware),
        x=pos[0] + 4, y=pos[1] - 4,
        colour=Screen.COLOUR_WHITE,
        clear=True,
        start_frame=start,
        stop_frame=start+90)

def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)
    podium = (38, 20,30,20)
    podium2 = (30, 20)

    # Scene 1.
    path = Path()
    path.jump_to(-20, centre[1])
    path.move_straight_to(centre[0], centre[1], 10)
    path.wait(30)
    path.move_straight_to(podium[0], podium[1], 10)
    path.wait(100)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "BIENVENIDO A  ~~THE MINERS~~~ !!!", centre, 30),
        _speak(screen, "Tercera parte de Postdigital (Enrique Tomás).", podium, 110),
        _speak(screen,
               "Quiero explicarte algo sobre la obra.", podium, 180),
    ]
    scenes.append(Scene(effects))

    # Scene 2.
    path = Path()
    path.jump_to(podium[0], podium[1])
    path.wait(1000)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "The Miners? ... ¿Los mineros?", podium, 10),
        _speak(screen, "Va sobre las criptomonedas y sus efectos...", podium, 80),
        #Print(screen,
        #      Box(screen.width, screen.height, uni=screen.unicode_aware),
        #      0, 0, start_frame=90),
        _speak(screen, "Las criptomonedas son dinero electrónico.",
               podium, 150),
        _speak(screen, "Sirven para transferir dinero sin intermediarios (como los bancos).", podium, 220),
        _speak2(screen, "Las transacciones necesitan ser verificadas por otros ordenadores de la red", podium, 300),
        _speak(screen, "que resuelven un complejo problema matemático.", podium, 400),
        _speak(screen, "...consumiendo mucha electricidad.", podium, 480),
        _speak2(screen, "Al año, tanta como un país como Irlanda o Suiza.", podium, 580),
        _speak(screen, "Por este motivo se recompensa económicamente a los nodos.",
               podium, 700),
        _speak2(screen, "El primero en resolverlo gana 12.5 bitcoins (1 bitcoin =~ 4200 euro) ",
               podium, 780),
        Stars(screen, (screen.width + screen.height) // 2, start_frame=360)
    ]
    scenes.append(Scene(effects, -1))

    # Scene 3.
    path = Path()
    path.move_straight_to(podium[2], podium[3], 10)
    path.wait(800)

    effects = [
        Arrow(screen, path, colour=Screen.COLOUR_GREEN),
        _speak(screen, "Durante esta obra, vamos a minar bitcoins...", podium2, 10),
        _speak2(screen, "Cada nota que tocará el Emsemble Container...",
               podium2, 70),
        _speak2(screen, "verificará (minará) una transaccion de bitcoins en tiempo real",
               podium2, 160),
        _speak(screen, " y si tenemos suerte (1 elevado a menos 36)...", podium2, 260),
        _speak(screen, "¡¡¡ganaremos 12.5 bitcoins en este concierto!!!", podium2,
               340),
        _speak(screen, "El minado (ejem... el concierto) va a empezar...", podium2,
               420),
        RandomNoise(screen,
                    signal=Rainbow(screen, FigletText("El concierto... va a empezar...", font="term")), start_frame=490)

    ]
    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
