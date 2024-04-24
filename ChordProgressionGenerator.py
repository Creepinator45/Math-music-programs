from scipy import optimize
import scamp
import scamp_extensions.pitch as pitch
import scamp_extensions.composers.barlicity as barlicity
import numpy as np
from itertools import permutations, combinations, zip_longest
from fractions import Fraction
import matplotlib.pyplot as plt
import math

s = scamp.Session()
instrument = s.new_part("Square wave")

maxDenom = 30

def ChordDissonance(notes: list[float]) -> float:
    totalDissonance = 0
    numIntervals = 0
    for interval in permutations(notes, 2):
        dyad = Fraction.from_float(interval[0]/interval[1]).limit_denominator(maxDenom).as_integer_ratio()
        print(dyad)
        #Harmonicity takes 2 frequencies in simplist form, and outputs a value from 0 to 1 where 0 is most dissonant and 1 is most harmonious. octave is 1, fifth is 0.375, unison is inf, values can be negative
        currentDissonance = pow(barlicity.harmonicity(dyad[0], dyad[1]), 2)
        if math.isinf(currentDissonance):
            currentDissonance = 1
        print(currentDissonance)
        totalDissonance += currentDissonance
        numIntervals += 1
    return totalDissonance

print(ChordDissonance([pitch.midi_to_hertz(i) for i in [50, 50+6, 50+12]]))

def Cost(chordProgression: list[float], idealDissonances: list[float], degree: int = 3) -> float:

    dissonanceCoeffecient = 1
    distanceCoeffecient = 0.000000001

    if len(chordProgression)/degree != len(idealDissonances):
        raise Exception("number of chords in chord progression doesn't match number if dissonances specified")

    chordProgression = [pitch.midi_to_hertz(note) for note in chordProgression]
    #simplify chord progression
    chordProgression = [(Fraction.from_float(note).limit_denominator(maxDenom)) for note in chordProgression]
    chordProgression = [note.numerator/note.denominator for note in chordProgression]

    #calculate variance from ideal dissonance
    totalDissonanceCost = 0
    for i in range(len(idealDissonances)):
        chord = [chordProgression[i*degree + j] for j in range(degree)]
        totalDissonanceCost += pow(ChordDissonance(chord) - idealDissonances[i], 2)

    #calculate distance notes move from their previous chord
    totalDistanceCost = 0
    for i in range(len(idealDissonances)):
        if i < 1:
            continue
        chord = [chordProgression[i*degree + j] for j in range(degree)]
        chord.sort()
        previousChord = [chordProgression[(i-1)*degree + j] for j in range(degree)]
        previousChord.sort()
        differences = [abs(j[0] - j[1]) for j in zip(chord, previousChord)]
        totalDistanceCost += pow(sum(differences), 2)

    totalCost = dissonanceCoeffecient * totalDissonanceCost + distanceCoeffecient * totalDistanceCost
    return totalCost

iteration = 0
def PrintStatus(result):
    global iteration    
    print("iteration")
    print(iteration)
    print(result)
    iteration += 1
    if iteration % 1000 != 1:
        return
    result = [(Fraction.from_float(note).limit_denominator(maxDenom)) for note in result]
    result = [note.numerator/note.denominator for note in result]

    dissonances = []
    instrument.play_note(None, 1.0, 2.0)
    for i in range(5):
        chord = [result[i*3 + j] for j in range(3)]
        print(chord)
        instrument.play_chord(chord, 1.0, 2.0)
        dissonances.append(ChordDissonance(chord))
    fig, ax = plt.subplots()
    ax.plot(dissonances)
    plt.show()
    


#startingValues = np.array([50, 54, 57, 50, 55, 58, 52, 55, 59, 52, 57, 61, 50, 54, 57])
#startingValues = np.random.random(15) + startingValues
startingValueRange = (70, 70+24)
startingValues = np.random.random(15) * (startingValueRange[0]-startingValueRange[1]) + startingValueRange[0]

PrintStatus(startingValues)
idealDissonances = [0, 0.3, 0.6, 1, 0]
progression = optimize.minimize(Cost, startingValues, idealDissonances, method="nelder-mead", callback=PrintStatus)

print(progression)
iteration = 0
PrintStatus(progression.x)