import matplotlib.pyplot as plt
from scamp_extensions.composers import barlicity
import numpy as np
from fractions import Fraction
import math

maxDenom = 30
rawX = (np.arange(1,maxDenom+1) / np.arange(1,maxDenom+1).reshape(maxDenom,1)).reshape(maxDenom**2)
rawX.sort()


def dissonance(x):
    dyad = Fraction.from_float(x).limit_denominator(maxDenom).as_integer_ratio()
    return dyad[1]

x = []
y = []
for i in rawX:
    if i >= 1:
        continue
    x.append(i)
    y.append(dissonance(i))

plt.plot(x,y)
#plt.yscale("log")
plt.savefig("Denominators Graph linear scale")
plt.show()
