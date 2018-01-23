import Evolution
import Hamiltonian
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 10:
	print("Неверное кол-во параметров")

N = int(sys.argv[1])
b = float(sys.argv[2])
wa = float(sys.argv[3])
wc = float(sys.argv[4])
Emin = int(sys.argv[5])
Emax = int(sys.argv[6])
dt = float(sys.argv[7])
HPLANKS = float(sys.argv[8])
CNTSteps = int(sys.argv[9])

# 6.62606957e-27

Hforsize = Hamiltonian.makeHamiltonian(False, N, b, wa, wc, Emin, Emax, 1)
R = Evolution.generateDensityMatrix(Hforsize.shape[0])
g = Evolution.cmpGen(R, dt, HPLANKS, N, b, wa, wc, Emin, Emax)

results = []
for i in range(CNTSteps):
	results.append(next(g))

xAxis = [i for i in range(CNTSteps)]
plt.plot(xAxis, results, '-b')
plt.show()

# print(results)
# print(xAxis)