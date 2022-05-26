import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot as plt


# Compare the correlation magnitude against this value to determine whether there is a preamble or not
def detect_preamble_auto_correlation(signal, length):
    lg = len(signal) - 2 * 2 * length  # 两个重复头部长200
    m = np.array(np.zeros((lg, 1)), dtype=complex)
    c = np.array(np.zeros((lg, 1)), dtype=complex)
    p = np.array(np.zeros((lg, 1)), dtype=complex)
    for n in range(lg):
        p[n] = np.sum(abs(signal[n:n + length] ** 2))
        for k in range(2 * length):
            c[n] = c[n] + abs(signal[n + k] * np.conjugate(signal[n + k + length]))
        m[n] = c[n] / p[n]
    x = np.arange(len(m))
    plt.plot(x, m)
    plt.show()
    if np.max(m) > 3 * np.min(m):
        # 返回数减去一个length是因为按所给代码，实际头部数据是在321-521
        return np.argmin(m) - length
    else:
        return None


# This cell will test your implementation of `detect_preamble`
short_preamble_length = 100
signal_length = 1000
short_preamble = np.exp(2j * np.pi * np.random.random(short_preamble_length))
preamble = np.tile(short_preamble, 2)
noise = np.random.normal(size=signal_length) + 1j * np.random.normal(size=signal_length)
signalA = 0.1 * noise
signalB = 0.1 * noise
preamble_start_idx = 321
signalB[preamble_start_idx:preamble_start_idx + len(preamble)] += preamble
np.testing.assert_equal(detect_preamble_auto_correlation(signalA, short_preamble_length), None)
np.testing.assert_equal(
    detect_preamble_auto_correlation(signalB, short_preamble_length) in range(preamble_start_idx - 10,
                                                                              preamble_start_idx + 10), True)
print("Successful!!!")
