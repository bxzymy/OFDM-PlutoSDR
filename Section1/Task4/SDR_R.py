# import settings
import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot
import matplotlib.pyplot as plt

count = 0

rx_args = "ip:192.168.3.2"
rx_freq = 915e6
bandwidth = 1e6
rx_gain = 0
rx_buffer_size = 1e4
gain_control_mode = "fast_attack"
while True:
    sdr_rx = pluto_receiver(rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode, verbose=True).pluto
    y = sdr_rx.rx()  # Record a buffer size signal one time
    len1 = len(y)
    L = 16
    N = len1 - 2 * L
    c = np.array(np.zeros((N, 1)), dtype=complex)
    p = np.array(np.zeros((N, 1)), dtype=complex)
    m = np.array(np.zeros((N, 1)), dtype=complex)
    for n in range(N):
        for k in range(L):
            c[n] = c[n] + abs(y[n + k] * np.conjugate(y[n + k + L]))
            p[n] = p[n] + abs(y[n + k] * y[n + k])
        m[n] = c[n] / p[n]
    x = np.arange(len(m))
    j = 0
    i = 0
    while i < len(m) - 1:
        if m[i] > 11 and m[i] > m[i - 1] and m[i] > m[i + 1]:
            count = count + 1
            print("RX:nrx %d" % count)
        i = i + 1