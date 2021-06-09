import pyaudio
import numpy as np
def signal_processing(x,incPercent):
    #incPercent = .9
    y = np.zeros(x.shape[0], dtype=np.int16)
    assert y.dtype == np.int16
    new_signal = np.interp(np.linspace(0, 10, int(np.ceil(512 * (1 + incPercent)))), np.linspace(0, 10, int(512)), x)
    L = len(x)
    l_new = len(new_signal)
    l_dif = l_new - L
    A = L - l_dif
    alfa1 = np.linspace(1, 0, l_new - L)
    alfa2 = np.linspace(0, 1, l_new - L)

    part2 = (np.multiply(alfa1, new_signal[A:L]) + np.multiply(alfa2, new_signal[L:l_new]))
    part1 = new_signal[0:A - 1]
    # print(part2,part1)
    y = np.concatenate((part1, part2))
    y = y.astype(np.int16)
    return y

CHUNK = 512
RATE = 44100
p = pyaudio.PyAudio()
incPercent = 0.3
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)


try:

    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype=np.int16)
        #Sig = Sig[:,1].reshape(-1, 1)
        out = signal_processing(x,incPercent)
        #out = np.hstack((out,out))
        assert out.dtype == np.int16
        player.write(out,CHUNK)

except KeyboardInterrupt:
    exit()

stream.stop_stream()
stream.close()
p.terminate()