#! /usr/bin/python3

import math


def real(c,r,t,u0):
	return u0 * math.exp(-1/(r*c) * t)


f = open("t", "br")
time = f.read()
f.close()

f = open("u", "br")
voltage = f.read()
f.close()

#print(time)

len1 = len(time)
len_numbers = int(len1/4)
#print(len_numbers)

for i in range(0,len_numbers):
	#print(time[i:i+4])
	if 1==2:
		print( time[i*4]-128 , end=" ")
		print( (time[(i*4)+1])<<0 , end=" ")
		print( (time[(i*4)+2])<<0 , end=" ")
		print( (time[(i*4)+3]) , end=" ")
		print()
	
	if 1==1:
		exp1 = float(time[i*4]-128)
		mantissa1 = float( ((time[(i*4)+1])<<16) + ((time[(i*4)+2])<<8) + (time[(i*4)+3]) )
		
		exp2 = float(voltage[i*4]-128)
		mantissa2 = float( ((voltage[(i*4)+1])<<16) + ((voltage[(i*4)+2])<<8) + (voltage[(i*4)+3]) )

		t = (mantissa1 * math.pow(2,exp1)) / (pow(2,22))
		
		print( t, round( (mantissa2 * math.pow(2,exp2)) / (pow(2,22)), 3), round(real(0.1,20.0,t,9.0), 3) )