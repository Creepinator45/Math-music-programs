from scamp import *
from scamp_extensions.pitch import *
from itertools import permutations, combinations, combinations_with_replacement
from fractions import Fraction
import pandas as pd

s = Session()

instrument = s.new_part("Saw wave")

instrument.play_note(60, 1, 4)

chords = [[1]+[1+1/j for j in i] for i in combinations(range(1,7), 2)]
print(chords)
current_pitch = 200

chord_data = {"chord":[], "pitches":[], "intervals":[], "interval_denoms": [], "sum_denom":[],"sum_squared_denom":[],"max_denom":[]}
for chord in chords:
    chord_data["chord"].append(chord)

    pitches = [current_pitch*i for i in chord]
    chord_data["pitches"].append(pitches)

    intervals = [(Fraction.from_float(pitch[0]/pitch[1]).limit_denominator()).as_integer_ratio() for pitch in permutations(pitches, 2)]
    chord_data["intervals"].append(intervals)

    interval_denoms = [interval[1] for interval in intervals]
    chord_data["interval_denoms"].append(interval_denoms)

    sum_denom = sum(interval_denoms)
    chord_data["sum_denom"].append(sum_denom)

    sum_squared_denom = sum([pow(interval_denom,2) for interval_denom in interval_denoms])
    chord_data["sum_squared_denom"].append(sum_squared_denom)

    max_denom = max(interval_denoms)
    chord_data["max_denom"].append(max_denom)

chord_data = pd.DataFrame(chord_data)
print(chord_data)


for chord in chords:
    pitches = [current_pitch*i for i in chord]
    
    print([(Fraction.from_float(i[0]/i[1]).limit_denominator()).as_integer_ratio() for i in permutations(pitches, 2)])
    print([round(i,3) for i in pitches])

    instrument.play_chord([hertz_to_midi(i) for i in pitches], 1.0, 4.0)