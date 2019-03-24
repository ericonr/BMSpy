#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simulation of a battery and resistor circuit.

                    _______
           ___1_____|  R   |______ 
      + __|__       |______|      |
         _ _                      |  
        - |_______________________| 
             2                 

"""

from bms import PhysicalSystem
from bms.physical.electrical import Battery, Resistor, ElectricalNode, Ground
from bms.signals.functions import Sinus


R = 10  # Resistance in Ohm
Rint = 10
Umax = 12.5
Umin = 6
C = 3600*10
soc = 0.8

n1 = ElectricalNode('1')
n2 = ElectricalNode('2')

Bat = Battery(n1, n2, Umin, Umax, C, soc, Rint)
Res = Resistor(n2, n1, R)
G = Ground(n1)

ps = PhysicalSystem(5000, 50, [Bat, Res, G], [])
ds = ps.dynamic_system

d = ds.Simulate()
ds.PlotVariables([[n1.variable, n2.variable], [Bat.soc], [Bat.variables[0]]])

# Validation: analytical solutions
