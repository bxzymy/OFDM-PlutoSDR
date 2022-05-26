import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot as plt

# Compare the correlation magnitude against this value to determine whether there is a preamble or not
def detect_preamble_sliding(signal, length):
    lg = len(signal) - 2*2*length
    pa = np.array(np.zeros((lg, 1)))
    pb = np.array(np.zeros((lg, 1)))
    ans = np.array(np.zeros((lg, 1)))
    for n in range(lg):
        pa[n] = pa[n] + abs(np.correlate(signal[n:n+length], signal[n:n+length], 'valid'))
        pb[n] = pb[n] + abs(np.correlate(signal[n+length:n+2*length], signal[n+length:n+2*length], 'valid'))
        ans[n] = ans[n] + pb[n]/pa[n]
    x = np.arange(len(ans))
    plt.plot(x, ans)
    plt.axvline(321, color='red')
    plt.show()
    if np.max(ans) > 3*np.min(ans):
        print(np.argmax(ans)+length)
        # 返回数加上一个length是因为按所给代码，实际头部数据是在321-521
        return np.argmax(ans) + length
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
np.testing.assert_equal(detect_preamble_sliding(signalA, short_preamble_length), None)
np.testing.assert_equal(detect_preamble_sliding(signalB, short_preamble_length) in range(preamble_start_idx-10, preamble_start_idx + 10), True)

print("Successful!!!")