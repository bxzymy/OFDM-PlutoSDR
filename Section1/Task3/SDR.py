import sys
import adi
import numpy as np
from numpy import *
from pluto_interface import pluto_transmitter, pluto_receiver


tx_args="ip:192.168.2.1"
tx_freq=915e6
bandwidth=1e6
tx_gain=-60
sdr_tx=pluto_transmitter(tx_args, tx_freq, bandwidth, tx_gain, verbose=True).pluto
# Receiver parameters configuration
""" Parameters for PlutoSDR device """
rx_args = "ip:192.168.3.2"
rx_freq = 915e6
bandwidth = 1e6
rx_gain = 0
rx_buffer_size = 1e4
gain_control_mode = "fast_attack"
sdr_rx = pluto_receiver(rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode, verbose=True).pluto
# Get transmitted signal and transmit
transmitted_signal=np.load("tx_signal.npy")
transmitted_signal=transmitted_signal*(2**14)
sdr_tx.tx_cyclic_buffer=True
sdr_tx.tx(transmitted_signal)# Cyclic transmit the signal
# Receive the signal and record
received_signal=sdr_rx.rx()# Record a buffer size signal one time
np.save("recorded_signal1.npy", received_signal)

