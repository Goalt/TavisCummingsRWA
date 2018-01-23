import Evolution
import Hamiltonian
import sys
import matplotlib.pyplot as plt

N = 5
wa = 0.0006
Emin = 0
Emax = 5
dt = 0.0001
HPLANKS = 1
CNTSteps = 10000

Hforsize = Hamiltonian.makeHamiltonian(False, N, 0, 0, 0, Emin, Emax, 1)
R = Evolution.generateDensityMatrix(Hforsize.shape[0])

tests = [(0.0001, 1000), (0.0001, 100), (0.0001, 10), (0.0001, 1), (0.0001, 0.1)]
# tests = [(1, 10000000), (0.0001, 0.1)]

xAxis = [k for k in range(CNTSteps)]
for i in range(len(tests)):
    g = Evolution.cmpGen(R, dt, HPLANKS, N, tests[i][0], wa, tests[i][1], Emin, Emax)

    results = []
    for j in range(CNTSteps):
        results.append(next(g))

    plt.plot(xAxis, results, label='b/(h*wc) =' + str(tests[i][0]/(tests[i][1]*HPLANKS)))

plt.xlabel('steps')
plt.ylabel('mse')
plt.legend()
# axes = plt.gca()
# axes.set_ylim([0,100])
plt.show()
