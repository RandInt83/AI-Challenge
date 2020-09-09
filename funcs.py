# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:46:26 2020

@author: chris
"""

from numpy import random

_prefix = ['Stinking', 'Brave', 'Slimey', 'Cowardly', 'Beautiful', 'Ugly', 'Penetrating', 'Slashing', 'Vengeful', 
        'Heroic', 'Decapitating', 'Super', 'Smelly', 'Dark', 'Invisible', 'Incontinent', 'Grumpy', 'Rotting', 'Sexy', 
        'Joyful', 'Well...', 'Obvious', 'Dancing', 'Fearful', 'Outdated', 'Weak', 'Unwanted', 'Never-asked-for', 
        'Questionable', 'Solar', 'Pompous', 'Average', 'Boring', 'Salty', 'Spicey', 'Racy', 'Mildy Interesting', 
        'Vicious', "Bloody", "Smoking", "Drunken", "Lazy", "Bombing", "Exploding"]
_name = ['Olaf', 'Goblin', 'Butterfly', 'Adahn', 'Hero', 'Villian', 'Princess', 'Zak-Zak', 'Grobi',
        'Decapitator', 'Skeletor', 'Link', 'Kirby', 'Mario', 'Imperator', 'Sith', 'Jedi', 'Conan', 'Jellyfish',
        'Huppa-Huppa', 'Terrorist', 'Trump', 'Putin', 'Wiener Schnitzel', 'Ferdinand', 'Captain', 'Failalot', 'Orbiter',
        'Peasant', "Hasselhoff", 'Master', "Bomberman", "Bomber"]
_suffix = ['Doom', 'Vengerberg', 'Joy', 'Might', 'Greyskull', 'Berlin', 'Decapitation', 'Toad Island', 'Infinity',
        'Destruction', 'Desperation', 'Sex Appeal', 'Obamacare', 'Alderaan', 'Excellence', 'Dance', 'Confusion',
        'Failure', 'Valium', 'Boring', 'Cabbage', 'the SPD', 'Desaster', 'Python', 'Physics', "Explosion"]

def get_name():
    final_name = ""
    if random.randint(10)<8:
        final_name = final_name+random.choice(_prefix)+" "
    final_name = final_name + random.choice(_name)
    if random.randint(10)<8:
        final_name = final_name+" of "+random.choice(_suffix)+" "
    return final_name

class TimeOutException(Exception):
    def __init__(self, message, errors):
        super(TimeOutException, self).__init__(message)
        self.errors = errors


def timeouthandler(signum, frame):
    raise TimeOutException
