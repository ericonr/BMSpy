#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of a first order ODE.

"""

from bms import Variable, DynamicSystem
from bms.signals.functions import Ramp
from bms.blocks.continuous import ODE


K = 1.
tau = 1.254

e = Ramp('e', 1.)
s = Variable('s', [0])

block = ODE(e, s, [K], [1, tau])
ds = DynamicSystem(10, 100, [block])
ds.Simulate()
ds.PlotVariables()
