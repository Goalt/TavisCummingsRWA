import struct
import numpy as np
import random as rand
import Hamiltonian

def writeMatrixToFile(mat, fileName):
    f = open(fileName, "wb")

    (N, M) = mat.shape
    data = struct.pack('l', N)
    f.write(data)
    data = struct.pack('l', M)
    f.write(data)   

    for i in range(N):
        for j in range(M):
            data = struct.pack('dd', mat[i,j].real, mat[i,j].imag)
            f.write(data)

    f.close()

def readMatrixFromFile(fileName):
    f = open(fileName, "rb")

    data = f.read(8)
    N = struct.unpack('l', data)
    data = f.read(8)
    M = struct.unpack('l', data)
    N = N[0]
    M = M[0]

    mat = np.zeros((N, M), dtype=np.complex_)

    for i in range(N):
        for j in range(M):
            data = f.read(16)
            (a, b) = struct.unpack('dd', data)
            mat[i, j] = complex(a, b)
            
    f.close()

    return mat

def generateDensityMatrix(n):
    rand.seed()
    mat = np.zeros((n, n), dtype="complex")

    for i in range(n):
        for j in range(i, n):
            re = rand.random() * 100
            im = rand.random() * 100

            # re = 0
            # im = 0
            # if (i == 3 and j == 3):
            #     re = 1

            mat[i][j] = complex(re, im)
            mat[j][i] = complex(re, im).conjugate()

        mat[i][i] = complex(mat[i][i].real, 0)

    return mat

def Evolution(R, H, dt, HPLanks):
    # Нахождение СВ и СЗ для H
    eigenvalue, eigenvectors = np.linalg.eigh(H)
    eigenvectors = np.matrix(eigenvectors)

    # exp(H)
    eigV = np.zeros((H.shape[0], H.shape[0]), dtype="complex")
    const = complex(0, - dt / HPLanks)
    for i in range(H.shape[0]):
        eigV[i][i] = np.exp(complex(eigenvalue[i], 0) * const)
    eigenvalue = np.matrix(eigV)

    Z = eigenvectors * eigenvalue * eigenvectors.H

    while 1:
        # Унитарная эволюция
        res = Z * R * Z.H
        yield res
        R = res.copy()

def cmpGen(R, dt, HPLanks, N, b, wa, wc, Emin, Emax):
    HRWA = Hamiltonian.makeHamiltonian(True, N, b, wa, wc, Emin, Emax, HPLanks)
    H = Hamiltonian.makeHamiltonian(False, N, b, wa, wc, Emin, Emax, HPLanks)

    if HRWA.shape[0] != R.shape[0] or H.shape[0] != R.shape[0]:
        return -1

    iteration = 0
    diag1G = Evolution(R.copy(), H, dt, HPLanks)
    diag2G = Evolution(R.copy(), HRWA, dt, HPLanks)
    while 1:
        diag1 = next(diag1G)
        diag2 = next(diag2G)
        diag1 = diag1.diagonal()
        # diag1 = diag1.tolist()
        diag2 = diag2.diagonal()
        # diag2 = diag2.tolist()

        # dif = 0
        # for i in range(len(diag1)):
        #     dif += abs(diag1[0][i] - diag2[0][i])

        dif = np.linalg.norm(diag1-diag2)

        print(iteration, ":", dif)
        iteration += 1
        yield dif