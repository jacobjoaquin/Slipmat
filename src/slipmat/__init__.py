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

'''WELCOME TO SLIPMAT!

SLIPMAT is a Python extension for computer music and audio 
synthesis. With it you will compose, live code, and remix
some of the most amazing digital instruments ever heard by
mortals. No laptop should be without one!
'''

import math
import operator
import struct

sr = 11025
ksmps = 100

class UGen:
    '''All unit generator classes inherit from this.'''

    def __init__(self): pass
    def __iter__(self): pass
    def next(self): raise StopIteration
    def __add__(self, ugen): return Add(self, ugen)
    def __mul__(self, ugen): return Mul(self, ugen)

class Instr():
    '''Creates a UGen class from a UGen returning function.'''

    def __init__(self, ugen_def, *args, **kwargs):
        self.ugen_def = ugen_def
        
    def __call__(self, *args, **kwargs):
        return self.__CreateUGen(self.ugen_def, *args, **kwargs)

    class __CreateUGen(UGen):
        def __init__(self, ugen_def, *args, **kwargs):
            self.ugen_def = ugen_def(*args, **kwargs)

        def __iter__(self):
            self.index = 0
            self._iter = (i for i in self.ugen_def)
            return self

        def next(self):
            if self.index >= ksmps: raise StopIteration
            self.index += 1
            return self._iter.next()

class __IterReduce(UGen):
    '''Reduces a list of iterators with the op function.'''

    op = operator.add

    def __init__(self, *ugens):
        self.ugens = ugens

    def __iter__(self):
        self.index = 0
        self.iters = [(j for j in i) for i in self.ugens]
        return self

    def next(self):
        if self.index >= ksmps: raise StopIteration
        self.index += 1
        return reduce(self.op, (i.next() for i in self.iters))

class Add(__IterReduce): pass
class Sub(__IterReduce): op = operator.sub
class Mul(__IterReduce): op = operator.mul

class RiseFall(UGen):
    '''A rise-fall envelope generator.'''

    def __init__(self, dur, peak=0.5):
        self.frames = sec_to_frames(dur)
        self.rise = int(peak * self.frames)
        self.fall = int(self.frames - self.rise)
        self.inc = 0
        self.v = 0

    def __iter__(self):
        self.index = 0

        if self.inc <= self.rise and self.rise != 0:
            self.v = self.inc / float(self.rise)
        else:
            self.v = (self.fall - (self.inc - self.rise)) / float(self.fall)

        self.inc += 1
        return self

    def next(self):
        if self.index >= ksmps: raise StopIteration
        self.index += 1
        return self.v

class Sine(UGen):
    '''A sine wave oscillator unit generator.'''

    def __init__(self, amp=1.0, freq=440, phase=0.0):
        self.amp = amp
        self.freq = float(freq)
        self.phase = phase

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        if self.index >= ksmps: raise StopIteration
        self.index += 1

        v = math.sin(self.phase * 2 * math.pi)
        self.phase += self.freq / sr
        return v * self.amp

class UVal(UGen):
    '''Convert a numeric value to a unit generator object.'''

    def __init__(self, v):
        self.v = v

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        if self.index >= ksmps: raise StopIteration
        self.index += 1
        return self.v

class ScoreEvents:
    '''Schedule unit generator events.'''

    def __init__(self, tempo=60):
        self.tempo = tempo
        self.event_dict = {}
        self.ID = 0
        self.last_frame = 0
        self.time = []

    def event(self, start, dur, ugen):
        t_start = sum(self.time, start)
        ugen_start = sec_to_frames(t_start * bps(self.tempo))
        ugen_end = ugen_start + sec_to_frames(dur * bps(self.tempo))
        self.last_frame = max(ugen_start, ugen_end, self.last_frame)

        if ugen_start not in self.event_dict.keys():
            self.event_dict.update({ugen_start: [(self.ID, 'start', ugen)]})
        else:
            self.event_dict[ugen_start].append((self.ID, 'start', ugen))

        if ugen_end not in self.event_dict.keys():
            self.event_dict.update({ugen_end: [(self.ID, 'stop', None)]})
        else:
            self.event_dict[ugen_end].append((self.ID, 'stop', None))

        self.ID += 1

def bps(tempo):
    '''Beats per second.'''
    
    return 60 / float(tempo)

def cpspch(p):
    '''Convert pitch class to frequency.'''
    
    octave, note = divmod(p, 1)
    return 440 * 2 ** (((octave - 8) * 12 + ((note * 100) - 9)) / 12.0)
        
def sec_to_frames(dur):
    '''Convert seconds into frames.'''
    
    return int(dur * sr / float(ksmps))

def ScoreEventsToWave(score, filename):
    '''Generate a wave file from a ScoreEvent object.'''
    
    events = {}
    wave = open(filename, 'wb')
    chunk_2_size = score.last_frame * ksmps * 2  
    wave.write(struct.pack('< 4s I 4s', 'RIFF', 36 + chunk_2_size, 'WAVE'))
    wave.write(struct.pack('< 4s I 2h 2I 2h', 'fmt ', 16, 1, 1, sr, \
                           sr * 2, 2, 16))                        
    wave.write(struct.pack('< 4s I', 'data', chunk_2_size))
        
    for f in range(score.last_frame + 1):
        print '%d:' % f

        if f in score.event_dict:
            for L in score.event_dict[f]:
                ID, command, function = L

                if command == 'start':
                    events.update({ID: function})
                elif command == 'stop':
                    del events[ID]

        iters = [(j for j in v) for v in events.itervalues()]

        for i in range(ksmps):
            if iters:
                v = reduce(operator.add, (i.next() for i in iters))
            else:
                v = 0

            if v > 1: v = 1
            if v < -1: v = -1
            
            wave.write(struct.pack('h', int(v * 32767)))

    wave.close()
