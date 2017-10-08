import matplotlib.pyplot as plt
import numpy
import wave


wave_file = wave.open('apt.wav')
skip = 1024*0
chunk = 1024*128
wave_file.readframes(skip)
data = wave_file.readframes(chunk)
b = []
n = []
i = 0
new = 0
print(len(data))
for ele in data:
    if i % 2 == 1:
        new += ele * 2 / 256
        if new > 1:
            new -= 2
        b.append(new)
        n.append(i / (2 * 44100))
    else:
        new = ele * 2 / (256 * 256)
    i += 1

c = numpy.fft.fft(b)
d = numpy.fft.fft(c)

plt.subplot(3, 1, 1)
plt.plot(n, b)
plt.subplot(3, 1, 2)
plt.plot(abs(c[:int(len(c)/2)]))
plt.subplot(3, 1, 3)
plt.plot(abs(d))
plt.show()
