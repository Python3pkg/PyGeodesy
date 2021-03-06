
# -*- coding: utf-8 -*-

'''N-vector base class L{Nvector} and function L{sumOf}.

Pure Python implementation of n-vector-based geodesy tools for
ellipsoidal earth models.  Transcribed from JavaScript originals by
I{(C) Chris Veness 2005-2016} and published under the same MIT Licence**,
see U{http://www.movable-type.co.uk/scripts/latlong-vectors.html}.

@newfield example: Example, Examples
'''

from .bases import LatLonHeightBase
from .utils import fsum, len2
from .vector3d import Vector3d, sumOf as _sumOf

# from math import cos, sin

# all public constants, classes and functions
__all__ = ('NorthPole', 'SouthPole',  # constants
           'Nvector',  # classes
           'sumOf')  # functions
__version__ = '17.04.30'


class Nvector(Vector3d):  # XXX kept private
    '''Base class for ellipsoidal and spherical L{Nvector}.
    '''
    _h = 0     #: (INTERNAL) Height (meter).

    H = ''  #: Heigth prefix (string), '↑' in JS version

    def __init__(self, x, y, z, h=0):
        '''New n-vector normal to the earth's surface.

           @param x: X component (scalar).
           @param y: Y component (scalar).
           @param z: Z component (scalar).
           @keyword h: Height above surface (meter).

           @example:

           >>> from sphericalNvector import Nvector
           >>> v = Nvector(0.5, 0.5, 0.7071, 1)
           >>> v.toLatLon()  # 45.0°N, 045.0°E, +1.00m
        '''
        Vector3d.__init__(self, x, y, z)
        if h:
            self._h = float(h)

    def copy(self):
        '''Copy this vector.

           @return: Copy (L{Nvector}).
        '''
        n = Vector3d.copy(self)
        if n.h != self.h:
            n.h = self.h
        return n

    @property
    def h(self):
        '''Gets the height above surface (meter).
        '''
        return self._h

    @h.setter  # PYCHOK setter!
    def h(self, h):
        '''Sets height above surface.

           @param h: Height (meter).
        '''
        self._update(h != self._h)
        self._h = h

    def to3llh(self):
        '''Converts this n-vector to (geodetic) lat-, longitude
           and height.

           @return: 3-Tuple (lat, lon, height) in (degrees90,
                    degrees180, meter).
        '''
        return Vector3d.to2ll(self) + (self.h,)

    def to4xyzh(self):
        '''Returns this n-vector as a 4-tuple.

           @return: 4-Tuple (x, y, z, h) in (meter).
        '''
        return self.x, self.y, self.z, self.h

    def toStr(self, prec=5, fmt='(%s)', sep=', '):  # PYCHOK expected
        '''Returns a string representation of this n-vector.

           Height component is only included if non-zero.

           @keyword prec: Number of decimals, unstripped (int).
           @keyword fmt: Enclosing backets format (string).
           @keyword sep: Separator between components (string).

           @return: Comma-separated "x, y, z [, h]" (string).

           @example:

           >>> Nvector(0.5, 0.5, 0.7071).toStr()  # (0.5, 0.5, 0.7071)
           >>> Nvector(0.5, 0.5, 0.7071, 1).toStr(-3)  # (0.500, 0.500, 0.707, +1.00)
        '''
        t = Vector3d.toStr(self, prec=prec, fmt='%s', sep=sep)
        if self.h:
            t = '%s%s%s%+.2f' % (t, sep, self.H, self.h)
        return fmt % (t,)

    def unit(self):
        '''Normalizes this vector to unit length.

           @return: Normalised, unit vector (L{Nvector}).
        '''
        if self._united is None:
            u = Vector3d.unit(self).copy()
            if u.h != self.h:
                u.h = self.h
            self._united = u._united = u
        return self._united


NorthPole = Nvector(0, 0, +1)  #: North pole (L{Nvector}).
SouthPole = Nvector(0, 0, -1)  #: South pole (L{Nvector}).


class LatLonNvectorBase(LatLonHeightBase):
    '''(INTERNAL) Base class for n-vector-based ellipsoidal
        and spherical LatLon.
    '''

    def others(self, other, name='other'):
        '''Refines class comparison.

           @param other: The other point (L{LatLon}).
           @keyword name: Other's name (string).

           @raise TypeError: Incompatible type(other).
        '''
        try:
            LatLonHeightBase.others(self, other, name=name)
        except TypeError:
            if not isinstance(other, Nvector):
                raise

    def to4xyzh(self):
        '''Converts this (geodetic) point to n-vector (normal
           to the earth's surface) x/y/z components and height.

           @return: 4-Tuple (x, y, z, h) in (meter).
        '''
        # Kenneth Gade eqn (3), but using right-handed
        # vector x -> 0°E,0°N, y -> 90°E,0°N, z -> 90°N
#       a, b = self.to2ab()
#       ca = cos(a)
#       x, y, z = ca * cos(b), ca * sin(b), sin(a)
        return LatLonHeightBase.to3xyz(self) + (self.height,)


def sumOf(nvectors, Vector=Nvector, h=None, **kwds):
    '''Returns the vectorial sum of any number of n-vectors.

       @param nvectors: Vectors to be added (L{Nvector}[]).
       @keyword Vector: Vector class for sum (L{Nvector}).
       @keyword kwds: Optional, additional Vector keyword argments.
       @keyword h: Optional height, overriding the mean height (meter).

       @return: Vectorial sum (Vector).

       @raise ValueError: No nvectors.
    '''
    n, nvectors = len2(nvectors)
    if n < 1:
        raise ValueError('no nvectors: %r' & (n,))
    if h is None:
        m = fsum(v.h for v in nvectors) / n
    else:
        m = h
    return _sumOf(nvectors, Vector=Vector, h=m, **kwds)

# **) MIT License
#
# Copyright (C) 2016-2017 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
