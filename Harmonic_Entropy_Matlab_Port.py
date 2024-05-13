import math
import numpy as np
import matplotlib.pyplot as plt

def calculate(ratio: float, fareySeries: list[float], dfarey: list[float], sigma: float = 0.007) -> float:
    out = 0
    for w, v in zip(dfarey, fareySeries):
        pp = w * np.exp((-0.5/sigma**2)*(v - ratio)**2)/np.sqrt(2*np.pi*sigma)
        if pp != 0:
            out = out + pp*np.emath.log(pp)

    return 1 - np.abs(out)

def generateFarey(order: int) -> tuple[list[float], list[float]]:
    #generate Farey series of order n
    f = [1]
    for n in range(1, order):
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
    
    return f, df

def main():
    f, df = generateFarey(50)

    #calculate entropy
    all = np.linspace(0, 1, 1000)
    he = np.zeros(all.shape, dtype=complex)
    for i, x in enumerate(all):
        he[i] = calculate(x, f, df)

    plt.plot(all, he)
    plt.show()

if __name__ == "__main__":
    main()