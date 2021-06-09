import matplotlib.pyplot as plt
import numpy as np
import time
import pyaudio


def signal_processing(Sig):
    out = Sig.copy()
    return out

CHUNK = 512
RATE = 8000
nchannels = 1

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
data = stream.read(CHUNK)
Sig = np.frombuffer(data, dtype='<i2').reshape(-1, nchannels)
Sig = Sig[:, 0]
#print(Sig)
fig, ax = plt.subplots()
line, = ax.plot(Sig,'r')
fig.canvas.draw()
plt.show(block=False)
plt.ylim([-32000,32000])
plt.xlim([0,512])
plt.title('MICROFON LIVE TIME DOMIN')
plt.xlabel('n')
plt.ylabel('x[n]')
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
ax.grid()
ax.draw_artist(ax.patch)
tstart = time.time()
num_plots = 0

try:

    while True:
        data = stream.read(CHUNK)
        # print(data)
        Sig = np.frombuffer(data, dtype='<i2').reshape(-1, nchannels)
        #print(Sig)
        Sig = Sig[:, 0]
        line.set_ydata(Sig)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()
        ax.grid()
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        #plt.grid(color='green', linestyle='--', linewidth=0.5)
        num_plots += 1
except KeyboardInterrupt:
    exit()

