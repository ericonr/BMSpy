#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulation of clutch of a vehicle.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Step, Sinus
from bms.blocks.continuous import Gain, ODE, Sum, Subtraction, Product, WeightedSum
from bms.blocks.nonlinear import CoulombVariableValue, Saturation, Coulomb


Cmax = 1000  # Max clutch torque handling
I1 = 0.5
I2 = 0.25
fv1 = 0.01
fv2 = 0.01

cc = Sinus(('Clutch command', 'cc'), 0.5, 0.1, 0, 0.5)
it = Step(('Input torque', 'it'), 200)
rt = Step(('Resistant torque', 'rt'), -180)

tc = Variable(('Clutch torque capacity', 'Tc'))
ct = Variable(('Clutch torque', 'ct'))
w1 = Variable(('Rotational speed of shaft 1', 'w1'))
w2 = Variable(('Rotational speed of shaft 2', 'w2'))
dw12 = Variable(('Clutch differential speed', 'dw12'))
st1 = Variable(('Sum of torques on 1', 'st1'))
st2 = Variable(('Sum of torques on 2', 'st2'))


block1 = Gain(cc, tc, Cmax)
block2 = WeightedSum([w1, w2], dw12, [1, -1])
block3 = CoulombVariableValue(it, dw12, tc, ct, 1)
block4 = ODE(st1, w1, [1], [fv1, I1])
block5 = ODE(st2, w2, [1], [fv2, I2])
block6 = WeightedSum([it, ct], st1, [1, 1])
block7 = WeightedSum([rt, ct], st2, [1, -1])

ds = DynamicSystem(50, 150, [block1, block2, block3, block4, block5, block6, block7])

r = ds.Simulate()
ds.PlotVariables([[dw12, w1, w2], [tc, ct, rt, it]])
