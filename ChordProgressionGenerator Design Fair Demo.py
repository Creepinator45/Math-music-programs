from scipy import optimize
import scamp
import scamp_extensions.pitch as pitch
import scamp_extensions.composers.barlicity as barlicity
import numpy as np
from itertools import permutations, combinations, zip_longest
from fractions import Fraction
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Button, Slider

s = scamp.Session()
instrument = s.new_part("Square wave")

maxDenom = 160


def ChordDissonance(notes: list[float]) -> float:
    totalDissonance = 0
    for interval in permutations(notes, 2):
        dyad = Fraction.from_float(interval[0]/interval[1]).limit_denominator(maxDenom * maxDenom).as_integer_ratio()
        totalDissonance += pow(barlicity.harmonicity(dyad[0], dyad[1]),2)
    return totalDissonance

def Cost(chordProgression: list[float], idealDissonances: list[float], degree: int = 3, ) -> float:
    dissonanceCoeffecient = 1
    distanceCoeffecient = 0.0000001

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


#GUI
max_dissonance = 1
min_dissonance = 0

# Define initial parameters
init_dissonance1 = min_dissonance
init_dissonance2 = max_dissonance/3
init_dissonance3 = 2*max_dissonance/3
init_dissonance4 = max_dissonance
init_dissonance5 = min_dissonance

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot([0,1,2,3,4], [init_dissonance1, init_dissonance2, init_dissonance3, init_dissonance4, init_dissonance5], lw=2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.5)

SliderWidth = 0.0225
SliderHeight = 0.3
FirstSliderXpos = 0.15
SliderSpacing = 0.155
SliderYpos = 0.1

# Make Sliders.
axDis1 = fig.add_axes([FirstSliderXpos, SliderYpos, SliderWidth, SliderHeight])
dis_slider1 = Slider(
    ax=axDis1,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance1,
    orientation="vertical"
)

axDis2 = fig.add_axes([FirstSliderXpos+((2-1) * (SliderWidth + SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider2 = Slider(
    ax=axDis2,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance2,
    orientation="vertical"
)

axDis3 = fig.add_axes([FirstSliderXpos+((3-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider3 = Slider(
    ax=axDis3,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance3,
    orientation="vertical"
)

axDis4 = fig.add_axes([FirstSliderXpos+((4-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider4 = Slider(
    ax=axDis4,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance4,
    orientation="vertical"
)

axDis5 = fig.add_axes([FirstSliderXpos+((5-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider5 = Slider(
    ax=axDis5,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance5,
    orientation="vertical"
)

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata([dis_slider1.val, dis_slider2.val, dis_slider3.val, dis_slider4.val, dis_slider5.val])
    fig.canvas.draw_idle()

# register the update function with each slider
dis_slider1.on_changed(update)
dis_slider2.on_changed(update)
dis_slider3.on_changed(update)
dis_slider4.on_changed(update)
dis_slider5.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
generateAx = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(generateAx, 'Generate', hovercolor='0.975')

def generate(event):
    idealDissonances = [dis_slider1.val, dis_slider2.val, dis_slider3.val, dis_slider4.val, dis_slider5.val]

    idealHarmonicity = [i for i in idealDissonances]
    startingValueRange = (50, 50+24)
    startingValues = np.random.random(15) * (startingValueRange[0]-startingValueRange[1]) + startingValueRange[0]
    print(startingValues)
    progression = optimize.minimize(Cost, startingValues, idealHarmonicity, method="nelder-mead", callback=PrintStatus)

    print(progression)

    result = [(Fraction.from_float(note).limit_denominator(maxDenom)) for note in progression.x]
    result = [note.numerator/note.denominator for note in result]

    instrument.play_note(None, 1.0, 2.0)
    for i in range(5):
        chord = [result[i*3 + j] for j in range(3)]
        print(chord)
        instrument.play_chord(chord, 1.0, 2.0)

button.on_clicked(generate)

plt.show()


