import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def Calculate(ratio: float) -> float:
    out = 0
    for w, v in zip(df, f):
        pp = w * np.exp((-0.5/sigma**2)*(v - ratio)**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            out = out + pp*np.emath.log(pp)
    return 1 - np.abs(out)

#generate Farey series of order n
f = [1]
for n in range(1, 51):
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

#calculate entropy
sigma = 0.007
all = np.linspace(0, 1, 1000)
he = np.zeros(all.shape, dtype=complex)
for i, x in enumerate(all):
    he[i] = Calculate(x)

plt.plot(all, he)
plt.show()