#!/usr/bin/env python

import cProfile
from slipmat import *
import random

def main():    
    # Instruments
    @Instr
    def RingTine(dur, amp, freq_1, freq_2, peak=0):
        '''Two ring modulated sine waves with an amplitude envelope.'''
        
        return Sine(amp, freq_1) * Sine(amp, freq_2) * RiseFall(dur, peak)
    
    @Instr
    def DirtySine(dur, amp, freq, peak):
        amp = 1.0 / 1.44 * amp
        a1 = Sine(1, freq)
        a2 = Sine(0.1, freq * 3)
        a3 = Sine(0.24, freq * 5)
        a4 = Sine(0.1, freq * 1.15)
        ring = a1 + (a2 + a3 + a4) * Sine(1, 1.003)
        return ring * RiseFall(dur, peak) * UVal(amp)
    
    # Event Generators
    def dusty_vinyl(s, start, dur, amp, freq_min, freq_max, density):
        '''Granular Sine Event Generator.'''
        
        for i in range(int(density * dur)):
            freq = random.random() * (freq_max - freq_min) + freq_min
            t = random.random() * (dur - start) + start
            s.event(t, 1 / freq, Sine(amp * random.random(), freq))
    
    def sine_arp(s, start, bars, res, amp, note_list, decay):
        offset = start
        b = 60.0 / s.tempo  # duration of a beat in seconds
        
        for bar in range(bars):
            n = 0
            while n < 4.0 / res:
                note = cpspch(note_list[n % len(note_list)])
                ugen = Sine(amp, note) * RiseFall(decay * b, 0)
                s.event(offset, decay, ugen)
                n += 1
                offset = start + bar * 4 + n * res
             
    # Score
    s = ScoreEvents(tempo=169)
    b = 60.0 / s.tempo
    
    dusty_vinyl(s, 0, 80, 0.25, 1000, 10000, 30 * 60 / 169.0)
    
    s.event(6, 16, DirtySine(16 * b, 0.15, cpspch(8.07), 0.95))
    s.event(22, 4, RingTine(4, 0.5, cpspch(10.10), 55, 0))
    
    n = [8.00, 8.03, 8.02, 8.07, 8.05, 8.10, 8.09, 9.00]    
    sine_arp(s, 22, 8, 0.25, 0.1, n, 0.8)
    
    s.event(26, 9, RingTine(9, 0.3, cpspch(9.03), 33, 0.9))
    s.event(33, 9, RingTine(9, 0.5, cpspch(8.10), 55, 0))
    s.event(40, 9, RingTine(9, 0.25, cpspch(7.00), 11, 0))
    
    s.event(54.5, 9, RingTine(9 * b, 0.3, cpspch(9.03), 33, 0.1))
    s.event(54, 9, RingTine(9 * b, 0.5, cpspch(8.07), 44, 0))
    s.event(54, 8, DirtySine(8 * b, 0.15, cpspch(7.07), 0.1))
    s.event(60, 4, DirtySine(4 * b, 0.15, cpspch(6.07), 0.1))
    
    ScoreEventsToWave(s, 'slipmat_lead-in.wav')
    
    
if __name__ == '__main__':
    main()



