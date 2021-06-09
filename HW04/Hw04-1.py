import pyaudio
import numpy as np
def signal_processing(Sig):
    out = Sig.copy()
    return out

CHUNK = 512
RATE = 8000
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)


try:

    while True:
        data = stream.read(CHUNK)
        Sig = np.frombuffer(data, dtype='<i2').reshape(512,1)
        #Sig = Sig[:,1].reshape(-1, 1)
        out = signal_processing(Sig)
        #out = np.hstack((out,out))
        assert out.dtype == np.int16
        data = out.tobytes()
        player.write(data,CHUNK)

except KeyboardInterrupt:
    exit()

stream.stop_stream()
stream.close()
p.terminate()