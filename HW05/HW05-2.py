import pyaudio
import numpy as np
import parselmouth
from parselmouth.praat import call

def change_pitch(sound, factor):
    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)

    pitch_tier = call(manipulation, "Extract pitch tier")

    call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, factor)

    call([pitch_tier, manipulation], "Replace pitch tier")
    return call(manipulation, "Get resynthesis (overlap-add)")

def signal_processing(x):
    #print(x)
    x = parselmouth.Sound(x, 8000)
    y = change_pitch(x,2.5)
    y = y.values.reshape(-1)
    y= y.astype(np.int16)
    return y

CHUNK = 512
RATE = 8000
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)


try:

    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype=np.int16)
        #Sig = Sig[:,1].reshape(-1, 1)
        out = signal_processing(x)
        #out = np.hstack((out,out))
        assert out.dtype == np.int16
        player.write(out,CHUNK)

except KeyboardInterrupt:
    exit()

stream.stop_stream()
stream.close()
p.terminate()