#!/usr/bin/python

import urllib
import time

import random

d=.98

out=[]
for k in range(10):
	j=0
	while 3<4:
		j=j+1
		if random.random()>d:
			break
	out.append(j)

print out
print float(sum(out))/len(out)