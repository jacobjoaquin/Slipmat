#!/usr/bin/env python
#
# Copyright (C) 2010 Jacob Joaquin
#
# This file is part of slipmat.
# 
# slipmat is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# slipmat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with slipmat.  If not, see <http://www.gnu.org/licenses/>.

from slipmat import *

@Instr
def SimpleFM(dur, amp, pch, env, index=1, ratio=1):
    freq = cpspch(pch)                            # Convert pch to Hz
    env_1 = RiseFall(dur, env) * UVal(index)      # Index envelope
    env_2 = RiseFall(dur, 0) * UVal(amp)          # Amplitude envelope
    m = Sine(env_1, freq * ratio)                 # Modulator
    c = Sine(env_2, UVal(freq) + UVal(freq) * m)  # Carrier
    return(c)

s = ScoreEvents()
s.event(0, 2, SimpleFM(2, 0.5, 8.03, 0.125, 4))
s.event(2, 2, SimpleFM(2, 0.5, 8.07, 0.5, 16, 2))
s.event(4, 4, SimpleFM(4, 0.3, 7.00, 0.125, 16, 3))
s.event(4, 2, SimpleFM(4, 0.3, 8.05, 0.5, 4))
s.event(6, 2, SimpleFM(2, 0.3, 8.03, 0.5, 4))
ScoreEventsToWave(s, "./fm.wav")


