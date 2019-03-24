#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Usage of a delay block.

"""

from bms import Variable, DynamicSystem
from bms.blocks import Delay
from bms.signals.functions import Ramp


delay = 2.3
end_time = 10
time_step = 200

input_ = Ramp()
output_ = Variable(('Output', 'o'))
delay = Delay(input_, output_, delay)

ds = DynamicSystem(end_time, time_step, blocks=[delay])

ds.Simulate()
ds.PlotVariables()
