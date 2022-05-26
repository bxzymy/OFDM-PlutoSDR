import math
import numpy as np
from pluto_interface import pluto_transmitter, pluto_receiver
from matplotlib import pyplot as plt


def detect_preamble_cross_correlation(signal, preamble, ch):
    len1, len2 = len(preamble), len(signal)
    ar = np.array(np.zeros(len2 - len1))
    pr = np.array(np.zeros(len2 - len1))
    ap = np.array(np.zeros(len2 - len1))
    p1 = np.sum(abs(preamble ** 2))
    start_index = np.array(0)
    # cross_correlation
    for i in range(len2 - len1):
        ar[i] += abs(np.correlate(preamble, np.conjugate(signal[i:i + len1]), 'valid'))
        pr[i] += np.sqrt(p1) * np.sqrt(np.sum(abs(signal[i:i + len1] ** 2)))
        ap[i] = ar[i] / pr[i]
        if i != 0 and i % 1000 == 0:
            if np.max(ap[i - 1000:i - 200]) > 0.3:
                # 不能取整个1000是因为最后的可能只是下一个头部前面部分，尚未达到高峰
                start_index = (np.append(start_index, int(i - 1000 +
                                                          (np.argmax(ap[i - 1000:i]) + np.argmax(ar[i - 1000:i])) / 2)))
    # plot
    x = np.arange(len(ap))
    plt.plot(x, ap)
    plt.title(ch)
    plt.show()
    # return the answer
    start_index = np.delete(start_index, 0)
    return start_index


def detect_preamble_auto_correlation(signal, length, ch):
    lg = len(signal) - 2 * length
    # 判断用
    m = np.array(np.zeros((lg, 1)))
    c = np.array(np.zeros((lg, 1)))
    p = np.array(np.zeros((lg, 1)))
    # 绘图用，本题以此难以判断，条件不太好找，所以分开
    mc = np.array(np.zeros((lg, 1)), dtype=complex)
    cc = np.array(np.zeros((lg, 1)), dtype=complex)
    pc = np.array(np.zeros((lg, 1)), dtype=complex)
    start_index = np.array(0)
    # auto_correlation
    for n in range(lg):
        for i in range(length):
            # 判断
            c[n] = c[n] + abs(signal[n+i] * np.conjugate(signal[n+length+i]))
            p[n] = p[n] + abs(signal[n+i] * signal[n+i])
            # 绘图
            cc[n] = cc[n] + (signal[n+i] * np.conjugate(signal[n+length+i]))
            pc[n] = pc[n] + abs(signal[n+i] * signal[n+i])
        m[n] = c[n] / p[n]
        mc[n] = cc[n] / pc[n]
        if n != 0 and n % 1000 == 0:
            if np.max(m[n - 1000:n - 20]) > 2.0:
                start_index = np.append(start_index, n - 1000 + np.argmax(m[n - 1000:n]) + length)
    x = np.arange(len(mc))
    plt.plot(x, mc)
    plt.title(ch)
    plt.show()
    # return the answer
    # start_index = np.delete(start_index, 0)
    # return start_index
    start_index = np.delete(start_index, 0)
    return start_index


def detect_preamble_energy(signal, ch):
    lg = len(signal)
    p = np.array(np.zeros((lg, 1)))
    start_index = np.array(0)
    flag = 1
    for n in range(lg):
        p[n] = abs(signal[n] ** 2)
        if flag and p[n] > 3e5:
            flag = 0
            start_index = np.append(start_index, n)
        if n > 300 and np.max(p[n - 299:n + 1]) < 7e4:
            flag = 1
    x = np.arange(len(p))
    plt.title(ch)
    plt.plot(x, p)
    plt.show()
    start_index = np.delete(start_index, 0)
    return start_index


def detect_preamble_sliding(signal, l, ch):
    lg = len(signal) - 2 * l
    pa = np.array(np.zeros((lg, 1)))
    pb = np.array(np.zeros((lg, 1)))
    ans = np.array(np.zeros((lg, 1)))
    start_index = np.array(0)
    for n in range(lg):
        pa[n] = abs(np.correlate(signal[n:n + l], signal[n:n + l], 'valid'))
        pb[n] = abs(np.correlate(signal[n + l:n + 2 * l], signal[n + l:n + 2 * l], 'valid'))
        ans[n] = pb[n] / pa[n]
        if n != 0 and n % 1000 == 0:
            if np.max(ans[n - 1000:n - 20]) > 8:
                # print(n - 1000 + np.argmax(ans[n-1000:n]))
                # 不能取整个1000是因为最后的可能只是下一个头部前面部分，尚未达到高峰
                start_index = (np.append(start_index, n - 1000 + l + np.argmax(ans[n-1000:n])))
    x = np.arange(len(ans))
    plt.title(ch)
    plt.plot(x, ans)
    plt.show()
    start_index = np.delete(start_index, 0)

    return start_index

signal = np.load("recorded_signal.npy")
preamble_sts = np.load("preamble_sts.npy")
PSTS_sig = np.tile(preamble_sts, 10)
# Method 1 cross_correlation
print("the start_index of received_signal(cross_correlation):")
print(detect_preamble_cross_correlation(signal, PSTS_sig, "Signal(cross_correlation)"))

# Method 2 auto_correlation
length = 16  # 320是整个OFDM前序的长
print("the start_index of received_signal(auto_correlation):")
print(detect_preamble_auto_correlation(signal, length, "Signal(auto_correlation)"))

# Method 3 energy
print("the start_index of received_signal(energy):")
print(detect_preamble_energy(signal, "Signal(energy)"))

# Method 4 sliding
length = 16
print("the start_index of received_signal(sliding):")
print(detect_preamble_sliding(signal, length, "Signal(sliding)"))

print("Finish!!!")

