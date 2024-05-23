from scipy import optimize
import scamp
import scamp_extensions.pitch as pitch
import scamp_extensions.composers.barlicity as barlicity
import numpy as np
from itertools import permutations, combinations, zip_longest
from fractions import Fraction
import matplotlib.pyplot as plt
import math
import typer

s = scamp.Session()
instrument = s.new_part("Square wave")

maxDenom = 30

#calculate Harmonic Entropy, a measure of interval dissonance based on Shannon Entropy
def calculateHE(ratio: float, fareySeries: list[float], dfarey: list[float], sigma: float = 0.007) -> float:
    out = 0
    for w, v in zip(dfarey, fareySeries):
        pp = w * np.exp((-0.5/sigma**2)*(v - ratio)**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            out = out + pp*np.emath.log(pp)

    return 1 - np.abs(out)

def generateFarey(order: int) -> tuple[list[float], list[float]]:
    #generate Farey series of order n
    f = [1]
    for n in range(1, order):
        for i in range(1, n):
            if math.gcd(n,i) == 1:
                f.append(i/n)
    f.sort()
    f=np.array(f)

    #find widths
    df = np.zeros(f.shape)
    df[0]=0
    df[-1]=0
    for i in range(1, len(f)-1):
        df[i]=-(f[i+1] - f[i-1])/2
    
    return f, df

def ChordDissonance(notes: list[float]) -> float:
    totalDissonance = 0
    numIntervals = 0
    for interval in permutations(notes, 2):
        dyad = Fraction.from_float(interval[0]/interval[1]).limit_denominator(maxDenom).as_integer_ratio()
        #print(dyad)
        #Harmonicity takes 2 frequencies in simplist form, and outputs a value from 0 to 1 where 0 is most dissonant and 1 is most harmonious. octave is 1, fifth is 0.375, unison is inf, values can be negative
        currentDissonance = pow(barlicity.harmonicity(dyad[0], dyad[1]), 2)
        if math.isinf(currentDissonance):
            currentDissonance = 1
        #print(currentDissonance)
        totalDissonance += currentDissonance
        numIntervals += 1
    return totalDissonance

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
    
def generate(dissonances: list[float], verbose: bool = False):
    startingValueRange = (70, 70+24)
    startingValues = np.random.random(15) * (startingValueRange[0]-startingValueRange[1]) + startingValueRange[0]

    if verbose:
        PrintStatus(startingValues)
        callback = PrintStatus
    else:
        def callback(result): None
    
    print("generating...")
    progression = optimize.minimize(Cost, startingValues, dissonances, method="nelder-mead", callback=callback)

    output = np.reshape(progression.x, (math.floor(len(progression.x)/3), 3))
    return output

if __name__ == "__main__":
    typer.run(generate)
