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


        harmonic_series_chord = [dyad[0] * (math.lcm(*[dyad[0] for dyad in clean_chord]) / dyad[1]) for dyad in clean_chord]
        chord_data["harmonic_series_chord"].append(harmonic_series_chord)

        sum_harmonic_chord = sum(harmonic_series_chord)
        chord_data["sum_harmonic_chord"].append(sum_harmonic_chord)

        sum_squared_harmonic_chord = sum([pow(harmonic,2) for harmonic in harmonic_series_chord])
        chord_data["sum_squared_harmonic_chord"].append(sum_squared_harmonic_chord)

        max_harmonic_chord = max(harmonic_series_chord)
        chord_data["max_harmonic_chord"].append(max_harmonic_chord)

    chord_data = pd.DataFrame(chord_data)

    return chord_data

chord_data = calculate_chords()
print(chord_data)
chord_data.sort_values(by=["sum_squared_harmonic_intervals"], inplace=True)

print("playing chords")

for index, data in chord_data.iterrows():
    print(data)
    instrument.play_chord([hertz_to_midi(i) for i in data["pitches"]], 1.0, 4.0)