# -*- coding: utf-8 -*-

"""Testing the derivative of a sine function.

Uses pytest.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Sinus
from bms.blocks.continuous import Gain, DifferentiationBlock

import numpy as np


# properties of the sine wave
amplitude_sine = 3
w_sine = 2 * np.pi
phase_sine = np.pi / 2
offset_sine = 1.5

# properties of the derivative of the sine wave
amplitude_dsine = amplitude_sine * w_sine
w_dsine = -w_sine
phase_dsine = np.pi/2 - phase_sine
offset_dsine = 0

# defining the sine wave
sine = Sinus(f'f = {amplitude_sine} * sin({w_sine:.2f}*t + {phase_sine:.2f}) + {offset_sine}',
    amplitude=amplitude_sine, w=w_sine, phase=phase_sine, offset=offset_sine)
# definining its derivative - calculated analytically
dsine_calc = Sinus('df/dt (calc)', amplitude=amplitude_dsine, w=w_dsine, phase=phase_dsine, offset=offset_dsine)
signals = [dsine_calc]

# defining the variable that will hold the simulated result of the derivative
dsine_sim = Variable('df/dt (sim)')


# defining blocks
blocks = []
blocks.append(DifferentiationBlock(sine, dsine_sim))

# defining and running the system
steps_second = 100
time = 5
ds = DynamicSystem(time, time*steps_second, blocks, signals)
ds.Simulate()


# verification
def test_sine_bounds():
    assert np.max(sine.values) <= amplitude_sine + offset_sine
    assert np.min(sine.values) >= -amplitude_sine + offset_sine

def test_simulated_dsine_bounds():
    assert np.max(dsine_sim.values) <= amplitude_dsine
    assert np.min(dsine_sim.values) >= -amplitude_dsine

def test_difference_simulated_calculated_dsine():
    assert np.max(np.abs(dsine_sim.values - dsine_calc.values)) < amplitude_dsine / 25

def test_dsine_zero_value():
    if w_dsine > 0:
        def test_phase(phase):
            return phase >= 0
        def increment(phase):
            return phase + np.pi
    else:
        def test_phase(phase):
            return phase <= 0
        def increment(phase):
            return phase - np.pi

    is_zero_dphase = 0 - phase_dsine
    while not test_phase(is_zero_dphase):
        is_zero_dphase = increment(is_zero_dphase)
    is_zero_dphase = increment(is_zero_dphase)
    is_zero_time = is_zero_dphase / w_dsine
    is_zero_index = int(is_zero_time * steps_second)

    assert np.abs(dsine_sim.values[is_zero_index]) < amplitude_dsine / 25
