import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot

# Compare the correlation magnitude against this value to determine whether there is a preamble or not
def detect_preamble_cross_correlation(preamble, signal):
    len1 = len(preamble)
    len2 = len(signal)
    ar = np.array(0)
    for i in range(len2 - len1):
        temp = abs(np.correlate(preamble, signal[i:i + len1], 'valid'))
        ar = np.append(ar, temp)
    # plot the picture with the next 3 lines code:
    arx = np.arange(len2-len1+1)
    pyplot.axvline(123, color='red')
    pyplot.plot(arx, ar)
    pyplot.show()
    if np.max(ar) > 80:
        return np.argmax(ar)-1
    else:
        return None

preamble_length = 100
signal_length = 1000
preamble = (np.random.random(preamble_length) + 1j * np.random.random(preamble_length))
signalA = np.random.random(signal_length) + 1j * np.random.random(signal_length)
signalB = np.random.random(signal_length) + 1j * np.random.random(signal_length)
preamble_start_idx = 123
signalB[preamble_start_idx:preamble_start_idx + preamble_length] += preamble
np.testing.assert_equal(detect_preamble_cross_correlation(preamble, signalA), None)
np.testing.assert_equal(detect_preamble_cross_correlation(preamble, signalB), preamble_start_idx)

print("Successful!!!")