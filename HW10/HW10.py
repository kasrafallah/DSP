from __future__ import division, print_function
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io
import wave
import pylab
import os
import scipy


f = scipy.io.loadmat('697.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_697
filter_697 = (data[0])

f = scipy.io.loadmat('770.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_770
filter_770 = (data[0])

f = scipy.io.loadmat('852.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_852
filter_852 = (data[0])

f = scipy.io.loadmat('941.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_941
filter_941 = (data[0])

f = scipy.io.loadmat('1209.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_1209
filter_1209 = (data[0])

f = scipy.io.loadmat('1336.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_1336
filter_1336 = (data[0])

f = scipy.io.loadmat('1477.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_1477
filter_1477 = (data[0])

f = scipy.io.loadmat('1633.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global filter_1633
filter_1633 = (data[0])

f = scipy.io.loadmat('lowpass.mat')
data = f.get('Num')
data = np.array(data)  # For converting to a NumPy array
global lowpass
lowpass = (data[0])


def wich_char( input ):

    out_697 = signal.lfilter(filter_697,1,input)

    out_770 = signal.lfilter(filter_770, 1, input)
    out_852 = signal.lfilter(filter_852, 1, input)
    out_941 = signal.lfilter(filter_941, 1, input)
    out_1209 = signal.lfilter(filter_1209, 1, input)
    out_1336 = signal.lfilter(filter_1336, 1, input)
    out_1477 = signal.lfilter(filter_1477, 1, input)
    out_1633 = signal.lfilter(filter_1633, 1, input)
    power_density_697 = sum(signal.lfilter(lowpass,1,np.power(out_697,2)))
    power_density_770 = sum(signal.lfilter(lowpass,1,np.power(out_770,2)))
    power_density_852 = sum(signal.lfilter(lowpass,1,np.power(out_852,2)))
    power_density_941 = sum(signal.lfilter(lowpass,1,np.power(out_941, 2)))
    power_density_1209 = sum(signal.lfilter(lowpass,1,np.power(out_1209, 2)))
    power_density_1336 = sum(signal.lfilter(lowpass,1,np.power(out_1336, 2)))
    power_density_1477 = sum(signal.lfilter(lowpass,1,np.power(out_1477, 2)))
    power_density_1633 = sum(signal.lfilter(lowpass,1,np.power(out_1633, 2)))
    power = [[power_density_697,power_density_770,power_density_852,power_density_941],[power_density_1209,power_density_1336,power_density_1477,power_density_1633]]
    index_max = np.argmax(power,axis=1)
    tot = np.sum(power,axis=1)
    #plt.plot(power[0],'r')
    #plt.plot(power[1],'g')
    #plt.show()
    numbers = [['1','2','3','A'],['4','5','6','B'],['7','8','9','c'],['*','0','#','D']]
    if power[0][index_max[0]] > tot[0]*0.80 and power[1][index_max[1]] > 0.80*tot[1]:
        return numbers[index_max[0]][index_max[1]]
    else:
        return 'silence'

    #print(power_density_697,power_density_770)

filename = "DialedSequence_SNR00dB.wav"
assert os.path.exists(filename) and os.path.isfile(filename)
fs,wav = wavfile.read(filename)
frame_len =1000;
#print(len(wav))
k = 1
l = 0
phone_number=['frist']
for x in range(0,len(wav),frame_len):

    out = wich_char(wav[x:x+999])

    if out != 'silence':
        if out != phone_number[k - 1] or l == 0:
            phone_number.append(out)
            k = k + 1
            l = 1
    else:
        l = 0
        k = k
print(phone_number)


