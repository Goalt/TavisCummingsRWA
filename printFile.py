import sys, struct

with open(sys.argv[1], "rb") as binary_file:
    # Read the whole file at once
    data = binary_file.read()

i = 0
while i < len(data):
	real = struct.unpack('d', data[i:i+8])
	imag = struct.unpack('d', data[i+8:i+16])
	print((real[0],imag[0]))
	i += 16

