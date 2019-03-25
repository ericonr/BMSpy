#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testing the derivative of a sine function.

Uses pytest.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Sinus
from bms.blocks.continuous import Gain, DifferentiationBlock

import numpy as np


amplitude = 3
w = 2 * np.pi
phase = np.pi / 2
offset = 1.5

amplitude_dsignal = amplitude * w

signal = Sinus(f'f = {amplitude} * sin({w:.2f}*t + {phase:.2f}) + {offset}',
    amplitude=amplitude, w=w, phase=phase, offset = 1.5)
dsignal_sim = Variable('df/dt (sim)')
dsignal_calc_signal = Sinus('df/dt calc', amplitude=amplitude_dsignal, w=-w, phase=np.pi/2 - phase, offset=0)
dsignal_calc = Variable('df/dt (calc)')

blocks = []
blocks.append(DifferentiationBlock(signal, dsignal_sim))
blocks.append(Gain(dsignal_calc_signal, dsignal_calc, 1))

steps_second = 100
time = 10
ds = DynamicSystem(time, time*steps_second, blocks)
ds.Simulate()


# verification
def test_signal_bounds():
    assert np.max(signal.values) <= amplitude + offset
    assert np.min(signal.values) >= -amplitude + offset

def test_simulated_dsignal_bounds():
    assert np.max(dsignal_sim.values) <= amplitude_dsignal
    assert np.min(dsignal_sim.values) >= -amplitude_dsignal

def test_difference_simulated_calculated_dsignal():
    assert np.max(np.abs(dsignal_sim.values[:] - dsignal_calc.values[:])) < amplitude_dsignal / 25
