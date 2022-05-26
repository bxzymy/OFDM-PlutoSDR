import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot as plt

def detect_preamble_energy(signal, ch):
    lg = len(signal)
    p = np.array(np.zeros((lg, 1)))
    start_index = np.array(0)
    flag = 1
    for n in range(lg):
        p[n] = abs(signal[n] ** 2)
        if flag and p[n] > 1e5:
            flag = 0
            start_index = np.append(start_index, n)
        if n > 300 and np.max(p[n - 299:n + 1]) < 7e4:
            flag = 1
    start_index = np.delete(start_index, 0)
    x = np.arange(len(p))
    plt.title(ch)
    plt.plot(x, p)
    plt.show()
    return start_index

preamble_lts = np.load("preamble_lts.npy")
plt.title("lts")
plt.plot(np.arange(len(preamble_lts)), preamble_lts)
plt.show()
preamble_sts = np.load("preamble_sts.npy")
plt.title("sts")
plt.plot(np.arange(len(preamble_sts)), preamble_sts)
plt.show()
received_signal_weak = np.load("recorded_signal_weak.npy")
plt.title("signal_weak")
plt.plot(np.arange(len(received_signal_weak)), received_signal_weak)
plt.show()
received_signal_strong = np.load("recorded_signal_strong.npy")
PSTS_sig = np.tile(preamble_sts, 10)

print("the start_index of received_signal_weak(energy):")
print(detect_preamble_energy(received_signal_weak, "Weak Signal(energy)"))
print("the start_index of received_signal_stong(energy):")
print(detect_preamble_energy(received_signal_strong, "Strong Signal(energy)"))