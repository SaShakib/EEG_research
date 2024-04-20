# import numpy as np 

from pylab import *
# # example data with some peaks:
# x = np.linspace(0,4,100)
# data = .2*np.sin(10*x)+ np.exp(-abs(2-x)**2)

# # that's the line, you need:
# a = np.diff(np.sign(np.diff(data))).nonzero()[0] + 1 # local min+max
# b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1 # local min
# c = (np.diff(np.sign(np.diff(data))) < 0).nonzero()[0] + 1 # local max

# d = [i for i in c if data[i] > 1]
# e = np.sort(b)[0]
# print(e)
# # print(data)
# # graphical output...
# plot(x,data)
# plot(x[d], data[d], "o", label="min")
# plot(x[e], data[e], "o", label="max")
# legend()
# show()

import numpy as np
from scipy.signal import argrelextrema

np.random.seed(42)
x = np.random.random(50)

# for local maxima
argrelextrema(x, np.greater)

# for local minima
c = argrelextrema(x, np.less)
time = np.arange(0,len(x))
d = (np.r_[True, x[1:] > x[:-1]] & np.r_[x[:-1] > x[1:], True]).nonzero()[0]

condition1 = np.r_[False, x[1:] > x[:-1]]  # Check if previous value is greater
condition2 = np.r_[x[:-1] > x[1:], False]  # Check if next value is greater
condition3 = x > 0.8  # Check if value is greater than 0.8

# Combine the conditions using bitwise AND operation
result = condition1 & condition2 & condition3# plot(time,x)


results = []

for i in range(2, len(x)):
    future = x[i]
    present = x[i - 1]
    past = x[i - 2]
    if ((present < past) and (present < future) and present < 0.25):
        results.append(i-1)

print("Resultsing indices:", results)
print("max: ", result.nonzero()[0])
plot(time, x)
plot(time[result.nonzero()[0]], x[result.nonzero()[0]], "o", label="min")
plot(time[results], x[results], "x", label="min")
show()