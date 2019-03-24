#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulation of a feedback loop.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Step
from bms.blocks.continuous import Gain, ODE, Sum, Subtraction, Product


Ka = 3
Kb = 4
Kc = 3
tau = 1

I = Step(('input', 'i'), 100.)
AI = Variable(('adapted input', 'ai'), [100.])
dI = Variable(('error', 'dI'))
O = Variable(('Output', 'O'))
F = Variable(('Feedback', 'F'))

b1 = Gain(I, AI, Ka)
b2 = Subtraction(AI, F, dI)
b3 = ODE(dI, O, [Kb], [1, tau])
b4 = Gain(O, F, Kc)

ds = DynamicSystem(3, 1000, [b1, b2, b3, b4])
r = ds.Simulate()
ds.PlotVariables([[I, O, dI, F]])


# I2=Step(('input','i'),100.)
#O2=Variable(('Output','O'))#
# ds2=bms.DynamicSystem(3,600,[ODE(I2,O2,[Ka*Kb],[1+Kc*Kb,tau])])
# ds2.Simulate()
# ds2.PlotVariables()
