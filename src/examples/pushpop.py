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

s = ScoreEvents(tempo=120)

# Measure 1
s.event(0, 0.25, Sine(1, cpspch(7.00)))
s.event(1, 0.25, Sine(1, cpspch(7.03)))
s.event(2, 0.25, Sine(1, cpspch(7.07)))
s.event(3, 0.25, Sine(1, cpspch(7.10)))

# Measure 2
s.time.append(4)
s.event(0, 0.25, Sine(1, cpspch(8.00)))
s.event(1, 0.25, Sine(1, cpspch(8.03)))
s.event(2, 0.25, Sine(1, cpspch(8.07)))
s.event(3, 0.25, Sine(1, cpspch(8.10)))
s.time.pop()

# Measure 3
s.time.append(8)
s.event(0, 0.25, Sine(1, cpspch(9.00)))
s.event(1, 0.25, Sine(1, cpspch(9.03)))
s.event(2, 0.25, Sine(1, cpspch(9.07)))
s.event(3, 0.25, Sine(1, cpspch(9.10)))
s.time.pop()

# Measure 4
s.time.append(12)
s.event(0, 4, Sine(0.25, cpspch(9.00)))
s.event(0, 4, Sine(0.25, cpspch(8.03)))
s.event(0, 4, Sine(0.25, cpspch(8.07)))
s.event(0, 4, Sine(0.25, cpspch(8.10)))
s.time.pop()

ScoreEventsToWave(s, "./pushpop.wav")

