import math
import numpy as np

def plus1(vec):
	vec.reverse()
	carry = 0
	i = 0
	while 1:
		if i == len(vec):
			return -1

		if vec[i] == 1:
			vec[i] = 0
			carry = 1
			i += 1
		else:
			vec[i] = 1
			carry = 0

		if carry == 0:
			break

	vec.reverse()
	return 0

def makeEnergyVector(E, N):
	vec = [0 for i in range(N)]
	result = []

	while 1:
		cnt1 = 0
		for i in vec:
			if i == 1:
				cnt1 += 1

		if (cnt1 <= E):
			result.append(list(vec))
			result[len(result) - 1].append(E - cnt1)

		if (plus1(vec) == -1):
			break

	return result

def hamDistance(vec1, vec2):
	result = 0
	for i in range(len(vec1) - 1):
		if vec1[i] != vec2[i]:
			result += 1
	return result

def calcTransferRWA(vec1, vec2, b, wa, wc, HPLANKS):
	dist = hamDistance(vec1, vec2)

	# Осталось прежним
	if (dist == 0) and (vec1[-1] == vec2[-1]):
		result = 0
		for i in range(len(vec1) - 1):
			result += vec1[i] * wa
		result += vec1[len(vec1) - 1] * wc
		return result * HPLANKS

	if (dist == 1):
		sign = 0
		for i in range(len(vec1) - 1):
			sign += vec1[i] - vec2[i]

		# Атом возбудился и исчез фотон
		if (sign == -1) and ((vec1[-1] - vec2[-1]) == 1):
			return b * math.sqrt(vec1[-1])

		# Атом релаксировал и родился фотон
		if (sign == 1) and ((vec1[-1] - vec2[-1]) == -1):
			return b * math.sqrt(vec1[-1] + 1)

	return 0

def calcTransfer(vec1, vec2, b, wa, wc, HPLANKS):
	dist = hamDistance(vec1, vec2)

	# Осталось прежним
	if (dist == 0) and (vec1[-1] == vec2[-1]):
		result = 0
		for i in range(len(vec1) - 1):
			result += vec1[i] * wa
		result += vec1[len(vec1) - 1] * wc
		return result * HPLANKS

	if (dist == 1):
		sign = 0
		for i in range(len(vec1) - 1):
			sign += vec1[i] - vec2[i]

		# Атом возбудился и исчез фотон
		if (sign == -1) and ((vec1[-1] - vec2[-1]) == 1):
			return b * math.sqrt(vec1[-1])

		# Атом релаксировал и родился фотон
		if (sign == 1) and ((vec1[-1] - vec2[-1]) == -1):
			return b * math.sqrt(vec1[-1] + 1)

		# Атом возбудился и родился фотон
		if (sign == -1) and ((vec1[-1] - vec2[-1]) == -1):
			return b * math.sqrt(vec1[-1] + 1)

		# Атом релаксировал и исчез фотон
		if (sign == 1) and ((vec1[-1] - vec2[-1]) == 1):
			return b * math.sqrt(vec1[-1])

	return 0

def makeHamiltonian(flagRWA, N, b, wa, wc, Emin, Emax, HPLANKS):
	energyV = []
	for i in range(Emin, Emax + 1):
		energyV.extend(makeEnergyVector(i, N))

	size = len(energyV)
	mas = np.zeros((size, size), dtype=np.complex_)

	for i in range(size):
		for j in range(size):
			if flagRWA == True:
				mas[i,j] = complex(calcTransferRWA(energyV[i], energyV[j], b, wa, wc, HPLANKS), 0)
			else:
				mas[i,j] = complex(calcTransfer(energyV[i], energyV[j], b, wa, wc, HPLANKS), 0)
	return mas