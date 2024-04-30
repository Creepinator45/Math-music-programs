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
print("f")
print(f)

centf=f

df = np.zeros(centf.shape)
df[0]=0
df[-1]=0
for i in range(2, np.max(centf.shape)):
    df[i-1]=-(centf[i] - centf[i-2])/2
print("df")
print(df)
sigma = 0.007
all = np.linspace(0, 1, 1000)
p = np.zeros(all.shape, dtype=complex)
for i in range(1, np.max(p.shape)+1):
    for j in range(1, np.max(f.shape)+1):
        pp = df[j-1]*np.exp((-0.5/sigma**2)*(centf[j-1]-all[i-1])**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            p[i-1] = p[i-1] + pp*np.emath.log(pp)



he=-p
print("he")
print(he)
print("1-abs he")
print(1-np.abs(he))
plt.plot(all, 1-np.abs(he))
plt.show()