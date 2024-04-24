from scamp import *
from scamp_extensions.pitch import *
from fractions import Fraction
import math

s = Session()

instrument = s.new_part("Square wave")

#octave
#chord = [1, 2]
#perfect fourth
chord = [1, 3/2]
#major sixth
#chord = [1, 5/3]
#minor seventh
#chord = [1, 15/8]
#augmented fourth (tritone)
#chord = [1, 25/18]
basePitch = 200

instrument.play_chord([hertz_to_midi(i*basePitch) for i in chord], 1.0, 4.0)