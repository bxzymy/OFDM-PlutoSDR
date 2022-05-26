import sys
import adi
import numpy as np
from numpy import *
from pluto_interface import pluto_transmitter, pluto_receiver

for i in range(500):
    tx_args = "ip:192.168.2.1"
    tx_freq = 915e6
    bandwidth = 1e6
    tx_gain = -60

    sdr_tx = pluto_transmitter(tx_args, tx_freq, bandwidth, tx_gain, verbose=True).pluto
    transmitted_signal = np.load("tx_signal.npy")
    transmitted_signal = transmitted_signal * (2 ** 14)
    sdr_tx.tx_cyclic_buffer = True
    sdr_tx.tx(transmitted_signal)  # Cyclic transmit the signal
    # Receive the signal and record
    # received_signal=sdr_rx.rx()# Record a buffer size signal one time
    # np.save("recorded_signal123.npy", received_signal)
    print("Tx:ntx %d" % i)
