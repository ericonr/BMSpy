#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulation of braking capabilities of a vehicle.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Step, Sinus
from bms.blocks.continuous import Gain, ODE, Sum, Subtraction, Product, WeightedSum
from bms.blocks.nonlinear import CoulombVariableValue, Saturation, Coulomb


Cmax = 300  # Max clutch torque handling
I1 = 1
I2 = 0.25
fv1 = 0.01
fv2 = 0.01

cc = Sinus(('Brake command', 'cc'), 0.5, 0.1, 0, 0.5)
it = Step(('Input torque', 'it'), 100)
rt = Step(('Resistant torque', 'rt'), -80)

tc = Variable(('Brake torque capacity', 'Tc'))
bt = Variable(('Brake torque', 'bt'))
w1 = Variable(('Rotational speed of shaft 1', 'w1'))
st1 = Variable(('Sum of torques on 1', 'st1'))
et1 = Variable(('Sum of ext torques on 1', 'et1'))

block1 = Gain(cc, tc, Cmax)
block2 = WeightedSum([it, rt], et1, [1, 1])
block3 = CoulombVariableValue(et1, w1, tc, bt, 0.1)
block4 = ODE(st1, w1, [1], [fv1, I1])
block6 = WeightedSum([it, rt, bt], st1, [1, 1, 1])

ds = DynamicSystem(100, 400, [block1, block2, block3, block4, block6])

r = ds.Simulate()
ds.PlotVariables([[w1], [tc, bt, rt, it, st1, et1]])
