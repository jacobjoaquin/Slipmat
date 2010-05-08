#!/usr/bin/env python

from slipmat import *
from random import random

@Instr
def Ping(amp=1, freq=440): return Sine(amp, freq)

s = ScoreEvents(tempo=120)

s.event(0, 0.25, Ping(freq=cpspch(7.00)))
s.event(1, 0.25, Ping(freq=cpspch(7.01)))
s.event(2, 0.25, Ping(freq=cpspch(7.02)))
s.event(3, 0.25, Ping(freq=cpspch(7.03)))

s.time.append(4)
s.event(0, 0.25, Ping(freq=cpspch(8.00)))
s.event(1, 0.25, Ping(freq=cpspch(8.01)))
s.event(2, 0.25, Ping(freq=cpspch(8.02)))
s.event(3, 0.25, Ping(freq=cpspch(8.03)))
s.time.pop()

s.time.append(8)
s.event([0, 1, 2, 3], 0.25, Ping(freq=cpspch(9.00)))
s.time.pop()

ScoreEventsToWave(s, "./pushpop.wav")
