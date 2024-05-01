import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

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
p = np.zeros(all.shape, dtype=complex)
for x, i in zip(all, range(0, len(all))):
    for j in range(0, len(f)):
        pp = df[j]*np.exp((-0.5/sigma**2)*(f[j]- x)**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            p[i] = p[i] + pp*np.emath.log(pp)
he=-p

plt.plot(all, 1-np.abs(he))
plt.show()