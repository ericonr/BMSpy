#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of a second order ODE.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Sinus
from bms.blocks.continuous import ODE


K = 1
Q = 0.3
w0 = 3

e = Sinus('e', 4., 5)
s = Variable('s', [0])

block = ODE(e, s, [1], [1, 2*Q/w0, 1/w0**2])
ds = DynamicSystem(5, 200, [block])

ds.Simulate()
ds.PlotVariables()
