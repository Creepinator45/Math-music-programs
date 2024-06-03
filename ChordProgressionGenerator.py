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
from typing_extensions import Annotated

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

#Currently I evaluate chord dissonance using the squared sum of the intervals within the chord
#There is some online discussion on using voronoi cells to extend harmonic entropy to larger chords, but nothing is concrete enough to use here yet
def ChordDissonance(notes: list[float]) -> float:
    totalDissonance = 0
    numIntervals = 0
    for interval in permutations(notes, 2):
        intervalRatio = interval[0]/interval[1]
        currentDissonance = pow(calculateHE(intervalRatio, farey, dfarey), 2)
        if currentDissonance == 1:
            currentDissonance = 0
            numIntervals -= 1
        if currentDissonance > 1:
            raise("invalid dissonance")
        totalDissonance += currentDissonance
        numIntervals += 1
        print(currentDissonance)
    totalDissonance = totalDissonance*2/numIntervals
    print(totalDissonance)
    return totalDissonance

#The cost function being used to evaluate the merit of a chord progression
#Currently it takes into account how closely the individual chords match the desired dissonance, and penalizes large note jumps in between chords
def Cost(chordProgression: list[float], idealDissonances: list[float], degree: int = 3) -> float:

    #these coefficients can be tweeked to place higher emphasis on closely matching chord dissonance or on having chords relate to their neighbors
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

    #calculate squared sum of distance notes move from their previous chord
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
    
farey, dfarey = generateFarey(30)

def generate(dissonances: list[float], verbose: bool = False, degree: int = 3):
    startingValueRange = (70, 70+24)
    startingValues = np.random.random(len(dissonances)*degree) * (startingValueRange[0]-startingValueRange[1]) + startingValueRange[0]

    #sets callback function to print every iteration if verbose, otherwise sets callback function to just return None
    #I think this is kind of a strange way to do this, but this was the cleanest way I could think to do it to avoid unnecassary global variables and multiple similar minimize function calls
    if verbose:
        PrintStatus(startingValues)
        callback = PrintStatus
    else:
        def callback(result): None
    
    print("generating...")
    progression = optimize.minimize(Cost, startingValues, (dissonances, degree), method="nelder-mead", callback=callback)

    output = np.reshape(progression.x, (math.floor(len(progression.x)/degree), degree))
    return output

def CMDgenerate(dissonances: Annotated[list[float], typer.Argument(min=0, max=1)], verbose: bool = False, degree: int = 3):
    progression = generate(dissonances, verbose, degree)
    print(progression)
    dissonances = []
    for chord in progression:
        print(chord)
        instrument.play_chord(chord, 1.0, 2.0)
        dissonances.append(ChordDissonance(chord))
    fig, ax = plt.subplots()
    ax.plot(dissonances)
    plt.show()

if __name__ == "__main__":
    typer.run(CMDgenerate)
