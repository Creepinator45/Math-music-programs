import math
import numpy as np
import matplotlib.pyplot as plt
f = [1]
for n in range(1, 51):
    for i in range(1, n):
        if math.gcd(n,i) == 1:
            f.append(i/n)

f.sort()
f=np.array(f)

df = np.zeros(f.shape)
df[0]=0
df[-1]=0
for i in range(1, np.max(f.shape)-1):
    df[i]=-(f[i+1] - f[i-1])/2

sigma = 0.007
all = np.linspace(0, 1, 1000)
p = np.zeros(all.shape, dtype=complex)
for i in range(0, np.max(p.shape)):
    for j in range(0, np.max(f.shape)):
        pp = df[j]*np.exp((-0.5/sigma**2)*(f[j]-all[i])**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            p[i] = p[i] + pp*np.emath.log(pp)

he=-p
plt.plot(all, 1-np.abs(he))
plt.show()