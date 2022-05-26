import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot as plt

# Compare the correlation magnitude against this value to determine whether there is a preamble or not
def detect_preamble_energy(signal, length):
    lg = len(signal) - 2*length
    p = np.array(np.zeros((lg, 1)))
    start_index = 0
    for n in range(lg):
        p[n] = abs(np.correlate(signal[n:n+length], signal[n:n+length], 'valid'))
    for i in range(lg):
        if p[i] > 100 and p[i+1] < p[i]:
            start_index = i
            break
    x = np.arange(len(p))
    plt.plot(x, p)
    plt.axvline(321, color='red')
    plt.show()
    # 其实不应该返回最大值的位置的，应该是返回斜率突变点，可是怎么表示呢？？？
    # kneed包找拐点 https://www.cnblogs.com/feffery/p/12325741.html
    if np.max(p) > 3*np.min(p):
        print('start_index', start_index)
        # 返回数减去一个length是因为按所给代码，实际头部数据是在321-521
        return start_index
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
np.testing.assert_equal(detect_preamble_energy(signalA, short_preamble_length), None)
np.testing.assert_equal(detect_preamble_energy(signalB, short_preamble_length) in range(preamble_start_idx-10, preamble_start_idx + 10), True)

print("Successful!!!")