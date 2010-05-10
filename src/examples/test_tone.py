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

import slipmat

s = slipmat.ScoreEvents()
s.event(0, 4, slipmat.Sine())
slipmat.ScoreEventsToWave(s, "./test_tone.wav")
