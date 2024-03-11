from scamp import *
from scamp_extensions.pitch import *
from scamp_extensions.composers.barlicity import *
from itertools import permutations, combinations, combinations_with_replacement
from fractions import Fraction
import pandas as pd
import math
from sympy.ntheory import primefactors

s = Session()

instrument = s.new_part("Square wave")

def calculate_chords():
    chords = [[1]+[1+1/j for j in i] for i in combinations(range(1,20), 2)]
    current_pitch = 200

    chord_data = {"chord":[], "clean_chord":[], "pitches":[], "intervals":[],
                  "interval_denoms": [], "sum_denom":[], "sum_squared_denom":[], "max_denom":[], 
                  "prime_denoms":[], "sum_prime_denom":[], "sum_squared_prime_denom":[], "max_prime_denom":[],
                  "harmonic_series_intervals":[], "sum_harmonic_intervals":[], "sum_squared_harmonic_intervals":[], "max_harmonic_intervals":[],
                  "harmonic_series_chord":[], "sum_harmonic_chord":[], "sum_squared_harmonic_chord":[], "max_harmonic_chord":[],
                  "harmonicity_intervals": [], "sum_harmonicity_intervals":[], "sum_squared_harmonicity_intervals":[], "max_harmonicity_intervals":[],
                  "harmonicity_chord": [], "sum_harmonicity_chord":[], "sum_squared_harmonicity_chord":[], "max_harmonicity_chord":[], 
                  }
    for chord in chords:
        chord_data["chord"].append(chord)

        clean_chord = [(Fraction.from_float(dyad).limit_denominator()).as_integer_ratio() for dyad in chord]
        chord_data["clean_chord"].append(clean_chord)

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


        prime_denoms = []
        for interval_denom in interval_denoms:
            prime_denoms += primefactors(interval_denom)
        chord_data["prime_denoms"].append(prime_denoms)

        sum_prime_denom = sum(prime_denoms)
        chord_data["sum_prime_denom"].append(sum_prime_denom)

        sum_squared_prime_denom = sum([pow(prime_denom,2) for prime_denom in prime_denoms])
        chord_data["sum_squared_prime_denom"].append(sum_squared_prime_denom)

        max_prime_denom = max(prime_denoms)
        chord_data["max_prime_denom"].append(max_prime_denom)


        harmonic_series_intervals = [interval[0] * (math.lcm(*interval_denoms) / interval[1]) for interval in intervals]
        chord_data["harmonic_series_intervals"].append(harmonic_series_intervals)

        sum_harmonic_intervals = sum(harmonic_series_intervals)
        chord_data["sum_harmonic_intervals"].append(sum_harmonic_intervals)

        sum_squared_harmonic_intervals = sum([pow(harmonic,2) for harmonic in harmonic_series_intervals])
        chord_data["sum_squared_harmonic_intervals"].append(sum_squared_harmonic_intervals)

        max_harmonic_intervals = max(harmonic_series_intervals)
        chord_data["max_harmonic_intervals"].append(max_harmonic_intervals)


        harmonic_series_chord = [dyad[0] * (math.lcm(*[dyad_2[1] for dyad_2 in clean_chord]) / dyad[1]) for dyad in clean_chord]
        chord_data["harmonic_series_chord"].append(harmonic_series_chord)

        sum_harmonic_chord = sum(harmonic_series_chord)
        chord_data["sum_harmonic_chord"].append(sum_harmonic_chord)

        sum_squared_harmonic_chord = sum([pow(harmonic,2) for harmonic in harmonic_series_chord])
        chord_data["sum_squared_harmonic_chord"].append(sum_squared_harmonic_chord)

        max_harmonic_chord = max(harmonic_series_chord)
        chord_data["max_harmonic_chord"].append(max_harmonic_chord)


        harmonicity_intervals = [harmonicity(interval[0], interval[1]) for interval in intervals]
        chord_data["harmonicity_intervals"].append(harmonicity_intervals)

        sum_harmonicity_intervals = sum(map(abs, harmonicity_intervals))
        chord_data["sum_harmonicity_intervals"].append(sum_harmonicity_intervals)

        sum_squared_harmonicity_intervals = sum([pow(interval,2) for interval in harmonicity_intervals])
        chord_data["sum_squared_harmonicity_intervals"].append(sum_squared_harmonicity_intervals)

        max_harmonicity_intervals = max(harmonicity_intervals)
        chord_data["max_harmonicity_intervals"].append(max_harmonicity_intervals)

        
        harmonicity_chord = [harmonicity(dyad[1], dyad[0]) for dyad in clean_chord]
        for i in range(len(harmonicity_chord)):
            if math.isinf(harmonicity_chord[i]):
                harmonicity_chord[i] = 0
                
        chord_data["harmonicity_chord"].append(harmonicity_chord)

        sum_harmonicity_chord = sum(harmonicity_chord)
        chord_data["sum_harmonicity_chord"].append(sum_harmonicity_chord)

        sum_squared_harmonicity_chord = sum([pow(dyad,2) for dyad in harmonicity_chord])
        chord_data["sum_squared_harmonicity_chord"].append(sum_squared_harmonicity_chord)

        max_harmonicity_chord = max(harmonicity_chord)
        chord_data["max_harmonicity_chord"].append(max_harmonicity_chord)
        

    chord_data = pd.DataFrame(chord_data)

    return chord_data

