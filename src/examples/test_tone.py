#!/usr/bin/env python

import slipmat

slipmat.sr = 11025
slipmat.ksmps = 25

s = slipmat.ScoreEvents()
s.event(0, 4, slipmat.Sine())
slipmat.ScoreEventsToWave(s, "./test_tone.wav")
