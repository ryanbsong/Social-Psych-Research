"""
Randomized combinations of people and preferences for experiment
"""

import random
from psychopy import event

def randomizer2(ppl, pref):
    array = []
    runs = []
    initial = 0
    counter = initial
    for x in range(len(pref)):
        if counter < len(pref)-1:
            counter += 1
            array.append(pref[counter])
        else:
            counter = 0
            array.append(pref[counter])
    initial += 1
    array *= len(ppl)/len(pref)
    random.shuffle(array)
    for x in range(len(pref)):
        for y in range(len(ppl)):
            runs.append([ppl[y], array[y]])
        random.shuffle(runs)
    return runs

ppl = []
pref = []
"""pplFile = open("people.csv", "r")
prefFile = open("preferences.csv", "r")

for line in pplFile:
    ppl.append(line)
for line in prefFile:
    pref.append(line)

"""
for x in range(6):
    ppl.append(x)
for x in range(3):
    pref.append(x)
#print randomizer2(ppl, pref)

print event.waitKeys()