chord_data = calculate_chords()
print(chord_data)
chord_data.sort_values(by=["sum_harmonicity_intervals"], inplace=True, ascending=False)

print("playing chords")


# for interval in [1+1/2, 1+2/3, 1+3/4, 1+8/9, 1+4/5, 1+3/5, 1+9/16, 1+5/8, 1+5/6, 1+5/9, 1+16/27, 1+8/15, 1+4/7, 1+9/10, 1+27/32, 1+15/16, 1+7/8, 1+6/7, 1+7/12, 1+7/9, 1+20/27, 1+9/14, 1+64/81]:
#     print(interval)
#     instrument.play_chord([hertz_to_midi(200), hertz_to_midi(200*interval)], 1.0, 4.0)
# instrument.play_note(None, 1.0, 4.0)

# for interval in [1+1/2, 1+2/3, 1+3/4, 1+3/5, 1+4/5, 1+5/6, 1+4/7, 1+6/7, 1+5/8, 1+7/8, 1+5/9, 1+7/9, 1+8/9, 1+9/10, 1+7/12, 1+9/14, 1+8/15, 1+9/16, 1+15/16, 1+16/27, 1+20/27, 1+27/32, 1+64/81]:
#     print(interval)
#     instrument.play_chord([hertz_to_midi(200), hertz_to_midi(200*interval)], 1.0, 4.0)
# instrument.play_note(None, 1.0, 4.0)

# for interval in [(1+3/5, 1+8/9), (1+5/6, 1+3/5), (1+4/7, 1+9/16), (1+6/7, 1+5/8), (1+5/8, 1+5/6), (1+7/8, 1+5/9), (1+5/9, 1+16/27), (1+7/9, 1+8/15), (1+8/9, 1+4/7), (1+7/12, 1+27/32), (1+9/14, 1+15/16), (1+8/15, 1+7/8), (1+9/16, 1+6/7), (1+15/16, 1+7/12), (1+16/27, 1+7/9), (1+27/32, 1+9/14)]:
#     print(interval)
#     instrument.play_chord([hertz_to_midi(200), hertz_to_midi(200*interval[0])], 1.0, 4.0)
#     instrument.play_chord([hertz_to_midi(200), hertz_to_midi(200*interval[1])], 1.0, 4.0)
#     instrument.play_note(None, 1.0, 4.0)
    

for index, data in chord_data.iterrows():
    print(data)
    instrument.play_chord([hertz_to_midi(i) for i in data["pitches"]], 1.0, 4.0)