#!/usr/bin/env python
# easyFig.py   Written by: Mitchell Sullivan   mjsull@gmail.com
# Supervisor: Dr. Scott Beatson and Dr. Nico Petty University of Queensland
# Version 2.2.3 08.11.2016
# License: GPLv3

import os
import subprocess
from math import ceil, hypot
import threading
import time
import struct
import base64
import string
from ftplib import FTP
import tarfile
import platform
import shutil
import webbrowser
import operator
import sys


def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def binar(s):
  transdict = {'0':'0000',
               '1':'0001',
               '2':'0010',
               '3':'0011',
               '4':'0100',
               '5':'0101',
               '6':'0110',
               '7':'0111',
               '8':'1000',
               '9':'1001',
               'a':'1010',
               'b':'1011',
               'c':'1100',
               'd':'1101',
               'e':'1110',
               'f':'1111'
  }
  outstring = ''
  for i in s:
    outstring += transdict[i]
  return outstring

class scalableVectorGraphics:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.out = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="%d"
   width="%d"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="easyfig">
  <metadata
     id="metadata122">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Easyfig</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs120" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="640"
     inkscape:window-height="480"
     id="namedview118"
     showgrid="false"
     inkscape:zoom="0.0584"
     inkscape:cx="2500"
     inkscape:cy="75.5"
     inkscape:window-x="55"
     inkscape:window-y="34"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <title
     id="title4">Easyfig</title>
  <g
     style="fill-opacity:1.0; stroke:black; stroke-width:1;"
     id="g6">''' % (self.height, self.width)

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0)):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" />\n' % (x1, y1, x2, y2, th, colorstr(cl))

    def writesvg(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.out + ' </g>\n</svg>')
        outfile.close()

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=0):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr(fill), lt)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill, lt=1):
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"\n' % size
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'

# class of blast hit data
class BlastHit:
    def __init__(self, query, ref, ident, length, mismatch, gaps, qStart, qEnd, rStart, rEnd, eValue, bitscore):
        self.query = query
        self.ref = ref
        self.ident = float(ident)
        self.length = int(length)
        self.mismatch = int(mismatch)
        self.gaps = int(gaps)
        self.qStart = int(qStart)
        self.qEnd = int(qEnd)
        self.rStart = int(rStart)
        self.rEnd = int(rEnd)
        self.eValue = float(eValue)
        self.bitscore = float(bitscore)
# class for feature data
class feature:
  def __init__(self, start, stop, type, strand, colour, name):
    self.start = start
    self.stop = stop
    self.type = type
    self.strand = strand
    self.colour = colour
    self.name = name
  def length(self):
    if type(self.start) == int:
      return self.stop - self.start
    else:
      return self.stop[-1] - self.start[0]

# method for converting base pair position into pixel position
def convertPos(length, maxlength, width, pos, aln):
    if aln == 'centre':
        return int(((((maxlength - length) * 1.0 /2) + pos) * 1.0 /maxlength) * width)
    elif aln == 'left':
        return int(((pos * 1.0 /maxlength) * width))
    elif aln == 'right':
        return int(((((maxlength - length) * 1.0) + pos) * 1.0 /maxlength) * width)
    elif aln == 'best blast':
        return int((((pos + shifter) * 1.0 /maxlength) * width))

# method for converting base pair position into pixel position if the genome has been reversed
def convertPosR(length, maxlength, width, pos, aln):
    if aln == 'centre':
        return int(width - (((((maxlength - length) * 1.0 /2) + pos) * 1.0 /maxlength) * width))
    elif aln == 'left':
        return int(width - (((((maxlength - length) * 1.0) + pos) * 1.0 /maxlength) * width))
    elif aln == 'right':
        return int(width - ((pos * 1.0 /maxlength) * width))
    elif aln == 'best blast':
        return int(width - (((((maxlength - length) * 1.0) + pos - shifter) * 1.0 /maxlength) * width))

''' Functions and classes for the bmp module.
This section of the code uses a modified version of Paul McGuire's
(http://www.geocities.com/ptmcg/) (RIP geocities/under constuction gifs)
bmp.py - module for constructing simple BMP graphics files
It is freely avaiable under the following license


license for all code contained:

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
def shortToString(i):
  hi = (i & 0xff00) >> 8
  lo = i & 0x00ff
  return chr(lo) + chr(hi)

def longToString(i):
  hi = (long(i) & 0x7fff0000) >> 16
  lo = long(i) & 0x0000ffff
  return shortToString(lo) + shortToString(hi)

#  class
class Color(object):
  """class for specifying s while drawing BitMap elements"""
  __slots__ = [ 'red', 'grn', 'blu' ]
  __shade = 32

  def __init__( self, r=0, g=0, b=0 ):
    self.red = r
    self.grn = g
    self.blu = b

  def __setattr__(self, name, value):
    if hasattr(self, name):
      raise AttributeError, "Color is immutable"
    else:
      object.__setattr__(self, name, value)

  def __str__( self ):
    return "R:%d G:%d B:%d" % (self.red, self.grn, self.blu )

  def __hash__( self ):
    return ( ( long(self.blu) ) +
              ( long(self.grn) <<  8 ) +
              ( long(self.red) << 16 ) )

  def __eq__( self, other ):
    return (self is other) or (self.toLong == other.toLong)

  def lighten( self ):
    return Color(
      min( self.red + Color.__shade, 255),
      min( self.grn + Color.__shade, 255),
      min( self.blu + Color.__shade, 255)
      )

  def darken( self ):
    return Color(
      max( self.red - Color.__shade, 0),
      max( self.grn - Color.__shade, 0),
      max( self.blu - Color.__shade, 0)
      )

  def toLong( self ):
    return self.__hash__()

  def fromLong( l ):
    b = l & 0xff
    l = l >> 8
    g = l & 0xff
    l = l >> 8
    r = l & 0xff
    return Color( r, g, b )
  fromLong = staticmethod(fromLong)

# define class constants for common s
Color.BLACK    = Color(   0,   0,   0 )
Color.RED      = Color( 255,   0,   0 )
Color.GREEN    = Color(   0, 255,   0 )
Color.BLUE     = Color(   0,   0, 255 )
Color.CYAN     = Color(   0, 255, 255 )
Color.MAGENTA  = Color( 255,   0, 255 )
Color.YELLOW   = Color( 255, 255,   0 )
Color.WHITE    = Color( 255, 255, 255 )
Color.DKRED    = Color( 128,   0,   0 )
Color.DKGREEN  = Color(   0, 128,   0 )
Color.DKBLUE   = Color(   0,   0, 128 )
Color.TEAL     = Color(   0, 128, 128 )
Color.PURPLE   = Color( 128,   0, 128 )
Color.BROWN    = Color( 128, 128,   0 )
Color.GRAY     = Color( 128, 128, 128 )






class BitMap(object):
  """class for drawing and saving simple Windows bitmap files"""

  LINE_SOLID  = 0
  LINE_DASHED = 1
  LINE_DOTTED = 2
  LINE_DOT_DASH=3
  _DASH_LEN = 12.0
  _DOT_LEN = 6.0
  _DOT_DASH_LEN = _DOT_LEN + _DASH_LEN


  def __init__( self, width, height,
                 bkgd = Color.WHITE, frgd = Color.BLACK ):
    self.wd = int( ceil(width) )
    self.ht = int( ceil(height) )
    self.bg = 0
    self.fg = 1
    self.palette = []
    self.palette.append( bkgd.toLong() )
    self.palette.append( frgd.toLong() )
    self.setDefaultPenColor()

    tmparray = [ self.bg ] * self.wd
    self.bitarray = [ tmparray[:] for i in range( self.ht ) ]
    self.currentPen = 1
    self.fontName = "%s-%d-%s" % ( "none", 0, "none" )
    self.defsize = 64
    self.amatrixwid = 41
    self.amatrixhei = 48
    self.amatrixori = 16
    self.amatrix = '3ff8000001ffffc00003fffff80003fffffe0003ffffff8003ffffffe003\
fffffff801ff801ffc01ff0001fe00ff00007f80ff00003fc07f80000fe0\
3fc00007f01fc00003f80fe00001fc00000000fe000000007f000000007f\
800000003fc0000000ffe000000ffff00003fffff8001ffffffc003fffff\
fe007fffff7f00fffff83f807fff001fc07ff8000fe07fe00007f03fc000\
03f81fe00001fc1fe00000fe0fe000007f07f000003f83f800001fc1fc00\
001fe0fe00000ff07f00000ff83fc0000ffc0ff0001ffe07fc001fff01ff\
807fffc0ffffffcffe3fffffc7ff0fffffc3ff83ffff80ffc07fff007fe0\
07f8000fe'
    self.bmatrixwid = 40
    self.bmatrixhei = 64
    self.bmatrixori = 0
    self.bmatrix = '7f000000007f000000007f000000007f000000007f000000007f00000000\
7f000000007f000000007f000000007f000000007f000000007f00000000\
7f000000007f000000007f000000007f000000007f007fc0007f03fff800\
7f07fffe007f1fffff007f3fffff807f7fffffc07f7fffffe07fff00fff0\
7ffc003ff07ff8000ff87ff00007f87fe00003fc7fe00003fc7fc00001fe\
7fc00001fe7f800000fe7f800000fe7f800000fe7f000000ff7f0000007f\
7f0000007f7f0000007fff0000007fff0000007fff0000007fff0000007f\
ff0000007fff0000007fff0000007fff800000feff800000feff800000fe\
ff800000feffc00001feffc00001fcffe00003fcffe00007f8fff00007f8\
fff8000ff8fffe003ff0ffff80ffe0feffffffe0fe7fffffc0fe3fffff80\
fe1ffffe00fe0ffffc000003fff00000003f0000'
    self.cmatrixwid = 37
    self.cmatrixhei = 48
    self.cmatrixori = 16
    self.cmatrix = '1ff0000007fff00000ffffe0001fffff8001ffffff001ffffff801ffffff\
e00ffc01ff80ff8007fc0ff8001ff07f80007f87f80001fe3fc0000ff1fc\
00003f9fe00001fcfe00000fe7f00000003f80000001f80000001fc00000\
00fe00000007f00000003f80000001fc0000000fe00000007f00000003f8\
0000001fc0000000fe00000007f00000001fc0000000fe000007f7f00000\
3fbfc00003f8fe00001fc7f80000fe3fc0000ff0ff0000ff07fc000ff81f\
f000ff807fe01ffc03ffffffc00ffffffc003fffffc000fffffc0001ffff\
c00003fff8000001fc000'
    self.dmatrixwid = 40
    self.dmatrixhei = 64
    self.dmatrixori = 0
    self.dmatrix = '7f000000007f000000007f000000007f000000007f000000007f00000000\
7f000000007f000000007f000000007f000000007f000000007f00000000\
7f000000007f000000007f000000007f0003ff007f001fffc07f003ffff0\
7f00fffffc7f01fffffe7f03ffffff7f07ffffffff0fff00ffff0ffc003f\
ff1ff0000fff1fe00007ff3fe00003ff3fc00003ff7f800001ff7f800001\
ff7f000000ff7f000000ff7f000000ffff000000fffe0000007ffe000000\
7ffe0000007ffe0000007ffe0000007ffe0000007ffe0000007ffe000000\
7ffe0000007ffe0000007f7f000000ff7f000000ff7f000000ff7f000000\
ff7f800001ff3f800001ff3fc00003ff3fe00003ff1ff00007ff1ff8000f\
ff0ffc003fff07ff00ffff07ffffff7f03fffffe7f01fffffc7f00fffff8\
7f003ffff07f000fffc0000000fc0000'
    self.ematrixwid = 39
    self.ematrixhei = 48
    self.ematrixori = 16
    self.ematrix = '1ff0000001fffe00000fffff00003fffff0001ffffff0007ffffff001fff\
ffff003ff007ff00ff8003ff03fe0003fe07f80001fe0fe00003fc3f8000\
03fc7f000003f9fc000007f3f800000fe7f000000fcfc000001fff800000\
3fff0000007fffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffff800000007f00000000fe00000001fc00000001f800000003\
f800000007f000001fcfe000003f8fe00000ff1fc00001fc3fc00007f83f\
c0001fe07fc0003fc07fe001ff007ff00ffe00fffffff800ffffffe000ff\
ffff80007ffffe00007ffff000003fff80000007f8000'
    self.fmatrixwid = 20
    self.fmatrixhei = 62
    self.fmatrixori = 0
    self.fmatrix = '7f003ff007ff00fff01fff01fff01fe003fc003f8003f8003f8003f8003f\
8003f8003f8003f8003f80ffffffffffffffffffffffffffffff03f8003f\
8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f\
8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f\
8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f\
8003f80'
    self.gmatrixwid = 39
    self.gmatrixhei = 65
    self.gmatrixori = 16
    self.gmatrix = '1ff0000000fff80fe007fffc1fc03ffffc3f80fffffc7f03fffffcfe0fff\
fffdfc1ff807fff87fc003fff1ff0003ffe3fc0003ffcff00003ff9fe000\
03ff3f800007feff000007fdfc00000ffbf800001ff7f000003fefc00000\
3fff8000007fff000000fffe000001fffc000003fff8000007fff000000f\
ffe000001fffc000003fff8000007fff000000fffe000001fefe000007fd\
fc00000ffbf800001ff7f800007fe7f00000ffcff00001ff9fe00007ff1f\
e0001ffe3fe0007ffc3fe001fff83ff00feff07fffffdfe07fffff3fc07f\
fffc7f807ffff0ff003fff81fe001ffe03f80007c007f00000000fe00000\
003fc00000007f9fc00000ff3f800001fc7f800007f87f00000ff0ff0000\
3fc1ff0000ff81ff0007fe01ff803ff803fffffff003ffffffc003fffffe\
0001fffff80000ffff8000001ff8000'
    self.hmatrixwid = 35
    self.hmatrixhei = 62
    self.hmatrixori = 0
    self.hmatrix = '3f80000007f0000000fe0000001fc0000003f80000007f0000000fe00000\
01fc0000003f80000007f0000000fe0000001fc0000003f80000007f0000\
000fe0000001fc0000003f803fe007f03fffc0fe0ffffc1fc7ffffe3f9ff\
fffe7f7fffffcfffe01ffdfff000ffbffc000ff7ff0000ffffc0001ffff0\
0001fffe00003fff800007fff00000fffe00001fff800003fff000007ffe\
00000fffc00001fff800003fff000007ffe00000fffc00001fff800003ff\
f000007ffe00000fffc00001fff800003fff000007ffe00000fffc00001f\
ff800003fff000007ffe00000fffc00001fff800003fff000007ffe00000\
fffc00001fff800003fff000007ffe00000fffc00001fff800003fff0000\
07f'
    self.imatrixwid = 7
    self.imatrixhei = 63
    self.imatrixori = 0
    self.imatrix = '1fffffffffffffffc0000000000000007fffffffffffffffffffffffffff\
fffffffffffffffffffffffffffffffffffffffffffffffffff'
    self.jmatrixwid = 14
    self.jmatrixhei = 80
    self.jmatrixori = 0
    self.jmatrix = '1fc07f01fc07f01fc07f01fc07f01fc00000000000000000000000000000\
7f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01\
fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07\
f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01fc07f01f\
c07f01fc0ff03fc1fffffbffefff3ff8ffc3f00'
    self.kmatrixwid = 38
    self.kmatrixhei = 62
    self.kmatrixori = 0
    self.kmatrix = 'fe00000003f80000000fe00000003f80000000fe00000003f80000000fe0\
0000003f80000000fe00000003f80000000fe00000003f80000000fe0000\
0003f80000000fe00000003f80000000fe00000003f80001ff8fe0000ff8\
3f80007fc0fe0003fe03f8001ff00fe000ff803f8007fc00fe003fe003f8\
01ff000fe00ff8003f807fc000fe03fe0003f81ff0000fe0ff80003f87fc\
0000fe3fe00003f9ffc0000fe7ff80003fbffe0000fffffc0003fffff000\
0fffbfe0003ffc7fc000ffe0ff0003ff03fe000ff807fc003fc01ff000fe\
003fe003f8007f800fe001ff003f8003fe00fe0007f803f8001ff00fe000\
3fe03f8000ff80fe0001ff03f80003fc0fe0000ff83f80001ff0fe00003f\
c3f80000ff8fe00001fe3f800007fcfe00000ffbf800001ff'
    self.lmatrixwid = 7
    self.lmatrixhei = 62
    self.lmatrixori = 0
    self.lmatrix = '3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
fffffffffffffffffffffffffffffffffffffffffffffffff'
    self.mmatrixwid = 59
    self.mmatrixhei = 46
    self.mmatrixori = 16
    self.mmatrix = '3fe0001ff007f03fff001fffc0fe0ffff807fffe1fc7ffff83ffffe3f9ff\
fff8fffffe7f7fffffbfffffcfffc07ffff01ffdffe003fff800ffbff800\
3ffe000ffffe0003ff8000ffff80007fe0001ffff00007fc0001fffc0000\
ff00003fff80001fe00007ffe00003f80000fffc00007f00001fff80000f\
e00003fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe\
00003fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe0\
0003fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe00\
003fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe000\
03fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe0000\
3fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe00003\
fff00001fc00007ffe00003f80000fffc00007f00001fff80000fe00003f\
ff00001fc00007f'
    self.nmatrixwid = 35
    self.nmatrixhei = 46
    self.nmatrixori = 16
    self.nmatrix = '1fe007f01fff80fe0ffffc1fc3ffffc3f8fffffc7f3fffffcfefe01ffdff\
f001ffbffc000ff7ff0001ffffc0001ffff00001fffe00003fff800007ff\
f00000fffe00001fff800003fff000007ffe00000fffc00001fff800003f\
ff000007ffe00000fffc00001fff800003fff000007ffe00000fffc00001\
fff800003fff000007ffe00000fffc00001fff800003fff000007ffe0000\
0fffc00001fff800003fff000007ffe00000fffc00001fff800003fff000\
007ffe00000fffc00001fff800003fff000007f'
    self.omatrixwid = 40
    self.omatrixhei = 48
    self.omatrixori = 16
    self.omatrix = '1ff8000000ffff000003ffffc0000ffffff0001ffffff8003ffffffc007f\
fffffe00fff00fff00ffc003ff01ff0000ff81fe00007f83fc00003fc3fc\
00003fc3f800001fc7f800001fe7f000000fe7f000000fe7f000000fefe0\
00000fffe0000007ffe0000007ffe0000007ffe0000007ffe0000007ffe0\
000007ffe0000007ffe0000007ffe0000007ffe0000007fff000000ff7f0\
00000fe7f000000fe7f000000fe7f800001fe3f800001fc3fc00003fc3fc\
00003fc1fe00007f81ff0000ff80ffc003ff007ff00ffe007ffffffe003f\
fffffc001ffffff8000fffffe00003ffffc00000ffff0000000ff0000'
    self.pmatrixwid = 40
    self.pmatrixhei = 64
    self.pmatrixori = 16
    self.pmatrix = '7fc000fe03fff800fe0ffffe00fe1fffff00fe3fffff80fe7fffffc0feff\
ffffe0ffff00fff0fffc003ff0fff8000ff8fff00007f8ffe00003fcffe0\
0003fcffc00001fcffc00001feff800000feff800000feff800000feff00\
0000ffff0000007fff0000007fff0000007fff0000007fff0000007fff00\
00007f7f0000007f7f0000007f7f0000007f7f0000007f7f800000ff7f80\
0000fe7f800000fe7f800000fe7fc00001fe7fc00001fc7fe00003fc7fe0\
0007fc7ff0000ff87ff8001ff87ffc003ff07fff80fff07fffffffe07f7f\
ffffc07f3fffff807f1fffff007f07fffc007f01fff0007f003f80007f00\
0000007f000000007f000000007f000000007f000000007f000000007f00\
0000007f000000007f000000007f000000007f000000007f000000007f00\
0000007f000000007f000000007f00000000'
    self.qmatrixwid = 40
    self.qmatrixhei = 64
    self.qmatrixori = 16
    self.qmatrix = '1fe0000000fffc07f003ffff07f00fffff87f01fffffe7f03ffffff7f07f\
fffff7f07ff007fff0ffc003fff1ff0000fff1fe00007ff3fe00003ff3fc\
00003ff3f800001ff7f800001ff7f000000ff7f000000ff7f000000ff7f0\
00000fffe0000007ffe0000007ffe0000007ffe0000007ffe0000007ffe0\
000007ffe0000007ffe0000007ffe0000007ffe0000007fff000000ff7f0\
00000ff7f000000ff7f000000ff7f800001ff7f800001ff3fc00003ff3fe\
00003ff1ff00007ff1ff8000fff0ffc003fff0fff00ffff07ffffff7f03f\
fffff7f01fffffe7f00fffff87f003ffff07f000fffc07f0001fc007f000\
000007f000000007f000000007f000000007f000000007f000000007f000\
000007f000000007f000000007f000000007f000000007f000000007f000\
000007f000000007f000000007f000000007f'
    self.rmatrixwid = 22
    self.rmatrixhei = 46
    self.rmatrixori = 16
    self.rmatrix = '3bf80fffe07fff87fffe3ffff9ffffe7ffffbfe0fffc03ffc00ffe003ff0\
00ff8003fe000ff0003fc000ff0003f8000fe0003f8000fe0003f8000fe0\
003f8000fe0003f8000fe0003f8000fe0003f8000fe0003f8000fe0003f8\
000fe0003f8000fe0003f8000fe0003f8000fe0003f8000fe0003f8000fe\
0003f8000'
    self.smatrixwid = 36
    self.smatrixhei = 48
    self.smatrixori = 16
    self.smatrix = '7fe000003fffc0001fffff0003fffffc007fffffe00fffffff01fffffff0\
1ff803ff83fe0007f83f80007f87f80003fc7f00001fc7f00001fc7f0000\
1fc7f00000007f00000007f80000003fc0000003ff8000003fff000001ff\
ff00000fffff00007fffff0001fffffc0007fffff0001fffff80001ffffc\
00001fffc000001ffe0000003fe0000001ff0000000ff00000007ffe0000\
07ffe000007fff000007f7f000007f7f80000fe7f80001fe7fe0007fe3ff\
801ffc3fffffff81fffffff80fffffff007fffffc001fffff80007fffc00\
0007fc000'
    self.tmatrixwid = 20
    self.tmatrixhei = 59
    self.tmatrixori = 5
    self.tmatrix = '3f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f80f\
fffffffffffffffffffffffffffff03f8003f8003f8003f8003f8003f800\
3f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f800\
3f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f800\
3f8003f8003f8003f8003fc003fff03fff01fff00fff007ff001fe'
    self.umatrixwid = 35
    self.umatrixhei = 47
    self.umatrixori = 17
    self.umatrix = '1fc00001fff800003fff000007ffe00000fffc00001fff800003fff00000\
7ffe00000fffc00001fff800003fff000007ffe00000fffc00001fff8000\
03fff000007ffe00000fffc00001fff800003fff000007ffe00000fffc00\
001fff800003fff000007ffe00000fffc00001fff800003fff000007ffe0\
0000fffc00001fff800003fff000007ffe00001fffc00003fff800007fff\
00001fffe00003fffe0000ffffe0003ffbfc000fff7fe003ffeffe03fdfc\
ffffff3f8fffffc7f0fffff0fe0ffffc1fc07ffe000001fe0000'
    self.vmatrixwid = 40
    self.vmatrixhei = 45
    self.vmatrixori = 17
    self.vmatrix = 'ff000000ffff000000ff7f800001fe7f800001fe7f800001fe3fc00003fc\
3fc00003fc3fc00003f81fe00007f81fe00007f81fe00007f00ff0000ff0\
0ff0000ff007f0000fe007f8001fe007f8001fc003f8001fc003fc003fc0\
03fc003f8001fc003f8001fe007f8001fe007f0000fe007f0000ff00fe00\
00ff00fe00007f00fe00007f01fc00007f81fc00003f83f800003f83f800\
003fc3f800001fc7f000001fc7f000000fe7f000000fefe000000fefe000\
0007ffc0000007ffc0000007ffc0000003ff80000003ff80000003ff8000\
0001ff00000001ff00000001fe0000'
    self.wmatrixwid = 60
    self.wmatrixhei = 45
    self.wmatrixori = 17
    self.wmatrix = 'ff00003fc0000ff7f00007fe0000ff7f80007fe0001fe7f80007fe0001fe\
7f80007fe0001fe3f8000fff0001fc3fc000fff0003fc3fc000fff0003fc\
1fc000fff0003f81fc001fff8003f81fe001fff8007f81fe001fbf8007f8\
0fe001fbf8007f00fe003f9fc007f00ff003f9fc00ff007f003f1fc00fe0\
07f003f1fc00fe007f007f0fe00fe007f807f0fe01fe003f807e0fe01fc0\
03f807e07f01fc003fc0fe07f01fc001fc0fe07f03f8001fc0fc07f03f80\
01fc0fc03f83f8001fe1fc03f83f8000fe1fc03f87f0000fe1f803f87f00\
00fe1f801fc7f00007f3f801fc7e00007f3f801fcfe00007f3f001fcfe00\
007f3f000fefe00003fff000fefc00003fff000fffc00003ffe000fffc00\
001ffe0007ff800001ffe0007ff800001ffe0007ff800001ffc0007ff800\
000ffc0003ff000000ffc0003ff000000ffc0003ff0000007f80003fe000\
0007f80001fe000'
    self.xmatrixwid = 39
    self.xmatrixhei = 45
    self.xmatrixori = 17
    self.xmatrix = '3fe00000ff3fc00003fc3fc0000ff03fc0001fc07f80007f807f8001fe00\
7f8003f800ff000ff000ff003fc000ff007f0001fe01fe0001fe07f80001\
fe0fe00003fc3fc00003fcff000003fdfc000007fff0000007ffe0000007\
ff8000000ffe0000000ffc0000000ff00000001fe00000007fe0000000ff\
e0000003ffc000000fffc000003fffc000007f7f800001fe7f800007f87f\
80000fe0ff00003fc0ff0000ff00ff0001fc01fe0007f801fe001fe001fe\
003f8003fc00ff0003fc03fc0007fc0ff00007f81fe00007f87f80000ff9\
fe00000ff7fc00000ff'
    self.ymatrixwid = 39
    self.ymatrixhei = 64
    self.ymatrixori = 17
    self.ymatrix = 'fe000001fffe000007f9fc00000ff3f800001fc7f800007f8ff00000ff0f\
e00001fc1fe00007f83fc0000ff03f80001fc07f80007f80ff0000ff00fe\
0001fc01fe0007f803fc000fe003f8001fc007f8007f800ff000fe000fe0\
01fc001fe007f8003fc00fe0003f803fc0007f807f8000ff00fe0000fe03\
fc0001fc07f00003fc0fe00003f83fc00007f07f00000ff0fe00000fe3fc\
00001fc7f000003fcfe000003fbfc000007f7f000000fffe000000fff800\
0001fff0000003ffe0000003ff80000007ff0000000ffe0000000ff80000\
001ff00000003fe00000003f80000000ff00000001fe00000003f8000000\
0ff00000001fc00000007f80000000ff00000001fc00000007f80000001f\
f00000007fc000003fff8000007ffe000000fff8000001ffe0000003ff80\
000007fe00000003e0000000'
    self.zmatrixwid = 36
    self.zmatrixhei = 45
    self.zmatrixori = 17
    self.zmatrix = '7fffffffe7fffffffe7fffffffe7fffffffe7fffffffe7fffffffe000000\
3fc0000007f8000000ff8000001ff0000001fe0000003fc0000007f80000\
00ff8000001ff0000003fe0000003fc0000007f8000000ff8000001ff000\
0003fe0000003fc0000007f8000000ff8000001ff0000003fe0000003fc0\
000007f8000000ff8000001ff0000003fe0000003fc0000007fc000000ff\
8000001ff0000003fe0000003fc0000007fc000000ff8000000fffffffff\
fffffffffffffffffffffffffffffffffffffffffffff'
    self.Amatrixwid = 55
    self.Amatrixhei = 62
    self.Amatrixori = 0
    self.Amatrix = 'ffe00000000001ffc00000000003ffc0000000000fff80000000001fff00\
000000003fff0000000000fffe0000000001fffc0000000003fffc000000\
000ff7f8000000001feff0000000007fcff000000000ff1fe000000001fe\
3fc000000007f83fc00000000ff07f800000001fe0ff800000007f80ff00\
000000ff01fe00000001fe03fe00000007f803fc0000000ff007f8000000\
1fe00ff80000007f800ff0000000ff001fe0000003fe003fe0000007f800\
3fc000000ff0007f8000003fc000ff8000007f8000ff000000ff0001fe00\
0003fc0003fe000007f80003fc00000ff00007fc00003fc0000ff800007f\
80000ff00000ff00001ff00003ffffffffe00007ffffffffc0001fffffff\
ffc0003fffffffff80007fffffffff0001ffffffffff0003fffffffffe00\
07f8000003fc001ff0000007fc003fc000000ff8007f8000000ff001ff00\
00001ff003fc0000003fe007f80000003fc01ff00000007fc03fc0000000\
ff80ff80000000ff81ff00000001ff03fc00000003fe0ff800000003fe1f\
e000000007fc3fc00000000ff8ff800000000ff9fe000000001ff7fc0000\
00001ff'
    self.Bmatrixwid = 46
    self.Bmatrixhei = 62
    self.Bmatrixori = 0
    self.Bmatrix = 'fffffffc0003ffffffff000fffffffff003ffffffffe00fffffffffc03ff\
fffffff80ffffffffff03fc00001ffe0ff000001ff83fc000003ff0ff000\
0007fc3fc000000ff0ff0000003fe3fc0000007f8ff0000001fe3fc00000\
07f8ff0000001fe3fc0000007f8ff0000001fe3fc0000007f0ff0000001f\
c3fc000000ff0ff0000003f83fc000001fe0ff000000ff83fc000007fc0f\
f00000ffe03fffffffff00fffffffff003ffffffff800fffffffff803fff\
ffffff80ffffffffff03ffffffffff0ff000001ffc3fc000001ff8ff0000\
001ff3fc0000003feff0000000ffbfc0000001feff00000007fbfc000000\
0ffff00000003fffc0000000ffff00000003fffc0000000ffff00000003f\
bfc0000000feff00000007fbfc0000001feff00000007fbfc0000003fcff\
0000001ff3fc000000ff8ff000000ffe3ffffffffff0ffffffffff83ffff\
fffffc0fffffffffe03fffffffff00fffffffff003fffffffc000'
    self.Cmatrixwid = 53
    self.Cmatrixhei = 65
    self.Cmatrixori = -1
    self.Cmatrix = '3ff8000000001ffffc00000007fffffc000000fffffff000001fffffffe0\
0001ffffffff80001ffffffffe0001fff000fff8001ffc0001ffc001ffc0\
0003ff001ff800000ffc00ff8000003fe00ff8000000ff807f80000003fc\
07fc0000001fe03fc00000007f83fc00000003fc1fe00000001fe1fe0000\
00007f8ff000000003fc7f800000000007f800000000003fc00000000001\
fe00000000000ff000000000007f800000000003f800000000003fc00000\
000001fe00000000000ff000000000007f800000000003fc00000000001f\
e00000000000ff000000000007f800000000003fc00000000001fe000000\
00000ff000000000007f800000000001fe00000000000ff000000000ff7f\
8000000007fbfc000000003fdfe000000003fc7f800000001fe3fc000000\
00ff1ff000000007f87f800000007fc3fe00000003fc0ff00000003fe07f\
c0000001ff01ff0000001ff00ffc000000ff803ff000000ff801ffc00000\
ffc007ff00000ffc001ffe0001ffc0007ffe007ffc0001ffffffffe00007\
fffffffc00001fffffffc000003ffffffc0000007fffff800000007fffe0\
000000003ff00000'
    self.Dmatrixwid = 49
    self.Dmatrixhei = 62
    self.Dmatrixori = 0
    self.Dmatrix = '3ffffffe00001ffffffff0000ffffffffe0007ffffffffc003fffffffff0\
01fffffffffe00ffffffffff807f800007ffe03fc000007ff01fe000000f\
fc0ff0000003ff07f8000000ff83fc0000003fe1fe0000000ff0ff000000\
07fc7f80000001fe3fc0000000ff9fe00000003fcff00000001fe7f80000\
0007fbfc00000003fdfe00000001feff00000000ff7f800000007fbfc000\
00001fffe00000000ffff000000007fff800000003fffc00000001fffe00\
000000ffff000000007fff800000003fffc00000001fffe00000000ffff0\
00000007fff800000003fffc00000001fffe00000000ffff00000000ff7f\
800000007fbfc00000003fdfe00000001feff00000000ff7f80000000ff3\
fc00000007f9fe00000007fcff00000003fc7f80000003fe3fc0000001fe\
1fe0000001ff0ff0000001ff07f8000001ff83fc000001ff81fe000003ff\
80ff00000fffc07fffffffffc03fffffffff801fffffffff800fffffffff\
8007ffffffff0003fffffffe0001fffffff00000'
    self.Ematrixwid = 44
    self.Ematrixhei = 62
    self.Ematrixori = 0
    self.Ematrix = 'ffffffffffeffffffffffeffffffffffeffffffffffeffffffffffefffff\
fffffeffffffffffeff000000000ff000000000ff000000000ff00000000\
0ff000000000ff000000000ff000000000ff000000000ff000000000ff00\
0000000ff000000000ff000000000ff000000000ff000000000ff0000000\
00ff000000000ff000000000ff000000000ff000000000ff000000000fff\
fffffffcffffffffffcffffffffffcffffffffffcffffffffffcffffffff\
ffcffffffffffcff000000000ff000000000ff000000000ff000000000ff\
000000000ff000000000ff000000000ff000000000ff000000000ff00000\
0000ff000000000ff000000000ff000000000ff000000000ff000000000f\
f000000000ff000000000ff000000000ff000000000ff000000000ff0000\
00000fffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffff'
    self.Fmatrixwid = 42
    self.Fmatrixhei = 62
    self.Fmatrixori = 0
    self.Fmatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
fffffffffffffffc00000000ff000000003fc00000000ff000000003fc00\
000000ff000000003fc00000000ff000000003fc00000000ff000000003f\
c00000000ff000000003fc00000000ff000000003fc00000000ff0000000\
03fc00000000ff000000003fc00000000ff000000003fffffffff0ffffff\
fffc3fffffffff0fffffffffc3fffffffff0fffffffffc3fffffffff0ff0\
00000003fc00000000ff000000003fc00000000ff000000003fc00000000\
ff000000003fc00000000ff000000003fc00000000ff000000003fc00000\
000ff000000003fc00000000ff000000003fc00000000ff000000003fc00\
000000ff000000003fc00000000ff000000003fc00000000ff000000003f\
c00000000ff000000003fc00000000ff000000003fc00000000'
    self.Gmatrixwid = 56
    self.Gmatrixhei = 65
    self.Gmatrixori = -1
    self.Gmatrix = 'ffe0000000001fffff000000007fffffc0000001fffffff0000007ffffff\
fc00000ffffffffe00003fffffffff00007fff000fff8000fff80003ffc0\
00ffe00000ffe001ff8000003ff003ff0000001ff007fe0000000ff807fc\
0000000ff80ff800000007fc0ff800000003fc1ff000000003fc1fe00000\
0003fc1fe000000001fe3fc000000001fe3fc000000000003fc000000000\
007f8000000000007f8000000000007f8000000000007f8000000000007f\
000000000000ff000000000000ff000000000000ff000000000000ff0000\
03ffffffff000003ffffffff000003ffffffff000003ffffffff000003ff\
ffffff000003ffffffff000003ffffffff00000000007f7f80000000007f\
7f80000000007f7f80000000007f7f80000000007f7fc0000000007f3fc0\
000000007f3fc000000000ff3fe000000000ff1fe000000000ff1ff00000\
0001ff1ff000000001ff0ff800000003ff0ffc00000007ff07fc00000007\
ff03fe0000000fff03ff0000001fff01ffc000007fff00ffe00000ffff00\
7ffc0003ff7f003fff001ffe3f001ffffffffc3f000ffffffff83f0007ff\
ffffe03f0001ffffff801f00007fffff001f00000ffff80000000000ff00\
0000'
    self.Hmatrixwid = 48
    self.Hmatrixhei = 62
    self.Hmatrixori = 0
    self.Hmatrix = 'ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffffffffffffffffffffffffffffffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ff'
    self.Imatrixwid = 8
    self.Imatrixhei = 62
    self.Imatrixori = 0
    self.Imatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffff'
    self.Jmatrixwid = 35
    self.Jmatrixhei = 64
    self.Jmatrixori = 0
    self.Jmatrix = '1fe0000003fc0000007f8000000ff0000001fe0000003fc0000007f80000\
00ff0000001fe0000003fc0000007f8000000ff0000001fe0000003fc000\
0007f8000000ff0000001fe0000003fc0000007f8000000ff0000001fe00\
00003fc0000007f8000000ff0000001fe0000003fc0000007f8000000ff0\
000001fe0000003fc0000007f8000000ff0000001fe0000003fc0000007f\
8000000ff0000001fe0000003fc0000007f8000000ff0000001fe0000003\
fffc00007fff80000ffff00001fffe00003fffc00007fff80000ffff0000\
1fffe00003fffc0000ffffc0001fe7f80003fcff8000ff9ff8003fe1ff80\
0ffc3ffc07ff03ffffffe03ffffff803fffffe003fffff0001ffffc0000f\
ffe000003fc000'
    self.Kmatrixwid = 49
    self.Kmatrixhei = 62
    self.Kmatrixori = 0
    self.Kmatrix = '3fc0000000ffffe0000000ffeff0000000ffe7f8000000ffe3fc000000ff\
e1fe000000ffe0ff000000ffe07f800000ffe03fc00000ffe01fe00000ff\
e00ff000007fe007f800007fe003fc00007fe001fe00007fe000ff00007f\
e0007f80007fe0003fc0007fe0001fe0007fe0000ff0007fe00007f8007f\
e00003fc007fe00001fe007fe00000ff007fe000007f807fe000003fc07f\
e000001fe07fe000000ff07ff8000007f87ffc000003fc7fff000001fe7f\
ffc00000ff7fffe000007fffcff800003fffc3fe00001fffc1ff00000fff\
c07fc00007ffc01ff00003ffc00ffc0001ffc003fe0000ffc000ff80007f\
c0007fe0003fc0001ff0001fe00007fc000ff00001ff0007f80000ff8003\
fc00003fe001fe00000ff800ff000007fe007f800001ff003fc000007fc0\
1fe000003ff00ff000000ff807f8000003fe03fc000001ff81fe0000007f\
c0ff0000001ff07f8000000ffc3fc0000003fe1fe0000000ff8ff0000000\
3fe7f80000001ffbfc00000007fdfe00000001ff'
    self.Lmatrixwid = 39
    self.Lmatrixhei = 62
    self.Lmatrixori = 0
    self.Lmatrix = '3fc00000007f80000000ff00000001fe00000003fc00000007f80000000f\
f00000001fe00000003fc00000007f80000000ff00000001fe00000003fc\
00000007f80000000ff00000001fe00000003fc00000007f80000000ff00\
000001fe00000003fc00000007f80000000ff00000001fe00000003fc000\
00007f80000000ff00000001fe00000003fc00000007f80000000ff00000\
001fe00000003fc00000007f80000000ff00000001fe00000003fc000000\
07f80000000ff00000001fe00000003fc00000007f80000000ff00000001\
fe00000003fc00000007f80000000ff00000001fe00000003fc00000007f\
80000000ff00000001fe00000003fc00000007f80000000ff00000001fff\
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
fffff'
    self.Mmatrixwid = 57
    self.Mmatrixhei = 62
    self.Mmatrixori = 0
    self.Mmatrix = '3ff800000000fffffc000000007ffffe000000003fffff800000003fffff\
c00000001fffffe00000000ffffff80000000ffffffc00000007fffffe00\
000003ffffff80000003ffffffc0000001ffffffe0000000fffffbf80000\
00fefffdfc0000007f7ffefe0000003fbfff3f8000003f9fff9fc000001f\
cfffcfe000000fe7ffe3f800000fe3fff1fc000007f1fff8fe000003f8ff\
fc3f800003f87ffe1fc00001fc3fff0fe00000fe1fff83f80000fe0fffc1\
fc00007f07ffe0fe00003f83fff03f80003f81fff81fc0001fc0fffc0fe0\
000fe07ffe03f8000fe03fff01fc0007f01fff807e0003f80fffc03f8003\
f807ffe01fc001fc03fff007e000fe01fff803f800fe00fffc01fc007f00\
7ffe007e003f803fff003f803f801fff801fc01fc00fffc007e00fe007ff\
e003f80fe003fff001fc07f001fff8007e03f800fffc003f83f8007ffe00\
1fc1fc003fff0007e0fe001fff8003f8fe000fffc001fc7f0007ffe0007e\
3f8003fff0003fbf8001fff8001fdfc000fffc0007ffe0007ffe0003ffe0\
003fff0001fff0001fff80007ff8000fffc0003ff80007ffe0001ffc0003\
fff00007fe0001fff80003fe0000fffc0001ff00007f'
    self.Nmatrixwid = 48
    self.Nmatrixhei = 62
    self.Nmatrixori = 0
    self.Nmatrix = 'ff000000007fff800000007fffc00000007fffc00000007fffe00000007f\
fff00000007ffff00000007ffff80000007ffffc0000007ffffc0000007f\
fffe0000007fffff0000007fffff0000007ffeff8000007ffe7f8000007f\
fe7fc000007ffe3fe000007ffe1fe000007ffe1ff000007ffe0ff800007f\
fe07f800007ffe07fc00007ffe03fe00007ffe01fe00007ffe01ff00007f\
fe00ff80007ffe007f80007ffe007fc0007ffe003fe0007ffe003fe0007f\
fe001ff0007ffe000ff8007ffe000ff8007ffe0007fc007ffe0003fe007f\
fe0003fe007ffe0001ff007ffe0000ff007ffe0000ff807ffe00007fc07f\
fe00003fc07ffe00003fe07ffe00001ff07ffe00000ff07ffe00000ff87f\
fe000007fc7ffe000003fc7ffe000003fe7ffe000001ff7ffe000001ff7f\
fe000000fffffe0000007ffffe0000007ffffe0000003ffffe0000001fff\
fe0000001ffffe0000000ffffe00000007fffe00000007fffe00000003ff\
fe00000001fffe00000001ff'
    self.Omatrixwid = 60
    self.Omatrixhei = 65
    self.Omatrixori = -1
    self.Omatrix = 'fff00000000000fffff0000000007fffffe00000000fffffff80000003ff\
fffffc000000fffffffff000001fffffffff800003fff000fffc00007ff8\
0001ffe0000ffe000007ff0001ffc000003ff8003ff0000000ffc003fe00\
000007fc007fc00000003fe00ff800000001ff00ff800000001ff01ff000\
000000ff81fe0000000007f83fe0000000007f83fe0000000007fc3fc000\
0000003fc3fc0000000003fc7f80000000001fe7f80000000001fe7f8000\
0000001fe7f80000000001fe7f00000000000feff00000000000ffff0000\
0000000ffff00000000000ffff00000000000ffff00000000000ffff0000\
0000000ffff00000000000ffff00000000000ffff00000000000ffff0000\
0000000ffff00000000000ff7f00000000000fe7f80000000001fe7f8000\
0000001fe7f80000000001fe7f80000000001fe3fc0000000003fc3fc000\
0000003fc3fe0000000007fc1fe0000000007f81ff000000000ff80ff000\
000000ff00ff800000001ff00ffc00000003ff007fc00000003fe003ff00\
00000ffc003ff8000001ff8001ffc000003ff8000fff00000fff00007ffc\
0003ffe00003fff801fffc00001fffffffff800000fffffffff0000003ff\
fffffc0000000fffffff000000003fffffc0000000007fffe00000000000\
3fe000000'
    self.Pmatrixwid = 44
    self.Pmatrixhei = 62
    self.Pmatrixori = 0
    self.Pmatrix = 'fffffffe000ffffffffc00fffffffff00fffffffffc0fffffffffe0fffff\
fffff0ffffffffff8ff000007ff8ff000001ffcff0000007fcff0000003f\
eff0000003feff0000001feff0000001feff0000000ffff0000000ffff00\
00000ffff0000000ffff0000000ffff0000000ffff0000000ffff0000000\
ffff0000001ffff0000001feff0000003feff0000007feff000000ffcff0\
00001ffcff000007ff8ffffffffff8ffffffffff0fffffffffe0ffffffff\
fc0fffffffff00ffffffffc00fffffffe000ff000000000ff000000000ff\
000000000ff000000000ff000000000ff000000000ff000000000ff00000\
0000ff000000000ff000000000ff000000000ff000000000ff000000000f\
f000000000ff000000000ff000000000ff000000000ff000000000ff0000\
00000ff000000000ff000000000ff000000000ff000000000ff000000000\
ff000000000ff000000000'
    self.Qmatrixwid = 60
    self.Qmatrixhei = 68
    self.Qmatrixori = -1
    self.Qmatrix = 'fff00000000000fffff0000000007fffffe00000000fffffff00000003ff\
fffffc000000fffffffff000001fffffffff800003fff000fffc00007ff8\
0001ffe0000ffe000007ff0001ffc000003ff8003ff0000000ffc003fe00\
000007fc007fc00000003fe00ff800000001ff00ff800000001ff01ff000\
000000ff81fe0000000007f83fe0000000007fc3fe0000000007fc3fc000\
0000003fc3fc0000000003fc7f80000000001fe7f80000000001fe7f8000\
0000001fe7f80000000001fe7f00000000000feff00000000000ffff0000\
0000000ffff00000000000ffff00000000000ffff00000000000ffff0000\
0000000ffff00000000000ffff00000000000ffff00000000000ffff0000\
0000000ffff00000000000ff7f00000000000fe7f80000000001fe7f8000\
0000001fe7f80000000001fe7f80000000001fe3fc0000000003fc3fc000\
0000003fc3fe0000000007fc1fe0000006007f81ff000000f00ff80ff000\
001f80ff00ff800001fc1ff00ffc00003ff3ff007fc00001ffbfe003fe00\
000ffffc003ff800007fffc001ffc00001fff8000fff00000fff00007ff8\
0003ffe00003fff801ffff00001ffffffffff80000ffffffffffe00003ff\
ffffffff00000fffffff9ff800003fffffe07fc000007ffff003fe000000\
3fe0001fc0000000000000f8000000000000070000000000000010'
    self.Rmatrixwid = 50
    self.Rmatrixhei = 62
    self.Rmatrixori = 0
    self.Rmatrix = 'ffffffffc0003fffffffff000ffffffffff003fffffffffe00ffffffffff\
e03ffffffffff80fffffffffff03fc000001ffe0ff0000001ff83fc00000\
03ff0ff00000007fc3fc0000000ff0ff00000003fe3fc00000007f8ff000\
00001fe3fc00000007f8ff00000001fe3fc00000007f8ff00000001fe3fc\
00000007f8ff00000001fc3fc00000007f0ff00000003fc3fc0000000ff0\
ff00000007f83fc0000003fc0ff0000001ff03fc000003ff80ffffffffff\
c03fffffffffc00fffffffffe003fffffffff800ffffffffff803fffffff\
fff00ffffffffffe03fc000001ffc0ff0000001ff03fc0000003fe0ff000\
00007f83fc0000000fe0ff00000003fc3fc00000007f0ff00000001fc3fc\
00000007f0ff00000001fc3fc00000007f0ff00000001fc3fc00000007f0\
ff00000001fc3fc00000007f0ff00000001fc3fc00000007f0ff00000001\
fc3fc00000007f0ff00000001fc3fc00000007f8ff00000001fe3fc00000\
007f8ff00000000ff3fc00000003feff00000000ffffc00000003ff'
    self.Smatrixwid = 49
    self.Smatrixhei = 65
    self.Smatrixori = -1
    self.Smatrix = '7ff800000003ffffc0000007fffff800000fffffff00000fffffffc0001f\
fffffff8001ffffffffe001fff000fff000ffc0000ffc00ffc00003ff007\
fc000007f807fc000001fe03fc000000ff01fe0000003f81fe0000001fc0\
ff0000000ff07f80000003f83fc0000001fc1fe0000000fe0ff000000000\
07fc0000000003fe0000000000ff80000000007fe0000000003ffc000000\
000fff8000000007fff800000001ffffc00000007ffffe0000001ffffff0\
000003ffffff8000007ffffff800000fffffff0000007fffffc0000003ff\
fff80000003ffffe00000001ffff800000000fffc000000001fff0000000\
003ff80000000007fe0000000001ff00000000007fbf800000003fffc000\
00000fffe000000007fff000000003fff800000001fefe00000000ff7f00\
0000007fbfc00000007f9fe00000003fc7f80000003fe3fe0000001fe0ff\
8000001ff07fe000003ff01ffc00007ff007ffe001fff801fffffffff800\
7ffffffff8001ffffffff00003fffffff000007fffffe000000fffff8000\
00003ff80000'
    self.Tmatrixwid = 48
    self.Tmatrixhei = 62
    self.Tmatrixori = 0
    self.Tmatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffffff00000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff0000000000ff0000000000ff0000000000ff00000\
00000ff0000000000ff00000'
    self.Umatrixwid = 48
    self.Umatrixhei = 64
    self.Umatrixori = 0
    self.Umatrix = 'ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ffff00000000ffff00000000ff\
ff00000000ffff00000000ffff00000000ff7f80000001fe7f80000001fe\
7fc0000003fe7fc0000003fc3fe0000007fc3ff000000ff81ff800003ff8\
0ffe0000fff007ffc007ffe007ffffffffc003ffffffff8000ffffffff00\
007ffffffc00000ffffff0000003ffffc00000001ff80000'
    self.Vmatrixwid = 52
    self.Vmatrixhei = 62
    self.Vmatrixori = 0
    self.Vmatrix = 'ff800000000ff7f800000000fe7fc00000001fe7fc00000001fe3fc00000\
001fc3fe00000003fc1fe00000003fc1fe00000003f81ff00000007f80ff\
00000007f80ff00000007f00ff8000000ff007f8000000ff007f8000000f\
e007fc000001fe003fc000001fe003fc000001fc003fe000003fc001fe00\
0003fc001fe000003f8000ff000007f8000ff000007f8000ff000007f000\
07f80000ff00007f80000ff00007fc0000fe00003fc0001fe00003fc0001\
fe00003fe0001fc00001fe0003fc00001fe0003fc00000ff0003f800000f\
f0007f800000ff0007f8000007f8007f0000007f800ff0000007f800ff00\
00003fc00fe0000003fc01fe0000003fc01fe0000001fe01fc0000001fe0\
3fc0000001fe03fc0000000ff03f80000000ff07f800000007f07f800000\
007f87f000000007f87f000000003fcff000000003fcfe000000003fcfe0\
00000001fffe000000001fffc000000001fffc000000000fff8000000000\
fff80000000007ff80000000007ff00000000007ff00000000003ff00000\
000003fe00000000003fe00000'
    self.Wmatrixwid = 77
    self.Wmatrixhei = 62
    self.Wmatrixori = 0
    self.Wmatrix = '3fe000000ff8000003ffff0000007fc000001ff7f8000003fe000000ff3f\
e000003ff800000ff9ff000001ffc000007fcff800000ffe000003fe3fc0\
0000fff000001fe1ff000007ffc00001ff0ff800003ffe00000ff87fc000\
01fff000007fc1fe00001fffc00003fc0ff80000fffe00003fe07fc00007\
f7f00001ff01fe00003fbf80000ff80ff00003f9fe00007f807f80001fc7\
f00003fc03fe0000fe3f80003fe00ff0000ff1fe0001fe007f80007f0ff0\
000ff003fc0003f83f80007f801ff0001fc1fc0007fc007f8001fe0ff000\
3fc003fc000fe03f8001fe001fe0007f01fc000ff000ff8003f80ff0007f\
8003fc003f807f8007f8001fe001fc01fc003fc000ff000fe00fe001fe00\
07f800ff007f800ff0001fe007f001fc00ff0000ff003f800fe007f80007\
f801fc007f003fc0003fc01fe003fc01fe0000ff00fe000fe00fe00007f8\
07f0007f00ff00003fc03f8003fc07f80001fe03f8001fe03fc00007f81f\
c0007f01fc00003fc0fe0003f81fe00001fe0ff0001fe0ff00000ff07f00\
007f07f800003f83f80003f83f800001fe1fc0001fe1fc00000ff1fe0000\
ff1fe000007f8fe00003f8ff000001fc7f00001fc7f000000ff3f80000ff\
3f8000007fbf800003fbfc000001fdfc00001fdfe000000fefe00000fffe\
0000007fff000007fff0000003fff000001fff8000000fff800000fffc00\
00007ffc000007ffc0000003ffe000001ffe0000001ffe000000fff00000\
007ff0000007ff80000003ff8000003ff80000001ffc000000ffc0000000\
ffc0000007fe00000003fe0000003ff00000001ff0000001ff0000'
    self.Xmatrixwid = 53
    self.Xmatrixhei = 62
    self.Xmatrixori = 0
    self.Xmatrix = '1ff80000000ffc7fe00000007fc1ff00000007fc07fc0000007fe03ff000\
0003fe00ff8000003fe003fe000003ff001ff800001ff0007fc00001ff00\
01ff00000ff8000ffc0000ff80003fe0000ff80000ff80007fc00007fe00\
07fc00001ff0007fc000007fc003fc000003ff003fe000000ff803fe0000\
003fe01fe0000001ff81ff00000007fc1ff00000001ff0ff000000007fcf\
f800000003feff800000000ffff8000000003fff8000000001fffc000000\
0007ffc0000000001ffc0000000000ffe00000000003fe00000000003ff8\
0000000003ffe0000000001fff8000000001fffc000000001ffff0000000\
01ff7fc00000000ffbfe00000000ff8ff80000000ff83fe00000007fc1ff\
00000007fc07fc0000007fc01ff0000003fe00ff8000003fe003fe000003\
fe000ff800001ff0007fe00001ff0001ff00001ff00007fc0001ff80003f\
f0000ff80000ff8000ff800003fe000ffc00001ff8007fc000007fc007fc\
000001ff007fe000000ffc03fe0000003fe03fe0000001ff83ff00000007\
fe1ff00000001ff1ff00000000ffdff800000003ff'
    self.Ymatrixwid = 55
    self.Ymatrixhei = 62
    self.Ymatrixori = 0
    self.Ymatrix = '3ff000000000ffbff000000003fe3fe00000000ffc7fe00000001ff07fe0\
0000007fc07fc0000000ff80ffc0000003fe00ff8000000ffc00ff800000\
1ff001ff8000007fc001ff000000ff8003ff000003fe0003fe000007fc00\
03fe00001ff00007fe00007fc00007fc0000ff800007fc0003fe00000ff8\
0007f800000ff8001ff000000ff8007fc000001ff000ff8000001ff003fe\
0000003fe007f80000003fe01ff00000003fe07fc00000007fc0ff000000\
007fc3fe000000007fc7f800000000ff9ff000000000ffbfc000000000ff\
ff0000000001fffe0000000001fff80000000003fff00000000003ffc000\
00000003ff000000000007fe000000000007f800000000000ff000000000\
001fe000000000003fc000000000007f800000000000ff000000000001fe\
000000000003fc000000000007f800000000000ff000000000001fe00000\
0000003fc000000000007f800000000000ff000000000001fe0000000000\
03fc000000000007f800000000000ff000000000001fe000000000003fc0\
00000000007f800000000000ff000000000001fe000000000003fc000000\
000007f800000'
    self.Zmatrixwid = 48
    self.Zmatrixhei = 62
    self.Zmatrixori = 0
    self.Zmatrix = '1ffffffffffe1ffffffffffe1ffffffffffe1ffffffffffe1ffffffffffe\
1ffffffffffe1ffffffffffe0000000007fe000000000ffc000000001ff8\
000000001ff8000000003ff0000000007fe000000000ffc000000000ffc0\
00000001ff8000000003ff0000000007fe0000000007fc000000000ffc00\
0000001ff8000000003ff0000000007fe0000000007fe000000000ffc000\
000001ff8000000003ff0000000003ff0000000007fe000000000ffc0000\
00001ff8000000001ff8000000003ff0000000007fe000000000ffc00000\
0000ff8000000001ff8000000003ff0000000007fe000000000ffc000000\
000ffc000000001ff8000000003ff0000000007fe0000000007fe0000000\
00ffc000000001ff8000000003ff0000000003ff0000000007fe00000000\
0ffc000000001ff8000000001ff0000000003ff0000000007fe000000000\
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffffff'
    self.onematrixwid = 21
    self.onematrixhei = 60
    self.onematrixori = 2
    self.onematrix = 'f80007c0007e0003f0001f8001fc000fe000ff000ff800ffc03ffe1fffff\
fffffffffffffffffffffffff8003fc001fe000ff0007f8003fc001fe000\
ff0007f8003fc001fc000fe0007f0003f8001fc000fe0007f0003f8001fc\
000fe0007f0003f8001fc000fe0007f0003f8001fc000fe0007f0003f800\
1fc000fe0007f0003f8001fc000fe0007f0003f8001fc000fe0007f0003f\
8001fc000fe'
    self.twomatrixwid = 40
    self.twomatrixhei = 60
    self.twomatrixori = 2
    self.twomatrix = '1ffc000000ffff800003ffffe0000ffffff8001ffffffc003ffffffe007f\
ffffff007ff007ff80ffc000ffc1ff00007fc1fe00003fe1fe00001fe3fc\
00000fe3f800000fe3f800000ff3f8000007f7f8000007f7f0000007f7f0\
000007f7f0000007f7f0000007f00000000ff00000000fe00000001fe000\
00001fe00000003fc00000007fc0000000ff80000003ff00000007ff0000\
001ffe0000007ffc000000fff8000003ffe000000fffc000003fff000000\
7ffe000001fff8000003ffe000000fff8000001ffe0000003ff80000007f\
e00000007fc0000000ff80000001fe00000001fc00000003fc00000003f8\
00000007f000000007f000000007f000000007f00000000fffffffffffff\
fffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    self.threematrixwid = 40
    self.threematrixhei = 62
    self.threematrixori = 2
    self.threematrix = '1ff8000001ffff800007ffffe0000ffffff0003ffffff8007ffffffc007f\
fffffe00ffe007ff01ff8001ff01fe0000ff81fc00007f83fc00003f83f8\
00003fc3f800001fc3f800001fc7f000001fc7f000001fc7f000001fc7f0\
00001fc00000001fc00000003f800000003f800000007f80000000ff0000\
0001ff0000001ffe00000ffffc00000ffff000000fffe000000ffff80000\
0ffffc00000fffff00000003ff80000000ffc00000003fc00000001fe000\
00001fe00000000fe00000000ff000000007f000000007f000000007ffe0\
000007ffe0000007ffe0000007ffe0000007f7f0000007f7f000000fe7f0\
00000fe7f800001fe3f800001fe3fc00003fc3fe00007fc1ff8001ff81ff\
e007ff80ffffffff007ffffffe003ffffffc001ffffff00007ffffe00001\
ffff0000001ff0000'
    self.fourmatrixwid = 41
    self.fourmatrixhei = 60
    self.fourmatrixori = 2
    self.fourmatrix = '1f000000001f800000001fc00000001fe00000000ff00000000ff8000000\
0ffc00000007fe00000007ff00000007ff80000007ffc0000003ffe00000\
03fff0000003fff8000003fdfc000001fcfe000001fc7f000001fe3f8000\
00fe1fc00000fe0fe00000ff07f00000ff03f800007f01fc00007f00fe00\
007f807f00003f803f80003f801fc0003fc00fe0003fc007f0001fc003f8\
001fc001fc001fe000fe000fe0007f000fe0003f800ff0001fc00ff0000f\
e007f00007f007f00003f803f80001fc01ffffffffffffffffffffffffff\
fffffffffffffffffffffffffffffffffffffffffffffc000001fc000000\
00fe000000007f000000003f800000001fc00000000fe000000007f00000\
0003f800000001fc00000000fe000000007f000000003f800000001fc000\
00000fe00'
    self.fivematrixwid = 40
    self.fivematrixhei = 62
    self.fivematrixori = 2
    self.fivematrix = '3fffffff803fffffff803fffffff803fffffff807fffffff807fffffff80\
7fffffff807f000000007f000000007f000000007e00000000fe00000000\
fe00000000fe00000000fe00000000fe00000000fe00000000fc00000000\
fc00000001fc00000001fc07f80001fc3fff0001fcffffe001fffffff001\
fffffff801fffffffe01fffffffe03ffe00fff03ff8003ff83fe0000ff83\
fc00007fc3f800003fc00000001fe00000001fe00000000fe00000000fe0\
0000000ff000000007f000000007f000000007f000000007f000000007f0\
00000007f000000007f000000007ffe0000007efe000000fe7f000000fe7\
f000001fe7f800001fc3f800003fc3fc00007f83fe0000ff81ff8001ff00\
ffe00ffe00fffffffe007ffffffc003ffffff8000fffffe00007ffffc000\
00fffe0000001ff0000'
    self.sixmatrixwid = 39
    self.sixmatrixhei = 62
    self.sixmatrixori = 2
    self.sixmatrix = '1ff0000001fffc00000ffffe00007ffffe0001fffffe0007fffffe001fff\
fffe007ff00ffc01ff8007fc03fc0007f80ff00007f81fe00007f07f8000\
0fe0fe00000fe1fc00001fc7f00000000fe00000001fc00000007f800000\
00fe00000001fc00000003f800000007f003f8000fe07ffe003fc3ffff00\
7f8fffff80ff3fffff81feffffff83ffffffff87fff807ff8fffc001ff1f\
fe0001ff3ff80001fe7ff00001feffc00003fdff000003fbfe000007f7fc\
00000ffff000000fffe000001fdfc000003fbf8000007f7f000000fefe00\
0001fdfc000003fbf8000007f3f800001fc7f000003f8ff000007f0fe000\
01fe1fe00007f81fe0000ff03fe0007fc07fe001ff807ff00ffe007fffff\
f8007fffffe0007fffff80007ffffe00007ffff000001fff80000003f800\
0'
    self.sevenmatrixwid = 40
    self.sevenmatrixhei = 60
    self.sevenmatrixori = 2
    self.sevenmatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffff00000000fe00000000fe00000001fc00000003f800000003f8\
00000007f00000000fe00000000fc00000001fc00000003f800000003f80\
0000007f00000000fe00000000fe00000001fc00000001fc00000003f800\
000003f000000007f00000000fe00000000fe00000001fc00000001fc000\
00003f800000003f800000007f000000007f00000000ff00000000fe0000\
0001fe00000001fc00000001fc00000003f800000003f800000007f80000\
0007f000000007f00000000ff00000000fe00000000fe00000001fe00000\
001fe00000001fc00000003fc00000003fc00000003f800000003f800000\
007f800000007f800000007f800000007f00000000ff00000000ff000000'
    self.eightmatrixwid = 40
    self.eightmatrixhei = 62
    self.eightmatrixori = 2
    self.eightmatrix = 'ff80000007fff000003ffffe00007fffff0000ffffff8001ffffffc003ff\
ffffe007ff007ff007fc001ff00ff8000ff80ff00007f80fe00003f81fe0\
0003fc1fc00001fc1fc00001fc1fc00001fc1fc00001fc1fc00001fc1fc0\
0001fc1fe00003fc0fe00003f80ff00007f807f8000ff007fe003ff003ff\
80ffe001ffffffc0007fffff00003ffffe00007ffffe0001ffffff8003ff\
ffffc007ff00fff00ff8001ff01ff0000ff83fc00003fc3f800001fc7f80\
0001fe7f000000fe7f000000fefe0000007ffe0000007ffe0000007ffe00\
00007ffe0000007ffe0000007ffe0000007ffe0000007f7f000000fe7f00\
0000fe7f800001fe7f800001fe3fc00003fc3fe0000ffc1ff8001ff80ffe\
00fff007ffffffe007ffffffe001ffffff8000ffffff00003ffffc00000f\
fff0000000ff0000'
    self.ninematrixwid = 39
    self.ninematrixhei = 62
    self.ninematrixori = 2
    self.ninematrix = 'ffc000000ffff000007ffff80001fffff80007fffff8003ffffff8007fff\
fff801ff803ff807fe001ff80ff0000ff03fc0000ff07f00001fe1fe0000\
1fe3f800001fc7f000003f8fe000007f3f8000007f7f000000fefe000001\
fdfc000003fbf8000007f7f000000fefe000001fffc000003fdfc00000ff\
bf800001ff7f800007feff00000ffcff00003ff9ff0000fff1ff0007ffe3\
ff803fffc3ffffffff83fffffeff03fffff9fe03ffffe3fc01ffff07f800\
fffc0fe0003f801fc00000003f800000007f00000000fe00000003fc0000\
0007f00000000fe00000001fc7f000007f8fe00000fe0fe00003fc1fc000\
07f03fc0001fe07fc0007fc07f8001ff00ffc007fc00ffc03ff800ffffff\
e001ffffff8001fffffe0001fffff80000ffffc000007ffe0000001fc000\
0'
    self.tenmatrixwid = 39
    self.tenmatrixhei = 62
    self.tenmatrixori = 2
    self.tenmatrix = '7fc0000007fff000003ffff80000fffff80003fffff8000ffffff8003fff\
fff800ffe03ff801ff001ff007f8001ff00ff0001fe03fc0001fe07f0000\
1fc1fe00003fc3f800003f87f000007f0fe00000fe3f800000fe7f000001\
fcfe000003f9fc000007f3f800000fe7e000000fdfc000001fff8000003f\
ff0000007ffe000000fffc000001fff8000003fff0000007ffe000000fff\
c000001fff8000003fff0000007ffe000000fffc000001fff8000003fff0\
000007ffe000000fefc000001fdfc000007f3f800000fe7f000001fcfe00\
0003f9fc000007f3f800000fe3f800003f87f000007f0ff00000fe0fe000\
03f81fc00007f03fc0001fc03fc0007f807fc001ff007fc007fc007fe03f\
f0007fffffc000ffffff00007ffffc00007ffff000003fff8000000ff800\
0'
    self._matrixwid = 51
    self._matrixhei = 4
    self._matrixori = 73
    self._matrix = 'fffffffffffffffffffffffffffffffffffffffffffffffffff'
    self.minusmatrixwid = 20
    self.minusmatrixhei = 6
    self.minusmatrixori = 36
    self.minusmatrix = 'ffffffffffffffffffffffffffffff'
    self.plusmatrixwid = 42
    self.plusmatrixhei = 42
    self.plusmatrixori = 21
    self.plusmatrix = '3f000000000fc000000003f000000000fc000000003f000000000fc00000\
0003f000000000fc000000003f000000000fc000000003f000000000fc00\
0000003f000000000fc000000003f000000000fc000000003f000000000f\
c0000fffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffff00003f000000000fc000000003f000000000fc000000003f0000\
00000fc000000003f000000000fc000000003f000000000fc000000003f0\
00000000fc000000003f000000000fc000000003f000000000fc00000000\
3f000000000fc0000'
    self.equalmatrixwid = 41
    self.equalmatrixhei = 21
    self.equalmatrixori = 32
    self.equalmatrix = '1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ff8000000000000000000000000000000000000000000000000000000000\
00000000000000000000000000000000003fffffffffffffffffffffffff\
ffffffffffffffffffffffffffffffffffff'
    self.exclmatrixwid = 7
    self.exclmatrixhei = 62
    self.exclmatrixori = 0
    self.exclmatrix = '3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffbe\
7cf9f3e7cf9f3e3870e1c3870000000007fffffffffffffff'
    self.atmatrixwid = 78
    self.atmatrixhei = 75
    self.atmatrixori = -1
    self.atmatrix = '3ffc000000000000001fffff80000000000003ffffffc000000000003fff\
ffffc00000000007ffffffffc0000000003fffffffffc000000003ffffff\
ffff800000003fffc000ffff80000001fff000007fff0000000fff000000\
3ffe000000fff00000003ffc000007ff000000003ff800003ff000000000\
7ff00001ff80000000007fe0000ffc0000000000ffc0007fc00000000001\
ff8001fe000000000003fe000ff0000000000007fc007fc000000000000f\
f801fe000003f800003fe00ff00000fff800007f807f80000ffff03f80ff\
01fc00007ffff1fc03fc0ff00007ffffc7f007f83f80003ff03fbfc01fe1\
fe0001ff003ffe003f87f0000ff0007ff800fe1fc0007f8000ffe003fcfe\
0001fc0003ff0007f3f8000fe00007fc001fcfc0007f80001ff0007f7f00\
01fc00007fc001fdfc000fe00001fe0007f7f0003f800007f8001fdf8001\
fe00001fe0007f7e0007f000007f0001fff8001fc00003fc0007ffe0007f\
00000ff0001fbf8003f800003f8000fefe000fe00000fe0003fbf8003f80\
0007f8000fefe000fe00001fc0007f3f8003f800007f0001fcfe000fe000\
03fc000ff3f8003f80000fe0003f8fe000fe00007f8001fe1fc003fc0001\
fe0007f07f0007f0000ff0003fc1fc001fe0007fc001fe07f8007f8003ff\
000ff00fe000ff001ffe007fc03fc003fe00fff807fe00ff0007fe0feff8\
7ff001fe000fffff3fffff8007f8001ffff8fffffc000ff0003fffc1ffff\
c0003fe0007ffc03fffc00007fc0003f8003ff800001ff80000000000000\
0003ff000000000000000007fe00000000000000000ffc00000000000000\
001ffc00000000000000003ff800000000000000007ff800000000000000\
00fff80000000000000001fffc000003c000000001ffff0001ff80000000\
03fffffffffe0000000003fffffffff80000000003fffffffff000000000\
03ffffffff800000000001fffffff0000000000000fffffc000000000000\
001ffc00000000'
    self.hashmatrixwid = 45
    self.hashmatrixhei = 60
    self.hashmatrixori = 3
    self.hashmatrix = '7e003f000007f003f800003f801fc00001f800fe00000fc007e000007e00\
3f000007f003f800003f801fc00001fc00fe00000fc007e000007e003f00\
0003f001f800003f801fc00001fc00fe00000fc007e000007e003f001fff\
fffffff8ffffffffffc7fffffffffe3ffffffffff1ffffffffff8fffffff\
fffc003f801fc00001fc00fe00000fe007f000007e003f000003f001f800\
001f800fc00001fc00fe00000fe007f000007f003f800003f001f800001f\
800fc00000fc007e00000fe007f000007f003f800003f001fc007fffffff\
ffe3ffffffffff1ffffffffff8ffffffffffc7fffffffffe3ffffffffff0\
00fc007e00000fe003f000007f003f800003f801fc00001f800fe00000fc\
007e000007e003f000007f003f800003f801fc00001f800fe00000fc007e\
000007e003f000007f003f800003f801fc00001f800fe00000fc007e0000\
07e003f0000'
    self.dollarmatrixwid = 41
    self.dollarmatrixhei = 77
    self.dollarmatrixori = -4
    self.dollarmatrix = '7c000000003e000000001f000000000f8000000007c00000000ffc000000\
7fffc00000fffff80001ffffff0003ffffffc003fffffff003ffcf8ffc01\
ff07c1fe01fe03e07f80fe01f01fc0fe00f80ff07f007c03f83f003e01fc\
3f801f007f1fc00f803f8fe007c01fc7f003e00fe3f801f00001fc00f800\
00fe007c00007f803e00001fc01f00000ff00f800007fc07c00001ff83e0\
00007ff1f000003ffff800000ffffe000003fffff00000ffffff00001fff\
ffe00003fffff800003fffff000003ffffc00000fffff000007c7ff80000\
3e0ffe00001f01ff00000f807fc00007c01fe00003e007f00001f001f800\
00f800fffc007c007ffe003e003fff001f001fff800f800fffc007c007ff\
f003e003f3f801f001f9fc00f801fcff007c00fe3f803e00fe1fe01f00ff\
0ff80f80ff03ff07c1ff80ffe3e3ff803fffffff800fffffff8003ffffff\
80007fffff00000ffffe0000007ff000000007c000000003e000000001f0\
00000000f8000000007c000000003e000000001f000000000f8000000007\
c0000'
    self.percentmatrixwid = 71
    self.percentmatrixhei = 61
    self.percentmatrixori = 2
    self.percentmatrix = '1f00000000000000007e0000003fc0000001f8000003fff0000003e00000\
0ffff800000fc000007ffff800001f000001fffff800007e000007fffff8\
0000f800000ff81ff80003f000003fc00ff00007c00000ff000ff0001f80\
0001fc000fe0003e000003f0000fc000fc00000fe0001fc003f000001f80\
001f8007e000003f00003f001f8000007e00007e003e000000fc0000fc00\
fc000001f80001f801f0000003f80007f007e0000003f0000fc00f800000\
07f0003f803f0000000ff000ff00fc0000000ff003fc01f80000000ff81f\
f007e00000001fffffe00fc00000001fffff803f000000001ffffe007c00\
0000000ffff001f80000000007ff8003e00000000001fc000fc000000000\
0000001f00000000000000007e0000000000000001f80007f00000000003\
f0007ffc000000000fc003fffe000000001f800ffffe000000007e003fff\
fe00000000f800fffffe00000003f003fe03fe00000007c007f803fc0000\
001f801fc001fc0000007e003f8003f8000000fc007e0003f0000003f001\
f80003f0000007e003f00007e000001f8007e0000fc000003f000fc0001f\
800000fc001f80003f000001f0003f00007e000007e0003f0001f800000f\
80007f0007f000003f0000fe000fe00000fc0000ff007f800001f80001ff\
01ff000007e00001fffffc00000fc00001fffff000003f000001ffffc000\
007e000001ffff000001f8000000fff8000007f00000003f800'
    self.hatmatrixwid = 32
    self.hatmatrixhei = 32
    self.hatmatrixori = 2
    self.hatmatrix = '7e000000ff000000ff000001ff000001ff800001ff800003ffc00003ffc0\
0007e7c00007e7e00007c7e0000fc3f0000fc3f0001f81f0001f81f8001f\
01f8003f00fc003f00fc007e007c007e007e007c007e00fc003f00fc003f\
01f8001f81f8001f81f0001f83f0000fc3f0000fc7e00007e7e00007efc0\
0003efc00003f'
    self.ampmatrixwid = 50
    self.ampmatrixhei = 62
    self.ampmatrixori = 2
    self.ampmatrix = '3fc0000000007ffe000000007fffc00000003ffffc0000001fffff800000\
0fffffe0000007fc07fc000001fe00ff800000fe001fe000003f8003f800\
001fc0007f000007f0001fc00001fc0007f000007f0001fc00001fc0007f\
000007f0001fc00000fe000fe000003f8003f800000ff001fe000001fe00\
ff0000007f80ffc000000ff07fe0000001fe3ff00000007ffff80000000f\
fff800000001fffc000000007ffc000000001ffe000000001fff00000000\
0fffe00000000ffffc00000007feff80000003ff1ff003f801ff07fe00fe\
00ff80ff803f807fc01ff00fe03fe003fe07f00ff0007fc1fc07f8000ff8\
7f01fc0003ff3fc07f00007fcfe03f80000ffff80fe00001fffc03f80000\
3fff00fe000007ff803f800001ffe00fe000003ff003f8000007fc00ff00\
0001ff801fc00000fff007f800007ffe01ff00003fffc03fe0001ffff00f\
fc001ffbfe01ffe03ffc7fc07ffffffe0ff80fffffff03ff01ffffff807f\
c03fffff800ff803ffffc001ff003fff8000000000ff0000000'
    self.strixmatrixwid = 25
    self.strixmatrixhei = 24
    self.strixmatrixori = 0
    self.strixmatrix = '3e00001f00000f800007c00003e00001f00100f804e07c0efe3e3fffffff\
fffffffffffff0ffff8007fc0003fe0003ff8001ffc001fbf001f8fc01f8\
3f01fc1fc0fc07e01c01c00600c0'
    self.opencparmatrixwid = 18
    self.opencparmatrixhei = 80
    self.opencparmatrixori = 0
    self.opencparmatrix = '3c001f000f8007e001f000f8003e001f000fc003f001f8007e001f000fc0\
03e001f8007e003f800fc003f001fc007e001f8007e003f800fc003f000f\
c007f001fc007f001f8007e001f800fe003f800fe003f800fe003f800fe0\
03f800fe003f800fe003f8007e001f8007e001fc007f001fc003f000fc00\
3f000fe003f8007e001f8007f000fc003f000fc001f8007e000f8003f000\
fc001f8007e000f8003f0007c000f8003e0007c001f0003e0007c001f'
    self.closecparmatrixwid = 18
    self.closecparmatrixhei = 80
    self.closecparmatrixori = 0
    self.closecparmatrix = 'f0003e0007c001f8003e0007c001f0007e000fc003f0007e001f8003e000\
fc003f0007e001f8007f000fc003f000fe001f8007e001f8007f000fc003\
f000fc003f800fe003f8007e001f8007e001fc007f001fc007f001fc007f\
001fc007f001fc007f001fc007f001f8007e001f800fe003f800fe003f00\
0fc003f001fc007f001f8007e003f800fc003f000fc007e001f8007c003f\
000fc007e001f8007c003f000f8007c001f000f8003e001f000f8003e000'
    self.opensparmatrixwid = 16
    self.opensparmatrixhei = 80
    self.opensparmatrixori = 0
    self.opensparmatrix = 'fffffffffffffffffffffffffe00fe00fe00fe00fe00fe00fe00fe00fe00\
fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00\
fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00\
fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00\
fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00ffff\
ffffffffffffffffffff'
    self.closesparmatrixwid = 16
    self.closesparmatrixhei = 80
    self.closesparmatrixori = 0
    self.closesparmatrix = 'ffffffffffffffffffffffff007f007f007f007f007f007f007f007f007f\
007f007f007f007f007f007f007f007f007f007f007f007f007f007f007f\
007f007f007f007f007f007f007f007f007f007f007f007f007f007f007f\
007f007f007f007f007f007f007f007f007f007f007f007f007f007f007f\
007f007f007f007f007f007f007f007f007f007f007f007f007f007fffff\
ffffffffffffffffffff'
    self.backslashmatrixwid = 25
    self.backslashmatrixhei = 63
    self.backslashmatrixori = 0
    self.backslashmatrix = '7c00001e00000f800007c00001e00000f800007c00003e00000f000007c0\
0003e00000f000007c00003e00000f000007c00003e00000f000007c0000\
3e00000f000007c00003e00000f000007c00003e00000f000007c00003e0\
0000f000007c00003e00001f000007800003e00001f000007800003e0000\
1f000007800003e00001f000007800003e00001f000007800003e00001f0\
00007800003e00001f000007800003e00001f000007800003e00001f0000\
0f800003c00001f00000f800003c00001f'
    self.semicolmatrixwid = 9
    self.semicolmatrixhei = 57
    self.semicolmatrixori = 17
    self.semicolmatrix = '1ffffffffffffffffffff000000000000000000000000000000000000000\
0000000000000000000001ffffffffffffffffffff0783c1e0f078383c1e\
1e7e3e1c0'
    self.postmatrixwid = 8
    self.postmatrixhei = 21
    self.postmatrixori = 2
    self.postmatrix = 'ffffffffffffffffffffffff7e7e7e7e7e3c3c3c3c'
    self.commamatrixwid = 9
    self.commamatrixhei = 21
    self.commamatrixori = 53
    self.commamatrix = '1ffffffffffffffffffff0783c1e0f078383c1e1e7e3e1c0'
    self.fullstopmatrixwid = 9
    self.fullstopmatrixhei = 9
    self.fullstopmatrixori = 53
    self.fullstopmatrix = '1ffffffffffffffffffff'
    self.forslashmatrixwid = 25
    self.forslashmatrixhei = 63
    self.forslashmatrixori = 0
    self.forslashmatrix = '7c00003c00003e00001f00000f00000f800007c00003e00001e00001f000\
00f800007800007c00003e00001e00001f00000f800007800007c00003e0\
0001e00001f00000f800007800007c00003e00001e00001f00000f800007\
800007c00003e00001f00000f00000f800007c00003c00003e00001f0000\
0f00000f800007c00003c00003e00001f00000f00000f800007c00003c00\
003e00001f00000f00000f800007c00003c00003e00001f00000f8000078\
00007c00003e00001e00001f00000'
    self.lesthanmatrixwid = 41
    self.lesthanmatrixhei = 41
    self.lesthanmatrixori = 22
    self.lesthanmatrix = '10000000003800000000fc00000001fe00000007ff0000000fff8000001f\
ffc000007fff800000ffff000001fffc000007fff800000fffe000001fff\
c000007fff000000fffe000003fffc000007fff000000fffe0000007ff80\
000003ff00000001fe00000000ffe00000007ffc0000003fffc0000003ff\
f80000007fff0000000ffff0000000fffe0000001fffe0000003fffc0000\
003fff80000007fff8000000ffff0000000ffff0000001fffc0000001ffe\
00000003ff000000007f8000000007c000000000e0000000001'
    self.greatthanmatrixwid = 42
    self.greatthanmatrixhei = 41
    self.greatthanmatrixori = 22
    self.greatthanmatrix = '30000000000f0000000003f000000000ff800000003ff80000000fffc000\
0003fffc0000003fffc0000001fffe0000001fffe0000000fffe0000000f\
fff0000000ffff00000007fff00000007fff80000003fff80000003fffc0\
000003fffc0000001fff00000001ffc00000000ff00000001ffc0000001f\
ff0000003fff8000003fff8000003fff8000007fff0000007fff000000ff\
ff000000fffe000001fffe000001fffe000003fffc000003fffc000003ff\
f8000000fff80000003ff80000000ff000000003f000000000f000000000\
20000000000'
    self.questionmatrixwid = 36
    self.questionmatrixhei = 63
    self.questionmatrixori = -1
    self.questionmatrix = '7fe000003fffe0000fffff8003fffffc007fffffe00fffffff00fffffff8\
1ff801ffc3fe0007fc3fc0003fe3f80001fe7f80000fe7f00000ff7f0000\
07f7e000007ffe000007ffe000007ffe000007ffe000007ffe000007f000\
0000fe0000000fe0000001fe0000003fc0000003fc0000007f8000000ff0\
000001ff0000003fe0000007fc000000ff8000001ff0000003fc0000007f\
8000000ff0000000ff0000001fe0000001fc0000003fc0000003f8000000\
3f80000003f80000003f80000003f80000003f80000003f8000000000000\
000000000000000000000000000000000000000000000000000000000000\
0000003f80000003f80000003f80000003f80000003f80000003f8000000\
3f80000003f80000003f8000'
    self.colonmatrixwid = 9
    self.colonmatrixhei = 45
    self.colonmatrixori = 17
    self.colonmatrix = '1ffffffffffffffffffff000000000000000000000000000000000000000\
0000000000000000000001ffffffffffffffffffff'
    self.quotematrixwid = 22
    self.quotematrixhei = 21
    self.quotematrixori = 2
    self.quotematrix = '3fc0ffff03fffc0ffff03fffc0ffff03fffc0ffff03fffc0ffff03fffc0f\
ffffffdf807e7e01f9f807e7e01f9f807e3c00f0f003c3c00f0f003c'
    self.opensquigmatrixwid = 19
    self.opensquigmatrixhei = 80
    self.opensquigmatrixori = 0
    self.opensquigmatrix = '7e007fc01ff807ff00ffe03ffc07f800fe003f8007f000fe001fc003f800\
7f000fe001fc003f8007f000fe001fc003f8007f000fe001fc003f8007f0\
00fe001fc003f8007f000fe001fc007f000fe003fc00ff007fc01ff803fc\
007f000fe001fe003fe001fe001fe001fc001fc003f8003f0007e000fe00\
1fc003f8007f000fe001fc003f8007f000fe001fc003f8007f000fe001fc\
003f8007f000fe001fc003f8007f000fe001fc001fc003fc007ff807ff00\
ffe00ffc00ff8003f'
    self.closesquigmatrixwid = 20
    self.closesquigmatrixhei = 80
    self.closesquigmatrixori = 0
    self.closesquigmatrix = 'fe000ffc00ffe00fff00fff00fff8007f8003f8001fc001fc001fc001fc0\
01fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc0\
01fc001fc001fc001fc001fc001fc001fc000fc000fe000fe0007f0007f8\
003fe001ff000ff0007f0007f000ff001ff003fe007f8007f000fe000fe0\
00fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc0\
01fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc001fc0\
03f8007f80fff80fff00fff00ffe00ff800fe000'
    self.barmatrixwid = 5
    self.barmatrixhei = 80
    self.barmatrixori = 0
    self.barmatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffffffffffffffffffffffff'
    self.miscmatrixwid = 46
    self.miscmatrixhei = 80
    self.miscmatrixori = 0
    self.miscmatrix = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffff8000000007fe000000001ff8000000007fe000000001ff8000\
000007fe000000001ff8000000007fe000000001ff8000000007fe000000\
001ff8000000007fe000000001ff8000000007fe000000001ff800000000\
7fe000000001ff8000000007fe000000001ff8000000007fe000000001ff\
8000000007fe000000001ff8000000007fe000000001ff8000000007fe00\
0000001ff8000000007fe000000001ff8000000007fe000000001ff80000\
00007fe000000001ff8000000007fe000000001ff8000000007fe0000000\
01ff8000000007fe000000001ff8000000007fe000000001ff8000000007\
fe000000001ff8000000007fe000000001ff8000000007fe000000001ff8\
000000007fe000000001ff8000000007fe000000001ff8000000007fe000\
000001ff8000000007fe000000001ff8000000007fe000000001ff800000\
0007fe000000001ff8000000007fe000000001ff8000000007fe00000000\
1ff8000000007fe000000001ff8000000007fe000000001ff8000000007f\
e000000001ffffffffffffffffffffffffffffffffffffffffffffffffff\
ffffffffffffffffffff'


  def writea(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.amatrix)
    charstring = (self.amatrixwid * self.amatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.amatrixwid * self.amatrixhei:
      charstring = charstring[0 - self.amatrixwid * self.amatrixhei:]
    for i in range(0, len(charstring), self.amatrixwid):
      for j in range(i, i + self.amatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.amatrixori - self.amatrixwid + j / self.amatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.amatrixori + j / self.amatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.amatrixori + j / self.amatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.amatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.amatrixori + j / self.amatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.amatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.amatrixwid) * sizeratio) - k, y + int((self.defsize - (self.amatrixori + j / self.amatrixwid)) * sizeratio) - l)


  def writeb(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.bmatrix)
    charstring = (self.bmatrixwid * self.bmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.bmatrixwid * self.bmatrixhei:
      charstring = charstring[0 - self.bmatrixwid * self.bmatrixhei:]
    for i in range(0, len(charstring), self.bmatrixwid):
      for j in range(i, i + self.bmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.bmatrixori - self.bmatrixwid + j / self.bmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.bmatrixori + j / self.bmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.bmatrixori + j / self.bmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.bmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.bmatrixori + j / self.bmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.bmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.bmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.bmatrixori + j / self.bmatrixwid)) * sizeratio) - l)


  def writec(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.cmatrix)
    charstring = (self.cmatrixwid * self.cmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.cmatrixwid * self.cmatrixhei:
      charstring = charstring[0 - self.cmatrixwid * self.cmatrixhei:]
    for i in range(0, len(charstring), self.cmatrixwid):
      for j in range(i, i + self.cmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.cmatrixori - self.cmatrixwid + j / self.cmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.cmatrixori + j / self.cmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.cmatrixori + j / self.cmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.cmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.cmatrixori + j / self.cmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.cmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.cmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.cmatrixori + j / self.cmatrixwid)) * sizeratio) - l)


  def writed(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.dmatrix)
    charstring = (self.dmatrixwid * self.dmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.dmatrixwid * self.dmatrixhei:
      charstring = charstring[0 - self.dmatrixwid * self.dmatrixhei:]
    for i in range(0, len(charstring), self.dmatrixwid):
      for j in range(i, i + self.dmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.dmatrixori - self.dmatrixwid + j / self.dmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.dmatrixori + j / self.dmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.dmatrixori + j / self.dmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.dmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.dmatrixori + j / self.dmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.dmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.dmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.dmatrixori + j / self.dmatrixwid)) * sizeratio) - l)


  def writee(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.ematrix)
    charstring = (self.ematrixwid * self.ematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.ematrixwid * self.ematrixhei:
      charstring = charstring[0 - self.ematrixwid * self.ematrixhei:]
    for i in range(0, len(charstring), self.ematrixwid):
      for j in range(i, i + self.ematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.ematrixori - self.ematrixwid + j / self.ematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.ematrixori + j / self.ematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.ematrixori + j / self.ematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.ematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.ematrixori + j / self.ematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.ematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.ematrixwid) * sizeratio) - k, y + int((self.defsize - (self.ematrixori + j / self.ematrixwid)) * sizeratio) - l)


  def writef(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.fmatrix)
    charstring = (self.fmatrixwid * self.fmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.fmatrixwid * self.fmatrixhei:
      charstring = charstring[0 - self.fmatrixwid * self.fmatrixhei:]
    for i in range(0, len(charstring), self.fmatrixwid):
      for j in range(i, i + self.fmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.fmatrixori - self.fmatrixwid + j / self.fmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.fmatrixori + j / self.fmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.fmatrixori + j / self.fmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.fmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.fmatrixori + j / self.fmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.fmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.fmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.fmatrixori + j / self.fmatrixwid)) * sizeratio) - l)


  def writeg(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.gmatrix)
    charstring = (self.gmatrixwid * self.gmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.gmatrixwid * self.gmatrixhei:
      charstring = charstring[0 - self.gmatrixwid * self.gmatrixhei:]
    for i in range(0, len(charstring), self.gmatrixwid):
      for j in range(i, i + self.gmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.gmatrixori - self.gmatrixwid + j / self.gmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.gmatrixori + j / self.gmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.gmatrixori + j / self.gmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.gmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.gmatrixori + j / self.gmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.gmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.gmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.gmatrixori + j / self.gmatrixwid)) * sizeratio) - l)


  def writeh(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.hmatrix)
    charstring = (self.hmatrixwid * self.hmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.hmatrixwid * self.hmatrixhei:
      charstring = charstring[0 - self.hmatrixwid * self.hmatrixhei:]
    for i in range(0, len(charstring), self.hmatrixwid):
      for j in range(i, i + self.hmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.hmatrixori - self.hmatrixwid + j / self.hmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.hmatrixori + j / self.hmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.hmatrixori + j / self.hmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.hmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.hmatrixori + j / self.hmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.hmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.hmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.hmatrixori + j / self.hmatrixwid)) * sizeratio) - l)


  def writei(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.imatrix)
    charstring = (self.imatrixwid * self.imatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.imatrixwid * self.imatrixhei:
      charstring = charstring[0 - self.imatrixwid * self.imatrixhei:]
    for i in range(0, len(charstring), self.imatrixwid):
      for j in range(i, i + self.imatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.imatrixori - self.imatrixwid + j / self.imatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.imatrixori + j / self.imatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.imatrixori + j / self.imatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.imatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.imatrixori + j / self.imatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.imatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.imatrixwid) * sizeratio) - k, y + int((self.defsize - (self.imatrixori + j / self.imatrixwid)) * sizeratio) - l)


  def writej(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.jmatrix)
    charstring = (self.jmatrixwid * self.jmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.jmatrixwid * self.jmatrixhei:
      charstring = charstring[0 - self.jmatrixwid * self.jmatrixhei:]
    for i in range(0, len(charstring), self.jmatrixwid):
      for j in range(i, i + self.jmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.jmatrixori - self.jmatrixwid + j / self.jmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.jmatrixori + j / self.jmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.jmatrixori + j / self.jmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.jmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.jmatrixori + j / self.jmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.jmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.jmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.jmatrixori + j / self.jmatrixwid)) * sizeratio) - l)


  def writek(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.kmatrix)
    charstring = (self.kmatrixwid * self.kmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.kmatrixwid * self.kmatrixhei:
      charstring = charstring[0 - self.kmatrixwid * self.kmatrixhei:]
    for i in range(0, len(charstring), self.kmatrixwid):
      for j in range(i, i + self.kmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.kmatrixori - self.kmatrixwid + j / self.kmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.kmatrixori + j / self.kmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.kmatrixori + j / self.kmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.kmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.kmatrixori + j / self.kmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.kmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.kmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.kmatrixori + j / self.kmatrixwid)) * sizeratio) - l)


  def writel(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.lmatrix)
    charstring = (self.lmatrixwid * self.lmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.lmatrixwid * self.lmatrixhei:
      charstring = charstring[0 - self.lmatrixwid * self.lmatrixhei:]
    for i in range(0, len(charstring), self.lmatrixwid):
      for j in range(i, i + self.lmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.lmatrixori - self.lmatrixwid + j / self.lmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.lmatrixori + j / self.lmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.lmatrixori + j / self.lmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.lmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.lmatrixori + j / self.lmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.lmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.lmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.lmatrixori + j / self.lmatrixwid)) * sizeratio) - l)


  def writem(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.mmatrix)
    charstring = (self.mmatrixwid * self.mmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.mmatrixwid * self.mmatrixhei:
      charstring = charstring[0 - self.mmatrixwid * self.mmatrixhei:]
    for i in range(0, len(charstring), self.mmatrixwid):
      for j in range(i, i + self.mmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.mmatrixori - self.mmatrixwid + j / self.mmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.mmatrixori + j / self.mmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.mmatrixori + j / self.mmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.mmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.mmatrixori + j / self.mmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.mmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.mmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.mmatrixori + j / self.mmatrixwid)) * sizeratio) - l)


  def writen(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.nmatrix)
    charstring = (self.nmatrixwid * self.nmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.nmatrixwid * self.nmatrixhei:
      charstring = charstring[0 - self.nmatrixwid * self.nmatrixhei:]
    for i in range(0, len(charstring), self.nmatrixwid):
      for j in range(i, i + self.nmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.nmatrixori - self.nmatrixwid + j / self.nmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.nmatrixori + j / self.nmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.nmatrixori + j / self.nmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.nmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.nmatrixori + j / self.nmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.nmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.nmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.nmatrixori + j / self.nmatrixwid)) * sizeratio) - l)


  def writeo(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.omatrix)
    charstring = (self.omatrixwid * self.omatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.omatrixwid * self.omatrixhei:
      charstring = charstring[0 - self.omatrixwid * self.omatrixhei:]
    for i in range(0, len(charstring), self.omatrixwid):
      for j in range(i, i + self.omatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.omatrixori - self.omatrixwid + j / self.omatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.omatrixori + j / self.omatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.omatrixori + j / self.omatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.omatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.omatrixori + j / self.omatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.omatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.omatrixwid) * sizeratio) - k, y + int((self.defsize - (self.omatrixori + j / self.omatrixwid)) * sizeratio) - l)


  def writep(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.pmatrix)
    charstring = (self.pmatrixwid * self.pmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.pmatrixwid * self.pmatrixhei:
      charstring = charstring[0 - self.pmatrixwid * self.pmatrixhei:]
    for i in range(0, len(charstring), self.pmatrixwid):
      for j in range(i, i + self.pmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.pmatrixori - self.pmatrixwid + j / self.pmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.pmatrixori + j / self.pmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.pmatrixori + j / self.pmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.pmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.pmatrixori + j / self.pmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.pmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.pmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.pmatrixori + j / self.pmatrixwid)) * sizeratio) - l)


  def writeq(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.qmatrix)
    charstring = (self.qmatrixwid * self.qmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.qmatrixwid * self.qmatrixhei:
      charstring = charstring[0 - self.qmatrixwid * self.qmatrixhei:]
    for i in range(0, len(charstring), self.qmatrixwid):
      for j in range(i, i + self.qmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.qmatrixori - self.qmatrixwid + j / self.qmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.qmatrixori + j / self.qmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.qmatrixori + j / self.qmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.qmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.qmatrixori + j / self.qmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.qmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.qmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.qmatrixori + j / self.qmatrixwid)) * sizeratio) - l)


  def writer(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.rmatrix)
    charstring = (self.rmatrixwid * self.rmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.rmatrixwid * self.rmatrixhei:
      charstring = charstring[0 - self.rmatrixwid * self.rmatrixhei:]
    for i in range(0, len(charstring), self.rmatrixwid):
      for j in range(i, i + self.rmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.rmatrixori - self.rmatrixwid + j / self.rmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.rmatrixori + j / self.rmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.rmatrixori + j / self.rmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.rmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.rmatrixori + j / self.rmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.rmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.rmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.rmatrixori + j / self.rmatrixwid)) * sizeratio) - l)


  def writes(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.smatrix)
    charstring = (self.smatrixwid * self.smatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.smatrixwid * self.smatrixhei:
      charstring = charstring[0 - self.smatrixwid * self.smatrixhei:]
    for i in range(0, len(charstring), self.smatrixwid):
      for j in range(i, i + self.smatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.smatrixori - self.smatrixwid + j / self.smatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.smatrixori + j / self.smatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.smatrixori + j / self.smatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.smatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.smatrixori + j / self.smatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.smatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.smatrixwid) * sizeratio) - k, y + int((self.defsize - (self.smatrixori + j / self.smatrixwid)) * sizeratio) - l)


  def writet(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.tmatrix)
    charstring = (self.tmatrixwid * self.tmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.tmatrixwid * self.tmatrixhei:
      charstring = charstring[0 - self.tmatrixwid * self.tmatrixhei:]
    for i in range(0, len(charstring), self.tmatrixwid):
      for j in range(i, i + self.tmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.tmatrixori - self.tmatrixwid + j / self.tmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.tmatrixori + j / self.tmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.tmatrixori + j / self.tmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.tmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.tmatrixori + j / self.tmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.tmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.tmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.tmatrixori + j / self.tmatrixwid)) * sizeratio) - l)


  def writeu(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.umatrix)
    charstring = (self.umatrixwid * self.umatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.umatrixwid * self.umatrixhei:
      charstring = charstring[0 - self.umatrixwid * self.umatrixhei:]
    for i in range(0, len(charstring), self.umatrixwid):
      for j in range(i, i + self.umatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.umatrixori - self.umatrixwid + j / self.umatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.umatrixori + j / self.umatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.umatrixori + j / self.umatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.umatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.umatrixori + j / self.umatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.umatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.umatrixwid) * sizeratio) - k, y + int((self.defsize - (self.umatrixori + j / self.umatrixwid)) * sizeratio) - l)


  def writev(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.vmatrix)
    charstring = (self.vmatrixwid * self.vmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.vmatrixwid * self.vmatrixhei:
      charstring = charstring[0 - self.vmatrixwid * self.vmatrixhei:]
    for i in range(0, len(charstring), self.vmatrixwid):
      for j in range(i, i + self.vmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.vmatrixori - self.vmatrixwid + j / self.vmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.vmatrixori + j / self.vmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.vmatrixori + j / self.vmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.vmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.vmatrixori + j / self.vmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.vmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.vmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.vmatrixori + j / self.vmatrixwid)) * sizeratio) - l)


  def writew(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.wmatrix)
    charstring = (self.wmatrixwid * self.wmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.wmatrixwid * self.wmatrixhei:
      charstring = charstring[0 - self.wmatrixwid * self.wmatrixhei:]
    for i in range(0, len(charstring), self.wmatrixwid):
      for j in range(i, i + self.wmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.wmatrixori - self.wmatrixwid + j / self.wmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.wmatrixori + j / self.wmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.wmatrixori + j / self.wmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.wmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.wmatrixori + j / self.wmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.wmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.wmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.wmatrixori + j / self.wmatrixwid)) * sizeratio) - l)


  def writex(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.xmatrix)
    charstring = (self.xmatrixwid * self.xmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.xmatrixwid * self.xmatrixhei:
      charstring = charstring[0 - self.xmatrixwid * self.xmatrixhei:]
    for i in range(0, len(charstring), self.xmatrixwid):
      for j in range(i, i + self.xmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.xmatrixori - self.xmatrixwid + j / self.xmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.xmatrixori + j / self.xmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.xmatrixori + j / self.xmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.xmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.xmatrixori + j / self.xmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.xmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.xmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.xmatrixori + j / self.xmatrixwid)) * sizeratio) - l)


  def writey(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.ymatrix)
    charstring = (self.ymatrixwid * self.ymatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.ymatrixwid * self.ymatrixhei:
      charstring = charstring[0 - self.ymatrixwid * self.ymatrixhei:]
    for i in range(0, len(charstring), self.ymatrixwid):
      for j in range(i, i + self.ymatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.ymatrixori - self.ymatrixwid + j / self.ymatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.ymatrixori + j / self.ymatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.ymatrixori + j / self.ymatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.ymatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.ymatrixori + j / self.ymatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.ymatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.ymatrixwid) * sizeratio) - k, y + int((self.defsize - (self.ymatrixori + j / self.ymatrixwid)) * sizeratio) - l)


  def writez(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.zmatrix)
    charstring = (self.zmatrixwid * self.zmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.zmatrixwid * self.zmatrixhei:
      charstring = charstring[0 - self.zmatrixwid * self.zmatrixhei:]
    for i in range(0, len(charstring), self.zmatrixwid):
      for j in range(i, i + self.zmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.zmatrixori - self.zmatrixwid + j / self.zmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.zmatrixori + j / self.zmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.zmatrixori + j / self.zmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.zmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.zmatrixori + j / self.zmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.zmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.zmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.zmatrixori + j / self.zmatrixwid)) * sizeratio) - l)


  def writeA(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Amatrix)
    charstring = (self.Amatrixwid * self.Amatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Amatrixwid * self.Amatrixhei:
      charstring = charstring[0 - self.Amatrixwid * self.Amatrixhei:]
    for i in range(0, len(charstring), self.Amatrixwid):
      for j in range(i, i + self.Amatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Amatrixori - self.Amatrixwid + j / self.Amatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Amatrixori + j / self.Amatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Amatrixori + j / self.Amatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Amatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Amatrixori + j / self.Amatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Amatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Amatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Amatrixori + j / self.Amatrixwid)) * sizeratio) - l)


  def writeB(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Bmatrix)
    charstring = (self.Bmatrixwid * self.Bmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Bmatrixwid * self.Bmatrixhei:
      charstring = charstring[0 - self.Bmatrixwid * self.Bmatrixhei:]
    for i in range(0, len(charstring), self.Bmatrixwid):
      for j in range(i, i + self.Bmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Bmatrixori - self.Bmatrixwid + j / self.Bmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Bmatrixori + j / self.Bmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Bmatrixori + j / self.Bmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Bmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Bmatrixori + j / self.Bmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Bmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Bmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Bmatrixori + j / self.Bmatrixwid)) * sizeratio) - l)


  def writeC(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Cmatrix)
    charstring = (self.Cmatrixwid * self.Cmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Cmatrixwid * self.Cmatrixhei:
      charstring = charstring[0 - self.Cmatrixwid * self.Cmatrixhei:]
    for i in range(0, len(charstring), self.Cmatrixwid):
      for j in range(i, i + self.Cmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Cmatrixori - self.Cmatrixwid + j / self.Cmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Cmatrixori + j / self.Cmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Cmatrixori + j / self.Cmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Cmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Cmatrixori + j / self.Cmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Cmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Cmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Cmatrixori + j / self.Cmatrixwid)) * sizeratio) - l)


  def writeD(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Dmatrix)
    charstring = (self.Dmatrixwid * self.Dmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Dmatrixwid * self.Dmatrixhei:
      charstring = charstring[0 - self.Dmatrixwid * self.Dmatrixhei:]
    for i in range(0, len(charstring), self.Dmatrixwid):
      for j in range(i, i + self.Dmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Dmatrixori - self.Dmatrixwid + j / self.Dmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Dmatrixori + j / self.Dmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Dmatrixori + j / self.Dmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Dmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Dmatrixori + j / self.Dmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Dmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Dmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Dmatrixori + j / self.Dmatrixwid)) * sizeratio) - l)


  def writeE(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Ematrix)
    charstring = (self.Ematrixwid * self.Ematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Ematrixwid * self.Ematrixhei:
      charstring = charstring[0 - self.Ematrixwid * self.Ematrixhei:]
    for i in range(0, len(charstring), self.Ematrixwid):
      for j in range(i, i + self.Ematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Ematrixori - self.Ematrixwid + j / self.Ematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Ematrixori + j / self.Ematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Ematrixori + j / self.Ematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Ematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Ematrixori + j / self.Ematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Ematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Ematrixwid) * sizeratio) - k, y + int((self.defsize - (self.Ematrixori + j / self.Ematrixwid)) * sizeratio) - l)


  def writeF(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Fmatrix)
    charstring = (self.Fmatrixwid * self.Fmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Fmatrixwid * self.Fmatrixhei:
      charstring = charstring[0 - self.Fmatrixwid * self.Fmatrixhei:]
    for i in range(0, len(charstring), self.Fmatrixwid):
      for j in range(i, i + self.Fmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Fmatrixori - self.Fmatrixwid + j / self.Fmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Fmatrixori + j / self.Fmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Fmatrixori + j / self.Fmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Fmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Fmatrixori + j / self.Fmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Fmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Fmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Fmatrixori + j / self.Fmatrixwid)) * sizeratio) - l)


  def writeG(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Gmatrix)
    charstring = (self.Gmatrixwid * self.Gmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Gmatrixwid * self.Gmatrixhei:
      charstring = charstring[0 - self.Gmatrixwid * self.Gmatrixhei:]
    for i in range(0, len(charstring), self.Gmatrixwid):
      for j in range(i, i + self.Gmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Gmatrixori - self.Gmatrixwid + j / self.Gmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Gmatrixori + j / self.Gmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Gmatrixori + j / self.Gmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Gmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Gmatrixori + j / self.Gmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Gmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Gmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Gmatrixori + j / self.Gmatrixwid)) * sizeratio) - l)


  def writeH(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Hmatrix)
    charstring = (self.Hmatrixwid * self.Hmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Hmatrixwid * self.Hmatrixhei:
      charstring = charstring[0 - self.Hmatrixwid * self.Hmatrixhei:]
    for i in range(0, len(charstring), self.Hmatrixwid):
      for j in range(i, i + self.Hmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Hmatrixori - self.Hmatrixwid + j / self.Hmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Hmatrixori + j / self.Hmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Hmatrixori + j / self.Hmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Hmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Hmatrixori + j / self.Hmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Hmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Hmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Hmatrixori + j / self.Hmatrixwid)) * sizeratio) - l)


  def writeI(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Imatrix)
    charstring = (self.Imatrixwid * self.Imatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Imatrixwid * self.Imatrixhei:
      charstring = charstring[0 - self.Imatrixwid * self.Imatrixhei:]
    for i in range(0, len(charstring), self.Imatrixwid):
      for j in range(i, i + self.Imatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Imatrixori - self.Imatrixwid + j / self.Imatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Imatrixori + j / self.Imatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Imatrixori + j / self.Imatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Imatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Imatrixori + j / self.Imatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Imatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Imatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Imatrixori + j / self.Imatrixwid)) * sizeratio) - l)


  def writeJ(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Jmatrix)
    charstring = (self.Jmatrixwid * self.Jmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Jmatrixwid * self.Jmatrixhei:
      charstring = charstring[0 - self.Jmatrixwid * self.Jmatrixhei:]
    for i in range(0, len(charstring), self.Jmatrixwid):
      for j in range(i, i + self.Jmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Jmatrixori - self.Jmatrixwid + j / self.Jmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Jmatrixori + j / self.Jmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Jmatrixori + j / self.Jmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Jmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Jmatrixori + j / self.Jmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Jmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Jmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Jmatrixori + j / self.Jmatrixwid)) * sizeratio) - l)


  def writeK(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Kmatrix)
    charstring = (self.Kmatrixwid * self.Kmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Kmatrixwid * self.Kmatrixhei:
      charstring = charstring[0 - self.Kmatrixwid * self.Kmatrixhei:]
    for i in range(0, len(charstring), self.Kmatrixwid):
      for j in range(i, i + self.Kmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Kmatrixori - self.Kmatrixwid + j / self.Kmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Kmatrixori + j / self.Kmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Kmatrixori + j / self.Kmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Kmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Kmatrixori + j / self.Kmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Kmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Kmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Kmatrixori + j / self.Kmatrixwid)) * sizeratio) - l)


  def writeL(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Lmatrix)
    charstring = (self.Lmatrixwid * self.Lmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Lmatrixwid * self.Lmatrixhei:
      charstring = charstring[0 - self.Lmatrixwid * self.Lmatrixhei:]
    for i in range(0, len(charstring), self.Lmatrixwid):
      for j in range(i, i + self.Lmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Lmatrixori - self.Lmatrixwid + j / self.Lmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Lmatrixori + j / self.Lmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Lmatrixori + j / self.Lmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Lmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Lmatrixori + j / self.Lmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Lmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Lmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Lmatrixori + j / self.Lmatrixwid)) * sizeratio) - l)


  def writeM(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Mmatrix)
    charstring = (self.Mmatrixwid * self.Mmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Mmatrixwid * self.Mmatrixhei:
      charstring = charstring[0 - self.Mmatrixwid * self.Mmatrixhei:]
    for i in range(0, len(charstring), self.Mmatrixwid):
      for j in range(i, i + self.Mmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Mmatrixori - self.Mmatrixwid + j / self.Mmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Mmatrixori + j / self.Mmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Mmatrixori + j / self.Mmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Mmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Mmatrixori + j / self.Mmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Mmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Mmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Mmatrixori + j / self.Mmatrixwid)) * sizeratio) - l)


  def writeN(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Nmatrix)
    charstring = (self.Nmatrixwid * self.Nmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Nmatrixwid * self.Nmatrixhei:
      charstring = charstring[0 - self.Nmatrixwid * self.Nmatrixhei:]
    for i in range(0, len(charstring), self.Nmatrixwid):
      for j in range(i, i + self.Nmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Nmatrixori - self.Nmatrixwid + j / self.Nmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Nmatrixori + j / self.Nmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Nmatrixori + j / self.Nmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Nmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Nmatrixori + j / self.Nmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Nmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Nmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Nmatrixori + j / self.Nmatrixwid)) * sizeratio) - l)


  def writeO(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Omatrix)
    charstring = (self.Omatrixwid * self.Omatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Omatrixwid * self.Omatrixhei:
      charstring = charstring[0 - self.Omatrixwid * self.Omatrixhei:]
    for i in range(0, len(charstring), self.Omatrixwid):
      for j in range(i, i + self.Omatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Omatrixori - self.Omatrixwid + j / self.Omatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Omatrixori + j / self.Omatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Omatrixori + j / self.Omatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Omatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Omatrixori + j / self.Omatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Omatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Omatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Omatrixori + j / self.Omatrixwid)) * sizeratio) - l)


  def writeP(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Pmatrix)
    charstring = (self.Pmatrixwid * self.Pmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Pmatrixwid * self.Pmatrixhei:
      charstring = charstring[0 - self.Pmatrixwid * self.Pmatrixhei:]
    for i in range(0, len(charstring), self.Pmatrixwid):
      for j in range(i, i + self.Pmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Pmatrixori - self.Pmatrixwid + j / self.Pmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Pmatrixori + j / self.Pmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Pmatrixori + j / self.Pmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Pmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Pmatrixori + j / self.Pmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Pmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Pmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Pmatrixori + j / self.Pmatrixwid)) * sizeratio) - l)


  def writeQ(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Qmatrix)
    charstring = (self.Qmatrixwid * self.Qmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Qmatrixwid * self.Qmatrixhei:
      charstring = charstring[0 - self.Qmatrixwid * self.Qmatrixhei:]
    for i in range(0, len(charstring), self.Qmatrixwid):
      for j in range(i, i + self.Qmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Qmatrixori - self.Qmatrixwid + j / self.Qmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Qmatrixori + j / self.Qmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Qmatrixori + j / self.Qmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Qmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Qmatrixori + j / self.Qmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Qmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Qmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Qmatrixori + j / self.Qmatrixwid)) * sizeratio) - l)


  def writeR(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Rmatrix)
    charstring = (self.Rmatrixwid * self.Rmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Rmatrixwid * self.Rmatrixhei:
      charstring = charstring[0 - self.Rmatrixwid * self.Rmatrixhei:]
    for i in range(0, len(charstring), self.Rmatrixwid):
      for j in range(i, i + self.Rmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Rmatrixori - self.Rmatrixwid + j / self.Rmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Rmatrixori + j / self.Rmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Rmatrixori + j / self.Rmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Rmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Rmatrixori + j / self.Rmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Rmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Rmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Rmatrixori + j / self.Rmatrixwid)) * sizeratio) - l)


  def writeS(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Smatrix)
    charstring = (self.Smatrixwid * self.Smatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Smatrixwid * self.Smatrixhei:
      charstring = charstring[0 - self.Smatrixwid * self.Smatrixhei:]
    for i in range(0, len(charstring), self.Smatrixwid):
      for j in range(i, i + self.Smatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Smatrixori - self.Smatrixwid + j / self.Smatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Smatrixori + j / self.Smatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Smatrixori + j / self.Smatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Smatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Smatrixori + j / self.Smatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Smatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Smatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Smatrixori + j / self.Smatrixwid)) * sizeratio) - l)


  def writeT(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Tmatrix)
    charstring = (self.Tmatrixwid * self.Tmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Tmatrixwid * self.Tmatrixhei:
      charstring = charstring[0 - self.Tmatrixwid * self.Tmatrixhei:]
    for i in range(0, len(charstring), self.Tmatrixwid):
      for j in range(i, i + self.Tmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Tmatrixori - self.Tmatrixwid + j / self.Tmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Tmatrixori + j / self.Tmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Tmatrixori + j / self.Tmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Tmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Tmatrixori + j / self.Tmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Tmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Tmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Tmatrixori + j / self.Tmatrixwid)) * sizeratio) - l)


  def writeU(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Umatrix)
    charstring = (self.Umatrixwid * self.Umatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Umatrixwid * self.Umatrixhei:
      charstring = charstring[0 - self.Umatrixwid * self.Umatrixhei:]
    for i in range(0, len(charstring), self.Umatrixwid):
      for j in range(i, i + self.Umatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Umatrixori - self.Umatrixwid + j / self.Umatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Umatrixori + j / self.Umatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Umatrixori + j / self.Umatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Umatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Umatrixori + j / self.Umatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Umatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Umatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Umatrixori + j / self.Umatrixwid)) * sizeratio) - l)


  def writeV(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Vmatrix)
    charstring = (self.Vmatrixwid * self.Vmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Vmatrixwid * self.Vmatrixhei:
      charstring = charstring[0 - self.Vmatrixwid * self.Vmatrixhei:]
    for i in range(0, len(charstring), self.Vmatrixwid):
      for j in range(i, i + self.Vmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Vmatrixori - self.Vmatrixwid + j / self.Vmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Vmatrixori + j / self.Vmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Vmatrixori + j / self.Vmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Vmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Vmatrixori + j / self.Vmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Vmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Vmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Vmatrixori + j / self.Vmatrixwid)) * sizeratio) - l)


  def writeW(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Wmatrix)
    charstring = (self.Wmatrixwid * self.Wmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Wmatrixwid * self.Wmatrixhei:
      charstring = charstring[0 - self.Wmatrixwid * self.Wmatrixhei:]
    for i in range(0, len(charstring), self.Wmatrixwid):
      for j in range(i, i + self.Wmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Wmatrixori - self.Wmatrixwid + j / self.Wmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Wmatrixori + j / self.Wmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Wmatrixori + j / self.Wmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Wmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Wmatrixori + j / self.Wmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Wmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Wmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Wmatrixori + j / self.Wmatrixwid)) * sizeratio) - l)


  def writeX(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Xmatrix)
    charstring = (self.Xmatrixwid * self.Xmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Xmatrixwid * self.Xmatrixhei:
      charstring = charstring[0 - self.Xmatrixwid * self.Xmatrixhei:]
    for i in range(0, len(charstring), self.Xmatrixwid):
      for j in range(i, i + self.Xmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Xmatrixori - self.Xmatrixwid + j / self.Xmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Xmatrixori + j / self.Xmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Xmatrixori + j / self.Xmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Xmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Xmatrixori + j / self.Xmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Xmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Xmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Xmatrixori + j / self.Xmatrixwid)) * sizeratio) - l)


  def writeY(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Ymatrix)
    charstring = (self.Ymatrixwid * self.Ymatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Ymatrixwid * self.Ymatrixhei:
      charstring = charstring[0 - self.Ymatrixwid * self.Ymatrixhei:]
    for i in range(0, len(charstring), self.Ymatrixwid):
      for j in range(i, i + self.Ymatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Ymatrixori - self.Ymatrixwid + j / self.Ymatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Ymatrixori + j / self.Ymatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Ymatrixori + j / self.Ymatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Ymatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Ymatrixori + j / self.Ymatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Ymatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Ymatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Ymatrixori + j / self.Ymatrixwid)) * sizeratio) - l)


  def writeZ(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.Zmatrix)
    charstring = (self.Zmatrixwid * self.Zmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.Zmatrixwid * self.Zmatrixhei:
      charstring = charstring[0 - self.Zmatrixwid * self.Zmatrixhei:]
    for i in range(0, len(charstring), self.Zmatrixwid):
      for j in range(i, i + self.Zmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.Zmatrixori - self.Zmatrixwid + j / self.Zmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.Zmatrixori + j / self.Zmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.Zmatrixori + j / self.Zmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.Zmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.Zmatrixori + j / self.Zmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.Zmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.Zmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.Zmatrixori + j / self.Zmatrixwid)) * sizeratio) - l)


  def writeone(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.onematrix)
    charstring = (self.onematrixwid * self.onematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.onematrixwid * self.onematrixhei:
      charstring = charstring[0 - self.onematrixwid * self.onematrixhei:]
    for i in range(0, len(charstring), self.onematrixwid):
      for j in range(i, i + self.onematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.onematrixori - self.onematrixwid + j / self.onematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.onematrixori + j / self.onematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.onematrixori + j / self.onematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.onematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.onematrixori + j / self.onematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.onematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.onematrixwid) * sizeratio) - k, y + int((self.defsize - (self.onematrixori + j / self.onematrixwid)) * sizeratio) - l)


  def writetwo(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.twomatrix)
    charstring = (self.twomatrixwid * self.twomatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.twomatrixwid * self.twomatrixhei:
      charstring = charstring[0 - self.twomatrixwid * self.twomatrixhei:]
    for i in range(0, len(charstring), self.twomatrixwid):
      for j in range(i, i + self.twomatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.twomatrixori - self.twomatrixwid + j / self.twomatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.twomatrixori + j / self.twomatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.twomatrixori + j / self.twomatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.twomatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.twomatrixori + j / self.twomatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.twomatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.twomatrixwid) * sizeratio) - k, y + int((self.defsize - (self.twomatrixori + j / self.twomatrixwid)) * sizeratio) - l)


  def writethree(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.threematrix)
    charstring = (self.threematrixwid * self.threematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.threematrixwid * self.threematrixhei:
      charstring = charstring[0 - self.threematrixwid * self.threematrixhei:]
    for i in range(0, len(charstring), self.threematrixwid):
      for j in range(i, i + self.threematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.threematrixori - self.threematrixwid + j / self.threematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.threematrixori + j / self.threematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.threematrixori + j / self.threematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.threematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.threematrixori + j / self.threematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.threematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.threematrixwid) * sizeratio) - k, y + int((self.defsize - (self.threematrixori + j / self.threematrixwid)) * sizeratio) - l)


  def writefour(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.fourmatrix)
    charstring = (self.fourmatrixwid * self.fourmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.fourmatrixwid * self.fourmatrixhei:
      charstring = charstring[0 - self.fourmatrixwid * self.fourmatrixhei:]
    for i in range(0, len(charstring), self.fourmatrixwid):
      for j in range(i, i + self.fourmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.fourmatrixori - self.fourmatrixwid + j / self.fourmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.fourmatrixori + j / self.fourmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.fourmatrixori + j / self.fourmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.fourmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.fourmatrixori + j / self.fourmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.fourmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.fourmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.fourmatrixori + j / self.fourmatrixwid)) * sizeratio) - l)


  def writefive(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.fivematrix)
    charstring = (self.fivematrixwid * self.fivematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.fivematrixwid * self.fivematrixhei:
      charstring = charstring[0 - self.fivematrixwid * self.fivematrixhei:]
    for i in range(0, len(charstring), self.fivematrixwid):
      for j in range(i, i + self.fivematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.fivematrixori - self.fivematrixwid + j / self.fivematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.fivematrixori + j / self.fivematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.fivematrixori + j / self.fivematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.fivematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.fivematrixori + j / self.fivematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.fivematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.fivematrixwid) * sizeratio) - k, y + int((self.defsize - (self.fivematrixori + j / self.fivematrixwid)) * sizeratio) - l)


  def writesix(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.sixmatrix)
    charstring = (self.sixmatrixwid * self.sixmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.sixmatrixwid * self.sixmatrixhei:
      charstring = charstring[0 - self.sixmatrixwid * self.sixmatrixhei:]
    for i in range(0, len(charstring), self.sixmatrixwid):
      for j in range(i, i + self.sixmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.sixmatrixori - self.sixmatrixwid + j / self.sixmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.sixmatrixori + j / self.sixmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.sixmatrixori + j / self.sixmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.sixmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.sixmatrixori + j / self.sixmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.sixmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.sixmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.sixmatrixori + j / self.sixmatrixwid)) * sizeratio) - l)


  def writeseven(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.sevenmatrix)
    charstring = (self.sevenmatrixwid * self.sevenmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.sevenmatrixwid * self.sevenmatrixhei:
      charstring = charstring[0 - self.sevenmatrixwid * self.sevenmatrixhei:]
    for i in range(0, len(charstring), self.sevenmatrixwid):
      for j in range(i, i + self.sevenmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.sevenmatrixori - self.sevenmatrixwid + j / self.sevenmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.sevenmatrixori + j / self.sevenmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.sevenmatrixori + j / self.sevenmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.sevenmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.sevenmatrixori + j / self.sevenmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.sevenmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.sevenmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.sevenmatrixori + j / self.sevenmatrixwid)) * sizeratio) - l)


  def writeeight(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.eightmatrix)
    charstring = (self.eightmatrixwid * self.eightmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.eightmatrixwid * self.eightmatrixhei:
      charstring = charstring[0 - self.eightmatrixwid * self.eightmatrixhei:]
    for i in range(0, len(charstring), self.eightmatrixwid):
      for j in range(i, i + self.eightmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.eightmatrixori - self.eightmatrixwid + j / self.eightmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.eightmatrixori + j / self.eightmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.eightmatrixori + j / self.eightmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.eightmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.eightmatrixori + j / self.eightmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.eightmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.eightmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.eightmatrixori + j / self.eightmatrixwid)) * sizeratio) - l)


  def writenine(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.ninematrix)
    charstring = (self.ninematrixwid * self.ninematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.ninematrixwid * self.ninematrixhei:
      charstring = charstring[0 - self.ninematrixwid * self.ninematrixhei:]
    for i in range(0, len(charstring), self.ninematrixwid):
      for j in range(i, i + self.ninematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.ninematrixori - self.ninematrixwid + j / self.ninematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.ninematrixori + j / self.ninematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.ninematrixori + j / self.ninematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.ninematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.ninematrixori + j / self.ninematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.ninematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.ninematrixwid) * sizeratio) - k, y + int((self.defsize - (self.ninematrixori + j / self.ninematrixwid)) * sizeratio) - l)


  def writeten(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.tenmatrix)
    charstring = (self.tenmatrixwid * self.tenmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.tenmatrixwid * self.tenmatrixhei:
      charstring = charstring[0 - self.tenmatrixwid * self.tenmatrixhei:]
    for i in range(0, len(charstring), self.tenmatrixwid):
      for j in range(i, i + self.tenmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.tenmatrixori - self.tenmatrixwid + j / self.tenmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.tenmatrixori + j / self.tenmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.tenmatrixori + j / self.tenmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.tenmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.tenmatrixori + j / self.tenmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.tenmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.tenmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.tenmatrixori + j / self.tenmatrixwid)) * sizeratio) - l)


  def write_(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self._matrix)
    charstring = (self._matrixwid * self._matrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self._matrixwid * self._matrixhei:
      charstring = charstring[0 - self._matrixwid * self._matrixhei:]
    for i in range(0, len(charstring), self._matrixwid):
      for j in range(i, i + self._matrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self._matrixori - self._matrixwid + j / self._matrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self._matrixori + j / self._matrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self._matrixori + j / self._matrixwid) * sizeratio) - l - self.defsize, x + int((j % self._matrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self._matrixori + j / self._matrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self._matrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self._matrixwid) * sizeratio) - k, y + int((self.defsize - (self._matrixori + j / self._matrixwid)) * sizeratio) - l)


  def writeminus(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.minusmatrix)
    charstring = (self.minusmatrixwid * self.minusmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.minusmatrixwid * self.minusmatrixhei:
      charstring = charstring[0 - self.minusmatrixwid * self.minusmatrixhei:]
    for i in range(0, len(charstring), self.minusmatrixwid):
      for j in range(i, i + self.minusmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.minusmatrixori - self.minusmatrixwid + j / self.minusmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.minusmatrixori + j / self.minusmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.minusmatrixori + j / self.minusmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.minusmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.minusmatrixori + j / self.minusmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.minusmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.minusmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.minusmatrixori + j / self.minusmatrixwid)) * sizeratio) - l)


  def writeplus(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.plusmatrix)
    charstring = (self.plusmatrixwid * self.plusmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.plusmatrixwid * self.plusmatrixhei:
      charstring = charstring[0 - self.plusmatrixwid * self.plusmatrixhei:]
    for i in range(0, len(charstring), self.plusmatrixwid):
      for j in range(i, i + self.plusmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.plusmatrixori - self.plusmatrixwid + j / self.plusmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.plusmatrixori + j / self.plusmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.plusmatrixori + j / self.plusmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.plusmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.plusmatrixori + j / self.plusmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.plusmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.plusmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.plusmatrixori + j / self.plusmatrixwid)) * sizeratio) - l)


  def writeequal(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.equalmatrix)
    charstring = (self.equalmatrixwid * self.equalmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.equalmatrixwid * self.equalmatrixhei:
      charstring = charstring[0 - self.equalmatrixwid * self.equalmatrixhei:]
    for i in range(0, len(charstring), self.equalmatrixwid):
      for j in range(i, i + self.equalmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.equalmatrixori - self.equalmatrixwid + j / self.equalmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.equalmatrixori + j / self.equalmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.equalmatrixori + j / self.equalmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.equalmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.equalmatrixori + j / self.equalmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.equalmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.equalmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.equalmatrixori + j / self.equalmatrixwid)) * sizeratio) - l)


  def writeexcl(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.exclmatrix)
    charstring = (self.exclmatrixwid * self.exclmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.exclmatrixwid * self.exclmatrixhei:
      charstring = charstring[0 - self.exclmatrixwid * self.exclmatrixhei:]
    for i in range(0, len(charstring), self.exclmatrixwid):
      for j in range(i, i + self.exclmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.exclmatrixori - self.exclmatrixwid + j / self.exclmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.exclmatrixori + j / self.exclmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.exclmatrixori + j / self.exclmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.exclmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.exclmatrixori + j / self.exclmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.exclmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.exclmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.exclmatrixori + j / self.exclmatrixwid)) * sizeratio) - l)


  def writeat(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.atmatrix)
    charstring = (self.atmatrixwid * self.atmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.atmatrixwid * self.atmatrixhei:
      charstring = charstring[0 - self.atmatrixwid * self.atmatrixhei:]
    for i in range(0, len(charstring), self.atmatrixwid):
      for j in range(i, i + self.atmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.atmatrixori - self.atmatrixwid + j / self.atmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.atmatrixori + j / self.atmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.atmatrixori + j / self.atmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.atmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.atmatrixori + j / self.atmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.atmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.atmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.atmatrixori + j / self.atmatrixwid)) * sizeratio) - l)


  def writehash(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.hashmatrix)
    charstring = (self.hashmatrixwid * self.hashmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.hashmatrixwid * self.hashmatrixhei:
      charstring = charstring[0 - self.hashmatrixwid * self.hashmatrixhei:]
    for i in range(0, len(charstring), self.hashmatrixwid):
      for j in range(i, i + self.hashmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.hashmatrixori - self.hashmatrixwid + j / self.hashmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.hashmatrixori + j / self.hashmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.hashmatrixori + j / self.hashmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.hashmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.hashmatrixori + j / self.hashmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.hashmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.hashmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.hashmatrixori + j / self.hashmatrixwid)) * sizeratio) - l)


  def writedollar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.dollarmatrix)
    charstring = (self.dollarmatrixwid * self.dollarmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.dollarmatrixwid * self.dollarmatrixhei:
      charstring = charstring[0 - self.dollarmatrixwid * self.dollarmatrixhei:]
    for i in range(0, len(charstring), self.dollarmatrixwid):
      for j in range(i, i + self.dollarmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.dollarmatrixori - self.dollarmatrixwid + j / self.dollarmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.dollarmatrixori + j / self.dollarmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.dollarmatrixori + j / self.dollarmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.dollarmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.dollarmatrixori + j / self.dollarmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.dollarmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.dollarmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.dollarmatrixori + j / self.dollarmatrixwid)) * sizeratio) - l)


  def writepercent(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.percentmatrix)
    charstring = (self.percentmatrixwid * self.percentmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.percentmatrixwid * self.percentmatrixhei:
      charstring = charstring[0 - self.percentmatrixwid * self.percentmatrixhei:]
    for i in range(0, len(charstring), self.percentmatrixwid):
      for j in range(i, i + self.percentmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.percentmatrixori - self.percentmatrixwid + j / self.percentmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.percentmatrixori + j / self.percentmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.percentmatrixori + j / self.percentmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.percentmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.percentmatrixori + j / self.percentmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.percentmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.percentmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.percentmatrixori + j / self.percentmatrixwid)) * sizeratio) - l)


  def writehat(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.hatmatrix)
    charstring = (self.hatmatrixwid * self.hatmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.hatmatrixwid * self.hatmatrixhei:
      charstring = charstring[0 - self.hatmatrixwid * self.hatmatrixhei:]
    for i in range(0, len(charstring), self.hatmatrixwid):
      for j in range(i, i + self.hatmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.hatmatrixori - self.hatmatrixwid + j / self.hatmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.hatmatrixori + j / self.hatmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.hatmatrixori + j / self.hatmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.hatmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.hatmatrixori + j / self.hatmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.hatmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.hatmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.hatmatrixori + j / self.hatmatrixwid)) * sizeratio) - l)


  def writeamp(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.ampmatrix)
    charstring = (self.ampmatrixwid * self.ampmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.ampmatrixwid * self.ampmatrixhei:
      charstring = charstring[0 - self.ampmatrixwid * self.ampmatrixhei:]
    for i in range(0, len(charstring), self.ampmatrixwid):
      for j in range(i, i + self.ampmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.ampmatrixori - self.ampmatrixwid + j / self.ampmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.ampmatrixori + j / self.ampmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.ampmatrixori + j / self.ampmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.ampmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.ampmatrixori + j / self.ampmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.ampmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.ampmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.ampmatrixori + j / self.ampmatrixwid)) * sizeratio) - l)


  def writestrix(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.strixmatrix)
    charstring = (self.strixmatrixwid * self.strixmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.strixmatrixwid * self.strixmatrixhei:
      charstring = charstring[0 - self.strixmatrixwid * self.strixmatrixhei:]
    for i in range(0, len(charstring), self.strixmatrixwid):
      for j in range(i, i + self.strixmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.strixmatrixori - self.strixmatrixwid + j / self.strixmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.strixmatrixori + j / self.strixmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.strixmatrixori + j / self.strixmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.strixmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.strixmatrixori + j / self.strixmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.strixmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.strixmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.strixmatrixori + j / self.strixmatrixwid)) * sizeratio) - l)


  def writeopencpar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.opencparmatrix)
    charstring = (self.opencparmatrixwid * self.opencparmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.opencparmatrixwid * self.opencparmatrixhei:
      charstring = charstring[0 - self.opencparmatrixwid * self.opencparmatrixhei:]
    for i in range(0, len(charstring), self.opencparmatrixwid):
      for j in range(i, i + self.opencparmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.opencparmatrixori - self.opencparmatrixwid + j / self.opencparmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.opencparmatrixori + j / self.opencparmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.opencparmatrixori + j / self.opencparmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.opencparmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.opencparmatrixori + j / self.opencparmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.opencparmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.opencparmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.opencparmatrixori + j / self.opencparmatrixwid)) * sizeratio) - l)


  def writeclosecpar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.closecparmatrix)
    charstring = (self.closecparmatrixwid * self.closecparmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.closecparmatrixwid * self.closecparmatrixhei:
      charstring = charstring[0 - self.closecparmatrixwid * self.closecparmatrixhei:]
    for i in range(0, len(charstring), self.closecparmatrixwid):
      for j in range(i, i + self.closecparmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.closecparmatrixori - self.closecparmatrixwid + j / self.closecparmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.closecparmatrixori + j / self.closecparmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.closecparmatrixori + j / self.closecparmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.closecparmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.closecparmatrixori + j / self.closecparmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.closecparmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.closecparmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.closecparmatrixori + j / self.closecparmatrixwid)) * sizeratio) - l)


  def writeopenspar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.opensparmatrix)
    charstring = (self.opensparmatrixwid * self.opensparmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.opensparmatrixwid * self.opensparmatrixhei:
      charstring = charstring[0 - self.opensparmatrixwid * self.opensparmatrixhei:]
    for i in range(0, len(charstring), self.opensparmatrixwid):
      for j in range(i, i + self.opensparmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.opensparmatrixori - self.opensparmatrixwid + j / self.opensparmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.opensparmatrixori + j / self.opensparmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.opensparmatrixori + j / self.opensparmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.opensparmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.opensparmatrixori + j / self.opensparmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.opensparmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.opensparmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.opensparmatrixori + j / self.opensparmatrixwid)) * sizeratio) - l)


  def writeclosespar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.closesparmatrix)
    charstring = (self.closesparmatrixwid * self.closesparmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.closesparmatrixwid * self.closesparmatrixhei:
      charstring = charstring[0 - self.closesparmatrixwid * self.closesparmatrixhei:]
    for i in range(0, len(charstring), self.closesparmatrixwid):
      for j in range(i, i + self.closesparmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.closesparmatrixori - self.closesparmatrixwid + j / self.closesparmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.closesparmatrixori + j / self.closesparmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.closesparmatrixori + j / self.closesparmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.closesparmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.closesparmatrixori + j / self.closesparmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.closesparmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.closesparmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.closesparmatrixori + j / self.closesparmatrixwid)) * sizeratio) - l)


  def writebackslash(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.backslashmatrix)
    charstring = (self.backslashmatrixwid * self.backslashmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.backslashmatrixwid * self.backslashmatrixhei:
      charstring = charstring[0 - self.backslashmatrixwid * self.backslashmatrixhei:]
    for i in range(0, len(charstring), self.backslashmatrixwid):
      for j in range(i, i + self.backslashmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.backslashmatrixori - self.backslashmatrixwid + j / self.backslashmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.backslashmatrixori + j / self.backslashmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.backslashmatrixori + j / self.backslashmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.backslashmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.backslashmatrixori + j / self.backslashmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.backslashmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.backslashmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.backslashmatrixori + j / self.backslashmatrixwid)) * sizeratio) - l)


  def writesemicol(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.semicolmatrix)
    charstring = (self.semicolmatrixwid * self.semicolmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.semicolmatrixwid * self.semicolmatrixhei:
      charstring = charstring[0 - self.semicolmatrixwid * self.semicolmatrixhei:]
    for i in range(0, len(charstring), self.semicolmatrixwid):
      for j in range(i, i + self.semicolmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.semicolmatrixori - self.semicolmatrixwid + j / self.semicolmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.semicolmatrixori + j / self.semicolmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.semicolmatrixori + j / self.semicolmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.semicolmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.semicolmatrixori + j / self.semicolmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.semicolmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.semicolmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.semicolmatrixori + j / self.semicolmatrixwid)) * sizeratio) - l)


  def writepost(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.postmatrix)
    charstring = (self.postmatrixwid * self.postmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.postmatrixwid * self.postmatrixhei:
      charstring = charstring[0 - self.postmatrixwid * self.postmatrixhei:]
    for i in range(0, len(charstring), self.postmatrixwid):
      for j in range(i, i + self.postmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.postmatrixori - self.postmatrixwid + j / self.postmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.postmatrixori + j / self.postmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.postmatrixori + j / self.postmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.postmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.postmatrixori + j / self.postmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.postmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.postmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.postmatrixori + j / self.postmatrixwid)) * sizeratio) - l)


  def writecomma(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.commamatrix)
    charstring = (self.commamatrixwid * self.commamatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.commamatrixwid * self.commamatrixhei:
      charstring = charstring[0 - self.commamatrixwid * self.commamatrixhei:]
    for i in range(0, len(charstring), self.commamatrixwid):
      for j in range(i, i + self.commamatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.commamatrixori - self.commamatrixwid + j / self.commamatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.commamatrixori + j / self.commamatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.commamatrixori + j / self.commamatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.commamatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.commamatrixori + j / self.commamatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.commamatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.commamatrixwid) * sizeratio) - k, y + int((self.defsize - (self.commamatrixori + j / self.commamatrixwid)) * sizeratio) - l)


  def writefullstop(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.fullstopmatrix)
    charstring = (self.fullstopmatrixwid * self.fullstopmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.fullstopmatrixwid * self.fullstopmatrixhei:
      charstring = charstring[0 - self.fullstopmatrixwid * self.fullstopmatrixhei:]
    for i in range(0, len(charstring), self.fullstopmatrixwid):
      for j in range(i, i + self.fullstopmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.fullstopmatrixori - self.fullstopmatrixwid + j / self.fullstopmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.fullstopmatrixori + j / self.fullstopmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.fullstopmatrixori + j / self.fullstopmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.fullstopmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.fullstopmatrixori + j / self.fullstopmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.fullstopmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.fullstopmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.fullstopmatrixori + j / self.fullstopmatrixwid)) * sizeratio) - l)


  def writeforslash(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.forslashmatrix)
    charstring = (self.forslashmatrixwid * self.forslashmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.forslashmatrixwid * self.forslashmatrixhei:
      charstring = charstring[0 - self.forslashmatrixwid * self.forslashmatrixhei:]
    for i in range(0, len(charstring), self.forslashmatrixwid):
      for j in range(i, i + self.forslashmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.forslashmatrixori - self.forslashmatrixwid + j / self.forslashmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.forslashmatrixori + j / self.forslashmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.forslashmatrixori + j / self.forslashmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.forslashmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.forslashmatrixori + j / self.forslashmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.forslashmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.forslashmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.forslashmatrixori + j / self.forslashmatrixwid)) * sizeratio) - l)


  def writelesthan(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.lesthanmatrix)
    charstring = (self.lesthanmatrixwid * self.lesthanmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.lesthanmatrixwid * self.lesthanmatrixhei:
      charstring = charstring[0 - self.lesthanmatrixwid * self.lesthanmatrixhei:]
    for i in range(0, len(charstring), self.lesthanmatrixwid):
      for j in range(i, i + self.lesthanmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.lesthanmatrixori - self.lesthanmatrixwid + j / self.lesthanmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.lesthanmatrixori + j / self.lesthanmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.lesthanmatrixori + j / self.lesthanmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.lesthanmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.lesthanmatrixori + j / self.lesthanmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.lesthanmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.lesthanmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.lesthanmatrixori + j / self.lesthanmatrixwid)) * sizeratio) - l)


  def writegreatthan(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.greatthanmatrix)
    charstring = (self.greatthanmatrixwid * self.greatthanmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.greatthanmatrixwid * self.greatthanmatrixhei:
      charstring = charstring[0 - self.greatthanmatrixwid * self.greatthanmatrixhei:]
    for i in range(0, len(charstring), self.greatthanmatrixwid):
      for j in range(i, i + self.greatthanmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.greatthanmatrixori - self.greatthanmatrixwid + j / self.greatthanmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.greatthanmatrixori + j / self.greatthanmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.greatthanmatrixori + j / self.greatthanmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.greatthanmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.greatthanmatrixori + j / self.greatthanmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.greatthanmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.greatthanmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.greatthanmatrixori + j / self.greatthanmatrixwid)) * sizeratio) - l)


  def writequestion(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.questionmatrix)
    charstring = (self.questionmatrixwid * self.questionmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.questionmatrixwid * self.questionmatrixhei:
      charstring = charstring[0 - self.questionmatrixwid * self.questionmatrixhei:]
    for i in range(0, len(charstring), self.questionmatrixwid):
      for j in range(i, i + self.questionmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.questionmatrixori - self.questionmatrixwid + j / self.questionmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.questionmatrixori + j / self.questionmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.questionmatrixori + j / self.questionmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.questionmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.questionmatrixori + j / self.questionmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.questionmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.questionmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.questionmatrixori + j / self.questionmatrixwid)) * sizeratio) - l)


  def writecolon(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.colonmatrix)
    charstring = (self.colonmatrixwid * self.colonmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.colonmatrixwid * self.colonmatrixhei:
      charstring = charstring[0 - self.colonmatrixwid * self.colonmatrixhei:]
    for i in range(0, len(charstring), self.colonmatrixwid):
      for j in range(i, i + self.colonmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.colonmatrixori - self.colonmatrixwid + j / self.colonmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.colonmatrixori + j / self.colonmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.colonmatrixori + j / self.colonmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.colonmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.colonmatrixori + j / self.colonmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.colonmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.colonmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.colonmatrixori + j / self.colonmatrixwid)) * sizeratio) - l)


  def writequote(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.quotematrix)
    charstring = (self.quotematrixwid * self.quotematrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.quotematrixwid * self.quotematrixhei:
      charstring = charstring[0 - self.quotematrixwid * self.quotematrixhei:]
    for i in range(0, len(charstring), self.quotematrixwid):
      for j in range(i, i + self.quotematrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.quotematrixori - self.quotematrixwid + j / self.quotematrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.quotematrixori + j / self.quotematrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.quotematrixori + j / self.quotematrixwid) * sizeratio) - l - self.defsize, x + int((j % self.quotematrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.quotematrixori + j / self.quotematrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.quotematrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.quotematrixwid) * sizeratio) - k, y + int((self.defsize - (self.quotematrixori + j / self.quotematrixwid)) * sizeratio) - l)


  def writeopensquig(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.opensquigmatrix)
    charstring = (self.opensquigmatrixwid * self.opensquigmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.opensquigmatrixwid * self.opensquigmatrixhei:
      charstring = charstring[0 - self.opensquigmatrixwid * self.opensquigmatrixhei:]
    for i in range(0, len(charstring), self.opensquigmatrixwid):
      for j in range(i, i + self.opensquigmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.opensquigmatrixori - self.opensquigmatrixwid + j / self.opensquigmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.opensquigmatrixori + j / self.opensquigmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.opensquigmatrixori + j / self.opensquigmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.opensquigmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.opensquigmatrixori + j / self.opensquigmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.opensquigmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.opensquigmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.opensquigmatrixori + j / self.opensquigmatrixwid)) * sizeratio) - l)


  def writeclosesquig(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.closesquigmatrix)
    charstring = (self.closesquigmatrixwid * self.closesquigmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.closesquigmatrixwid * self.closesquigmatrixhei:
      charstring = charstring[0 - self.closesquigmatrixwid * self.closesquigmatrixhei:]
    for i in range(0, len(charstring), self.closesquigmatrixwid):
      for j in range(i, i + self.closesquigmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.closesquigmatrixori - self.closesquigmatrixwid + j / self.closesquigmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.closesquigmatrixori + j / self.closesquigmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.closesquigmatrixori + j / self.closesquigmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.closesquigmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.closesquigmatrixori + j / self.closesquigmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.closesquigmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.closesquigmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.closesquigmatrixori + j / self.closesquigmatrixwid)) * sizeratio) - l)


  def writebar(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.barmatrix)
    charstring = (self.barmatrixwid * self.barmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.barmatrixwid * self.barmatrixhei:
      charstring = charstring[0 - self.barmatrixwid * self.barmatrixhei:]
    for i in range(0, len(charstring), self.barmatrixwid):
      for j in range(i, i + self.barmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.barmatrixori - self.barmatrixwid + j / self.barmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.barmatrixori + j / self.barmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.barmatrixori + j / self.barmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.barmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.barmatrixori + j / self.barmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.barmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.barmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.barmatrixori + j / self.barmatrixwid)) * sizeratio) - l)


  def writemisc(self, x, y, size, ital, bold, sans, rotate):
    xpos = x
    sizeratio = size * 1.0 / self.defsize
    sizeint = (size - 1) / self.defsize + 1
    if bold:
      sizeint = sizeint + 2 + int(sizeratio)
    charstring = binar(self.miscmatrix)
    charstring = (self.miscmatrixwid * self.miscmatrixhei - len(charstring)) * '0' + charstring
    if len(charstring) > self.miscmatrixwid * self.miscmatrixhei:
      charstring = charstring[0 - self.miscmatrixwid * self.miscmatrixhei:]
    for i in range(0, len(charstring), self.miscmatrixwid):
      for j in range(i, i + self.miscmatrixwid):
        if charstring[j] == '1':
          for k in range(sizeint):
            for l in range(sizeint):
              if ital and rotate == -1:
                x = xpos + (int(((self.miscmatrixori - self.miscmatrixwid + j / self.miscmatrixwid)) * sizeratio) - l) / 3
              elif ital:
                x = xpos + (int((self.defsize - (self.miscmatrixori + j / self.miscmatrixwid)) * sizeratio) - l) / 3
              if rotate == 1:
                self.plotPoint(y + int((self.miscmatrixori + j / self.miscmatrixwid) * sizeratio) - l - self.defsize, x + int((j % self.miscmatrixwid) * sizeratio) - k)
              elif rotate == -1:
                self.plotPoint(y + int((self.defsize - (self.miscmatrixori + j / self.miscmatrixwid)) * sizeratio) - l, 2 * x - (x + int((j % self.miscmatrixwid) * sizeratio) - k))
              else:
                self.plotPoint(x + int((j % self.miscmatrixwid) * sizeratio) - k, y + int((self.defsize - (self.miscmatrixori + j / self.miscmatrixwid)) * sizeratio) - l)


  def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
    xpos = x
    if rotate != 0:
      xpos, y = y, xpos
    if justify == 'right':
        xpos -= self.lengthString(thestring, size)    
    for i in thestring:
      if i == 'a':
        self.writea(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.amatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.amatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'b':
        self.writeb(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.bmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.bmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'c':
        self.writec(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.cmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.cmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'd':
        self.writed(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.dmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.dmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'e':
        self.writee(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.ematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.ematrixwid * size / self.defsize + 1  + size / 20
      elif i == 'f':
        self.writef(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.fmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.fmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'g':
        self.writeg(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.gmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.gmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'h':
        self.writeh(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.hmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.hmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'i':
        self.writei(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.imatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.imatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'j':
        self.writej(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.jmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.jmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'k':
        self.writek(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.kmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.kmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'l':
        self.writel(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.lmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.lmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'm':
        self.writem(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.mmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.mmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'n':
        self.writen(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.nmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.nmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'o':
        self.writeo(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.omatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.omatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'p':
        self.writep(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.pmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.pmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'q':
        self.writeq(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.qmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.qmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'r':
        self.writer(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.rmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.rmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 's':
        self.writes(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.smatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.smatrixwid * size / self.defsize + 1  + size / 20
      elif i == 't':
        self.writet(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.tmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.tmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'u':
        self.writeu(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.umatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.umatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'v':
        self.writev(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.vmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.vmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'w':
        self.writew(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.wmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.wmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'x':
        self.writex(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.xmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.xmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'y':
        self.writey(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.ymatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.ymatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'z':
        self.writez(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.zmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.zmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'A':
        self.writeA(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Amatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Amatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'B':
        self.writeB(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Bmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Bmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'C':
        self.writeC(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Cmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Cmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'D':
        self.writeD(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Dmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Dmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'E':
        self.writeE(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Ematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Ematrixwid * size / self.defsize + 1  + size / 20
      elif i == 'F':
        self.writeF(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Fmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Fmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'G':
        self.writeG(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Gmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Gmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'H':
        self.writeH(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Hmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Hmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'I':
        self.writeI(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Imatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Imatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'J':
        self.writeJ(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Jmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Jmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'K':
        self.writeK(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Kmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Kmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'L':
        self.writeL(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Lmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Lmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'M':
        self.writeM(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Mmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Mmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'N':
        self.writeN(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Nmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Nmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'O':
        self.writeO(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Omatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Omatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'P':
        self.writeP(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Pmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Pmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Q':
        self.writeQ(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Qmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Qmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'R':
        self.writeR(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Rmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Rmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'S':
        self.writeS(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Smatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Smatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'T':
        self.writeT(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Tmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Tmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'U':
        self.writeU(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Umatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Umatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'V':
        self.writeV(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Vmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Vmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'W':
        self.writeW(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Wmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Wmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'X':
        self.writeX(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Xmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Xmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Y':
        self.writeY(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Ymatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Ymatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Z':
        self.writeZ(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.Zmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.Zmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '1':
        self.writeone(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.onematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.onematrixwid * size / self.defsize + 1  + size / 20
      elif i == '2':
        self.writetwo(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.twomatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.twomatrixwid * size / self.defsize + 1  + size / 20
      elif i == '3':
        self.writethree(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.threematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.threematrixwid * size / self.defsize + 1  + size / 20
      elif i == '4':
        self.writefour(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.fourmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.fourmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '5':
        self.writefive(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.fivematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.fivematrixwid * size / self.defsize + 1  + size / 20
      elif i == '6':
        self.writesix(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.sixmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.sixmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '7':
        self.writeseven(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.sevenmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.sevenmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '8':
        self.writeeight(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.eightmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.eightmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '9':
        self.writenine(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.ninematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.ninematrixwid * size / self.defsize + 1  + size / 20
      elif i == '0':
        self.writeten(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.tenmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.tenmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '_':
        self.write_(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self._matrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self._matrixwid * size / self.defsize + 1  + size / 20
      elif i == '-':
        self.writeminus(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.minusmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.minusmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '+':
        self.writeplus(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.plusmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.plusmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '=':
        self.writeequal(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.equalmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.equalmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '!':
        self.writeexcl(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.exclmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.exclmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '@':
        self.writeat(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.atmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.atmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '#':
        self.writehash(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.hashmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.hashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '$':
        self.writedollar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.dollarmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.dollarmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '%':
        self.writepercent(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.percentmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.percentmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '^':
        self.writehat(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.hatmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.hatmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '&':
        self.writeamp(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.ampmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.ampmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '*':
        self.writestrix(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.strixmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.strixmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '(':
        self.writeopencpar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.opencparmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.opencparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ')':
        self.writeclosecpar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.closecparmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.closecparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '[':
        self.writeopenspar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.opensparmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.opensparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ']':
        self.writeclosespar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.closesparmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.closesparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '\\':
        self.writebackslash(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.backslashmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.backslashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ';':
        self.writesemicol(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.semicolmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.semicolmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '\'':
        self.writepost(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.postmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.postmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ',':
        self.writecomma(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.commamatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.commamatrixwid * size / self.defsize + 1  + size / 20
      elif i == '.':
        self.writefullstop(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.fullstopmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.fullstopmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '/':
        self.writeforslash(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.forslashmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.forslashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '<':
        self.writelesthan(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.lesthanmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.lesthanmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '>':
        self.writegreatthan(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.greatthanmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.greatthanmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '?':
        self.writequestion(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.questionmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.questionmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ':':
        self.writecolon(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.colonmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.colonmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '"':
        self.writequote(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.quotematrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.quotematrixwid * size / self.defsize + 1  + size / 20
      elif i == '{':
        self.writeopensquig(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.opensquigmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.opensquigmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '}':
        self.writeclosesquig(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.closesquigmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.closesquigmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '|':
        self.writebar(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.barmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.barmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ' ':
        if rotate == -1:
          xpos -= 24 * size / self.defsize + 1  + size / 20
        else:
          xpos += 24 * size / self.defsize + 1  + size / 20
      else:
        self.writemisc(xpos, y, size, ital, bold, True, rotate)
        if rotate == -1:
          xpos -= self.miscmatrixwid * size / self.defsize + 1  + size / 20
        else:
          xpos += self.miscmatrixwid * size / self.defsize + 1  + size / 20

  def lengthString(self, theString, size):
    xpos = 0
    for i in theString:
      if i == 'a':
        xpos += self.amatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'b':
        xpos += self.bmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'c':
        xpos += self.cmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'd':
        xpos += self.dmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'e':
        xpos += self.ematrixwid * size / self.defsize + 1  + size / 20
      elif i == 'f':
        xpos += self.fmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'g':
        xpos += self.gmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'h':
        xpos += self.hmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'i':
        xpos += self.imatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'j':
        xpos += self.jmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'k':
        xpos += self.kmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'l':
        xpos += self.lmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'm':
        xpos += self.mmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'n':
        xpos += self.nmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'o':
        xpos += self.omatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'p':
        xpos += self.pmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'q':
        xpos += self.qmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'r':
        xpos += self.rmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 's':
        xpos += self.smatrixwid * size / self.defsize + 1  + size / 20
      elif i == 't':
        xpos += self.tmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'u':
        xpos += self.umatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'v':
        xpos += self.vmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'w':
        xpos += self.wmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'x':
        xpos += self.xmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'y':
        xpos += self.ymatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'z':
        xpos += self.zmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'A':
        xpos += self.Amatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'B':
        xpos += self.Bmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'C':
        xpos += self.Cmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'D':
        xpos += self.Dmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'E':
        xpos += self.Ematrixwid * size / self.defsize + 1  + size / 20
      elif i == 'F':
        xpos += self.Fmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'G':
        xpos += self.Gmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'H':
        xpos += self.Hmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'I':
        xpos += self.Imatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'J':
        xpos += self.Jmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'K':
        xpos += self.Kmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'L':
        xpos += self.Lmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'M':
        xpos += self.Mmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'N':
        xpos += self.Nmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'O':
        xpos += self.Omatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'P':
        xpos += self.Pmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Q':
        xpos += self.Qmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'R':
        xpos += self.Rmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'S':
        xpos += self.Smatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'T':
        xpos += self.Tmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'U':
        xpos += self.Umatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'V':
        xpos += self.Vmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'W':
        xpos += self.Wmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'X':
        xpos += self.Xmatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Y':
        xpos += self.Ymatrixwid * size / self.defsize + 1  + size / 20
      elif i == 'Z':
        xpos += self.Zmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '1':
        xpos += self.onematrixwid * size / self.defsize + 1  + size / 20
      elif i == '2':
        xpos += self.twomatrixwid * size / self.defsize + 1  + size / 20
      elif i == '3':
        xpos += self.threematrixwid * size / self.defsize + 1  + size / 20
      elif i == '4':
        xpos += self.fourmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '5':
        xpos += self.fivematrixwid * size / self.defsize + 1  + size / 20
      elif i == '6':
        xpos += self.sixmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '7':
        xpos += self.sevenmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '8':
        xpos += self.eightmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '9':
        xpos += self.ninematrixwid * size / self.defsize + 1  + size / 20
      elif i == '0':
        xpos += self.tenmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '_':
        xpos += self._matrixwid * size / self.defsize + 1  + size / 20
      elif i == '-':
        xpos += self.minusmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '+':
        xpos += self.plusmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '=':
        xpos += self.equalmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '!':
        xpos += self.exclmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '@':
        xpos += self.atmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '#':
        xpos += self.hashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '$':
        xpos += self.dollarmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '%':
        xpos += self.percentmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '^':
        xpos += self.hatmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '&':
        xpos += self.ampmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '*':
        xpos += self.strixmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '(':
        xpos += self.opencparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ')':
        xpos += self.closecparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '[':
        xpos += self.opensparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ']':
        xpos += self.closesparmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '\\':
        xpos += self.backslashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ';':
        xpos += self.semicolmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '\'':
        xpos += self.postmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ',':
        xpos += self.commamatrixwid * size / self.defsize + 1  + size / 20
      elif i == '.':
        xpos += self.fullstopmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '/':
        xpos += self.forslashmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '<':
        xpos += self.lesthanmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '>':
        xpos += self.greatthanmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '?':
        xpos += self.questionmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ':':
        xpos += self.colonmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '"':
        xpos += self.quotematrixwid * size / self.defsize + 1  + size / 20
      elif i == '{':
        xpos += self.opensquigmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '}':
        xpos += self.closesquigmatrixwid * size / self.defsize + 1  + size / 20
      elif i == '|':
        xpos += self.barmatrixwid * size / self.defsize + 1  + size / 20
      elif i == ' ':
        xpos += 24 * size / self.defsize + 1  + size / 20
      else:
        xpos += self.miscmatrixwid * size / self.defsize + 1  + size / 20
    return xpos

  def setDefaultPenColor( self ):
    self.currentPen = self.fg

  def setPenColor( self, p ):
    oldColor = self.currentPen
    # look for c in palette
    pnum = p.toLong()
    try:
      self.currentPen = self.palette.index( pnum )
    except ValueError:
      if len( self.palette ) < 256 :
        self.palette.append( pnum )
        self.currentPen = len( self.palette ) - 1
      else:
        self.currentPen = self.fg

    return Color.fromLong( self.palette[oldColor] )

  def getPenColor( self ):
    return Color.fromLong( self.palette[self.currentPen] )

  def plotPoint( self, x, y ):
    if ( 0 <= x < self.wd and 0 <= y < self.ht ):
      x = int(x)
      y = int(y)
      self.bitarray[y][x] = self.currentPen


  def drawOutRect(self, x, y, wid, ht, lt):
    if wid == 1:
      if lt != 0:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        self.drawLine(x, y, x, y+ht-1)
        self.setPenColor(temp)
      else:
        self.drawLine(x,y,x,y+ht-1)
    else:
      if lt > wid/2 and lt != 1:
        lt = wid/2
      if lt > ht/2 and lt != 1:
        lt = ht/2
      self.drawRect(x,y,wid,ht,True)
      temp = self.getPenColor()
      self.setPenColor(Color.BLACK)
      for i in range(lt):
        self.drawRect(x+i,y+i,wid - i,ht -i)
      self.setPenColor(temp)


  def drawRect( self, x, y, wid, ht, fill=False ):
    x = int(x)
    y = int(y)
    cury = y

    # subtract one for line width
    wid -= 1
    ht -= 1

    self.drawLine( x, y, x+wid, y )
    if fill:
      cury = y
      while cury < y+ht:
        self.drawLine( x, cury, x+wid, cury )
        cury += 1
    else:
      self.drawLine( x, y, x, y+ht )
      self.drawLine( x+wid, y, x+wid, y+ht )
    self.drawLine( x, y+ht, x+wid, y+ht )

  def drawSquare( self, x, y, wid, fill=False ):
    self.drawRect( x, y, wid, wid, fill )

  def drawDash(self, x1, y1, x2, y2, wid=1, dashl=3, dashg=3):
    currX = x1
    currY = y1
    if x1 == x2:
      for i in range(wid):
        currY = y1
        while (y1 < y2 and currY + dashl < y2) or (y1 > y2 and currY - dashl > y2):
          if y1 < y2:
            self.drawLine(currX, currY, currX, currY + dashl)
            currY = currY + dashl + dashg
          else:
            self.drawLine(currX, currY, currX, currY - dashl)
            currY = currY - dashl - dashg
        if (y1 < y2 and currY < y2) or (y2 < y1 and currY > y2):
          self.drawLine(currX, currY, currX, y2)
        currX -= 1
    elif y1 == y2:
      for i in range(wid):
        currX = x1
        while (x1 < x2 and currX + dashl < x2) or (x1 > x2 and currX - dashl > x1):
          if x1 < x2:
            self.drawLine(currX, currY, currX + dashl, currY)
            currX = currX + dashl + dashg
          else:
            self.drawLine(currX, currY, currX - dashl, currY)
            currX = currX - dashl - dashg
        if (x1 < x2 and currX < x2) or (x2 < x1 and currX > x2):
          self.drawLine(currX, currY, x2, currY)
        currY -= 1
    else:
      ratio = abs(x1-x2) * 1.0 / abs(y1-y2)
      while (x1 < x2 and currX + dashl * min([ratio, 1]) < x2) or (x1 > x2 and currX - dashl * min([ratio, 1]) > x2):
        if ratio > 1:
          if x1 < x2:
            nextX = currX + dashl
            currXt = currX + dashl + dashg
          else:
            nextX = currX - dashl
            currXt = currX - dashl - dashg
          if y1 < y2:
            nextY = currY + dashl / ratio
            currYt = currY + (dashl + dashg) / ratio
          else:
            nextY = currY - dashl / ratio
            currYt = currY - (dashl + dashg) / ratio
        else:
          if x1 < x2:
            nextX = currX + dashl * ratio
            currXt = currX + (dashl + dashg) * ratio
          else:
            nextX = currX - dashl * ratio
            currXt = currX - (dashl + dashg) * ratio
          if y1 < y2:
            nextY = currY + dashl
            currYt = currY + dashl + dashg
          else:
            nextY = currY - dashl
            currYt = currY - (dashl + dashg)
        self.drawLine(currX, currY, nextX, nextY)
        currX = currXt
        currY = currYt
      if currX + dashl * min([ratio, 1]) < x2:
        self.drawLine(currX, currY, x2, y2)


  def drawRightArrow(self, x, y, wid, ht, lt, outline=True):
    if lt > ht /2:
        lt = ht/2
    x1 = x + wid
    y1 = y + ht/2
    x2 = x + wid - ht / 2
    ht -= 1
    if wid > ht/2:
      for i in range(y, y+ht+1):
        self.drawLine(x2, i, x1, y1)
      self.drawRect(x, y + ht/4, wid - ht/2, ht/2, True)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x + i, y+ht/4 + i, x2 + i, y+ht/4 + i)
          self.drawLine(x2 + i, y+ht/4 + i, x2 + i, y + i *2)
          self.drawLine(x2 + i, y + i * 2, x1 -i, y1)
          self.drawLine(x1 - i, y1, x2 + i, y+ht - i * 2)
          self.drawLine(x2 + i, y+ht-i * 2, x2 + i, y+ht/4+ht/2 - i)
          self.drawLine(x2 + i, y+ht/4+ht/2 - i, x + i, y+ht/4+ht/2 - i)
          self.drawLine(x + i, y+ht/4+ht/2 - i, x + i, y+ht/4 + i)
        self.setPenColor(temp)
    else:
      for i in range(y, y+ht+1):
        self.drawLine(x, i, x1, y1)
      if outline and lt != 0:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x, y+ht-i, x1-i, y1)
          self.drawLine(x, y+i, x1-i, y1)
          if x1 != x:
            crapliney1 = (y1 - y)/(x1 - x)*(x+i - x + 1) + y
            crapliney2 = y + ht - (y1 - y)/(x1 - x)*(x+i - x + 1)
            self.drawLine(x+i, crapliney1, x+i, crapliney2)
        self.setPenColor(temp)

  def drawLeftArrow(self, x, y, wid, ht, lt, outline=True):
    if lt > ht /2:
        lt = ht/2
    y1 = y + (ht/2)
    x1 = x + wid
    x2 = x + ht/2
    ht -= 1
    if wid > ht/2:
      for i in range(y, y+ht+1):
        self.drawLine(x, y1, x2, i)
      self.drawRect(x2, y+ht/4, wid - ht/2, ht/2, True)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x+i, y1, x2-i, y+i*2)
          self.drawLine(x2-i, y+i*2, x2-i, y+ht/4+i)
          self.drawLine(x2-i, y+ht/4+i, x1-i, y+ht/4+i)
          self.drawLine(x1-i, y+ht/4+i, x1-i, y+ht/4 + ht/2-i)
          self.drawLine(x1-i, y+ht/4+ht/2-i, x2-i, y+ht/4+ht/2-i)
          self.drawLine(x2-i, y+ht/4+ht/2-i, x2-i, y+ht-i*2)
          self.drawLine(x2-i, y+ht-i*2, x+i, y1)
        self.setPenColor(temp)
    else:
      if lt > wid /2:
          lt = wid/2
      for i in range(y, y+ht+1):
        self.drawLine(x, y1, x1, i)
      if outline and lt != 0:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x+i, y1, x1, y+i)
          if x1 != x:
            crapliney1 = (y1 - y)/(x1 - x)*(x+i - x + 1) + y
            crapliney2 = y + ht - (y1 - y)/(x1 - x)*(x+i - x + 1)
            self.drawLine(x1-i, crapliney1, x1-i, crapliney2)
            self.drawLine(x1, y+ht-i, x+i, y1)
        self.setPenColor(temp)

  def drawRightFrame(self, x, y, wid, ht, lt, frame, outline=True):
    if lt > ht /2:
      lt = ht /2
    if frame == 1:
      y1 = y + ht/2
      y2 = y + ht * 5/8
      y3 = y + ht * 3/4
    elif frame == 2:
      y1 = y + ht * 5/8
      y2 = y + ht * 3/4
      y3 = y + ht * 7/8
    elif frame == 0:
      y1 = y + ht * 3/4
      y2 = y + ht * 7/8
      y3 = y + ht - 1
    x1 = x
    x2 = x + wid - ht/8
    x3 = x + wid
    if wid > ht/8:
      for i in range(y1, y3 + 1):
        self.drawLine(x1, i, x2, i)
        self.drawLine(x2, i, x3, y2)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x1, y1 + i, x2, y1 + i)
          self.drawLine(x2, y1 + i, x3 - i, y2)
          self.drawLine(x3 - i, y2, x2, y3 - i)
          self.drawLine(x2, y3 - i, x1, y3 -i)
          self.drawLine(x1 + i, y3 - i, x1 + i, y1 + i)
        self.setPenColor(temp)
    else:
      for i in range(y1, y3 + 1):
        self.drawLine(x1, i, x3, y2)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        self.drawLine(x1, y1, x3, y2)
        self.drawLine(x3, y2, x1, y3)
        self.drawLine(x1, y1, x1, y3)
        self.setPenColor(temp)

  def drawRightFrameRect(self, x, y, wid, ht, lt, frame, outline=True):
    if lt > ht /2:
      lt = ht /2
    if frame == 1:
      y1 = y + ht/2
      y3 = y + ht * 3/4
    elif frame == 2:
      y1 = y + ht * 5/8
      y3 = y + ht * 7/8
    elif frame == 0:
      y1 = y + ht * 3/4
      y3 = y + ht - 1
    x1 = x
    x2 = x + wid
    for i in range(y1, y3 + 1):
      self.drawLine(x1, i, x2, i)
    if outline:
      temp = self.getPenColor()
      self.setPenColor(Color.BLACK)
      for i in range(lt):
        self.drawLine(x1, y1 + i, x2, y1 + i)
        self.drawLine(x2, y1 + i, x2 - i, y3)
        self.drawLine(x2, y3 - i, x1, y3 -i)
        self.drawLine(x1 + i, y3 - i, x1 + i, y1 + i)
      self.setPenColor(temp)

  def drawLeftFrame(self, x, y, wid, ht, lt, frame, outline=True):
    if lt > ht /2:
      lt = ht /2
    if frame == 1:
      y1 = y
      y2 = y + ht /8
      y3 = y + ht/4
    elif frame == 2:
      y1 = y + ht /8
      y2 = y + ht/4
      y3 = y + ht * 3/8
    elif frame == 0:
      y1 = y + ht / 4
      y2 = y + ht * 3/8
      y3 = y + ht / 2
    x1 = x + wid
    x2 = x + ht/8
    x3 = x
    if wid > ht/8:
      for i in range(y1, y3 + 1):
        self.drawLine(x1, i, x2, i)
        self.drawLine(x2, i, x3, y2)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        for i in range(lt):
          self.drawLine(x1, y1 + i, x2, y1 + i)
          self.drawLine(x2, y1 + i, x3 - i, y2)
          self.drawLine(x3 - i, y2, x2, y3 - i)
          self.drawLine(x2, y3 - i, x1, y3 -i)
          self.drawLine(x1 + i, y3 - i, x1 + i, y1 + i)
        self.setPenColor(temp)
    else:
      for i in range(y1, y3 + 1):
        self.drawLine(x1, i, x3, y2)
      if outline:
        temp = self.getPenColor()
        self.setPenColor(Color.BLACK)
        self.drawLine(x1, y1, x3, y2)
        self.drawLine(x3, y2, x1, y3)
        self.drawLine(x1, y1, x1, y3)
        self.setPenColor(temp)

  def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, outline=True):
    if lt > ht /2:
      lt = ht /2
    if frame == 1:
      y1 = y
      y3 = y + ht/4
    elif frame == 2:
      y1 = y + ht /8
      y3 = y + ht * 3/8
    elif frame == 0:
      y1 = y + ht / 4
      y3 = y + ht / 2
    x1 = x + wid
    x2 = x
    for i in range(y1, y3 + 1):
      self.drawLine(x1, i, x2, i)
    if outline:
      temp = self.getPenColor()
      self.setPenColor(Color.BLACK)
      for i in range(lt):
        self.drawLine(x1, y1 + i, x2, y1 + i)
        self.drawLine(x2 - i, y1, x2 - i, y3)
        self.drawLine(x2, y3 - i, x1, y3 -i)
        self.drawLine(x1 + i, y3, x1 + i, y1)
      self.setPenColor(temp)

  def drawPointer(self, x, y, ht, lt, outline=True):
    x1 = x - int(round(0.577350269 * ht/2))
    x2 = x + int(round(0.577350269 * ht/2))
    y1 = y + ht/2
    y2 = y + ht - 1
    for i in range(x1, x2 + 1):
      self.drawLine(i, y2, x, y1)
    if outline:
      temp = self.getPenColor()
      self.setPenColor(Color.BLACK)
      self.drawLine(x, y1, x1, y2)
      self.drawLine(x, y1, x2, y2)
      self.drawLine(x1, y2, x2, y2)
      self.setPenColor(temp)


  def bresLine(x,y,x2,y2):
    """Bresenham line algorithm"""
    steep = 0
    coords = []
    dx = int(abs(x2 - x)+0.5)
    if (x2 - x) > 0:
      sx = 1
    else:
      sx = -1
    dy = int(abs(y2 - y)+0.5)
    if (y2 - y) > 0:
      sy = 1
    else:
      sy = -1
    if dy > dx:
      steep = 1
      x,y = y,x
      dx,dy = dy,dx
      sx,sy = sy,sx
    dx2 = dx*2
    dy2 = dy*2
    d = dy2 - dx
    for i in range(0,dx):
      coords.append( (x,y) )
      while d >= 0:
        y += sy
        d -= dx2
      x += sx
      d += dy2

    if steep: #transpose x's and y's
      coords = [ (c[1],c[0]) for c in coords ]

    coords.append( (x2,y2) )

    return coords
  bresLine = staticmethod( bresLine )

  def _drawLine( self, x1, y1, x2, y2 ):
    # special checks for vert and horiz lines
    if ( x1 == x2 ):
      if 0 <= x1 < self.wd:
        if ( y2 < y1 ):
          y1,y2 = y2,y1
        cury = max( y1, 0 )
        maxy = min( y2, self.ht-1 )
        while cury <= maxy :
          self.plotPoint( x1, cury )
          cury += 1
      return

    if ( y1 == y2 ):
      if ( 0 <= y1 < self.ht ):
        if ( x2 < x1 ):
          x1,x2 = x2,x1
        curx = max( x1, 0 )
        maxx = min( x2, self.wd-1 )
        while curx <= maxx:
          self.plotPoint( curx, y1 )
          curx += 1
      return

    for pt in BitMap.bresLine(x1, y1, x2, y2):
      self.plotPoint( pt[0], pt[1] )

  def _drawLines( self, lineSegs ):
    for x1,y1,x2,y2 in lineSegs:
      self._drawLine( x1, y1, x2, y2 )

  def drawLine( self, x1, y1, x2, y2, type=LINE_SOLID ):
    if type == BitMap.LINE_SOLID:
      self._drawLine( x1, y1, x2, y2 )
    elif type == BitMap.LINE_DASHED:
      # how many segs?
      len = hypot( x2-x1, y2-y1 )
      numsegs = len / BitMap._DASH_LEN
      dx = ( x2 - x1 ) / numsegs
      dy = ( y2 - y1 ) / numsegs
      dx2 = dx / 2.0
      dy2 = dy / 2.0
      if ( x2 < x1 ):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
      segs = []
      curx = x1
      cury = y1
      for i in range( int(numsegs) ):
        segs.append( ( curx, cury, curx + dx2, cury + dy2 ) )
        curx += dx
        cury += dy
      if curx + dx2 > x2:
        segs.append( ( curx, cury, x2, y2 ) )
      else:
        segs.append( ( curx, cury, curx + dx2, cury + dy2 ) )
      self._drawLines( segs )
    elif type == BitMap.LINE_DOTTED:
      len = hypot( x2-x1, y2-y1 )
      numsegs = len / BitMap._DOT_LEN
      dx = ( x2 - x1 ) / numsegs
      dy = ( y2 - y1 ) / numsegs
      dx2 = dx / 2.0
      dy2 = dy / 2.0
      if ( x2 < x1 ):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
      segs = []
      curx = x1
      cury = y1
      for i in range( int(numsegs) ):
        segs.append( ( curx, cury, curx + dx2, cury + dy2 ) )
        curx += dx
        cury += dy
      if curx + dx2 > x2:
        segs.append( ( curx, cury, x2, y2 ) )
      else:
        segs.append( ( curx, cury, curx + dx2, cury + dy2 ) )
      self._drawLines( segs )
    elif type == BitMap.LINE_DOT_DASH:
      len = hypot( x2-x1, y2-y1 )
      numsegs = len / BitMap._DOT_DASH_LEN
      dx = ( x2 - x1 ) / numsegs
      dy = ( y2 - y1 ) / numsegs
      dx3 = dx / 3.0
      dy3 = dy / 3.0
      dx23 = 0.62*dx
      dy23 = 0.62*dy
      dx56 = 0.78*dx
      dy56 = 0.78*dy
      if ( x2 < x1 ):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
      segs = []
      curx = x1
      cury = y1
      for i in range( int(numsegs) ):
        segs.append( ( curx, cury, curx + dx3, cury + dy3 ) )
        segs.append( ( curx + dx23, cury + dy23, curx + dx56, cury + dy56  ) )
        curx += dx
        cury += dy
      if curx + dx3 > x2:
        segs.append( ( curx, cury, x2, y2 ) )
      else:
        segs.append( ( curx, cury, curx + dx3, cury + dy3 ) )
        if curx + dx23 < x2:
          if curx + dx56 > x2:
            segs.append( ( curx + dx23, cury + dy23, x2, y2 ) )
          else:
            segs.append( ( curx + dx23, cury + dy23, curx + dx56, cury + dy56  ) )
        else:
          pass #segs.append( ( curx, cury, curx + dx3, cury + dy3 ) )
      segs.append( ( curx, cury, x2, y2 ) )
      self._drawLines( segs )

  def drawCircle( self, cx, cy, r, fill=False ):
    x = 0
    y = r
    d = 1 - r

    self.plotPoint(cx, cy + y)
    self.plotPoint(cx, cy - y)
    if fill:
      self.drawLine(cx - y, cy, cx + y, cy)
    else:
      self.plotPoint(cx + y, cy)
      self.plotPoint(cx - y, cy)

    while( y > x ):
      if ( d < 0 ):
        d += ( 2*x + 3 )
      else:
        d += ( 2*(x-y) + 5 )
        y -= 1
      x += 1

      if fill:
        self.drawLine(cx + x - 1, cy + y, cx - x + 1, cy + y)
        self.drawLine(cx - x + 1, cy - y, cx + x - 1, cy - y)
        self.drawLine(cx + y - 1, cy + x, cx - y + 1, cy + x)
        self.drawLine(cx - y + 1, cy - x, cx + y - 1, cy - x)
      else:
        self.plotPoint(cx + x, cy + y)
        self.plotPoint(cx + y, cy + x)
        self.plotPoint(cx - x, cy - y)
        self.plotPoint(cx - y, cy - x)
        self.plotPoint(cx + x, cy - y)
        self.plotPoint(cx - y, cy + x)
        self.plotPoint(cx - x, cy + y)
        self.plotPoint(cx + y, cy - x)

# method for creating gif string
  def createGIFString(self, oneistone):
        if not oneistone:
            if self.wd > 1000:
                modifier = 1000.0 / self.wd
                self.wd = 1000
                self.ht = int(self.ht * modifier)
            else:
                oneistone = True
        binarystring = 'GIF89a' # header
        binarystring += struct.pack('h', self.wd) + struct.pack('h', self.ht) + chr(int('10010110', 2)) + '\x00\x00'
        if len(self.palette) <= 128:
            for i in self.palette:
                colour = Color.fromLong(i)
                binarystring += chr(colour.red) + chr(colour.grn) + chr(colour.blu)
            for i in range(128 - len(self.palette)):
                binarystring += chr(255) + chr(255) + chr(255)
        else:
            for i in range(8): # 128 colour table
                for j in range(4):
                    for k in range(4):
                        binarystring += chr(int(i*36.5)) + chr(j*85) + chr(k*85)
        binarystring += ',\x00\x00\x00\x00' + struct.pack('h', self.wd) + struct.pack('h', self.ht) + '\x00' # image descriptor
        binarystring += '\x07' # LZW Minimum code size
        pixstring = ''
        self.bitarray.reverse()
        for a, i in enumerate(self.bitarray):
            for b, j in enumerate(i):
                if len(self.palette) <= 128:
                    if oneistone:
                        pixstring += chr(j)
                    else:
                        if (int(a*modifier) != int((a-1) * modifier) or a == 0) and (int(b*modifier) != int((b-1)*modifier) or b == 0):
                            pixstring += chr(j)
                else:
                    colourhash = self.palette[j]
                    colour = Color.fromLong(colourhash)
                    colbin = "{0:b}".format(colour.red / 32).zfill(3) + "{0:b}".format(colour.grn / 64).zfill(2) + "{0:b}".format(colour.blu / 64).zfill(2)
                    if oneistone:
                        pixstring += chr(int(colbin, 2))
                    else:
                        if (int(a*modifier) != int((a-1) * modifier) or a == 0) and (int(b*modifier) != int((b-1)*modifier) or b == 0):
                            pixstring += chr(int(colbin, 2))
        for i in range(0, len(pixstring), 8):
            binarystring += '\x09\x80' + pixstring[i:i+8]
        binarystring += '\x01\x81'
        binarystring += '\x00;'
        return base64.b64encode(binarystring)


  def _saveBitMapNoCompression( self, filename ):
    # open file
    f = file( filename, "wb" )

    # write bitmap header
    f.write( "BM" )
    f.write( longToString( 54 + 256*4 + self.ht*self.wd ) )   # DWORD size in bytes of the file
    f.write( longToString( 0 ) )    # DWORD 0
    f.write( longToString( 54 + 256*4 ) )    # DWORD offset to the data
    f.write( longToString( 40 ) )    # DWORD header size = 40
    f.write( longToString( self.wd ) )    # DWORD image width
    f.write( longToString( self.ht ) )    # DWORD image height
    f.write( shortToString( 1 ) )    # WORD planes = 1
    f.write( shortToString( 8 ) )    # WORD bits per pixel = 8
    f.write( longToString( 0 ) )    # DWORD compression = 0
    f.write( longToString( self.wd * self.ht ) )    # DWORD sizeimage = size in bytes of the bitmap = width * height
    f.write( longToString( 0 ) )    # DWORD horiz pixels per meter (?)
    f.write( longToString( 0 ) )    # DWORD ver pixels per meter (?)
    f.write( longToString( 256 ) )    # DWORD number of s used = 256
    f.write( longToString( len(self.palette) ) )    # DWORD number of "import s = len( self.palette )

    # write bitmap palette
    for clr in self.palette:
      f.write( longToString( clr ) )
    for i in range( len(self.palette), 256 ):
      f.write( longToString( 0 ) )

    # write pixels
    for row in self.bitarray:
      for pixel in row:
        f.write( chr( pixel ) )
      padding = ( 4 - len(row) % 4 ) % 4
      for i in range(padding):
        f.write( chr( 0 ) )

    # close file
    f.close()

  def _saveBitMapWithCompression( self, filename ):
    """
    """
    # open file
    f = file( filename, "wb" )

    # write bitmap header
    f.write( "BM" )
    f.write( longToString( 54 + 256*4 + self.ht*self.wd ) )   # DWORD size in bytes of the file
    f.write( longToString( 0 ) )    # DWORD 0
    f.write( longToString( 54 + 256*4 ) )    # DWORD offset to the data
    f.write( longToString( 40 ) )    # DWORD header size = 40
    f.write( longToString( self.wd ) )    # DWORD image width
    f.write( longToString( self.ht ) )    # DWORD image height
    f.write( shortToString( 1 ) )    # WORD planes = 1
    f.write( shortToString( 8 ) )    # WORD bits per pixel = 8
    f.write( longToString( 1 ) )    # DWORD compression = 1=RLE8
    f.write( longToString( self.wd * self.ht ) )    # DWORD sizeimage = size in bytes of the bitmap = width * height
    f.write( longToString( 0 ) )    # DWORD horiz pixels per meter (?)
    f.write( longToString( 0 ) )    # DWORD ver pixels per meter (?)
    f.write( longToString( 256 ) )    # DWORD number of s used = 256
    f.write( longToString( len(self.palette) ) )    # DWORD number of "import s = len( self.palette )

    # write bitmap palette
    for clr in self.palette:
      f.write( longToString( clr ) )
    for i in range( len(self.palette), 256 ):
      f.write( longToString( 0 ) )

    # write pixels
    pixelBytes = 0
    for row in self.bitarray:
      rleStart = 0
      curPixel = rleStart+1
      while curPixel < len(row):
        if row[curPixel] != row[rleStart] or curPixel-rleStart == 255:
          # write out from rleStart thru curPixel-1
          f.write( chr( curPixel-rleStart ) )
          f.write( chr( row[rleStart] ) )
          pixelBytes += 2
          rleStart = curPixel
        else:
          pass
        curPixel += 1

      # write out last run of s
      f.write( chr( curPixel-rleStart ) )
      f.write( chr( row[rleStart] ) )
      pixelBytes += 2

      # end of line code
      f.write( chr(0) )
      f.write( chr(0) )
      pixelBytes += 2

    # end of bitmap code
    f.write( chr(0) )
    f.write( chr(1) )
    pixelBytes += 2

    # now fix sizes in header
    f.seek(2)
    f.write( longToString( 54 + 256*4 + pixelBytes ) )   # DWORD size in bytes of the file
    f.seek(34)
    f.write( longToString( pixelBytes ) )   # DWORD size in bytes of the file

    # close file
    f.close()

  def saveFile( self, filename, compress=True ):
    if compress:
      self._saveBitMapWithCompression( filename )
    else:
      self._saveBitMapNoCompression( filename )



# For converting arttemis colour codes to an RGB value
def artColourTable(x):
    if x == 0:
        y = (255, 255, 255)
    elif x == 1:
        y = (100, 100, 100)
    elif x == 2:
        y = (255, 0, 0)
    elif x == 3:
        y = (0, 255, 0)
    elif x == 4:
        y = (0, 0, 255)
    elif x == 5:
        y = (0, 255, 255)
    elif x == 6:
        y = (255, 0, 255)
    elif x == 7:
        y = (255, 255, 0)
    elif x == 8:
        y = (152, 255, 152)
    elif x == 9:
        y = (135, 206, 250)
    elif x == 10:
        y = (255, 165, 0)
    elif x == 11:
        y = (200, 150, 100)
    elif x == 12:
        y = (255, 200, 200)
    elif x == 13:
        y = (170, 170, 170)
    elif x == 14:
        y = (0, 0, 0)
    elif x == 15:
        y = (255, 63, 63)
    elif x == 16:
        y = (255, 127, 127)
    elif x == 17:
        y = (255, 191, 191)
    return y



# For reading in genbank or EMBL files
def getArrows(filename, legname):
    length = None
    theseq = ''
    genbank = open(filename)
    outlist = []
    getFeats = False
    emblcheck = False
    getColour = False
    getemblseq = False
    getgenseq = False
    getmultifasta = False
    for line in genbank:
        if '\t' in line:
            sys.stderr.write('Tab found in genbank file, this may cause some Features to be missed, please remove tabs.')
        if line.startswith('FEATURES') or line.startswith('     source'):
            getFeats = True
        elif line.startswith('FT'):
            getFeats = True
            emblcheck = True
        elif line.startswith('>') and not getFeats:
            if getmultifasta:
                theseq += 'qqq'
            else:
                getmultifasta = True
        elif getmultifasta:
            theseq += line.rstrip()
        elif not line.startswith(' ') and not emblcheck:
            getFeats = False
        elif emblcheck:
            getFeats = False
        if line[2:].startswith('   ') and line[5] != ' ' and getFeats:
            feat, loc = line[2:].split()
            if 'join(' in loc or 'order(' in loc:
                if loc.startswith('join('):
                    temp2 = loc[5:-1].split(',')
                    strand = '+'
                elif loc.startswith('complement('):
                    temp2 = loc[11:-1].split(',')
                    strand = '-'
                elif loc.startswith('order('):
                    temp2 = loc[6:-1].split(',')
                temp = [[], []]
                gotit = True
                for i in temp2:
                    if ':' in i:
                        i = i.split(':')[1]
                    if '<' in i:
                        i = i.replace('<', '')
                    if '>' in i:
                        i = i.replace('>', '')
                    if ')' in i:
                        i = i.replace(')', '')
                    if i.startswith('complement('):
                        strand = '-'
                        i = i[11:]
                    if i.startswith('join('):
                        i = i[5:]
                    if i.startswith('order('):
                        i = i[6:]
                    if '..' in i:
                        try:
                            start, stop = i.split('..')
                        except:
                            start, stop = 'x', 'y'
                    elif '^' in i:
                        try:
                            start, stop = i.split('^')
                        except:
                            start, stop = 'x', 'y'
                    elif '.' in i:
                        try:
                            start, stop = i.split('.')
                        except:
                            start, stop = 'x', 'y'
                    else:
                        if i.startswith('gap('):
                            start = None
                        else:
                            start = i
                            stop = i
                    try:
                        if start != None:
                            temp[0].append(int(start))
                            temp[1].append(int(stop))
                    except:
                        if gotit:
                            print 'feature could not be processed:\n' + line
                        gotit = False
                if gotit:
                    aninstance = feature(temp[0], temp[1], feat, strand, None, None)
                    outlist.append(aninstance)
                if feat == 'source':
                    try:
                        lengtht = max([max(temp[0]), max(temp[1])])
                        if lengtht > length:
                            length = lengtht
                    except:
                        pass
            else:
                if loc.startswith('complement('):
                    strand = '-'
                    loc = loc[11:-1]
                else:
                    strand = '+'
                if ':' in loc:
                    loc = loc.split(':')[1]
                if '<' in loc:
                    loc = loc.replace('<', '')
                if '>' in loc:
                    loc = loc.replace('>', '')
                if '..' in loc:
                    try:
                        start, stop = loc.split('..')
                    except:
                        start, stop = 'x', 'y'
                elif '^' in loc:
                    try:
                        start, stop = loc.split('^')
                    except:
                        start, stop = 'x', 'y'
                elif '.' in loc:
                    try:
                        start, stop = loc.split('.')
                    except:
                        start, stop = 'x', 'y'
                else:
                    start = loc
                    stop = loc
                try:
                    aninstance = feature(int(start), int(stop), feat, strand, None, None)
                    outlist.append(aninstance)
                except:
                    print 'feature could not be processed:\n' + line
                if feat == 'source':
                    try:
                        lengtht = max([int(start), int(stop)])
                        if lengtht > length:
                            length = lengtht
                    except:
                        pass
        elif line[2:].startswith('                 /colour=') and getFeats:
            temp = line[27:-1]
            temp = temp.replace('"', '')
            temp = temp.replace("'", "")
            artColourF = temp.split()
            try:
                if len(artColourF) == 1:
                    artColour = artColourTable(int(artColourF[0]))
                else:
                    artColour = (int(artColourF[0]), int(artColourF[1]), int(artColourF[2]))
                outlist[-1].colour = artColour
            except:
                print 'Colour could not be processed:\n' + line
        elif line[2:].startswith('                 /color=') and getFeats:
            temp = line[26:-1]
            temp = temp.replace('"', '')
            temp = temp.replace("'", "")
            artColourF = temp.split()
            try:
                if len(artColourF) == 1:
                    artColour = artColourTable(int(artColourF[0]))
                else:
                    artColour = (int(artColourF[0]), int(artColourF[1]), int(artColourF[2]))
                outlist[-1].colour = artColour
            except:
                print 'Colour could not be processed:\n' + line
        elif line[2:].startswith('                   /colour=') and getFeats:
            temp = line[29:-1]
            temp = temp.replace('"', '')
            temp = temp.replace("'", "")
            artColourF = temp.split()
            try:
                if len(artColourF) == 1:
                    artColour = artColourTable(int(artColourF[0]))
                else:
                    artColour = (int(artColourF[0]), int(artColourF[1]), int(artColourF[2]))
                outlist[-1].colour = artColour
            except:
                print 'Colour could not be processed:\n' + line
        elif line[2:].startswith('                   /color=') and getFeats:
            temp = line[28:-1]
            temp = temp.replace('"', '')
            temp = temp.replace("'", "")
            try:
                artColourF = temp.split()
                if len(artColourF) == 1:
                    artColour = artColourTable(int(artColourF[0]))
                else:
                    artColour = (int(artColourF[0]), int(artColourF[1]), int(artColourF[2]))
            except:
                print 'Colour could not be processed:\n' + line
            outlist[-1].colour = artColour
        elif line[2:].startswith('                   /gene=') and getFeats and legname == 'gene':
            outlist[-1].name = line.rstrip()[27:].replace('"', '')
        elif line[2:].startswith('                   /product=') and getFeats and legname == 'product':
            outlist[-1].name = line.rstrip()[30:].replace('"', '')
        elif line[2:].startswith('                   /locus_tag=') and getFeats and legname == 'locus_tag':
            outlist[-1].name = line.rstrip()[32:].replace('"', '')
        elif line[2:].startswith('                   /note=') and getFeats and legname == 'note':
            outlist[-1].name = line.rstrip()[27:].replace('"', '')
        elif line.startswith('ORIGIN') and length == None:
            getgenseq = True
        elif line.startswith('SQ   Sequence ') and length == None:
            getemblseq = True
        elif line.startswith('//'):
            getemblseq = False
            getgenseq = False
            if length == None:
                length = len(theseq)
        elif getemblseq:
            theseq += ''.join(line.split()[:-1])
        elif getgenseq:
            theseq += ''.join(line.split()[1:])
    if getmultifasta:
        insertSize = len(theseq) / 500
        multifastapos = 1
        for i in theseq.split('qqq'):
            aninstance = feature(multifastapos, multifastapos + len(i) - 1, 'contig', '+', None, None)
            outlist.append(aninstance)
            multifastapos += len(i) -1 + insertSize
    theseq = theseq.replace('qqq', 'n' * (len(theseq) / 500))
    if length == None and theseq != '':
        length = len(theseq)
    return length, outlist

# detects whether blast+ is in your path
def isNewBlastDB():
    path = os.environ["PATH"].split(os.pathsep)
    isit = False
    for i in path:
        if os.path.exists(i + '/' + 'makeblastdb.exe') or os.path.exists(i + '/' 'makeblastdb'):
            isit = True
    return isit

def isNewBlastn():
    path = os.environ["PATH"].split(os.pathsep)
    isit = False
    for i in path:
        if os.path.exists(i + '/' + 'blastn.exe') or os.path.exists(i + '/' 'blastn'):
            isit = True
    return isit

def isNewTblastx():
    path = os.environ["PATH"].split(os.pathsep)
    isit = False
    for i in path:
        if os.path.exists(i + '/' + 'tblastx.exe') or os.path.exists(i + '/' 'tblastx'):
            isit = True
    return isit

# detects legacy blast in your path
def isLegBlastDB():
    path = os.environ["PATH"].split(os.pathsep)
    isit = False
    for i in path:
        if os.path.exists(i + '/' + 'formatdb.exe') or os.path.exists(i + '/' 'formatdb'):
            isit = True
    return isit

def isLegBlastall():
    path = os.environ["PATH"].split(os.pathsep)
    isit = False
    for i in path:
        if os.path.exists(i + '/' + 'blastall.exe') or os.path.exists(i + '/' 'blastall'):
            isit = True
    return isit




# gets all blast hits length >minlength and e value < mineval and identity > minident
def getBlast(filename, minlength, mineval, minident):
    if filename == '':
        return []
    blast = open(filename)
    testline = blast.readline()
    try:
        query, subject, ident, length, mismatch, indel, qStart, qEnd, rStart, rEnd, eVal, bitScore = testline.split()
        ident = float(ident)
        length = int(length)
        mismatch = int(mismatch)
        indel = int(indel)
        qStart = int(qStart)
        qEnd = int(qEnd)
        rStart = int(rStart)
        rEnd = int(rEnd)
        eVal = float(eVal)
        bitScore = float(bitScore)
        crunch = False
    except:
        crunch = True
    blast.close()
    blast = open(filename)
    outlist = []
    for line in blast:
        if crunch:
            score, ident, qStart, qEnd, query, rStart, rEnd, subject = line.split()[:8]
            qStart = int(qStart)
            qEnd = int(qEnd)
            eVal = 0
            length = abs(qStart - qEnd)
        else:
            query, subject, ident, length, mismatch, indel, qStart, qEnd, rStart, rEnd, eVal, bitScore = line.split()
            eVal = float(eVal)
        ident = float(ident)
        length = int(length)
        qStart = int(qStart)
        qEnd = int(qEnd)
        rStart = int(rStart)
        rEnd = int(rEnd)
        eVal = float(eVal)
        if length >= minlength and eVal <= mineval and ident >= minident:
            outlist.append((qStart, qEnd, rStart, rEnd, ident))
    return outlist


#draws teh image
def draw(filename, minlength, mineval, minIdent, inputlist, width, height1, height2,
         minblastc, maxblastc, minblastci, maxblastci, drawfig1, drawfig2, drawfig3,
         compress, reverseList, featDict, glt, exont, genet, featlengths, aln,
         graphit, blastoutline, minmaxlist, autodetect, legend, legname, writebmp=0):
    # global variable for stopping script midway
    global abortCaptain
    secondlist = []
    maxlength = 0
    totalheight = 0
    # returning a minident value of 101 means the script has been aborted
    minident = 101
    # gets feature file and blast information
    for i in range(0, len(inputlist)):
        if i % 2 == 0:
            temp = getArrows(inputlist[i], legname)
            thirdlist = []
            if minmaxlist[i/2][1] == 'Max':
                if temp[0] == None:
                    maxcut = featlengths[i/2]
                else:
                    maxcut = temp[0]
                if minmaxlist[i/2][0] == 1:
                    minmaxopt = 0
                else:
                    minmaxopt = 1
                    mincut = minmaxlist[i/2][0]
            else:
                mincut = minmaxlist[i/2][0]
                maxcut = minmaxlist[i/2][1]
                if minmaxlist[i/2][0] < minmaxlist[i/2][1]:
                    minmaxopt = 1
                else:
                    minmaxopt = 2
            for j in temp[1]:
                if j.type in featDict:
                    if j.colour == None:
                        j.colour = featDict[j.type][1]
                    if minmaxopt == 0:
                        thirdlist.append(j)
                    elif minmaxopt == 1:
                        if type(j.start) == int:
                            if j.start >= mincut and j.stop <= maxcut:
                                aninstance = feature(j.start - mincut + 1, j.stop - mincut + 1, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                        else:
                            if j.start[0] >= mincut and j.stop[-1] <= maxcut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                    elif minmaxopt == 2:
                        if temp[0] == None:
                            templength = featlengths[i/2]
                        else:
                            templength = temp[0]
                        if type(j.start) == int:
                            if j.stop <= maxcut:
                                tempstart = j.start + templength - mincut + 1
                                tempstop = j.stop + templength - mincut + 1
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                            elif j.start >= mincut:
                                tempstart = j.start - mincut + 1
                                tempstop = j.stop - mincut + 1
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                        else:
                            if j.stop[-1] <= maxcut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k + templength - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k + templength - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                            elif j.start[0] >= mincut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
            thirdlist.sort(key=lambda ii: ii.length(), reverse=True)
            if minmaxopt == 0:
                if temp[0] == None:
                    secondlist.append((featlengths[i/2], thirdlist))
                    if featlengths[i/2] > maxlength:
                        maxlength = featlengths[i/2]
                else:
                    secondlist.append((temp[0], thirdlist))
                    if temp[0] > maxlength:
                        maxlength = temp[0]
            elif minmaxopt == 1:
                secondlist.append((maxcut - mincut + 1, thirdlist))
                if maxcut - mincut + 1 > maxlength:
                    maxlength = maxcut - mincut + 1
            elif minmaxopt == 2:
                if temp[0] == None:
                    templength = featlengths[i/2]
                else:
                    templength = temp[0]
                secondlist.append((templength - mincut + maxcut + 1, thirdlist))
                if templength - mincut + maxcut + 1 > maxlength:
                    maxlength = templength - mincut + maxlength + 1
            totalheight += height1
        else:
            totalheight += height2
            temp = getBlast(inputlist[i], minlength, mineval, minIdent)
            for j in temp:
                if j[4] < minident:
                    minident = j[4]
            secondlist.append(temp)
    # calculates offsets for genomes if best blast alignment is selected
    if autodetect and maxlength > 100000:
        tempsecond = []
        minident = 101
        for i in range(len(secondlist)):
            temp = []
            if i % 2 == 0:
                for j in secondlist[i][1]:
                    if type(j.start) == int:
                        if (j.stop - j.start) * 1.0/ maxlength * width > 4:
                            temp.append(j)
                    else:
                        if (j.stop[0] - j.start[0]) * 1.0/ maxlength * width > 4:
                            temp.append(j)
                tempsecond.append((secondlist[i][0], temp))
            else:
                for j in secondlist[i]:
                    if (j[1] - j[0]) * 1.0 / maxlength * width > 3:
                        temp.append(j)
                        if j[4] < minident:
                            minident = j[4]
                tempsecond.append(temp)
        secondlist = tempsecond
    if minIdent != 0:
        minident = minIdent
    if aln == 'best blast':
        blastmatch = [0]
        for i in range(1, len(secondlist), 2):
            maxbitscore = 0
            for j in secondlist[i]:
                if j[1] - j[0] > maxbitscore:
                    qstart, qend, rstart, rend = j[0], j[1], j[2], j[3]
                    maxbitscore = j[1] - j[0]
            if len(secondlist[i]) == 0:
                theQstart = 0
            elif reverseList[i/2]:
                theQstart = secondlist[i-1][0] - qend
            else:
                theQstart = qstart
            if reverseList[(i+1)/2]:
                if len(secondlist[i]) == 0:
                    theRstart = 0
                elif rstart < rend:
                    theRstart = secondlist[i+1][0] - rend
                else:
                    theRstart = secondlist[i+1][0] - rstart
            else:
                if len(secondlist[i]) == 0:
                    theRstart = 0
                elif rstart < rend:
                    theRstart = rstart
                else:
                    theRstart = rend
            blastmatch.append(blastmatch[-1] + theQstart - theRstart)
        theminblast = min(blastmatch)
        templist = []
        for i in blastmatch:
            templist.append(i - theminblast)
        blastmatch = templist
        for i in range(0, len(secondlist) + 1, 2):
            if secondlist[i][0] + blastmatch[i/2] > maxlength:
                maxlength = secondlist[i][0] + blastmatch[i/2]
    leghei = 0
    if legend == 'Single column' or legend == 'Two columns':
        legendArrows = set()
        legendList = []
        for i in range(len(secondlist)):
            if i % 2 == 0:
                legendList.append([])
                for j in secondlist[i][1]:
                    if j.name != None and (j.name, j.colour, featDict[j.type][0]) not in legendArrows:
                        legendArrows.add((j.name, j.colour, featDict[j.type][0]))
                        if type(j.start) == int:
                            tempjstart = j.start
                        else:
                            tempjstart = j.start[0]
                        legendList[i/2].append((j.name, j.colour, featDict[j.type][0], tempjstart))
        if legend == 'Single column':
            leghei += min([5000, len(legendArrows) * 90])
        elif legend == 'Two columns':
            leghei = min([5000, (len(legendArrows) + 1) / 2 * 90])
    global shifter
    if legend == 'Top' or legend == 'Top & Bottom':
        toplegpos = [0, 0, 0, set(), set(), set()]
        legendTop = []
        testbmp = BitMap(10, 10)
        if aln == 'best blast':
            shifter = blastmatch[0]
        genrev1 = reverseList[0]
        for j in secondlist[0][1]:
            if j.name != None:
                if type(j.start) == int:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:                        
                        legpos = convertPosR(secondlist[0][0], maxlength, width, (j.start + j.stop)/2, aln)
                    else:
                        legpos = convertPos(secondlist[0][0], maxlength, width, (j.start + j.stop)/2, aln)
                    for q in range(legpos  - 40, legpos + 50):
                        if q in toplegpos[3]:
                            firstleg = False
                        if q in toplegpos[4]:
                            secondleg = False
                        if q in toplegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[0]:
                            toplegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            toplegpos[3].add(q)
#                    elif secondleg:
#                        therung = 2
#                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[1]:
#                            toplegpos[1] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            toplegpos[4].add(q)
#                    elif thirdleg:
#                        therung = 3
#                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[2]:
#                            toplegpos[2] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            toplegpos[5].add(q)
                    else:
                        therung = None
                    legendTop.append((j.name[:10], legpos, therung))
                else:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[0][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    else:
                        legpos = convertPos(secondlist[0][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    for q in range(legpos - 40, legpos + 50):
                        if q in toplegpos[3]:
                            firstleg = False
                        if q in toplegpos[4]:
                            secondleg = False
                        if q in toplegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[0]:
                            toplegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            toplegpos[3].add(q)
#                    elif secondleg:
#                        therung = 2
#                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[1]:
#                            toplegpos[1] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            toplegpos[4].add(q)
#                    elif thirdleg:
#                        therung = 3
#                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[2]:
#                            toplegpos[2] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            toplegpos[5].add(q)
                    else:
                        therung = None
                    legendTop.append((j.name[:10], legpos, therung))
        totalheight += sum(toplegpos[:3]) + 40
    if legend == 'Bottom' or legend == 'Top & Bottom':
        botlegpos = [0, 0, 0, set(), set(), set()]
        legendBot = []
        testbmp = BitMap(10, 10)
        if aln == 'best blast':
            shifter = blastmatch[-1]
        genrev1 = reverseList[-1]
        for j in secondlist[-1][1]:
            if j.name != None:
                if type(j.start) == int:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:                        
                        legpos = convertPosR(secondlist[-1][0], maxlength, width, (j.start + j.stop)/2, aln)
                    else:
                        legpos = convertPos(secondlist[-1][0], maxlength, width, (j.start + j.stop)/2, aln)
                    for q in range(legpos - 40, legpos + 50):
                        if q in botlegpos[3]:
                            firstleg = False
                        if q in botlegpos[4]:
                            secondleg = False
                        if q in botlegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[0]:
                            botlegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            botlegpos[3].add(q)
#                    elif secondleg:
#                        therung = 2
#                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[1]:
#                            botlegpos[1] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            botlegpos[4].add(q)
#                    elif thirdleg:
#                        therung = 3
#                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[2]:
#                            botlegpos[2] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range(legpos - 40, legpos + 50):
#                            botlegpos[5].add(q)
                    else:
                        therung = None
                    legendBot.append((j.name[:10], legpos, therung))
                else:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[-1][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    else:
                        legpos = convertPos(secondlist[-1][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
                        if q in botlegpos[3]:
                            firstleg = False
                        if q in botlegpos[4]:
                            secondleg = False
                        if q in botlegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[0]:
                            botlegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
                            botlegpos[3].add(q)
#                    elif secondleg:
#                        therung = 2
#                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[1]:
#                            botlegpos[1] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
#                            botlegpos[4].add(q)
#                    elif thirdleg:
#                        therung = 3
#                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[2]:
#                            botlegpos[2] = testbmp.lengthString(j.name[:10], 64)
#                        for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
#                            botlegpos[5].add(q)
                    else:
                        therung = None
                    legendBot.append((j.name[:10], (j.start[0] + j.stop[0])/2, therung))
        totalheight += sum(botlegpos[:3]) + 40
    # creates extra width for blast identity legend
    drawfig1hei = 0
    if drawfig1 and minident != 101:
        drawfig1hei = 500
    extraheight = 0
    # creates extra height for scale legend
    drawfig2hei = 0
    if drawfig2:
        drawfig2hei = height1 + 70
    # creates extra height for graph
    totalheight += max([leghei, drawfig1hei, drawfig2hei])
    hei = totalheight
    if graphit != None:
        hei += graphit[3] * len(graphit[0]) + 2 * graphit[7] * len(graphit[0])
        extraheight = (graphit[3] + 20) * len(graphit[0])
    bmp = BitMap(width, hei + 1)
    # draws the scale figure
    columnhei = max([leghei, drawfig1hei, drawfig2hei])
    if legend == 'Single column':
        index = 0
        legendArrows = []
        for i in range(len(legendList)):
            x = legendList[i]
            x.sort(key=operator.itemgetter(3))
            if reverseList[i]:
                x.reverse()
            legendArrows += x
        for i in range(columnhei - 74, 10, -90):
         #   print len(legendArrows), legendArrows[index][2]
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawOutRect(5, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'arrow':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightArrow(5, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'frame':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightFrame(5, i - 48, 96, 128, genet, 1)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'pointer':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawPointer(34, i, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0], 106, i, 64)
            else:
                print 'wang'
            index += 1
    elif legend == 'Two columns':
        index = 0
        legendArrows = []
        for i in range(len(legendList)):
            x = legendList[i]
            x.sort(key=operator.itemgetter(3))
            if reverseList[i]:
                x.reverse()
            legendArrows += x
        for i in range(columnhei - 74, 10, -90):
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawOutRect(5, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'arrow':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightArrow(5, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'frame':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightFrame(5, i - 48, 96, 128, genet, 1)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'pointer':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawPointer(34, i, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106, i, 64)
            index += 1
        for i in range(columnhei - 74, 10, -90):
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawOutRect(5 + width/3, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and  legendArrows[index][2] == 'arrow':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightArrow(5 + width/3, i, 96, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and  legendArrows[index][2] == 'frame':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawRightFrame(5 + width/3, i - 48, 96, 128, genet, 1)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and  legendArrows[index][2] == 'pointer':
                theColor = Color(legendArrows[index][1][0], legendArrows[index][1][1], legendArrows[index][1][2])
                bmp.setPenColor(theColor)
                bmp.drawPointer(34 + width/3, i, 64, genet)
                bmp.setPenColor(Color.BLACK)
                bmp.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            index += 1
    if legend == 'Top' or legend == 'Top & Bottom':
        rung1 = totalheight - sum(toplegpos[:3]) - 30
        rung2 = rung1 + toplegpos[0] + 10
        rung3 = rung2 + toplegpos[1] + 10
        for i in legendTop:
            if i[0][0].lower() == i[0][0]:
                xpos = i[1] + 24
            else:
                xpos = i[1] + 32
            if i[2] == 1:
                bmp.writeString(i[0], xpos, rung1, 64, False, False, 1)
            elif i[2] == 2:
                bmp.writeString(i[0], xpos, rung2, 64, False, False, 1)
            elif i[2] == 3:
                bmp.writeString(i[0], xpos, rung3, 64, False, False, 1)

    if legend == 'Bottom' or legend == 'Top & Bottom':
        rung1 = sum(botlegpos[:3]) + 30 + columnhei
        rung2 = rung1 - botlegpos[0] - 10
        rung3 = rung2 - botlegpos[1] - 10
        for i in legendBot:
            if i[0][-1].lower() == i[0][-1]:
                xpos = i[1] + 24
            else:
                xpos = i[1] + 32
            if i[2] == 1:
                bmp.writeString(i[0], xpos, rung1, 64, False, False, 1, 'right')
            elif i[2] == 2:
                bmp.writeString(i[0], xpos, rung2, 64, False, False, 1, 'right')
            elif i[2] == 3:
                bmp.writeString(i[0], xpos, rung3, 64, False, False, 1, 'right')
    if drawfig2 != False:
        bmp.setPenColor(Color.BLACK)
        x1 = width - 600 - drawfig2 * 1.0 / maxlength * width
        x2 = width - 600
        bmp.drawLine(x1, columnhei - height1/2 - 74, x2, columnhei - height1/2 - 74)
        bmp.drawLine(x1, columnhei - height1/2-1 - 74, x2, columnhei - height1/2-1 - 74)
        bmp.drawLine(x1, columnhei - height1/2+1 - 74, x2, columnhei - height1/2+1 - 74)
        bmp.drawLine(x1-1, columnhei - height1 /4 - 74, x1-1, columnhei - height1 /4 * 3 - 74)
        bmp.drawLine(x1+1, columnhei - height1 /4 - 74, x1+1, columnhei - height1 /4 * 3 - 74)
        bmp.drawLine(x1, columnhei - height1 /4 - 74, x1, columnhei - height1 /4 * 3 - 74)
        bmp.drawLine(x2, columnhei - height1 /4 - 74, x2, columnhei - height1 /4 * 3 - 74)
        bmp.drawLine(x2+1, columnhei - height1 /4 - 74, x2+1, columnhei - height1 /4 * 3 - 74)
        bmp.drawLine(x2-1, columnhei - height1 /4 - 74, x2-1, columnhei - height1 /4 * 3 - 74)
        strfig2 = str(drawfig2)
        if strfig2[-6:] == '000000':
            strfig2 = strfig2[:-6] + ' Mbp'
        elif strfig2[-3:] == '000':
            strfig2 = strfig2[:-3] + ' Kbp'
        testbmp = BitMap(10, 10)
        bmp.writeString(strfig2, (x1 + x2)/2 - testbmp.lengthString(strfig2, 64)/2, columnhei - height1 /4 - 59, 64)
    # draws the graph
    if graphit != None:
        thearray, maxgc, mingc, gheight, glinet, gtype, gmaxy, ggap = graphit
        widthpixellist = []
        leftpixellist = []
        rightpixellist = []
        for i in range(len(thearray)):
            if aln == 'best blast':
                shifter = blastmatch[i]
            if reverseList[i]:
                rightpixel = convertPosR(secondlist[i*2][0], maxlength, width, 0, aln)
                leftpixel = convertPosR(secondlist[i*2][0], maxlength, width, secondlist[i*2][0], aln)
                thearray[i].reverse()
            else:
                leftpixel = convertPos(secondlist[i*2][0], maxlength, width, 0, aln)
                rightpixel = convertPos(secondlist[i*2][0], maxlength, width, secondlist[i*2][0], aln)

            widthpixel = rightpixel - leftpixel + 1
            widthpixellist.append(widthpixel)
            leftpixellist.append(leftpixel)
            rightpixellist.append(rightpixel)
        neg = False
        if gmaxy == 'Auto':
            gmaxy = 0
            for i in range(0, len(thearray)):
                if min(thearray[i]) < 0:
                    neg = True
                for j in range(0, widthpixellist[i]):
                    aa = int(j * (len(thearray[i]) * 1.0 / widthpixellist[i]))
                    bb = int((j + 1) * (len(thearray[i]) * 1.0/ widthpixellist[i]))
                    if aa == bb:
                        bb += 1
                    temparr = thearray[i][aa:bb]
                    gyval = abs(sum(temparr) * 1.0 / len(temparr))
                    if gyval > gmaxy:
                        gmaxy = gyval
        else:
            gmaxy = float(gmaxy)
            for i in range(0, len(thearray)):
                if min(thearray[i]) < 0:
                    neg = True
        if neg:
            axispos = hei - ggap - gheight/2 - glinet/2
        else:
            axispos = hei - ggap - gheight - glinet
        gc1, gc2, gc3 = maxgc
        maxgcColour = Color(gc1, gc2, gc3)
        bmp.setPenColor(maxgcColour)
        gc1, gc2, gc3 = mingc
        mingcColour = Color(gc1, gc2, gc3)
        for qq in range(len(thearray)):
            bmp.setPenColor(Color.BLACK)
            lastgypos = None
            for i in range(axispos, axispos + glinet):
                bmp.drawLine(leftpixellist[qq], i, rightpixellist[qq], i)
            bmp.setPenColor(maxgcColour)
            for i in range(0, widthpixellist[qq]):
                aa = int(i * (len(thearray[qq]) * 1.0 / widthpixellist[qq]))
                bb = int((i + 1) * (len(thearray[qq]) * 1.0/ widthpixellist[qq]))
                if aa == bb:
                    bb += 1
                temparr = thearray[qq][aa:bb]
                gyval = sum(temparr) * 1.0 / len(temparr)
                yvalpixratio = gyval/gmaxy
                if yvalpixratio > 1:
                    yvalpixratio = 1
                if yvalpixratio < -1:
                    yvalpixratio = -1
                if neg:
                    if yvalpixratio < 0:
                        gc1, gc2, gc3 = mingc
                        bmp.setPenColor(mingcColour)
                        yvalpix = round(yvalpixratio *  (gheight /2 - glinet/2))
                        if gtype == 'Line':
                            if lastgypos != None:
                                bmp.drawLine(leftpixellist[qq] + i-1, lastgypos, leftpixellist[qq] + i, axispos + yvalpix)
                            lastgypos = axispos + yvalpix
                        elif gtype == 'Histogram':
                            bmp.drawLine(leftpixellist[qq] + i, axispos -1, leftpixellist[qq] + i, axispos + yvalpix)
                    else:
                        gc1, gc2, gc3 = maxgc
                        yvalpix = round(yvalpixratio * (gheight /2 - (glinet - glinet/2)))
                        bmp.setPenColor(maxgcColour)
                        if gtype == 'Line':
                            if lastgypos != None:
                                bmp.drawLine(leftpixellist[qq] + i-1, lastgypos, leftpixellist[qq] + i, axispos + glinet + yvalpix)
                            lastgypos = axispos + glinet + yvalpix
                        elif gtype == 'Histogram' and round(yvalpix) != 0.0:
                            bmp.drawLine(leftpixellist[qq] + i, axispos + glinet, leftpixellist[qq] + i, axispos + yvalpix)
                else:
                    yvalpix = round(yvalpixratio * (gheight - glinet))
                    if gtype == 'Line':
                        if lastgypos != None:
                            bmp.drawLine(leftpixellist[qq] + i-1, lastgypos, i, leftpixellist[qq] + axispos + glinet + yvalpix)
                        lastgypos = axispos + glinet + 1 + yvalpix
                    elif gtype == 'Histogram' and round(yvalpix) != 0.0:
                        bmp.drawLine(leftpixellist[qq] + i, axispos + glinet , leftpixellist[qq] + i, axispos + glinet + yvalpix)
            axispos -= gheight + 2 * ggap + height1 + height2
        modfig1 = (graphit[3] + 2 * ggap) * len(graphit[0])
    else:
        modfig1 = 0
    # draws the blast gradient legend
    if drawfig1 and minident != 101:
        bmp.setPenColor(Color.BLACK)
        bmp.writeString(str(int(round(minident))) + '%', width - 300, columnhei - 480, 64)
        bmp.writeString('100%', width - 300, columnhei - 84, 64)
        for i in range(columnhei - 480, columnhei - 20):
            ratio = round((i - (columnhei - 480) * 1.0) / 460, 2)
            r1 = int(minblastc[0] * (1 - ratio) + maxblastc[0] * ratio)
            r2 = int(minblastc[1] * (1 - ratio) + maxblastc[1] * ratio)
            r3 = int(minblastc[2] * (1 - ratio) + maxblastc[2] * ratio)
            theColor = Color(r1, r2, r3)
            bmp.setPenColor(theColor)
            bmp.drawLine(width - 400, i, width - 360, i)
            r1 = int(minblastci[0] * (1 - ratio) + maxblastci[0] * ratio)
            r2 = int(minblastci[1] * (1 - ratio) + maxblastci[1] * ratio)
            r3 = int(minblastci[2] * (1 - ratio) + maxblastci[2] * ratio)
            theColor = Color(r1, r2, r3)
            bmp.setPenColor(theColor)
            bmp.drawLine(width - 360, i, width - 320, i)
    # draws feature and blast figures
    for i in range(0, len(secondlist)):
        # draws the blast figure
        if i % 2 == 0:
            if aln == 'best blast':
                shifter = blastmatch[i/2]
            genrev1 = reverseList[i/2]
            ymod = totalheight - (height1 * i/2 + height2 * i/2) - height1
            if graphit != None and len(thearray) > 1:
                ymod += (gheight + 2 * ggap) * (len(thearray) - i/2 - 1)
            if legend == 'Top' or legend == 'Top & Bottom':
                ymod -= sum(toplegpos[:3]) + 40
            length = secondlist[i][0]
            bmp.setPenColor(Color.BLACK)
            jj = height1 / 2 + glt / 2
            for j in range(glt):
                bmp.drawLine(convertPos(length, maxlength, width, 0, aln), (ymod +jj),
                             convertPos(length, maxlength, width, length, aln), (ymod + jj))
                jj -= 1
            bmp.setPenColor(Color.RED)
            for j in secondlist[i][1]:
                if abortCaptain:
                    return None
                if (j.strand == '+' and not genrev1) or (j.strand == '-' and genrev1):
                    theColor = Color(j.colour[0], j.colour[1], j.colour[2])
                    bmp.setPenColor(theColor)
                    if type(j.start) == int:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start, aln)
                            x1 = convertPosR(length, maxlength, width, j.stop, aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start, aln)
                            x2 = convertPos(length, maxlength, width, j.stop, aln)
                        if featDict[j.type][0] == 'rect':
                            bmp.drawOutRect(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'arrow':
                            bmp.drawRightArrow(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'frame':
                            bmp.drawRightFrame(x1, ymod, x2-x1, height1, genet, j.start % 3)
                        elif featDict[j.type][0] == 'pointer':
                            bmp.drawPointer(x1, ymod, height1, genet)
                    else:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start[-1], aln)
                            x1 = convertPosR(length, maxlength, width, j.stop[-1], aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start[-1], aln)
                            x2 = convertPos(length, maxlength, width, j.stop[-1], aln)
                        if featDict[j.type][0] == 'rect':
                            bmp.drawOutRect(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'arrow':
                            bmp.drawRightArrow(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'frame':
                            bmp.drawRightFrame(x1, ymod, x2-x1, height1, genet, j.start[-1] % 3)
                        elif featDict[j.type][0] == 'pointer':
                            bmp.drawPointer(x1, ymod, height1, genet)
                        for k in range(2, len(j.start) + 1):
                            if genrev1:
                                x4 = convertPosR(length, maxlength, width, j.start[-k], aln)
                                x3 = convertPosR(length, maxlength, width, j.stop[-k], aln)
                            else:
                                x3 = convertPos(length, maxlength, width, j.start[-k], aln)
                                x4 = convertPos(length, maxlength, width, j.stop[-k], aln)
                            if featDict[j.type][0] == 'arrow' or featDict[j.type][0] == 'rect':
                                if x1 - x4 > 2:
                                    bmp.setPenColor(Color.BLACK)
                                    bmp.drawDash(x4, ymod + 3*height1/4, x4, ymod + height1, exont)
                                    bmp.drawDash(x4, ymod + height1, x1, ymod + height1, exont)
                                    bmp.drawDash(x1, ymod + height1, x1, ymod + 3*height1/4, exont)
                                    bmp.setPenColor(theColor)
                                bmp.drawOutRect(x3, ymod + height1/4, x4-x3, height1/2, genet)
                            elif featDict[j.type][0] == 'frame':
                                if x1 - x4 > 2:
                                    bmp.setPenColor(Color.BLACK)
                                    bmp.drawDash(x4, ymod + 3*height1/4, x4, ymod + height1, exont)
                                    bmp.drawDash(x4, ymod + height1, x1, ymod + height1, exont)
                                    bmp.drawDash(x1, ymod + height1, x1, ymod + 3*height1/4, exont)
                                    bmp.setPenColor(theColor)
                                bmp.drawRightFrameRect(x3, ymod, x4-x3, height1, genet, j.start[-k] % 3)
                            x1, x2 = x3, x4
                else:
                    theColor = Color(j.colour[0], j.colour[1], j.colour[2])
                    bmp.setPenColor(theColor)
                    if type(j.start) == int:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start, aln)
                            x1 = convertPosR(length, maxlength, width, j.stop, aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start, aln)
                            x2 = convertPos(length, maxlength, width, j.stop, aln)
                        if featDict[j.type][0] == 'rect':
                            bmp.drawOutRect(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'arrow':
                            bmp.drawLeftArrow(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'frame':
                            bmp.drawLeftFrame(x1, ymod, x2-x1, height1, genet, j.stop%3)
                        elif featDict[j.type][0] == 'pointer':
                            bmp.drawPointer(x2, ymod, height1, genet)
                    else:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start[0], aln)
                            x1 = convertPosR(length, maxlength, width, j.stop[0], aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start[0], aln)
                            x2 = convertPos(length, maxlength, width, j.stop[0], aln)
                        if featDict[j.type][0] == 'rect':
                            bmp.drawOutRect(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'arrow':
                            bmp.drawLeftArrow(x1, ymod, x2-x1, height1, genet)
                        elif featDict[j.type][0] == 'frame':
                            bmp.drawLeftFrame(x1, ymod, x2-x1, height1, genet, j.stop[0] % 3)
                        elif featDict[j.type][0] == 'pointer':
                            bmp.drawPointer(x2, ymod, height1, genet)
                        for k in range(1, len(j.start)):
                            if genrev1:
                                x4 = convertPosR(length, maxlength, width, j.start[k], aln)
                                x3 = convertPosR(length, maxlength, width, j.stop[k], aln)
                            else:
                                x3 = convertPos(length, maxlength, width, j.start[k], aln)
                                x4 = convertPos(length, maxlength, width, j.stop[k], aln)
                            if featDict[j.type][0] == 'rect' or featDict[j.type][0] == 'arrow':
                                if x3 - x2 > 2:
                                    bmp.setPenColor(Color.BLACK)
                                    bmp.drawDash(x2, ymod + 3*height1/4, x2, ymod + height1, exont)
                                    bmp.drawDash(x2, ymod + height1, x3, ymod + height1, exont)
                                    bmp.drawDash(x3, ymod + height1, x3, ymod + 3*height1/4, exont)
                                    bmp.setPenColor(theColor)
                                bmp.drawOutRect(x3, ymod + height1/4, x4-x3, height1/2, genet)
                            elif featDict[j.type][0] == 'frame':
                                if x3 - x2 > 2:
                                    bmp.setPenColor(Color.BLACK)
                                    bmp.drawDash(x2, ymod + height1/4, x2, ymod, exont)
                                    bmp.drawDash(x2, ymod, x3, ymod, exont)
                                    bmp.drawDash(x3, ymod, x3, ymod + height1/4, exont)
                                    bmp.setPenColor(theColor)
                                bmp.drawLeftFrameRect(x3, ymod, x4-x3, height1, genet, j.stop[k] % 3)
                            x1, x2 = x3, x4
        else:
            # draws teh blast hits
            genrev2 = reverseList[(i+1)/2]
            length1 = secondlist[i-1][0]
            length2 = secondlist[i+1][0]
            ymod = totalheight - (height1 * (i - 1)/2 + height2 * (i - 1)/2) - height1 - 1
            if graphit != None and len(thearray) > 1:
                ymod += (gheight + 2 * ggap) * (len(thearray) - i/2 - 1)
            if legend == 'Top' or legend == 'Top & Bottom':
                ymod -= sum(toplegpos[:3]) + 40
            y1 = ymod
            y2 = y1 - height2 + 1
            for j in secondlist[i]:
                if abortCaptain:
                    return None
                qStart, qEnd, rStart, rEnd, ident = j
                # is the blast hit inverted
                if (rStart < rEnd and not genrev1 and not genrev2) or \
                   (rStart > rEnd and not genrev1 and genrev2) or \
                   (rStart < rEnd and genrev1 and genrev2) or \
                   (rStart > rEnd and genrev1 and not genrev2):
                    crisscross = False
                else:
                    crisscross = True
                try:
                    ratio = round((ident - minident) / (100 - minident), 2)
                except:
                    ratio = 1
                if crisscross:
                    r1 = int(minblastci[0] * (1 - ratio) + maxblastci[0] * ratio)
                    r2 = int(minblastci[1] * (1 - ratio) + maxblastci[1] * ratio)
                    r3 = int(minblastci[2] * (1 - ratio) + maxblastci[2] * ratio)
                else:
                    r1 = int(minblastc[0] * (1 - ratio) + maxblastc[0] * ratio)
                    r2 = int(minblastc[1] * (1 - ratio) + maxblastc[1] * ratio)
                    r3 = int(minblastc[2] * (1 - ratio) + maxblastc[2] * ratio)
                theColor = Color(r1, r2, r3)
                bmp.setPenColor(theColor)
                if aln == 'best blast':
                    shifter = blastmatch[i/2]
                if genrev1:
                    x1e = convertPosR(length1, maxlength, width, qStart, aln)
                    x1s = convertPosR(length1, maxlength, width, qEnd, aln)
                else:
                    x1s = convertPos(length1, maxlength, width, qStart, aln)
                    x1e = convertPos(length1, maxlength, width, qEnd, aln)
                if aln == 'best blast':
                    shifter = blastmatch[(i+1)/2]
                if genrev2 and rStart < rEnd:
                    x2e = convertPosR(length2, maxlength, width, rStart, aln)
                    x2s = convertPosR(length2, maxlength, width, rEnd, aln)
                elif genrev2 and rStart >= rEnd:
                    x2s = convertPosR(length2, maxlength, width, rStart, aln)
                    x2e = convertPosR(length2, maxlength, width, rEnd, aln)
                elif not genrev2 and rStart < rEnd:
                    x2s = convertPos(length2, maxlength, width, rStart, aln)
                    x2e = convertPos(length2, maxlength, width, rEnd, aln)
                else:
                    x2e = convertPos(length2, maxlength, width, rStart, aln)
                    x2s = convertPos(length2, maxlength, width, rEnd, aln)
                if crisscross:
                    if x1e - x1s >= x2e - x2s:
                        for k in range(x1s, x1e):
                            try:
                                x2 = x2e - (k - x1s) * 1.0 / (x1e - x1s) * (x2e - x2s)
                                bmp.drawLine(k, y1, x2, y2)
                            except:
                                pass
                    else:
                        for k in range(x2s, x2e):
                            x1 = x1e - (k - x2s) * 1.0 / (x2e - x2s) * (x1e - x1s)
                            bmp.drawLine(x1, y1, k, y2)
                    if blastoutline:
                        bmp.setPenColor(Color.BLACK)
                    bmp.drawLine(x1s, y1, x2e, y2)
                    bmp.drawLine(x1e, y1, x2s, y2)
                else:
                    if x1e - x1s >= x2e - x2s:
                        for k in range(x1s, x1e):
                            try:
                                x2 = (k - x1s) * 1.0 / (x1e - x1s) * (x2e - x2s) + x2s
                                bmp.drawLine(k, y1, x2, y2)
                                bmp.drawLine(k+1, y1, x2, y2)
                            except:
                                pass
                    else:
                        for k in range(x2s, x2e):
                            x1 = (k - x2s) * 1.0 / (x2e - x2s) * (x1e - x1s) + x1s
                            bmp.drawLine(x1, y1, k, y2)
                            bmp.drawLine(x1, y1, k+1, y2)
                    if blastoutline:
                        bmp.setPenColor(Color.BLACK)
                    bmp.drawLine(x1s, y1, x2s, y2)
                    bmp.drawLine(x1e, y1, x2e, y2)
    if writebmp == 0:
        bmp.saveFile(filename, compress)
        return minident
    elif writebmp == 1:
        return bmp.createGIFString(True), minident, bmp.wd, bmp.ht
    elif writebmp == 2:
        return bmp.createGIFString(False), minident, bmp.wd, bmp.ht

def drawsvg(filename, minlength, mineval, minIdent, inputlist, width, height1, height2,
         minblastc, maxblastc, minblastci, maxblastci, drawfig1, drawfig2, drawfig3,
         compress, reverseList, featDict, glt, exont, genet, featlengths, aln,
         graphit, blastoutline, minmaxlist, autodetect, legend, legname):
    # global variable for stopping script midway
    global abortCaptain
    secondlist = []
    maxlength = 0
    totalheight = 0
    # returning a minident value of 101 means the script has been aborted
    minident = 101
    # gets feature file and blast information
    for i in range(0, len(inputlist)):
        if i % 2 == 0:
            temp = getArrows(inputlist[i], legname)
            thirdlist = []
            if minmaxlist[i/2][1] == 'Max':
                if temp[0] == None:
                    maxcut = featlengths[i/2]
                else:
                    maxcut = temp[0]
                if minmaxlist[i/2][0] == 1:
                    minmaxopt = 0
                else:
                    minmaxopt = 1
                    mincut = minmaxlist[i/2][0]
            else:
                mincut = minmaxlist[i/2][0]
                maxcut = minmaxlist[i/2][1]
                if minmaxlist[i/2][0] < minmaxlist[i/2][1]:
                    minmaxopt = 1
                else:
                    minmaxopt = 2
            for j in temp[1]:
                if j.type in featDict:
                    if j.colour == None:
                        j.colour = featDict[j.type][1]
                    if minmaxopt == 0:
                        thirdlist.append(j)
                    elif minmaxopt == 1:
                        if type(j.start) == int:
                            if j.start >= mincut and j.stop <= maxcut:
                                aninstance = feature(j.start - mincut + 1, j.stop - mincut + 1, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                        else:
                            if j.start[0] >= mincut and j.stop[-1] <= maxcut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                    elif minmaxopt == 2:
                        if temp[0] == None:
                            templength = featlength[i/2]
                        else:
                            templength = temp[0]
                        if type(j.start) == int:
                            if j.stop <= maxcut:
                                tempstart = j.start + templength - mincut + 1
                                tempstop = j.stop + templength - mincut + 1
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                            elif j.start >= mincut:
                                tempstart = j.start - mincut + 1
                                tempstop = j.stop - mincut + 1
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                        else:
                            if j.stop[-1] <= maxcut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k + templength - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k + templength - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
                            elif j.start[0] >= mincut:
                                tempstart = []
                                for k in j.start:
                                    tempstart.append(k - mincut + 1)
                                tempstop = []
                                for k in j.stop:
                                    tempstop.append(k - mincut + 1)
                                aninstance = feature(tempstart, tempstop, j.type, j.strand, j.colour, j.name)
                                thirdlist.append(aninstance)
            thirdlist.sort(key=lambda i: i.length(), reverse=True)
            if minmaxopt == 0:
                if temp[0] == None:
                    secondlist.append((featlengths[i/2], thirdlist))
                    if featlengths[i/2] > maxlength:
                        maxlength = featlengths[i/2]
                else:
                    secondlist.append((temp[0], thirdlist))
                    if temp[0] >= maxlength:
                        maxlength = temp[0]
            elif minmaxopt == 1:
                if maxcut == 'Max':
                    maxcut = temp[0]
                secondlist.append((maxcut - mincut + 1, thirdlist))
                if maxcut - mincut + 1 > maxlength:
                    maxlength = maxcut - mincut + 1
            elif minmaxopt == 2:
                if temp[0] == None:
                    templength = featlengths[i/2]
                else:
                    templength = temp[0]
                secondlist.append((templength - mincut + maxcut + 1, thirdlist))
                if templength - mincut + maxcut + 1 > maxlength:
                    maxlength = templength - mincut + maxlength + 1
            totalheight += height1
        else:
            totalheight += height2
            temp = getBlast(inputlist[i], minlength, mineval, minIdent)
            for j in temp:
                if j[4] < minident:
                    minident = j[4]
            secondlist.append(temp)
    # calculates offsets for genomes if best blast alignment is selected
    if autodetect and maxlength > 100000:
        tempsecond = []
        minident = 101
        for i in range(len(secondlist)):
            temp = []
            if i % 2 == 0:
                for j in secondlist[i][1]:
                    if type(j.start) == int:
                        if (j.stop - j.start) * 1.0/ maxlength * width > 4:
                            temp.append(j)
                    else:
                        if (j.stop[0] - j.start[0]) * 1.0/ maxlength * width > 4:
                            temp.append(j)
                tempsecond.append((secondlist[i][0], temp))
            else:
                for j in secondlist[i]:
                    if (j[1] - j[0]) * 1.0 / maxlength * width > 3:
                        temp.append(j)
                        if j[4] < minident:
                            minident = j[4]
                tempsecond.append(temp)
        secondlist = tempsecond
    if minIdent != 0:
        minident = minIdent
    if aln == 'best blast':
        blastmatch = [0]
        for i in range(1, len(secondlist), 2):
            maxbitscore = 0
            for j in secondlist[i]:
                if j[1] - j[0] > maxbitscore:
                    qstart, qend, rstart, rend = j[0], j[1], j[2], j[3]
                    maxbitscore = j[1] - j[0]
            if len(secondlist[i]) == 0:
                theQstart = 0
            elif reverseList[i/2]:
                theQstart = secondlist[i-1][0] - qend
            else:
                theQstart = qstart
            if reverseList[(i+1)/2]:
                if len(secondlist[i]) == 0:
                    theRstart = 0
                elif rstart < rend:
                    theRstart = secondlist[i+1][0] - rend
                else:
                    theRstart = secondlist[i+1][0] - rstart
            else:
                if len(secondlist[i]) == 0:
                    theRstart = 0
                elif rstart < rend:
                    theRstart = rstart
                else:
                    theRstart = rend
            blastmatch.append(blastmatch[-1] + theQstart - theRstart)
        theminblast = min(blastmatch)
        templist = []
        for i in blastmatch:
            templist.append(i - theminblast)
        blastmatch = templist
        for i in range(0, len(secondlist) + 1, 2):
            if secondlist[i][0] + blastmatch[i/2] > maxlength:
                maxlength = secondlist[i][0] + blastmatch[i/2]
    fighei = 0
    if legend == 'Single column' or legend == 'Two columns':
        legendArrows = set()
        legendList = []
        for i in range(len(secondlist)):
            if i % 2 == 0:
                legendList.append([])
                for j in secondlist[i][1]:
                    if j.name != None and (j.name, j.colour, featDict[j.type][0]) not in legendArrows:
                        legendArrows.add((j.name, j.colour, featDict[j.type][0]))
                        if type(j.start) == int:
                            tempjstart = j.start
                        else:
                            tempjstart = j.start[0]
                        legendList[i/2].append((j.name, j.colour, featDict[j.type][0], tempjstart))
        if legend == 'Single column':
            fighei = min([5000, len(legendArrows) * 90])
        elif legend == 'Two columns':
            fighei = min([5000, (len(legendArrows) + 1) / 2 * 90])
    global shifter
    if legend == 'Top' or legend == 'Top & Bottom':
        toplegpos = [0, 0, 0, set(), set(), set()]
        legendTop = []
        testbmp = BitMap(10, 10)
        if aln == 'best blast':
            shifter = blastmatch[0]
        genrev1 = reverseList[0]
        for j in secondlist[0][1]:
            if j.name != None:
                if type(j.start) == int:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[0][0], maxlength, width, (j.start + j.stop)/2, aln)
                    else:
                        legpos = convertPos(secondlist[0][0], maxlength, width, (j.start + j.stop)/2, aln)
                    for q in range(legpos  - 40, legpos + 50):
                        if q in toplegpos[3]:
                            firstleg = False
                        if q in toplegpos[4]:
                            secondleg = False
                        if q in toplegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[0]:
                            toplegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            toplegpos[3].add(q)
    #                elif secondleg:
    #                    therung = 2
    #                    if testbmp.lengthString(j.name[:10], 64) > toplegpos[1]:
    #                        toplegpos[1] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        toplegpos[4].add(q)
    #                elif thirdleg:
    #                    therung = 3
    #                    if testbmp.lengthString(j.name[:10], 64) > toplegpos[2]:
    #                        toplegpos[2] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        toplegpos[5].add(q)
                    else:
                        therung = None
                    legendTop.append((j.name[:10], legpos, therung))
                else:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[0][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    else:
                        legpos = convertPos(secondlist[0][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    for q in range(legpos - 40, legpos + 50):
                        if q in toplegpos[3]:
                            firstleg = False
                        if q in toplegpos[4]:
                            secondleg = False
                        if q in toplegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > toplegpos[0]:
                            toplegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            toplegpos[3].add(q)
    #                elif secondleg:
    #                    therung = 2
    #                    if testbmp.lengthString(j.name[:10], 64) > toplegpos[1]:
    #                        toplegpos[1] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        toplegpos[4].add(q)
    #                elif thirdleg:
    #                    therung = 3
    #                    if testbmp.lengthString(j.name[:10], 64) > toplegpos[2]:
    #                        toplegpos[2] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        toplegpos[5].add(q)
                    else:
                        therung = None
                    legendTop.append((j.name[:10], legpos, therung))
        totalheight += sum(toplegpos[:3]) + 40
    if legend == 'Bottom' or legend == 'Top & Bottom':
        botlegpos = [0, 0, 0, set(), set(), set()]
        legendBot = []
        testbmp = BitMap(10, 10)
        if aln == 'best blast':
            shifter = blastmatch[-1]
        genrev1 = reverseList[-1]
        if aln == 'best blast':
            shifter = blastmatch[-1]
        genrev1 = reverseList[-1]
        for j in secondlist[-1][1]:
            if j.name != None:
                if type(j.start) == int:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[-1][0], maxlength, width, (j.start + j.stop)/2, aln)
                    else:
                        legpos = convertPos(secondlist[-1][0], maxlength, width, (j.start + j.stop)/2, aln)
                    for q in range(legpos - 40, legpos + 50):
                        if q in botlegpos[3]:
                            firstleg = False
                        if q in botlegpos[4]:
                            secondleg = False
                        if q in botlegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[0]:
                            botlegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range(legpos - 40, legpos + 50):
                            botlegpos[3].add(q)
    #                elif secondleg:
    #                    therung = 2
    #                    if testbmp.lengthString(j.name[:10], 64) > botlegpos[1]:
    #                        botlegpos[1] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        botlegpos[4].add(q)
    #                elif thirdleg:
    #                    therung = 3
    #                    if testbmp.lengthString(j.name[:10], 64) > botlegpos[2]:
    #                        botlegpos[2] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range(legpos - 40, legpos + 50):
    #                        botlegpos[5].add(q)
                    else:
                        therung = None
                    legendBot.append((j.name[:10], legpos, therung))
                else:
                    firstleg = True
                    secondleg = True
                    thirdleg = True
                    if genrev1:
                        legpos = convertPosR(secondlist[-1][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    else:
                        legpos = convertPos(secondlist[-1][0], maxlength, width, (j.start[0] + j.stop[0])/2, aln)
                    for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
                        if q in botlegpos[3]:
                            firstleg = False
                        if q in botlegpos[4]:
                            secondleg = False
                        if q in botlegpos[5]:
                            thirdleg = False
                    if firstleg:
                        therung = 1
                        if testbmp.lengthString(j.name[:10], 64) > botlegpos[0]:
                            botlegpos[0] = testbmp.lengthString(j.name[:10], 64)
                        for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
                            botlegpos[3].add(q)
    #                elif secondleg:
    #                    therung = 2
    #                    if testbmp.lengthString(j.name[:10], 64) > botlegpos[1]:
    #                        botlegpos[1] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
    #                        botlegpos[4].add(q)
    #                elif thirdleg:
    #                    therung = 3
    #                    if testbmp.lengthString(j.name[:10], 64) > botlegpos[2]:
    #                        botlegpos[2] = testbmp.lengthString(j.name[:10], 64)
    #                    for q in range((j.start[0] + j.stop[0])/2 - 40, (j.start[0] + j.stop[0])/2 + 50):
    #                        botlegpos[5].add(q)
                    else:
                        therung = None
                    legendBot.append((j.name[:10], (j.start[0] + j.stop[0])/2, therung))
        totalheight += sum(botlegpos[:3]) + 40
    # creates extra width for blast identity legend
    drawfig1hei = 0
    if drawfig1 and minident != 101:
        drawfig1hei = 500
    extraheight = 0
    # creates extra height for scale legend
    drawfig2hei = 0
    if drawfig2:
        drawfig2hei = height1
    columnhei = max([fighei, drawfig1hei, drawfig2hei])
    totalheight += columnhei
    hei = totalheight
    # creates extra height for graph
    if graphit != None:
        hei += graphit[3] * len(graphit[0]) + 2 * graphit[7] * len(graphit[0])
        extraheight = (graphit[3] + 20) * len(graphit[0])
    svg = scalableVectorGraphics(hei + 1, width)
    if legend == 'Single column':
        index = 0
        legendArrows = []
        for i in range(len(legendList)):
            x = legendList[i]
            x.sort(key=operator.itemgetter(3))
            if reverseList[i]:
                x.reverse()
            legendArrows += x
        for i in range(hei - columnhei + 74, hei, 90):
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                svg.drawOutRect(5, i - 64, 96, 64, legendArrows[index][1], genet)
                svg.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'arrow':
                svg.drawRightArrow(5, i - 64, 96, 64, legendArrows[index][1], (0, 0, 0), genet)
                svg.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'frame':
                svg.drawRightFrame(5, i - 16, 96, 128, genet, 1, legendArrows[index][1])
                svg.writeString(legendArrows[index][0], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'pointer':
                svg.drawPointer(34, i - 64, 64, genet, legendArrows[index][1])
                svg.writeString(legendArrows[index][0], 106, i, 64)
            index += 1
    elif legend == 'Two columns':
        index = 0
        legendArrows = []
        for i in range(len(legendList)):
            x = legendList[i]
            x.sort(key=operator.itemgetter(3))
            if reverseList[i]:
                x.reverse()
            legendArrows += x
        for i in range(hei - columnhei + 74, hei, 90):
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                svg.drawOutRect(5, i - 64, 96, 64, legendArrows[index][1], genet)
                svg.writeString(legendArrows[index][0][:45], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'arrow':
                svg.writeString(legendArrows[index][0][:45], 106, i, 64)
                svg.drawRightArrow(5, i - 64, 96, 64, legendArrows[index][1], (0, 0, 0), genet)
            elif index < len(legendArrows) and legendArrows[index][2] == 'frame':
                svg.drawRightFrame(5, i - 16, 96, 128, genet, 1, legendArrows[index][1])
                svg.writeString(legendArrows[index][0][:45], 106, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'pointer':
                svg.drawPointer(34, i - 64, 64, genet, legendArrows[index][1])
                svg.writeString(legendArrows[index][0][:45], 76, i, 64)
            index += 1
        for i in range(hei - columnhei + 74, hei, 90):
            if index < len(legendArrows) and legendArrows[index][2] == 'rect':
                svg.drawOutRect(5 + width/3, i - 64, 96, 64, legendArrows[index][1], genet)
                svg.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'arrow':
                svg.drawRightArrow(5 + width/3, i - 64, 96, 64, legendArrows[index][1], (0, 0, 0), genet)
                svg.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'frame':
                svg.drawRightFrame(5 + width/3, i - 16, 96, 128, genet, 1, legendArrows[index][1])
                svg.writeString(legendArrows[index][0][:45], 106 + width/3, i, 64)
            elif index < len(legendArrows) and legendArrows[index][2] == 'pointer':
                svg.drawPointer(34 + width/3, i - 64, 64, genet, legendArrows[index][1])
                svg.writeString(legendArrows[index][0][:45], 76 + width/3, i, 64)
            index += 1
    if legend == 'Top' or legend == 'Top & Bottom':
        rung1 = sum(toplegpos[:3]) + 30
        rung2 = rung1 - toplegpos[0] - 10
        rung3 = rung2 - toplegpos[1] - 10
        for i in legendTop:
            if i[0][0].lower() == i[0][0]:
                xpos = i[1] + 16
            else:
                xpos = i[1] + 32
            if i[2] == 1:
                svg.writeString(i[0], xpos, rung1, 64, False, False, 1)
            elif i[2] == 2:
                svg.writeString(i[0], xpos, rung2, 64, False, False, 1)
            elif i[2] == 3:
                svg.writeString(i[0], xpos, rung3, 64, False, False, 1)
    if legend == 'Bottom' or legend == 'Top & Bottom':
        rung1 = hei - sum(botlegpos[:3]) - 30 - columnhei
        rung2 = rung1 + botlegpos[0] + 10
        rung3 = rung2 + botlegpos[1] + 10
        for i in legendBot:
            if i[0][-1].lower() == i[0][-1]:
                xpos = i[1] + 16
            else:
                xpos = i[1] + 32
            if i[2] == 1:
                svg.writeString(i[0], xpos, rung1, 64, False, False, 1, 'right')
            elif i[2] == 2:
                svg.writeString(i[0], xpos, rung2, 64, False, False, 1, 'right')
            elif i[2] == 3:
                svg.writeString(i[0], xpos, rung3, 64, False, False, 1, 'right')
    # draws the scale figure
    if drawfig2 != False:
        testbmp = BitMap(5, 5)
        x1 = width - 600 -  drawfig2 * 1.0 / maxlength * width
        x2 = width - 600
        svg.drawLine(x1, hei - columnhei + height1/2 + 70, x2, hei - columnhei + height1/2 + 70, 3)
        svg.drawLine(x1, hei - columnhei + height1 /4 + 70, x1, hei - columnhei + height1 /4 * 3 + 70, 3)
        svg.drawLine(x2, hei - columnhei + height1 /4 + 70, x2, hei - columnhei + height1 /4 * 3 + 70, 3)
        strfig2 = str(drawfig2)
        if strfig2[-6:] == '000000':
            strfig2 = strfig2[:-6] + ' Mbp'
        elif strfig2[-3:] == '000':
            strfig2 = strfig2[:-3] + ' Kbp'
        svg.writeString(strfig2, (x1 + x2)/2 - testbmp.lengthString(strfig2, 64) / 2, hei - columnhei + height1 /4 + 65, 64)
    # draws the graph
    if graphit != None:
        thearray, maxgc, mingc, gheight, glinet, gtype, gmaxy, ggap = graphit
        widthpixellist = []
        leftpixellist = []
        rightpixellist = []
        for i in range(len(thearray)):
            if aln == 'best blast':
                shifter = blastmatch[i]
            if reverseList[i]:
                rightpixel = convertPosR(secondlist[i*2][0], maxlength, width, 0, aln)
                leftpixel = convertPosR(secondlist[i*2][0], maxlength, width, secondlist[i*2][0], aln)
                thearray[i].reverse()
            else:
                leftpixel = convertPos(secondlist[i*2][0], maxlength, width, 0, aln)
                rightpixel = convertPos(secondlist[i*2][0], maxlength, width, secondlist[i*2][0], aln)

            widthpixel = rightpixel - leftpixel + 1
            widthpixellist.append(widthpixel)
            leftpixellist.append(leftpixel)
            rightpixellist.append(rightpixel)
        neg = False
        if gmaxy == 'Auto':
            gmaxy = 0
            for i in range(0, len(thearray)):
                if min(thearray[i]) < 0:
                    neg = True
                for j in range(0, widthpixellist[i]):
                    aa = int(j * (len(thearray[i]) * 1.0 / widthpixellist[i]))
                    bb = int((j + 1) * (len(thearray[i]) * 1.0/ widthpixellist[i]))
                    if aa == bb:
                        bb += 1
                    temparr = thearray[i][aa:bb]
                    gyval = abs(sum(temparr) * 1.0 / len(temparr))
                    if gyval > gmaxy:
                        gmaxy = gyval
        else:
            gmaxy = float(gmaxy)
            for i in range(0, len(thearray)):
                if min(thearray[i]) < 0:
                    neg = True
        if neg:
            axispos = ggap + gheight/2 + glinet/2
        else:
            axispos = ggap + gheight
        for qq in range(len(thearray)):
            lastgypos = None
            svg.drawLine(leftpixellist[qq], axispos + glinet/2, rightpixellist[qq], axispos + glinet/2, glinet)
            for i in range(0, widthpixellist[qq]):
                aa = int(i * (len(thearray[qq]) * 1.0 / widthpixellist[qq]))
                bb = int((i + 1) * (len(thearray[qq]) * 1.0/ widthpixellist[qq]))
                if aa == bb:
                    bb += 1
                temparr = thearray[qq][aa:bb]
                gyval = sum(temparr) * 1.0 / len(temparr)
                yvalpixratio = gyval/gmaxy
                if yvalpixratio > 1:
                    yvalpixratio = 1
                if yvalpixratio < -1:
                    yvalpixratio = -1
                if neg:
                    if yvalpixratio < 0:
                        gc1, gc2, gc3 = mingc
                        yvalpix = round(yvalpixratio *  (gheight /2 - glinet/2))
                        if gtype == 'Line':
                            if lastgypos != None:
                                svg.drawLine(leftpixellist[qq] + i-1, lastgypos, leftpixellist[qq] + i, axispos - yvalpix, 1, mingc)
                            lastgypos = axispos - yvalpix
                        elif gtype == 'Histogram':
                            svg.drawLine(leftpixellist[qq] + i, axispos + glinet/2, leftpixellist[qq] + i, axispos - yvalpix, 1, mingc)
                    else:
                        gc1, gc2, gc3 = maxgc
                        yvalpix = round(yvalpixratio * (gheight /2 - (glinet - glinet/2)))
                        if gtype == 'Line':
                            if lastgypos != None:
                                svg.drawLine(leftpixellist[qq] + i-1, lastgypos, leftpixellist[qq] + i, axispos - glinet - yvalpix, 1, maxgc)
                            lastgypos = axispos - glinet - yvalpix
                        elif gtype == 'Histogram' and round(yvalpix) != 0.0:
                            svg.drawLine(leftpixellist[qq] + i, axispos - glinet /2, leftpixellist[qq] + i, axispos - yvalpix, 1, maxgc)
                else:
                    yvalpix = round(yvalpixratio * (gheight - glinet))
                    if gtype == 'Line':
                        if lastgypos != None:
                            svg.drawLine(leftpixellist[qq] + i-1, lastgypos, i, leftpixellist[qq] - axispos - glinet - yvalpix, 1, maxgc)
                        lastgypos = axispos - glinet - 1 - yvalpix
                    elif gtype == 'Histogram' and round(yvalpix) != 0.0:
                        svg.drawLine(leftpixellist[qq] + i, axispos , leftpixellist[qq] + i, axispos - yvalpix, 1, maxgc)
            axispos += gheight + 2 * ggap + height1 + height2
        modfig1 = (graphit[3] + 2 * ggap) * len(graphit[0])
    else:
        modfig1 = 0
    # draws the blast gradient legend
    if drawfig1 and minident != 101:
        svg.writeString(str(int(round(minident))) + '%', width - 300, hei - columnhei + 480, 64)
        svg.writeString('100%',  width - 300, hei - columnhei + 84, 64)
        svg.drawGradient(width -400, hei - columnhei + 20, 40, 460, minblastc, maxblastc)
        svg.drawGradient2(width -360, hei - columnhei + 20, 40, 460, minblastci, maxblastci)
    # draws feature and blast figures
    for i in range(0, len(secondlist)):
        # draws the blast figure
        if i % 2 == 0:
            if aln == 'best blast':
                shifter = blastmatch[i/2]
            genrev1 = reverseList[i/2]
            ymod = (height1 * i/2 + height2 * i/2)
            if graphit != None:
                ymod += (gheight + 2 * ggap) * (min([len(thearray), i/2 + 1]))
            if legend == 'Top' or legend == 'Top & Bottom':
                ymod += sum(toplegpos[:3]) + 40
            length = secondlist[i][0]
            svg.drawLine(convertPos(length, maxlength, width, 0, aln), ymod + height1/2,
                             convertPos(length, maxlength, width, length, aln), ymod + height1/2, glt)
            for j in secondlist[i][1]:
                if abortCaptain:
                    return None
                if (j.strand == '+' and not genrev1) or (j.strand == '-' and genrev1):
                    if type(j.start) == int:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start, aln)
                            x1 = convertPosR(length, maxlength, width, j.stop, aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start, aln)
                            x2 = convertPos(length, maxlength, width, j.stop, aln)
                        if featDict[j.type][0] == 'rect':
                            svg.drawOutRect(x1, ymod, max([x2-x1, 1]), height1, j.colour, genet)
                        elif featDict[j.type][0] == 'arrow':
                            svg.drawRightArrow(x1, ymod, max([x2-x1, 1]), height1, j.colour, (0, 0, 0), genet)
                        elif featDict[j.type][0] == 'frame':
                            svg.drawRightFrame(x1, ymod, max([x2-x1, 1]), height1, genet, j.start % 3, j.colour)
                        elif featDict[j.type][0] == 'pointer':
                            svg.drawPointer(x1, ymod, height1, genet, j.colour)
                    else:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start[-1], aln)
                            x1 = convertPosR(length, maxlength, width, j.stop[-1], aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start[-1], aln)
                            x2 = convertPos(length, maxlength, width, j.stop[-1], aln)
                        if featDict[j.type][0] == 'rect':
                            svg.drawOutRect(x1, ymod, max([x2-x1, 1]), height1, j.colour, genet)
                        elif featDict[j.type][0] == 'arrow':
                            svg.drawRightArrow(x1, ymod, max([x2-x1, 1]), height1, j.colour, (0, 0, 0), genet)
                        elif featDict[j.type][0] == 'frame':
                            svg.drawRightFrame(x1, ymod, max([x2-x1, 1]), height1, genet, j.start[-1] % 3, j.colour)
                        elif featDict[j.type][0] == 'pointer':
                            svg.drawPointer(x1, ymod, height1, genet, j.colour)
                        for k in range(2, len(j.start) + 1):
                            if genrev1:
                                x4 = convertPosR(length, maxlength, width, j.start[-k], aln)
                                x3 = convertPosR(length, maxlength, width, j.stop[-k], aln)
                            else:
                                x3 = convertPos(length, maxlength, width, j.start[-k], aln)
                                x4 = convertPos(length, maxlength, width, j.stop[-k], aln)
                            if featDict[j.type][0] == 'arrow' or featDict[j.type][0] == 'rect':
                                if x1 - x4 > 2:
                                    svg.drawDash(x4, ymod + height1/4, x4, ymod, exont)
                                    svg.drawDash(x4, ymod, x1, ymod, exont)
                                    svg.drawDash(x1, ymod, x1, ymod + height1/4, exont)
                                svg.drawOutRect(x3, ymod + height1/4, x4-x3, height1/2, j.colour, genet)
                            elif featDict[j.type][0] == 'frame':
                                if x1 - x4 > 2:
                                    svg.drawDash(x4, ymod + height1/4, x4, ymod, exont)
                                    svg.drawDash(x4, ymod, x1, ymod, exont)
                                    svg.drawDash(x1, ymod, x1, ymod + height1/4, exont)
                                svg.drawRightFrameRect(x3, ymod, x4-x3, height1, genet, j.start[-k] % 3, j.colour)
                            # need to get exons working for other types
                            x1, x2 = x3, x4
                else:
                    if type(j.start) == int:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start, aln)
                            x1 = convertPosR(length, maxlength, width, j.stop, aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start, aln)
                            x2 = convertPos(length, maxlength, width, j.stop, aln)
                        if featDict[j.type][0] == 'rect':
                            svg.drawOutRect(x1, ymod, x2-x1, height1, j.colour, genet)
                        elif featDict[j.type][0] == 'arrow':
                            svg.drawLeftArrow(x1, ymod, x2-x1, height1, j.colour, (0, 0, 0), genet)
                        elif featDict[j.type][0] == 'frame':
                            svg.drawLeftFrame(x1, ymod, x2-x1, height1, genet, j.stop % 3, j.colour)
                        elif featDict[j.type][0] == 'pointer':
                            svg.drawPointer(x1, ymod, height1, genet, j.colour)
                    else:
                        if genrev1:
                            x2 = convertPosR(length, maxlength, width, j.start[0], aln)
                            x1 = convertPosR(length, maxlength, width, j.stop[0], aln)
                        else:
                            x1 = convertPos(length, maxlength, width, j.start[0], aln)
                            x2 = convertPos(length, maxlength, width, j.stop[0], aln)
                        if featDict[j.type][0] == 'rect':
                            svg.drawOutRect(x1, ymod, x2-x1, height1, j.colour, genet)
                        elif featDict[j.type][0] == 'arrow':
                            svg.drawLeftArrow(x1, ymod, x2-x1, height1, j.colour, (0, 0, 0), genet)
                        elif featDict[j.type][0] == 'frame':
                            svg.drawLeftFrame(x1, ymod, x2-x1, height1, genet, j.stop[0] % 3, j.colour)
                        elif featDict[j.type][0] == 'pointer':
                            svg.drawPointer(x1, ymod, height1, genet, j.colour)
                        for k in range(1, len(j.start)):
                            if genrev1:
                                x4 = convertPosR(length, maxlength, width, j.start[k], aln)
                                x3 = convertPosR(length, maxlength, width, j.stop[k], aln)
                            else:
                                x3 = convertPos(length, maxlength, width, j.start[k], aln)
                                x4 = convertPos(length, maxlength, width, j.stop[k], aln)
                            if featDict[j.type][0] == 'rect' or featDict[j.type][0] == 'arrow':
                                if x3 - x2 > 2:
                                    svg.drawDash(x2, ymod + 3*height1/4, x2, ymod + height1, exont)
                                    svg.drawDash(x2, ymod + height1, x3, ymod + height1, exont)
                                    svg.drawDash(x3, ymod + height1, x3, ymod + 3*height1/4, exont)
                            elif featDict[j.type][0] == 'frame':
                                if x3 - x2 > 2:
                                    svg.drawDash(x2, ymod + 3*height1/4, x2, ymod + height1, exont)
                                    svg.drawDash(x2, ymod + height1, x3, ymod + height1, exont)
                                    svg.drawDash(x3, ymod + height1, x3, ymod + 3*height1/4, exont)
                                svg.drawLeftFrameRect(x3, ymod, x4-x3, height1, genet, j.stop[k] % 3, j.colour)
                            x1, x2 = x3, x4
        else:
            # draws teh blast hits
            genrev2 = reverseList[(i+1)/2]
            length1 = secondlist[i-1][0]
            length2 = secondlist[i+1][0]
            ymod = (height1 * (i - 1)/2 + height2 * (i - 1)/2) - 1 + height1
            if graphit != None:
                ymod += (gheight + 2 * ggap) * (min([len(thearray), i/2 + 1]))
            if legend == 'Top' or legend == 'Top & Bottom':
                ymod += sum(toplegpos[:3]) + 40
            y1 = ymod
            y2 = y1 + height2 + 1
            for j in secondlist[i]:
                if abortCaptain:
                    return None
                qStart, qEnd, rStart, rEnd, ident = j
                # is the blast hit inverted
                if (rStart < rEnd and not genrev1 and not genrev2) or \
                   (rStart > rEnd and not genrev1 and genrev2) or \
                   (rStart < rEnd and genrev1 and genrev2) or \
                   (rStart > rEnd and genrev1 and not genrev2):
                    crisscross = False
                else:
                    crisscross = True
                try:
                    ratio = round((ident - minident) / (100 - minident), 2)
                except:
                    ratio = 1
                if crisscross:
                    r1 = int(minblastci[0] * (1 - ratio) + maxblastci[0] * ratio)
                    r2 = int(minblastci[1] * (1 - ratio) + maxblastci[1] * ratio)
                    r3 = int(minblastci[2] * (1 - ratio) + maxblastci[2] * ratio)
                else:
                    r1 = int(minblastc[0] * (1 - ratio) + maxblastc[0] * ratio)
                    r2 = int(minblastc[1] * (1 - ratio) + maxblastc[1] * ratio)
                    r3 = int(minblastc[2] * (1 - ratio) + maxblastc[2] * ratio)
                if aln == 'best blast':
                    shifter = blastmatch[i/2]
                if genrev1:
                    x1e = convertPosR(length1, maxlength, width, qStart, aln)
                    x1s = convertPosR(length1, maxlength, width, qEnd, aln)
                else:
                    x1s = convertPos(length1, maxlength, width, qStart, aln)
                    x1e = convertPos(length1, maxlength, width, qEnd, aln)
                if aln == 'best blast':
                    shifter = blastmatch[(i+1)/2]
                if genrev2 and rStart < rEnd:
                    x2e = convertPosR(length2, maxlength, width, rStart, aln)
                    x2s = convertPosR(length2, maxlength, width, rEnd, aln)
                elif genrev2 and rStart >= rEnd:
                    x2s = convertPosR(length2, maxlength, width, rStart, aln)
                    x2e = convertPosR(length2, maxlength, width, rEnd, aln)
                elif not genrev2 and rStart < rEnd:
                    x2s = convertPos(length2, maxlength, width, rStart, aln)
                    x2e = convertPos(length2, maxlength, width, rEnd, aln)
                else:
                    x2e = convertPos(length2, maxlength, width, rStart, aln)
                    x2s = convertPos(length2, maxlength, width, rEnd, aln)
                if crisscross:
                    svg.drawBlastHit(x1s, y1, x1e, y1, x2s, y2, x2e, y2, (r1, r2, r3))
                    if blastoutline:
                        svg.drawLine(x1s, y1, x2e, y2)
                        svg.drawLine(x1e, y1, x2s, y2)
                else:
                    svg.drawBlastHit(x1s, y1, x1e, y1, x2e, y2, x2s, y2, (r1, r2, r3))
                    if blastoutline:
                        svg.drawLine(x1s, y1, x2s, y2)
                        svg.drawLine(x1e, y1, x2e, y2)
    svg.writesvg(filename)
    return minident

# The GUI
class App:
    def __init__(self, master):
        self.pwd = os.getcwd()
        self.menubar = Menu(master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Figure", command=self.defaultoptions)
        self.filemenu.add_command(label="Save Settings", command=self.saveOptions)
        self.filemenu.add_command(label="Load Settings", command=self.openOptions)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Preferences", command=self.preferencewindow)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # create more pulldown menus
        self.confmenu = Menu(self.menubar, tearoff=0)
        self.confmenu.add_command(label="Figure", command=self.figureoptions)
        self.confmenu.add_command(label="Annotation", command=self.annotateoptions)
        self.confmenu.add_command(label="Blast", command=self.blastoptions)
        self.confmenu.add_command(label="Graph", command=self.graphoptions)
        self.confmenu.add_command(label="Subregions", command=self.annmod)
        self.menubar.add_cascade(label="Image", menu=self.confmenu)

        self.blastmenu = Menu(self.menubar, tearoff=0)
        self.blastmenu.add_command(label="Download Blast Automatically", command=self.downloadBlastAuto)
        self.blastmenu.add_command(label="Download Blast Manually", command=self.downloadBlastMan)
        self.blastmenu.add_command(label="Choose Blast Location", command=self.chooseBlastDir)
        self.menubar.add_cascade(label="Blast", menu=self.blastmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.openhelpsite)
        self.helpmenu.add_command(label="Support", command=self.supportwin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About", command=self.openabout)
        self.helpmenu.add_command(label="Reference", command=self.openref)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        master.config(menu=self.menubar)
        frame1 = Frame(master)
        frame1.grid(row=0, column=0, padx=40, pady=10)
        master.geometry('+10+20')
        self.showit = False
        self.running = False
        self.graphshow = False
        self.cutstate = None
        self.orderstate = None
        self.blastlDir = None
        self.blastnDir = None
        self.dblDir = None
        self.dbnDir = None
        self.workingDir = 'test'
        self.mincutlist = {}
        self.maxcutlist = {}
        self.revlist = {}
        self.entrynum = 0
        self.theTitle = Label(frame1, text='Easyfig 2.2.3', font='TkDefaultFont 24 bold')
        self.theTitle.grid(row=0, column=1, columnspan=3, padx=10, sticky='W')
        self.annLab = Label(frame1, text="Annotation Files", font='TkDefaultFont 13 bold underline')
        self.annLab.grid(row=1, column=2, pady=10)
        self.scrollbar = Scrollbar(frame1, orient=VERTICAL)
        self.genlist = DDlistbox(frame1, yscrollcommand=self.scrollbar.set)
        self.genlist.bind('<Double-Button-1>', self.annmod)
        self.genlist.config(height=10)
        self.blastlist = DDlistbox(frame1, yscrollcommand=self.scrollbar.set)
        self.blastlist.config(height=9)
        self.scrollbar.config(command=self.yview)
        self.scrollbar.grid(row=2, column=1, rowspan=9, sticky=NS)
        self.genlist.grid(row=2, column=2, rowspan=9)
        self.annLab = Label(frame1, text="Blast Files", font='TkDefaultFont 13 bold underline')
        self.annLab.grid(row=1, column=3)
        self.blastlist.grid(row=2, column=3, rowspan=9)
        self.addgenbutton = Button(frame1, text='Add feature file', command=self.addfeat)
        self.addgenbutton.grid(row=11, column=2, sticky=EW)
        self.addgenbutton = Button(frame1, text='Add folder', command=self.addfolder)
        self.addgenbutton.grid(row=12, column=2, sticky=EW)
        self.removegenbutton = Button(frame1, text='Remove feature file', command=self.removefeat)
        self.removegenbutton.grid(row=13, column=2, sticky=EW)

        self.addblastbutton = Button(frame1, text='Add blast file', command=self.addblast)
        self.addblastbutton.grid(row=11, column=3, sticky=EW)
        self.removeblastbutton = Button(frame1, text='Remove blast file', command=self.removeblast)
        self.removeblastbutton.grid(row=12, column=3, sticky=EW)
        

        self.spacefiller = Label(frame1, text=' ')
        self.spacefiller.grid(row=12, column=0)
        self.blastit = Button(frame1, text='Generate blastn Files', command=self.genBlast)
        self.blastit.grid(row=14, column=3, sticky='EW')
        self.blastx = Button(frame1, text='Generate tblastx Files', command=self.genBlastX)
        self.blastx.grid(row=15, column=3, sticky='EW')


        self.outfile = StringVar(value='')
        self.outopen = Button(frame1, text="Save As", command=self.getoutfile)
        self.outopen.grid(row=17, column=2, columnspan=2, sticky=W)
        self.outfilename = Entry(frame1, textvariable=self.outfile)
        self.outfilename.grid(row=17, column=2, columnspan=2)
        self.filetype = StringVar(value='Bitmap (bmp)')
        self.filetypelabel = Label(frame1, text='File type:')
        self.filetypelabel.grid(row=18, column=2, columnspan=2, pady=5, sticky=W)
        self.filetypeentry = OptionMenu(frame1, self.filetype, 'Bitmap (bmp)', 'Vector file (svg)', 'Preview (shrink)', 'Preview (1:1)')
        self.filetypeentry.grid(row=18, column=2, columnspan=2, pady=5)
        self.createFigure = Button(frame1, text="Create Figure", font='TkDefaultFont 12 bold', width=20, command=self.makeFigure)
        self.createFigure.grid(row=19, column=2, columnspan=2, rowspan=3, sticky='NS')


        self.processLab = Label(frame1, bg='#FFFF99', relief=SUNKEN)
        self.processLab.grid(row=14, column=1, rowspan=3, columnspan=2, sticky='NSEW', padx=5, pady=5)

        self.gap = Label(frame1, text=' ')
        self.gap.grid(row=18, column=3)
        self.gap2 = Label(frame1, text=' ')
        self.gap2.grid(row=16, column=3)
        self.gap3 = Label(frame1, text=' ')
        self.gap3.grid(row=19, column=4)
        self.gap4 = Label(frame1, text=' ')
        self.gap4.grid(row=20, column=4)
        self.gap4 = Label(frame1, text=' ')
        self.gap4.grid(row=21, column=4)
        
        self.defaultpreferences()
        if os.path.exists('.easyfig.pref'):
            self.opendefault()

    def yview(self, *args):
        apply(self.genlist.yview, args)
        apply(self.blastlist.yview, args)

    def addfolder(self):
        tempfolder = tkFileDialog.askdirectory(title='Please select a directory with feature files.')
        if tempfolder == () or tempfolder == '':
            return
        for i in os.listdir(tempfolder):
            if self.entrynum == 99:
                if self.genlist.size() == 99:
                    tkMessageBox.showerror('Maximum feature files reached.', 'At this time easyfig only supports 99 genomes.\nEasyfig_CL does not have a maximum limit.')
                    return
                self.renumbergen()
            filename = tempfolder + '/' + i
            self.entrynum += 1
            entryname = '%02d' % self.entrynum + '. ' + filename
            self.genlist.insert(END, entryname)
            self.mincutlist[entryname[:2]] = '1'
            self.maxcutlist[entryname[:2]] = 'Max'
            self.revlist[entryname[:2]] = False
        self.genlist.xview_moveto(1)
        

    def addfeat(self):
        if self.entrynum == 99:
            if self.genlist.size() == 99:
                tkMessageBox.showerror('Maximum feature files reached.', 'At this time easyfig only supports 99 genomes.\nEasyfig_CL does not have a maximum limit.')
                return
            self.renumbergen()
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        if filename == '':
            return
        self.entrynum += 1
        entryname = '%02d' % self.entrynum + '. ' + filename
        self.genlist.insert(END, entryname)
        self.genlist.xview_moveto(1)
        self.mincutlist[entryname[:2]] = '1'
        self.maxcutlist[entryname[:2]] = 'Max'
        self.revlist[entryname[:2]] = False
    
    def renumbergen(self):
        try:
            self.annwindow.destroy()
        except:
            pass
        tempmincutlist = {}
        tempmaxcutlist = {}
        temprevlist = {}
        for i in range(self.genlist.size()):
            tempgen = self.genlist.get(i)
            self.genlist.delete(i)
            self.genlist.insert(i, '%02d' % (i + 1) + tempgen[2:])
            tempmincutlist['%02d' % (i + 1)] = self.mincutlist[tempgen[:2]]
            tempmaxcutlist['%02d' % (i + 1)] = self.maxcutlist[tempgen[:2]]
            temprevlist['%02d' % (i + 1)] = self.revlist[tempgen[:2]]
        self.mincutlist = tempmincutlist
        self.maxcutlist = tempmaxcutlist
        self.revlist = temprevlist
        self.entrynum = self.genlist.size()
        self.genlist.xview_moveto(1)
    
    def removefeat(self):
        self.genlist.delete(ANCHOR)
        self.renumbergen()

    def addblast(self):
        filename = tkFileDialog.askopenfilename()
        self.blastlist.insert(END, filename)
        self.blastlist.xview_moveto(1)
        self.orderstate = None
        self.cutstate = None
    
    def removeblast(self):
        self.blastlist.delete(ANCHOR)

    def defaultoptions(self):
        try:
            self.prefwin.destroy()
        except:
            pass
        try:
            self.figureoptionswindow.destroy()
        except:
            pass
        try:
            self.blastoptionswindow.destroy()
        except:
            pass
        try:
            self.annotateoptionswindow.destroy()
        except:
            pass
        try:
            self.graphoptionswindow.destroy()
        except:
            pass
        try:
            self.annwindow.destroy()
        except:
            pass
        try:
            self.doublecutswin.destroy()
        except:
            pass
        self.outfile.set('')
        self.genlist.delete(0, END)
        self.blastlist.delete(0, END)
        self.defaultpreferences()
        self.entrynum = 0
        self.cutstate = None
        self.orderstate = None
        if os.path.exists('.easyfig.pref'):
            self.opendefault()
        else:
            self.defaultpreferences()


    def defaultpreferences(self):
        self.filetype.set('Bitmap (bmp)')
        self.figwidthvar = StringVar(value='5000')
        self.height1var = StringVar(value='150')
        self.height2var = StringVar(value='500')
        self.aln = StringVar(value='centre')
        self.autodetect = IntVar()
        self.autodetect.set(1)
        self.drawfig1 = IntVar()
        self.drawfig1.set(1)
        self.drawfig2var = StringVar(value='0')

        self.minlengthvar = StringVar(value='0')
        self.minevalvar = StringVar(value='0.001')
        self.minIdentvar = StringVar(value='0')
        self.minblastc = (200, 200, 200)
        self.minblastchex = '#C8C8C8'
        self.minblastci = (200, 200, 200)
        self.minblastcihex = '#C8C8C8'
        self.maxblastc = (100, 100, 100)
        self.maxblastchex = '#646464'
        self.maxblastci = (100, 100, 100)
        self.maxblastcihex = '#646464'
        self.blastoutline = IntVar()
        self.blastoutline.set(1)

        self.leg = StringVar(value='None')
        self.leg2 = StringVar(value='None')
        self.legname = StringVar(value='gene')
        self.gltvar = StringVar(value='20')
        self.exontvar = StringVar(value='2')
        self.genetvar = StringVar(value='1')

        self.genef = IntVar()
        self.genef.set(1)
        self.genefcolour = (64, 224, 208)
        self.genefcolourhex = '#40e0d0'
        self.genefrect = StringVar(value='arrow')

        self.cdsf = IntVar()
        self.cdsfcolour = (255, 140, 0)
        self.cdsfcolourhex = '#ff8c00'
        self.cdsfrect = StringVar(value='arrow')

        self.trnaf = IntVar()
        self.trnafcolour = (165, 42, 42)
        self.trnafcolourhex = '#a52a2a'
        self.trnafrect = StringVar(value='rect')

        self.miscf = IntVar()
        self.miscfcolour = (0, 191, 255)
        self.miscfcolourhex = '#00bfff'
        self.miscfrect = StringVar(value='rect')

        self.randfeat = StringVar()
        self.randf = IntVar()
        self.randfcolour = (72, 61, 139)
        self.randfcolourhex = '#483d8b'
        self.randfrect = StringVar(value='arrow')

        self.graphtype = StringVar(value='None')
        self.allorone = IntVar()
        self.graphfile = StringVar()
        self.step = StringVar(value='1000')
        self.windsize = StringVar(value='1000')
        self.graphheight = StringVar(value='200')
        self.maxy = StringVar(value='Auto')
        self.logit = IntVar()
        self.histo = StringVar(value='Histogram')
        self.graphlinet = StringVar(value='1')
        self.poscol = (255, 0, 0)
        self.poscolhex ='#FF0000'
        self.negcol = (0, 0, 255)
        self.negcolhex = '#0000FF'
        self.ggap = StringVar(value='10')
        self.blastnDir = None
        self.dbnDir = None

    def saveOptions(self):
        filename = ''
        filename = tkFileDialog.asksaveasfilename(filetypes = [('easycfg', '*.easycfg'), ('All files','*')])
        if filename == '' or filename == ():
            return
        savefile = open(filename, 'w')
        savefile.write('\t'.join(self.genlist.get(0, END)) + '\n')
        for i in self.genlist.get(0, END):
            savefile.write(i[:2] + '\t' + self.mincutlist[i[:2]] + '\t' + self.maxcutlist[i[:2]] + '\t' + str(self.revlist[i[:2]]) + '\n')
        savefile.write('\t'.join(self.blastlist.get(0, END)) + '\n')

        savefile.write(self.outfile.get() + '\n')
        savefile.write(self.filetype.get() + '\n')

        savefile.write(self.figwidthvar.get() + '\n')
        savefile.write(self.height1var.get() + '\n')
        savefile.write(self.height2var.get() + '\n')
        savefile.write(self.aln.get() + '\n')
        savefile.write(str(self.autodetect.get()) + '\n')
        savefile.write(str(self.drawfig1.get()) + '\n')
        savefile.write(self.drawfig2var.get() + '\n')

        savefile.write(self.minlengthvar.get() + '\n')
        savefile.write(self.minevalvar.get() + '\n')
        savefile.write(self.minIdentvar.get() + '\n')
        savefile.write(str(self.minblastc[0]) + '\n')
        savefile.write(str(self.minblastc[1]) + '\n')
        savefile.write(str(self.minblastc[2]) + '\n')
        savefile.write(self.minblastchex + '\n')
        savefile.write(str(self.minblastci[0]) + '\n')
        savefile.write(str(self.minblastci[1]) + '\n')
        savefile.write(str(self.minblastci[2]) + '\n')
        savefile.write(self.minblastcihex + '\n')
        savefile.write(str(self.maxblastc[0]) + '\n')
        savefile.write(str(self.maxblastc[1]) + '\n')
        savefile.write(str(self.maxblastc[2]) + '\n')
        savefile.write(self.maxblastchex + '\n')
        savefile.write(str(self.maxblastci[0]) + '\n')
        savefile.write(str(self.maxblastci[1]) + '\n')
        savefile.write(str(self.maxblastci[2]) + '\n')
        savefile.write(self.maxblastcihex + '\n')
        savefile.write(str(self.blastoutline.get()) + '\n')

        savefile.write(self.leg.get() + '\n')
        savefile.write(self.leg2.get() + '\n')
        savefile.write(self.legname.get() + '\n')
        savefile.write(self.gltvar.get() + '\n')
        savefile.write(self.exontvar.get() + '\n')
        savefile.write(self.genetvar.get() + '\n')


        savefile.write(str(self.genef.get()) + '\n')
        savefile.write(str(self.genefcolour[0]) + '\n')
        savefile.write(str(self.genefcolour[1]) + '\n')
        savefile.write(str(self.genefcolour[2]) + '\n')
        savefile.write(self.genefcolourhex + '\n')
        savefile.write(self.genefrect.get() + '\n')


        savefile.write(str(self.cdsf.get()) + '\n')
        savefile.write(str(self.cdsfcolour[0]) + '\n')
        savefile.write(str(self.cdsfcolour[1]) + '\n')
        savefile.write(str(self.cdsfcolour[2]) + '\n')
        savefile.write(self.cdsfcolourhex + '\n')
        savefile.write(self.cdsfrect.get() + '\n')

        savefile.write(str(self.trnaf.get()) + '\n')
        savefile.write(str(self.trnafcolour[0]) + '\n')
        savefile.write(str(self.trnafcolour[1]) + '\n')
        savefile.write(str(self.trnafcolour[2]) + '\n')
        savefile.write(self.trnafcolourhex + '\n')
        savefile.write(self.trnafrect.get() + '\n')


        savefile.write(str(self.miscf.get()) + '\n')
        savefile.write(str(self.miscfcolour[0]) + '\n')
        savefile.write(str(self.miscfcolour[1]) + '\n')
        savefile.write(str(self.miscfcolour[2]) + '\n')
        savefile.write(self.miscfcolourhex + '\n')
        savefile.write(self.miscfrect.get() + '\n')

        savefile.write(self.randfeat.get() + '\n')
        savefile.write(str(self.randf.get()) + '\n')
        savefile.write(str(self.randfcolour[0]) + '\n')
        savefile.write(str(self.randfcolour[1]) + '\n')
        savefile.write(str(self.randfcolour[2]) + '\n')
        savefile.write(self.randfcolourhex + '\n')
        savefile.write(self.randfrect.get() + '\n')

        savefile.write(self.graphtype.get() + '\n')
        savefile.write(str(self.allorone.get()) + '\n')
        savefile.write(self.graphfile.get() + '\n')
        savefile.write(self.step.get() + '\n')
        savefile.write(self.windsize.get() + '\n')
        savefile.write(self.graphheight.get() + '\n')
        savefile.write(self.maxy.get() + '\n')
        savefile.write(str(self.logit.get()) + '\n')
        savefile.write(self.histo.get() + '\n')
        savefile.write(self.graphlinet.get() + '\n')
        savefile.write(str(self.poscol[0]) + '\n')
        savefile.write(str(self.poscol[1]) + '\n')
        savefile.write(str(self.poscol[2]) + '\n')
        savefile.write(self.poscolhex + '\n')
        savefile.write(str(self.negcol[0]) + '\n')
        savefile.write(str(self.negcol[1]) + '\n')
        savefile.write(str(self.negcol[2]) + '\n')
        savefile.write(self.negcolhex + '\n')
        savefile.write(self.ggap.get() + '\n')
        savefile.close()


    def openOptions(self):
        try:
            filename = tkFileDialog.askopenfilename(filetypes = [('easycfg', '*.easycfg'), ('All files','*')])
            if filename == '':
                return
            openfile = open(filename)
            templist = openfile.readline().rstrip().split('\t')
            self.genlist.delete(0, END)
            if templist == ['']:
                templist = []
            for i in templist:
                self.genlist.insert(END, i)
            self.genlist.xview_moveto(1)
            for i in range(len(templist)):
                name, mincut, maxcut, rev = openfile.readline().rstrip().split('\t')
                self.mincutlist[name] = mincut
                self.maxcutlist[name] = maxcut
                if rev == 'True':
                    self.revlist[name] = True
                else:
                    self.revlist[name] = False
            templist = openfile.readline().rstrip().split('\t')
            if templist == ['']:
                templist = []
            self.blastlist.delete(0, END)
            for i in templist:
                self.blastlist.insert(END, i)
            self.blastlist.xview_moveto(1)
            self.outfile.set(openfile.readline().rstrip())
            self.filetype.set(openfile.readline().rstrip())

            self.figwidthvar.set(openfile.readline().rstrip())
            self.height1var.set(openfile.readline().rstrip())
            self.height2var.set(openfile.readline().rstrip())
            self.aln.set(openfile.readline().rstrip())
            self.autodetect.set(int(openfile.readline().rstrip()))
            self.drawfig1.set(int(openfile.readline().rstrip()))
            self.drawfig2var.set(openfile.readline().rstrip())

            self.minlengthvar.set(openfile.readline().rstrip())
            self.minevalvar.set(openfile.readline().rstrip())
            self.minIdentvar.set(openfile.readline().rstrip())
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.minblastc = (x, y, z)
            self.minblastchex = openfile.readline().rstrip()
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.minblastci = (x, y, z)
            self.minblastcihex = openfile.readline().rstrip()
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.maxblastc = (x, y, z)
            self.maxblastchex = openfile.readline().rstrip()
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.maxblastci = (x, y, z)
            self.maxblastcihex = openfile.readline().rstrip()
            self.blastoutline.set(int(openfile.readline().rstrip()))

            self.leg.set(openfile.readline().rstrip())
            self.leg2.set(openfile.readline().rstrip())
            self.legname.set(openfile.readline().rstrip())
            self.gltvar.set(openfile.readline().rstrip())
            self.exontvar.set(openfile.readline().rstrip())
            self.genetvar.set(openfile.readline().rstrip())

            self.genef.set(int(openfile.readline().rstrip()))
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.genefcolour = (x, y, z)
            self.genefcolourhex = openfile.readline().rstrip()
            self.genefrect.set(openfile.readline().rstrip())

            self.cdsf.set(int(openfile.readline().rstrip()))
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.cdsfcolour = (x, y, z)
            self.cdsfcolourhex = openfile.readline().rstrip()
            self.cdsfrect.set(openfile.readline().rstrip())

            self.trnaf.set(int(openfile.readline().rstrip()))
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.trnafcolour = (x, y, z)
            self.trnafcolourhex = openfile.readline().rstrip()
            self.trnafrect.set(openfile.readline().rstrip())

            self.miscf.set(int(openfile.readline().rstrip()))
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.miscfcolour = (x, y, z)
            self.miscfcolourhex = openfile.readline().rstrip()
            self.miscfrect.set(openfile.readline().rstrip())

            self.randfeat.set(openfile.readline().rstrip())
            self.randf.set(int(openfile.readline().rstrip()))
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.randfcolour = (x, y, z)
            self.randfcolourhex = openfile.readline().rstrip()
            self.randfrect.set(openfile.readline().rstrip())

            self.graphtype.set(openfile.readline().rstrip())
            self.allorone.set(int(openfile.readline().rstrip()))
            self.graphfile.set(openfile.readline().rstrip())
            self.step.set(openfile.readline().rstrip())
            self.windsize.set(openfile.readline().rstrip())
            self.graphheight.set(openfile.readline().rstrip())
            self.maxy.set(openfile.readline().rstrip())
            self.logit.set(openfile.readline().rstrip())
            self.histo.set(openfile.readline().rstrip())
            self.graphlinet.set(openfile.readline().rstrip())
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.poscol = (x, y, z)
            self.poscolhex = openfile.readline().rstrip()
            x = int(openfile.readline().rstrip())
            y = int(openfile.readline().rstrip())
            z = int(openfile.readline().rstrip())
            self.negcol = (x, y, z)
            self.negcolhex = openfile.readline().rstrip()
            self.ggap.set(openfile.readline().rstrip())
            openfile.close()
        except:
            tkMessageBox.showerror('Try again.', 'Easyfig config file invalid.')

    def opendefault(self):
        try:
            if not os.path.exists('.easyfig.pref'):
                self.defaultpreferences()
                return
            preffile = open('.easyfig.pref')
            gotpref = False
            for line in preffile:
                if line.startswith('>'):
                    preflist = line.split('\t')[1:]
                    gotpref = True
            preffile.close()
            if not gotpref:
                self.defaultpreferences()
                return
            self.filetype.set(preflist.pop(0))

            self.figwidthvar.set(preflist.pop(0))
            self.height1var.set(preflist.pop(0))
            self.height2var.set(preflist.pop(0))
            self.aln.set(preflist.pop(0))
            self.autodetect.set(int(preflist.pop(0)))
            self.drawfig1.set(int(preflist.pop(0)))
            self.drawfig2var.set(preflist.pop(0))

            self.minlengthvar.set(preflist.pop(0))
            self.minevalvar.set(preflist.pop(0))
            self.minIdentvar.set(preflist.pop(0))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.minblastc = (x, y, z)
            self.minblastchex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.minblastci = (x, y, z)
            self.minblastcihex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.maxblastc = (x, y, z)
            self.maxblastchex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.maxblastci = (x, y, z)
            self.maxblastcihex = preflist.pop(0)
            self.blastoutline.set(int(preflist.pop(0)))
 
            self.leg.set(preflist.pop(0))
            self.leg2.set(preflist.pop(0))
            self.legname.set(preflist.pop(0))
            self.gltvar.set(preflist.pop(0))
            self.exontvar.set(preflist.pop(0))
            self.genetvar.set(preflist.pop(0))

            self.genef.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.genefcolour = (x, y, z)
            self.genefcolourhex = preflist.pop(0)
            self.genefrect.set(preflist.pop(0))

            self.cdsf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.cdsfcolour = (x, y, z)
            self.cdsfcolourhex = preflist.pop(0)
            self.cdsfrect.set(preflist.pop(0))

            self.trnaf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.trnafcolour = (x, y, z)
            self.trnafcolourhex = preflist.pop(0)
            self.trnafrect.set(preflist.pop(0))

            self.miscf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.miscfcolour = (x, y, z)
            self.miscfcolourhex = preflist.pop(0)
            self.miscfrect.set(preflist.pop(0))

            self.randfeat.set(preflist.pop(0))
            self.randf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.randfcolour = (x, y, z)
            self.randfcolourhex = preflist.pop(0)
            self.randfrect.set(preflist.pop(0))

            self.graphtype.set(preflist.pop(0))
            self.allorone.set(int(preflist.pop(0)))
            self.graphfile.set(preflist.pop(0))
            self.step.set(preflist.pop(0))
            self.windsize.set(preflist.pop(0))
            self.graphheight.set(preflist.pop(0))
            self.maxy.set(preflist.pop(0))
            self.logit.set(preflist.pop(0))
            self.histo.set(preflist.pop(0))
            self.graphlinet.set(preflist.pop(0))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.poscol = (x, y, z)
            self.poscolhex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.negcol = (x, y, z)
            self.negcolhex = preflist.pop(0)
            self.ggap.set(preflist.pop(0))
            self.blastnDir = preflist.pop(0)
            if self.blastnDir == 'None':
                self.blastnDir = None
            self.dbnDir = preflist.pop(0).rstrip()
            if self.dbnDir == 'None':
                self.dbnDir = None
        except:
            self.defaultpreferences()

    def openhelpsite(self):
        webbrowser.open_new('https://github.com/mjsull/Easyfig/wiki')

    def openabout(self):
        try:
            self.aboutpanel.destroy()
        except:
            pass
        self.aboutpanel = Toplevel()
        self.frame7 = Frame(self.aboutpanel)
        self.about1label = Label(self.frame7, text='Easyfig', font='TkDefaultFont 13 bold')
        self.about1label.grid(row=0, column=0)
        self.about2label = Label(self.frame7, text='Easyfig is a Python application for creating linear\n\
comparison figures of multiple genomic loci\n with an easy-to-use graphical user interface (GUI).\n\n\
Version 2.2.3\n\nIf Easyfig is used to generate figures for publication,\n\
please cite our paper:\n\n\
Sullivan MJ, Petty NK, Beatson SA. (2011)\nEasyfig: a genome comparison visualiser.\nBioinformatics; 27 (7): 1009-1010')
        self.about2label.grid(row=1, column=0)
        self.frame7.grid(padx=10, pady=10)

    def supportwin(self):
        try:
            self.supportpanel.destroy()
        except:
            pass
        self.supportpanel = Toplevel()
        self.frame9 = Frame(self.supportpanel)
        self.about1label1 = Label(self.frame9, text='Easyfig', font='TkDefaultFont 13 bold')
        self.about1label1.grid(row=0, column=0)
        self.supportlabel2 = Label(self.frame9, text='written by Mitchell Sullivan - mjsull@gmail.com\n\
To submit a bug please visit https://github.com/mjsull/Easyfig/issues.')
        self.supportlabel2.grid(row=1, column=0)
        self.frame9.grid(padx=10, pady=10)


    def preferencewindow(self):
        try:
            self.prefwin.destroy()
        except:
            pass
        self.prefwin = Toplevel()
        self.frame8 = Frame(self.prefwin)
        self.prefwin.title('preferences')
        self.scrollbar3 = Scrollbar(self.frame8)
        self.preflist = Listbox(self.frame8, yscrollcommand=self.scrollbar3.set)
        templist = ['easyfig_standard']
        validfile = True
        if os.path.exists('.easyfig.pref'):
            preffile = open('.easyfig.pref')
            for line in preffile:
                if len(line.split('\t')) == 87:
                    templist.append(line.split('\t')[0])
                else:
                    validfile = False
        if not validfile:
            nocompare = tkMessageBox.askquestion('Preference file not valid', 'Do you wish to create a new preference file at ' + os.getcwd() + '/.easyfig.pref?', parent=self.frame8)
            if nocompare == 'no':
                return
            else:
                preffile = open('.easyfig.pref', 'w')
                preffile.close()
        templist.sort(key=str.lower)
        for i in templist:
            self.preflist.insert(END, i)
        self.preflist.grid(column=1, row=0, rowspan=10)
        self.scrollbar3.config(command=self.preflist.yview)
        self.scrollbar3.grid(column=0, row=0, rowspan=10, sticky=NS)
        self.addprefbut = Button(self.frame8, text='Save preferences as', command=self.addpref)
        self.addprefbut.grid(column=2, row=0, sticky=EW)
        self.loadprefbut = Button(self.frame8, text='Load preferences', command=self.loadpref)
        self.loadprefbut.grid(column=2, row=1, sticky=EW)
        self.removeprefbut = Button(self.frame8, text='Remove', command=self.removepref)
        self.removeprefbut.grid(column=2, row=2, sticky=EW)
        self.setdefaultbut = Button(self.frame8, text='Set as default', command=self.setdefault)
        self.setdefaultbut.grid(column=2, row=3, sticky=EW)
        self.closeprefwinbut = Button(self.frame8, text='close', command=self.closeprefwin)
        self.closeprefwinbut.grid(column=2, row=9, sticky=E)
        self.frame8.grid(padx=20, pady=20)

    def addpref(self):
        preffile = open('.easyfig.pref', 'a')
        savename = tkSimpleDialog.askstring('Input name', 'Please choose name to save preferences under.', parent=self.frame8)
        if savename == None:
            return None
        while savename in self.preflist.get(0, END):
            savename = tkSimpleDialog.askstring('Name taken', 'Please choose name to save preferences under.', parent=self.frame8)
            if savename == None:
                return None
        savestring = savename + '\t'
        savestring += self.filetype.get() + '\t'
        savestring += self.figwidthvar.get() + '\t'
        savestring += self.height1var.get() + '\t'
        savestring += self.height2var.get() + '\t'
        savestring += self.aln.get() + '\t'
        savestring += str(self.autodetect.get()) + '\t'
        savestring += str(self.drawfig1.get()) + '\t'
        savestring += self.drawfig2var.get() + '\t'
        savestring += self.minlengthvar.get() + '\t'
        savestring += self.minevalvar.get() + '\t'
        savestring += self.minIdentvar.get() + '\t'
        savestring += str(self.minblastc[0]) + '\t'
        savestring += str(self.minblastc[1]) + '\t'
        savestring += str(self.minblastc[2]) + '\t'
        savestring += self.minblastchex + '\t'
        savestring += str(self.minblastci[0]) + '\t'
        savestring += str(self.minblastci[1]) + '\t'
        savestring += str(self.minblastci[2]) + '\t'
        savestring += self.minblastcihex + '\t'
        savestring += str(self.maxblastc[0]) + '\t'
        savestring += str(self.maxblastc[1]) + '\t'
        savestring += str(self.maxblastc[2]) + '\t'
        savestring += self.maxblastchex + '\t'
        savestring += str(self.maxblastci[0]) + '\t'
        savestring += str(self.maxblastci[1]) + '\t'
        savestring += str(self.maxblastci[2]) + '\t'
        savestring += self.maxblastcihex + '\t'
        savestring += str(self.blastoutline.get()) + '\t'
        savestring += self.leg.get() + '\t'
        savestring += self.leg2.get() + '\t'
        savestring += self.legname.get() + '\t'
        savestring += self.gltvar.get() + '\t'
        savestring += self.exontvar.get() + '\t'
        savestring += self.genetvar.get() + '\t'
        savestring += str(self.genef.get()) + '\t'
        savestring += str(self.genefcolour[0]) + '\t'
        savestring += str(self.genefcolour[1]) + '\t'
        savestring += str(self.genefcolour[2]) + '\t'
        savestring += self.genefcolourhex + '\t'
        savestring += self.genefrect.get() + '\t'
        savestring += str(self.cdsf.get()) + '\t'
        savestring += str(self.cdsfcolour[0]) + '\t'
        savestring += str(self.cdsfcolour[1]) + '\t'
        savestring += str(self.cdsfcolour[2]) + '\t'
        savestring += self.cdsfcolourhex + '\t'
        savestring += self.cdsfrect.get() + '\t'
        savestring += str(self.trnaf.get()) + '\t'
        savestring += str(self.trnafcolour[0]) + '\t'
        savestring += str(self.trnafcolour[1]) + '\t'
        savestring += str(self.trnafcolour[2]) + '\t'
        savestring += self.trnafcolourhex + '\t'
        savestring += self.trnafrect.get() + '\t'
        savestring += str(self.miscf.get()) + '\t'
        savestring += str(self.miscfcolour[0]) + '\t'
        savestring += str(self.miscfcolour[1]) + '\t'
        savestring += str(self.miscfcolour[2]) + '\t'
        savestring += self.miscfcolourhex + '\t'
        savestring += self.miscfrect.get() + '\t'
        savestring += self.randfeat.get() + '\t'
        savestring += str(self.randf.get()) + '\t'
        savestring += str(self.randfcolour[0]) + '\t'
        savestring += str(self.randfcolour[1]) + '\t'
        savestring += str(self.randfcolour[2]) + '\t'
        savestring += self.randfcolourhex + '\t'
        savestring += self.randfrect.get() + '\t'
        savestring += self.graphtype.get() + '\t'
        savestring += str(self.allorone.get()) + '\t'
        savestring += self.graphfile.get() + '\t'
        savestring += self.step.get() + '\t'
        savestring += self.windsize.get() + '\t'
        savestring += self.graphheight.get() + '\t'
        savestring += self.maxy.get() + '\t'
        savestring += str(self.logit.get()) + '\t'
        savestring += self.histo.get() + '\t'
        savestring += self.graphlinet.get() + '\t'
        savestring += str(self.poscol[0]) + '\t'
        savestring += str(self.poscol[1]) + '\t'
        savestring += str(self.poscol[2]) + '\t'
        savestring += self.poscolhex + '\t'
        savestring += str(self.negcol[0]) + '\t'
        savestring += str(self.negcol[1]) + '\t'
        savestring += str(self.negcol[2]) + '\t'
        savestring += self.negcolhex + '\t'
        savestring += self.ggap.get() + '\t'
        if self.blastnDir == None:
            savestring += 'None\t'
        else:
            savestring += self.blastnDir + '\t'
        if self.dbnDir == None:
            savestring += 'None\n'
        else:
            savestring += self.dbnDir + '\n'
        if savestring.count('\t') == 86:
            if savestring.startswith('>'):
                tkMessageBox.showerror('Try again.', 'Please remove > from start of preference name.')
            else:
                preffile.write(savestring)
                self.preflist.insert(END, savename)
        else:
            tkMessageBox.showerror('Try again.', '<tab> character in variable, please remove.')
        preffile.close()

    def loadpref(self):
        try:
            prefname = self.preflist.get(ACTIVE)
            if prefname == 'easyfig_standard':
                self.defaultpreferences()
                return
            if not os.path.exists('.easyfig.pref'):
                tkMessageBox.showerror('Try again.', 'Where\'d the preference file go?')
                return
            preffile = open('.easyfig.pref')
            for line in preffile:
                splitline = line.split('\t')
                if splitline[0] == prefname:
                    preflist = splitline[1:]
            preffile.close()
            self.filetype.set(preflist.pop(0))

            self.figwidthvar.set(preflist.pop(0))
            self.height1var.set(preflist.pop(0))
            self.height2var.set(preflist.pop(0))
            self.aln.set(preflist.pop(0))
            self.autodetect.set(int(preflist.pop(0)))
            self.drawfig1.set(int(preflist.pop(0)))
            self.drawfig2var.set(preflist.pop(0))

            self.minlengthvar.set(preflist.pop(0))
            self.minevalvar.set(preflist.pop(0))
            self.minIdentvar.set(preflist.pop(0))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.minblastc = (x, y, z)
            self.minblastchex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.minblastci = (x, y, z)
            self.minblastcihex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.maxblastc = (x, y, z)
            self.maxblastchex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.maxblastci = (x, y, z)
            self.maxblastcihex = preflist.pop(0)
            self.blastoutline.set(int(preflist.pop(0)))

            self.leg.set(preflist.pop(0))
            self.leg2.set(preflist.pop(0))
            self.legname.set(preflist.pop(0))
            self.gltvar.set(preflist.pop(0))
            self.exontvar.set(preflist.pop(0))
            self.genetvar.set(preflist.pop(0))

            self.genef.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.genefcolour = (x, y, z)
            self.genefcolourhex = preflist.pop(0)
            self.genefrect.set(preflist.pop(0))

            self.cdsf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.cdsfcolour = (x, y, z)
            self.cdsfcolourhex = preflist.pop(0)
            self.cdsfrect.set(preflist.pop(0))

            self.trnaf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.trnafcolour = (x, y, z)
            self.trnafcolourhex = preflist.pop(0)
            self.trnafrect.set(preflist.pop(0))

            self.miscf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.miscfcolour = (x, y, z)
            self.miscfcolourhex = preflist.pop(0)
            self.miscfrect.set(preflist.pop(0))

            self.randfeat.set(preflist.pop(0))
            self.randf.set(int(preflist.pop(0)))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.randfcolour = (x, y, z)
            self.randfcolourhex = preflist.pop(0)
            self.randfrect.set(preflist.pop(0))

            self.graphtype.set(preflist.pop(0))
            self.allorone.set(int(preflist.pop(0)))
            self.graphfile.set(preflist.pop(0))
            self.step.set(preflist.pop(0))
            self.windsize.set(preflist.pop(0))
            self.graphheight.set(preflist.pop(0))
            self.maxy.set(preflist.pop(0))
            self.logit.set(preflist.pop(0))
            self.histo.set(preflist.pop(0))
            self.graphlinet.set(preflist.pop(0))
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.poscol = (x, y, z)
            self.poscolhex = preflist.pop(0)
            x = int(preflist.pop(0))
            y = int(preflist.pop(0))
            z = int(preflist.pop(0))
            self.negcol = (x, y, z)
            self.negcolhex = preflist.pop(0)
            self.ggap.set(preflist.pop(0))
            self.blastnDir = preflist.pop(0)
            if self.blastnDir == 'None':
                self.blastnDir = None
            self.dbnDir = preflist.pop(0).rstrip()
            if self.dbnDir == 'None':
                self.dbnDir = None
        except:
            self.defaultpreferences()
            tkMessageBox.showerror('Preference File Invalid', 'Loaded default preferences.')
            nocompare = tkMessageBox.askquestion('Preference file not valid', 'Do you wish to create a new preference file at ' + os.getcwd() + '/.easyfig.pref?', parent=self.frame8)
            if nocompare == 'no':
                return
            else:
                preffile = open('.easyfig.pref', 'w')
                preffile.close()
                self.preflist.delete(0, END)
                self.preflist.insert('easyfig_standard')

    def removepref(self):
        nocompare = tkMessageBox.askquestion('Delete?', 'Are you sure you wish to delete this preference?', parent=self.frame8)
        if nocompare == 'no':
            return
        preffile = open('.easyfig.pref')
        preflist = []
        prefname = self.preflist.get(ACTIVE)
        self.preflist.delete(ACTIVE)
        for line in preffile:
            if not line.split('\t')[0] == prefname:
                preflist.append(line)
        preffile.close()
        preffile = open('.easyfig.pref', 'w')
        for i in preflist:
            preffile.write(i)
        preffile.close()

    def setdefault(self):
        preffile = open('.easyfig.pref')
        preflist = []
        prefname = self.preflist.get(ACTIVE)
        if prefname.startswith('>'):
            return
        templist = []
        for line in preffile:
            if line.startswith('>'):
                line = line[1:]
            elif line.split('\t')[0] == prefname:
                line = '>' + line
            templist.append(line.split('\t')[0])
            preflist.append(line)
        preffile.close()
        preffile = open('.easyfig.pref', 'w')
        for i in preflist:
            preffile.write(i)
        self.preflist.delete(0, END)
        templist.append('easyfig_standard')
        templist.sort(key=str.lower)
        for i in templist:
            self.preflist.insert(END, i)
        preffile.close()

    def closeprefwin(self):
        self.prefwin.destroy()

    def openref(self):
        webbrowser.open_new('http://www.ncbi.nlm.nih.gov/pubmed/21278367')

    def pickposcol(self):
        colour = tkColorChooser.askcolor(self.poscol, parent=self.graphoptionswindow)
        if colour != None:
            self.poscol = colour[0]
            self.poscolhex = colour[1]
            self.poscollabel.configure(bg=colour[1])

    def picknegcol(self):
        colour = tkColorChooser.askcolor(self.negcol, parent=self.graphoptionswindow)
        if colour != None:
            self.negcol = colour[0]
            self.negcolhex = colour[1]
            self.negcollabel.configure(bg=colour[1])

    def getGCcontent(self, filename, mincut, maxcut):
        try:
            gen = open(filename)
            getseq = False
            getembl = False
            seq = ''
            for line in gen:
                if line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('SQ   Sequence'):
                    getembl = True
                elif line.startswith('//'):
                    getseq = False
                    getembl = False
                elif getseq:
                    seq += ''.join(line.split()[1:])
                elif getembl:
                    seq += ''.join(line.split()[:-1])
            gen.close()
            seq = seq.upper()
        except:
            tkMessageBox.showerror('Try again.', 'feature file ' + filename + ' not valid, or does not exist.')
            return None
        if len(seq) == 0:
            tkMessageBox.showerror('Try again.', 'Sequence not found in feature file ' + filename + '.')
            return None
        if maxcut == 'Max':
            seq = seq[int(mincut)-1:]
        elif int(maxcut) <= int(mincut):
            seq = seq[int(mincut)-1:] + seq[:int(maxcut)+1]
        else:
            seq = seq[int(mincut)-1:int(maxcut)+1]
        window1 = int(self.windsize.get()) / 2
        window2 = int(self.windsize.get()) - window1
        thearray = []
        for i in range(0, len(seq), int(self.step.get())):
            seqstring = seq[max([0, i-window1]):i+window2]
            thearray.append((seqstring.count('G') + seqstring.count('C')) * 1.0 / len(seqstring) - 0.5)
        return thearray

    def getGCskew(self, filename, mincut, maxcut):
        try:
            getseq = False
            getembl = False
            seq = ''
            gen = open(filename)
            for line in gen:
                if line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('SQ   Sequence'):
                    getembl = True
                elif line.startswith('//'):
                    getseq = False
                    getembl = False
                elif getseq:
                    seq += ''.join(line.split()[1:])
                elif getembl:
                    seq += ''.join(line.split()[:-1])
            gen.close()
            seq = seq.upper()
        except:
            tkMessageBox.showerror('Try again.', 'feature file ' + filename + ' not valid, or does not exist.')
            return None
        if len(seq) == 0:
            tkMessageBox.showerror('Try again.', 'Sequence not found in feature file ' + filename + '.')
            return None
        window1 = int(self.windsize.get()) / 2
        window2 = int(self.windsize.get()) - window1
        if maxcut == 'Max':
            seq = seq[int(mincut)-1:]
        elif int(maxcut) <= int(mincut):
            seq = seq[int(mincut)-1:] + seq[:int(maxcut)+1]
        else:
            seq = seq[int(mincut)-1:int(maxcut)+1]
        thearray = []
        for i in range(0, len(seq), int(self.step.get())):
            seqstring = seq[max([0, i-window1]):i+window2]
            gcount = seqstring.count('G')
            ccount = seqstring.count('C')
            try:
                thearray.append((gcount - ccount) * 1.0 / (gcount + ccount))
            except:
                thearray.append(0)
        return thearray

    def getCoverage(self):
    # DEFNIITION: takes a file and reads in all contigs, their start positions and the reads located within the contig
    # REQUIRES: a valid ace file
    # RETURNS: A list of objects of class contig
        seq = ''
        getseq = False
        getembl = False
        try:
            gen = open(self.gen1.get())
            for line in gen:
                if line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('SQ   Sequence'):
                    getembl = True
                elif line.startswith('//'):
                    getseq = False
                    getembl = False
                elif getseq:
                    seq += ''.join(line.split()[1:])
                elif getembl:
                    seq += ''.join(line.split()[:-1])
            gen.close()
        except:
            tkMessageBox.showerror('Try again.', 'feature file not valid, or does not exist.')
            return None
        if len(seq) == 0:
            tkMessageBox.showerror('Try again.', 'Sequence not found in feature file.')
            return None
        seq = seq.lower()
        if self.gen1maxcut.get() == 'Max':
            seq = seq[int(self.gen1mincut.get())-1:]
        elif int(self.gen1maxcut) <= int(self.gen1mincut):
            seq = seq[int(self.gen1mincut)-1:] + seq[:int(self.gen1maxcut)+1]
        else:
            seq = seq[int(self.gen1mincut.get())-1:(self.gen1maxcut.get())+1]
        outlist = [0 for i in range(len(seq))]
        readlist = [] # list of reads to be added to the contig class
        index = 0 # switches to 1 once program has dealt with the initial contig
        # iterates through the file determines what information is contained in each line then reads it to the
        # right locationregular expressions python
        transtab = string.maketrans('atgc', 'tacg')
        for line in file:
            # puts name in file and starts reading sequence below
            if line.startswith("CO "):
                if index != 0:
                    freqDict = {}
                    for j in readlist:
                        for k in range(j.startpos, (j.startpos + j.readLength)):
                            if k in freqDict:
                                freqDict[k] += 1
                            else:
                                freqDict[k] = 1
                    coverageList = []
                    for j in range(1, len(contigSeq) + 1):
                        if contigSeq[j - 1] != '*':
                            coverageList.append(freqDict[j])
                    contigSeq = contigSeq.lower()
                    thepos = seq.find(contigSeq)
                    if thepos != -1:
                        outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
                    else:
                        contigSeq = contigSeq[::-1]
                        contigSeq = contigSeq.translate(transtab)
                        thepos = seq.find(contigSeq)
                        if thepos != -1:
                            coverageList.reverse()
                            outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
                    readlist = []
                index = 1
                contigSeq = ''
                contigName = line.split()[1] # splits the line into a list with elements seperated by whitespace characters
                                          # then returns the second element of that list (the name)
                readnumber = 0 # initiates the read number used to determine where the readsequence will be added
          # creates a object of class read with the name and location within the contig, leaves sequence as the
          # empty string to be read in later
            elif line.startswith('BQ'):
                index = 2
            elif line.startswith("AF "):
                readIt = line.split() # splits the line into a list of strings seperated by whitespace characters
                readName = readIt[1] # the name of the read
                readPos = int(readIt[3]) # the position of the read within the contig
                readInstance = read(readName, readPos, None) # creates an instance of class read
                readlist.append(readInstance) # appends to list
            elif index == 1:
                contigSeq += line[:-1]
            elif line.startswith("QA "):
                readlist[readnumber].startpos = readlist[readnumber].startpos + int(line.split()[1]) - 1
                readlist[readnumber].readLength = int(line.split()[2]) - int(line.split()[1]) + 1
                readnumber += 1
        freqDict = {}
        for j in readlist:
            for k in range(j.startpos, (j.startpos + j.readLength)):
                if k in freqDict:
                    freqDict[k] += 1
                else:
                    freqDict[k] = 1
        coverageList = []
        for j in range(1, len(contigSeq) + 1):
            if contigSeq[j - 1] != '*':
                coverageList.append(freqDict[j])
        contigSeq = contigSeq.lower()
        thepos = seq.find(contigSeq)
        if thepos != -1:
            outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
        else:
            contigSeq = contigSeq[::-1]
            contigSeq = contigSeq.translate(transtab)
            thepos = seq.find(contigSeq)
            if thepos != -1:
                coverageList.reverse()
                outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
        return outlist

    def getCustom(self):
        try:
            thearray = []
            gen = open(self.graphfile.get())
            templine = gen.readline().rstrip().split('\t')
            linelen = len(templine)
            for i in templine:
                thearray.append([float(i)])
            for line in gen:
                templine = line.rstrip().split('\t')
                for i in range(len(templine)):
                    if templine[i] != '':
                        thearray[i].append(float(templine[i]))
            return thearray
        except:
            tkMessageBox.showerror('Try again.', 'graph file not valid, or does not exist.')
            return None

    def graphtypechanges(self, something):
        if something == 'None':
            self.alloroneentry.config(state=DISABLED)
            self.graphfileentry.config(state=DISABLED)
            self.graphfilebut.config(state=DISABLED)
            self.stepentry.config(state=DISABLED)
            self.windsizeentry.config(state=DISABLED)
            self.graphheightentry.config(state=DISABLED)
            self.maxyentry.config(state=DISABLED)
            self.histoentry.config(state=DISABLED)
            self.graphlinetentry.config(state=DISABLED)
            self.poscolbutton.config(state=DISABLED)
            self.negcolbutton.config(state=DISABLED)
            self.logitbut.config(state=DISABLED)
            self.ggapentry.config(state=DISABLED)
        elif something == 'GC Content':
            self.alloroneentry.config(state=NORMAL)
            self.graphfileentry.config(state=DISABLED)
            self.graphfilebut.config(state=DISABLED)
            self.stepentry.config(state=NORMAL)
            self.windsizeentry.config(state=NORMAL)
            self.graphheightentry.config(state=NORMAL)
            self.maxyentry.config(state=NORMAL)
            self.histoentry.config(state=NORMAL)
            self.graphlinetentry.config(state=NORMAL)
            self.poscolbutton.config(state=NORMAL)
            self.negcolbutton.config(state=NORMAL)
            self.logitbut.config(state=DISABLED)
            self.ggapentry.config(state=NORMAL)
        elif something == 'GC Skew':
            self.alloroneentry.config(state=NORMAL)
            self.graphfileentry.config(state=DISABLED)
            self.graphfilebut.config(state=DISABLED)
            self.stepentry.config(state=NORMAL)
            self.windsizeentry.config(state=NORMAL)
            self.graphheightentry.config(state=NORMAL)
            self.maxyentry.config(state=NORMAL)
            self.histoentry.config(state=NORMAL)
            self.graphlinetentry.config(state=NORMAL)
            self.poscolbutton.config(state=NORMAL)
            self.negcolbutton.config(state=NORMAL)
            self.logitbut.config(state=DISABLED)
            self.ggapentry.config(state=NORMAL)
        elif something == 'Coverage':
            self.alloroneentry.config(state=DISABLED)
            self.graphfileentry.config(state=NORMAL)
            self.graphfilebut.config(state=NORMAL)
            self.stepentry.config(state=DISABLED)
            self.windsizeentry.config(state=NORMAL)
            self.graphheightentry.config(state=NORMAL)
            self.maxyentry.config(state=NORMAL)
            self.histoentry.config(state=NORMAL)
            self.graphlinetentry.config(state=NORMAL)
            self.poscolbutton.config(state=NORMAL)
            self.negcolbutton.config(state=DISABLED)
            self.logitbut.config(state=NORMAL)
            self.ggapentry.config(state=NORMAL)
        elif something == 'Custom':
            self.alloroneentry.config(state=NORMAL)
            self.graphfileentry.config(state=NORMAL)
            self.graphfilebut.config(state=NORMAL)
            self.stepentry.config(state=DISABLED)
            self.windsizeentry.config(state=DISABLED)
            self.graphheightentry.config(state=NORMAL)
            self.maxyentry.config(state=NORMAL)
            self.histoentry.config(state=NORMAL)
            self.graphlinetentry.config(state=NORMAL)
            self.poscolbutton.config(state=NORMAL)
            self.negcolbutton.config(state=NORMAL)
            self.logitbut.config(state=NORMAL)
            self.ggapentry.config(state=NORMAL)

    def figureoptions(self):
        try:
            self.figureoptionswindow.destroy()
        except:
            pass
        self.figureoptionswindow = Toplevel()
        self.figureoptionswindow.title('Figure')
        self.frame2 = Frame(self.figureoptionswindow)
        self.mainoptionslab = Label(self.frame2, text='Figure Options', font='TkDefaultFont 13 bold underline')
        self.mainoptionslab.grid(row=0, column=0)
        self.figwidthlabel = Label(self.frame2, text='Width of Figure (pixels):')
        self.figwidthlabel.grid(row=1, column=0)
        self.figwidthentry = Entry(self.frame2, textvariable=self.figwidthvar)
        self.figwidthentry.grid(row=1, column=1)
        self.gltlabel = Label(self.frame2, text='Thickness of genome line:')
        self.gltlabel.grid(row=2, column=0)
        self.gltentry = Entry(self.frame2, textvariable=self.gltvar)
        self.gltentry.grid(row=2, column=1)
        self.height1label = Label(self.frame2, text='Height of genes in figure:')
        self.height1label.grid(row=3, column=0)
        self.height1entry = Entry(self.frame2, textvariable=self.height1var)
        self.height1entry.grid(row=3, column=1)
        self.height2label = Label(self.frame2, text='Height of Blast hits in figure:')
        self.height2label.grid(row=4, column=0)
        self.height2entry = Entry(self.frame2, textvariable=self.height2var)
        self.height2entry.grid(row=4, column=1)
        self.alnlabel = Label(self.frame2, text='Alignment of genomes:')
        self.alnlabel.grid(row=5, column=0)
        self.alnentry = OptionMenu(self.frame2, self.aln, 'left', 'centre', 'right', 'best blast')
        self.alnentry.config(width=5)
        self.alnentry.grid(row=5, column=1, sticky=EW)
        self.legendoptionslab = Label(self.frame2, text='Legend Options', font='TkDefaultFont 13 bold')
        self.legendoptionslab.grid(row=6, column=0)
        self.drawfig1label = Label(self.frame2, text='Draw Blast identity legend?')
        self.drawfig1label.grid(row=7, column=0)
        self.drawfig1entry = Checkbutton(self.frame2, variable=self.drawfig1)
        self.drawfig1entry.grid(row=7, column=1)
        self.drawfig2label = Label(self.frame2, text='Length of scale legend (in base pairs):')
        self.drawfig2label.grid(row=8, column=0)
        self.drawfig2entry = Entry(self.frame2, textvariable=self.drawfig2var)
        self.drawfig2entry.grid(row=8, column=1)
        self.leg2label = Label(self.frame2, text='Feature Legend:')
        self.leg2label.grid(row=9, column=0)
        self.leg2entry = OptionMenu(self.frame2, self.leg2, 'None', 'Single column', 'Two columns')
        self.leg2entry.grid(row=9, column=1, sticky=EW)
        self.legnamelabel = Label(self.frame2, text='Get feature name from')
        self.legnamelabel.grid(row=10, column=0)
        self.legnameentry = OptionMenu(self.frame2, self.legname, 'gene', 'product', 'locus_tag', 'note')
        self.legnameentry.grid(row=10, column=1, sticky=EW)
        self.figureoptionsclosebutton = Button(self.frame2, text='close', command=self.figureoptionsclose)
        self.figureoptionsclosebutton.grid(row=11, column=1, sticky=E, pady=5)
        self.figureoptionswindow.geometry('+30+40')
        self.frame2.grid(padx=30, pady=10)

    def figureoptionsclose(self):
        self.figureoptionswindow.destroy()


    def blastoptions(self):
        try:
            self.blastoptionswindow.destroy()
        except:
            pass
        self.blastoptionswindow = Toplevel()
        self.blastoptionswindow.title('Blast')
        self.frame3 = Frame(self.blastoptionswindow)
        self.blastoptionslab = Label(self.frame3, text='Blast Options', font='TkDefaultFont 13 bold underline')
        self.blastoptionslab.grid(row=0, column=0)
        self.minlengthlabel = Label(self.frame3, text='Min. length:')
        self.minlengthlabel.grid(row=1, column=0)
        self.minlengthentry = Entry(self.frame3, textvariable=self.minlengthvar)
        self.minlengthentry.grid(row=1, column=1, columnspan=4)
        self.minevallabel = Label(self.frame3, text='Max. e Value:')
        self.minevallabel.grid(row=2, column=0)
        self.minevalentry = Entry(self.frame3, textvariable=self.minevalvar)
        self.minevalentry.grid(row=2, column=1, columnspan=4)
        self.minIdentlabel = Label(self.frame3, text='Min. Identity value:')
        self.minIdentlabel.grid(row=3, column=0)
        self.minIdententry = Entry(self.frame3, textvariable=self.minIdentvar)
        self.minIdententry.grid(row=3, column=1, columnspan=4)
        self.blastlabel = Label(self.frame3, text='normal')
        self.blastlabel.grid(row=4, column=1, columnspan=2)
        self.blastilabel = Label(self.frame3, text='inverted')
        self.blastilabel.grid(row=4, column=3, columnspan=2)
        self.minblastctag = Label(self.frame3, text='Choose minimum blast colour:')
        self.minblastctag.grid(row=5, column=0)
        self.minblastcentry = Button(self.frame3, text='...', command=self.getminblastc)
        self.minblastcentry.grid(row=5, column=2)
        self.minblastclabel = Label(self.frame3, width=3, bg=self.minblastchex, relief=RIDGE)
        self.minblastclabel.grid(row=5, column=1)
        self.minblastcentryi = Button(self.frame3, text='...', command=self.getminblastci)
        self.minblastcentryi.grid(row=5, column=4)
        self.minblastclabeli = Label(self.frame3, width=3, bg=self.minblastcihex, relief=RIDGE)
        self.minblastclabeli.grid(row=5, column=3)
        self.maxblastctag = Label(self.frame3, text='Choose maximum blast colour:')
        self.maxblastctag.grid(row=6, column=0)
        self.maxblastcentry = Button(self.frame3, text='...', command=self.getmaxblastc)
        self.maxblastcentry.grid(row=6, column=2)
        self.maxblastclabel = Label(self.frame3, width=3, bg=self.maxblastchex, relief=RIDGE)
        self.maxblastclabel.grid(row=6, column=1)
        self.maxblastcentryi = Button(self.frame3, text='...', command=self.getmaxblastci)
        self.maxblastcentryi.grid(row=6, column=4)
        self.maxblastclabeli = Label(self.frame3, width=3, bg=self.maxblastcihex, relief=RIDGE)
        self.maxblastclabeli.grid(row=6, column=3)
        self.blastoutlinetag = Label(self.frame3, text='Outline blast hits in black:')
        self.blastoutlinetag.grid(row=7, column=0)
        self.blastoutlineentry = Checkbutton(self.frame3, variable=self.blastoutline)
        self.blastoutlineentry.grid(row=7, column=1, columnspan=4)
        self.autodetectlab = Label(self.frame3, text='Filter small blast hits/annotations:')
        self.autodetectlab.grid(row=8, column=0)
        self.autodetectentry = Checkbutton(self.frame3, variable=self.autodetect)
        self.autodetectentry.grid(row=8, column=1, columnspan=4)
        self.blastoptionsclosebutton = Button(self.frame3, text='close', command=self.blastoptionsclose)
        self.blastoptionsclosebutton.grid(row=9, column=1, columnspan=4, sticky=E, pady=5)
        self.blastoptionswindow.geometry('+30+40')
        self.frame3.grid(padx=30, pady=10)

    def blastoptionsclose(self):
        self.blastoptionswindow.destroy()


    def annotateoptions(self):
        try:
            self.annotateoptionswindow.destroy()
        except:
            pass
        self.annotateoptionswindow = Toplevel()
        self.annotateoptionswindow.title('Annotation')
        self.frame4 = Frame(self.annotateoptionswindow)
        self.annotLab = Label(self.frame4, text='Annotation Options', font='TkDefaultFont 13 bold underline')
        self.annotLab.grid(row=0, column=0)
        self.leglabel = Label(self.frame4, text='Feature Labels:')
        self.leglabel.grid(row=1, column=0)
        self.leg = StringVar(value='None')
        self.legentry = OptionMenu(self.frame4, self.leg, 'None', 'Top', 'Bottom', 'Top & Bottom')
        self.legentry.config(width=5)
        self.legentry.grid(row=1, column=1, columnspan=4, sticky=EW)
        self.legnamelabel = Label(self.frame4, text='Get feature name from:')
        self.legnamelabel.grid(row=2, column=0)
        self.legnameentry = OptionMenu(self.frame4, self.legname, 'gene', 'product', 'locus_tag', 'note')
        self.legnameentry.grid(row=2, column=1, columnspan=4, sticky=EW)
        self.exontlabel = Label(self.frame4, text='Thickness of exon lines:')
        self.exontlabel.grid(row=3, column=0)
        self.exontentry = Entry(self.frame4, textvariable=self.exontvar)
        self.exontentry.grid(row=3, column=1, columnspan=4)
        self.genetlabel = Label(self.frame4, text='Thickness of gene outlines:')
        self.genetlabel.grid(row=4, column=0)
        self.genetentry = Entry(self.frame4, textvariable=self.genetvar)
        self.genetentry.grid(row=4, column=1, columnspan=4)

        self.featlabel = Label(self.frame4, text='Include following features', font='TkDefaultFont 13 bold')
        self.featlabel.grid(row=5, column=0)
        self.featcolour = Label(self.frame4, text='Colour', font='TkDefaultFont 13 bold')
        self.featcolour.grid(row=5, column=1, columnspan=2)
        self.featshape = Label(self.frame4, text='type', font='TkDefaultFont 13 bold')
        self.featshape.grid(row=5, column=3, columnspan=2)

        self.geneflabel = Label(self.frame4, text='gene')
        self.geneflabel.grid(row=6, column=0)
        self.genefentry = Checkbutton(self.frame4, variable=self.genef)
        self.genefentry.grid(row=6, column=0, sticky=E)
        self.genefcolourBut = Button(self.frame4, width=1, height=1, text='...', command=self.pickcolourgene)
        self.genefcolourBut.grid(row=6, column=2)
        self.genefcolourlabel = Label(self.frame4, width=3, bg=self.genefcolourhex, relief=RIDGE)
        self.genefcolourlabel.grid(row=6, column=1)
        self.genefrectentry = OptionMenu(self.frame4, self.genefrect, 'arrow', 'rect', 'frame', 'pointer')
        self.genefrectentry.config(width=10)
        self.genefrectentry.grid(row=6, column=3, columnspan=2, sticky=EW)

        self.cdsflabel = Label(self.frame4, text='CDS')
        self.cdsflabel.grid(row=7, column=0)
        self.cdsfentry = Checkbutton(self.frame4, variable=self.cdsf)
        self.cdsfentry.grid(row=7, column=0, sticky=E)
        self.cdsfcolourBut = Button(self.frame4, width=1, height=1, text='...', command=self.pickcolourcds)
        self.cdsfcolourBut.grid(row=7, column=2)
        self.cdsfcolourlabel = Label(self.frame4, width=3, bg=self.cdsfcolourhex, relief=RIDGE)
        self.cdsfcolourlabel.grid(row=7, column=1)
        self.cdsfrectentry = OptionMenu(self.frame4, self.cdsfrect, 'arrow', 'rect', 'frame', 'pointer')
        self.cdsfrectentry.config(width=6)
        self.cdsfrectentry.grid(row=7, column=3, columnspan=2, sticky=EW)

        self.trnaflabel = Label(self.frame4, text='tRNA')
        self.trnaflabel.grid(row=8, column=0)
        self.trnafentry = Checkbutton(self.frame4, variable=self.trnaf)
        self.trnafentry.grid(row=8, column=0, sticky=E)
        self.trnafcolourBut = Button(self.frame4, width=1, height=1, text='...', command=self.pickcolourtrna)
        self.trnafcolourBut.grid(row=8, column=2)
        self.trnafcolourlabel = Label(self.frame4, width=3, bg=self.trnafcolourhex, relief=RIDGE)
        self.trnafcolourlabel.grid(row=8, column=1)
        self.trnafrectentry = OptionMenu(self.frame4, self.trnafrect, 'arrow', 'rect', 'frame', 'pointer')
        self.trnafrectentry.config(width=6)
        self.trnafrectentry.grid(row=8, column=3, columnspan=2, sticky=EW)

        self.miscflabel = Label(self.frame4, text='misc_feature')
        self.miscflabel.grid(row=9, column=0)
        self.miscfentry = Checkbutton(self.frame4, variable=self.miscf)
        self.miscfentry.grid(row=9, column=0, sticky=E)
        self.miscfcolourBut = Button(self.frame4, width=1, height=1, text='...', command=self.pickcolourmisc)
        self.miscfcolourBut.grid(row=9, column=2)
        self.miscfcolourlabel = Label(self.frame4, width=3, bg=self.miscfcolourhex, relief=RIDGE)
        self.miscfcolourlabel.grid(row=9, column=1)
        self.miscfrectentry = OptionMenu(self.frame4, self.miscfrect, 'arrow', 'rect', 'frame', 'pointer')
        self.miscfrectentry.config(width=6)
        self.miscfrectentry.grid(row=9, column=3, columnspan=2, sticky=EW)

        self.randflabel = Entry(self.frame4, textvariable=self.randfeat)
        self.randflabel.grid(row=10, column=0)
        self.randfentry = Checkbutton(self.frame4, variable=self.randf)
        self.randfentry.grid(row=10, column=0, sticky=E)
        self.randfcolourBut = Button(self.frame4, width=1, height=1, text='...', command=self.pickcolourrand)
        self.randfcolourBut.grid(row=10, column=2)
        self.randfcolourlabel = Label(self.frame4, width=3, bg=self.randfcolourhex, relief=RIDGE)
        self.randfcolourlabel.grid(row=10, column=1)
        self.randfrectentry = OptionMenu(self.frame4, self.randfrect, 'arrow', 'rect', 'frame', 'pointer')
        self.randfrectentry.config(width=6)
        self.randfrectentry.grid(row=10, column=3, columnspan=2, sticky=EW)
        self.annotateoptionsclosebutton = Button(self.frame4, text='close', command=self.annotateoptionsclose)
        self.annotateoptionsclosebutton.grid(row=11, column=3, columnspan=2, sticky=E, pady=5)
        self.annotateoptionswindow.geometry('+30+40')
        self.frame4.grid(padx=30, pady=10)

    def annotateoptionsclose(self):
        self.annotateoptionswindow.destroy()


    def graphoptions(self):
        try:
            self.graphoptionswindow.destroy()
        except:
            pass
        self.graphoptionswindow = Toplevel()
        self.graphoptionswindow.title('Graph')
        self.frame5 = Frame(self.graphoptionswindow)
        self.graphlabel = Label(self.frame5, text='Graph options', font='TkDefaultFont 13 bold')
        self.graphlabel.grid(row=0, column=0)

        self.graphtypelabel = Label(self.frame5, text='Graph:')
        self.graphtypelabel.grid(row=1, column=0)
        self.graphtypeentry = OptionMenu(self.frame5, self.graphtype, 'None', 'GC Content', 'GC Skew', 'Coverage', 'Custom', command=self.graphtypechanges)
        self.graphtypeentry.grid(row=1, column=1)

        self.alloronelabel = Label(self.frame5, text='Multiple graphs:')
        self.alloronelabel.grid(row=2, column=0)
        self.alloroneentry = Checkbutton(self.frame5, variable=self.allorone, state=DISABLED)
        self.alloroneentry.grid(row=2, column=1)

        self.graphfilelabel = Label(self.frame5, text='Input file:')
        self.graphfilelabel.grid(row=3, column=0)
        self.graphfileentry = Entry(self.frame5, textvariable=self.graphfile, state=DISABLED)
        self.graphfileentry.grid(row=3, column=1)
        self.graphfilebut = Button(self.frame5, width=1, height=1, text='...', command=self.opengraphfile, state=DISABLED)
        self.graphfilebut.grid(row=3, column=2)

        self.steplabel = Label(self.frame5, text='Step size:')
        self.steplabel.grid(row=4, column=0)
        self.stepentry = Entry(self.frame5, textvariable=self.step, state=DISABLED)
        self.stepentry.grid(row=4, column=1)

        self.windsizelabel = Label(self.frame5, text='Window size:')
        self.windsizelabel.grid(row=5, column=0)
        self.windsizeentry = Entry(self.frame5, textvariable=self.windsize, state=DISABLED)
        self.windsizeentry.grid(row=5, column=1)

        self.graphheightlabel = Label(self.frame5, text='Graph Height:')
        self.graphheightlabel.grid(row=6, column=0)
        self.graphheightentry = Entry(self.frame5, textvariable=self.graphheight, state=DISABLED)
        self.graphheightentry.grid(row=6, column=1)

        self.maxylabel = Label(self.frame5, text='Maximum Y:')
        self.maxylabel.grid(row=7, column=0)
        self.maxyentry = Entry(self.frame5, textvariable=self.maxy, state=DISABLED)
        self.maxyentry.grid(row=7, column=1)

        self.logitlabel = Label(self.frame5, text='Log scale (log10):')
        self.logitlabel.grid(row=8, column=0)
        self.logitbut = Checkbutton(self.frame5, variable=self.logit, state=DISABLED)
        self.logitbut.grid(row=8, column=1)

        self.histolabel = Label(self.frame5, text='Graph Type:')
        self.histolabel.grid(row=9, column=0)
        self.histoentry = OptionMenu(self.frame5, self.histo, 'Histogram', 'Line')
        self.histoentry.config(state=DISABLED)
        self.histoentry.grid(row=9, column=1)

        self.graphlinetlabel = Label(self.frame5, text='Axis line thickness:')
        self.graphlinetlabel.grid(row=10, column=0)
        self.graphlinetentry = Entry(self.frame5, textvariable=self.graphlinet, state=DISABLED)
        self.graphlinetentry.grid(row=10, column=1)

        self.poslabel = Label(self.frame5, text='Positive value colour:')
        self.poslabel.grid(row=11, column=0)
        self.poscollabel = Label(self.frame5, width=3, bg=self.poscolhex, relief=RIDGE)
        self.poscollabel.grid(row=11, column=1, sticky=EW)
        self.poscolbutton = Button(self.frame5, width=1, height=1, text='...', command=self.pickposcol, state=DISABLED)
        self.poscolbutton.grid(row=11, column=2)

        self.neglabel = Label(self.frame5, text='Negative value colour:')
        self.neglabel.grid(row=12, column=0)
        self.negcollabel = Label(self.frame5, width=3, bg=self.negcolhex, relief=RIDGE)
        self.negcollabel.grid(row=12, column=1, sticky=EW)
        self.negcolbutton = Button(self.frame5, width=1, height=1, text='...', command=self.picknegcol, state=DISABLED)
        self.negcolbutton.grid(row=12, column=2)

        self.ggaplabel = Label(self.frame5, text='Gap between graph and figure:')
        self.ggaplabel.grid(row=13, column=0)
        self.ggapentry = Entry(self.frame5, textvariable=self.ggap, state=DISABLED)
        self.ggapentry.grid(row=13, column=1)

        self.graphoptionsclosebutton = Button(self.frame5, text='close', command=self.graphoptionsclose)
        self.graphoptionsclosebutton.grid(row=14, column=1, columnspan=2, sticky=E, pady=5)
        self.graphoptionswindow.geometry('+30+40')
        self.graphtypechanges(self.graphtype.get())
        self.frame5.grid(padx=30, pady=10)

    def graphoptionsclose(self):
        self.graphoptionswindow.destroy()

    def opengraphfile(self):
        filename = tkFileDialog.askopenfilename(parent=self.graphoptionswindow)
        self.graphfile.set(filename)


    def pickcolourgene(self):
        colour = tkColorChooser.askcolor(self.genefcolour, parent=self.annotateoptionswindow)
        if colour != None:
            self.genefcolour = colour[0]
            self.genefcolourhex = colour[1]
            self.genefcolourlabel.configure(bg=colour[1])

    def pickcolourcds(self):
        colour = tkColorChooser.askcolor(self.cdsfcolour, parent=self.annotateoptionswindow)
        if colour != None:
            self.cdsfcolour = colour[0]
            self.cdsfcolourhex = colour[1]
            self.cdsfcolourlabel.configure(bg=colour[1])

    def pickcolourtrna(self):
        colour = tkColorChooser.askcolor(self.trnafcolour, parent=self.annotateoptionswindow)
        if colour != None:
            self.trnafcolour = colour[0]
            self.trnafcolourhex = colour[1]
            self.trnafcolourlabel.configure(bg=colour[1])

    def pickcolourrand(self):
        colour = tkColorChooser.askcolor(self.randfcolour, parent=self.annotateoptionswindow)
        if colour != None:
            self.randfcolour = colour[0]
            self.randfcolourhex = colour[1]
            self.randfcolourlabel.configure(bg=colour[1])

    def pickcolourmisc(self):
        colour = tkColorChooser.askcolor(self.miscfcolour, parent=self.annotateoptionswindow)
        if colour != None:
            self.miscfcolour = colour[0]
            self.miscfcolourhex = colour[1]
            self.miscfcolourlabel.configure(bg=colour[1])

    def getminblastc(self):
        colour = tkColorChooser.askcolor(self.minblastc, parent=self.blastoptionswindow)
        if colour != None:
            self.minblastc = colour[0]
            self.minblastchex = colour[1]
            self.minblastclabel.configure(bg=colour[1])

    def getmaxblastc(self):
        colour = tkColorChooser.askcolor(self.maxblastc, parent=self.blastoptionswindow)
        if colour != None:
            self.maxblastc = colour[0]
            self.maxblastchex = colour[1]
            self.maxblastclabel.configure(bg=colour[1])

    def getminblastci(self):
        colour = tkColorChooser.askcolor(self.minblastci, parent=self.blastoptionswindow)
        if colour != None:
            self.minblastci = colour[0]
            self.minblastcihex = colour[1]
            self.minblastclabeli.configure(bg=colour[1])

    def getmaxblastci(self):
        colour = tkColorChooser.askcolor(self.maxblastci, parent=self.blastoptionswindow)
        if colour != None:
            self.maxblastci = colour[0]
            self.maxblastcihex = colour[1]
            self.maxblastclabeli.configure(bg=colour[1])

    def makeFigure(self):
        global abortCaptain
        if self.outfile.get() == '' and not self.filetype.get().startswith('Preview'):
            self.getoutfile()
        if self.outfile.get() == '' and not self.filetype.get().startswith('Preview'):
            return None
        try:
            if self.thegenblast.isAlive():
                tkMessageBox.showerror('Please wait', 'BLAST already running.')
                return None
        except:
            pass
        if self.running:
            abortCaptain = True
        else:
            abortCaptain = False
            self.running = True
            self.createFigure.config(text='Cancel Figure')
            try:
                self.minlength = int(self.minlengthvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for minimum length.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.mineval = float(self.minevalvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid floating point number for minimum e value.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.minIdent = float(self.minIdentvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid floating point number for minimum identity.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.figwidth = int(self.figwidthvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for figure width.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.height1 = int(self.height1var.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for height of genes.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.height2 = int(self.height2var.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for height of blast matches.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.glt = int(self.gltvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for genome line thickness.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.exont = int(self.exontvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for exon line thickeness.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.genet = int(self.genetvar.get())
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for exon line thickeness.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            self.featDict = {}
            if self.genef.get() == 1:
                self.featDict['gene'] = (self.genefrect.get(), self.genefcolour)
            if self.cdsf.get() == 1:
                self.featDict['CDS'] = (self.cdsfrect.get(), self.cdsfcolour)
            if self.trnaf.get() == 1:
                self.featDict['tRNA'] = (self.trnafrect.get(), self.trnafcolour)
            if self.miscf.get() == 1:
                self.featDict['misc_feature'] = (self.miscfrect.get(), self.miscfcolour)
            if self.randf.get() == 1:
                self.featDict[self.randfeat.get()] = (self.randfrect.get(), self.randfcolour)
            self.reverseList = []
            self.minmaxlist = []
            for i in self.genlist.get(0, END):
                self.reverseList.append(self.revlist[i[:2]])
                try:
                    if self.maxcutlist[i[:2]] == 'Max':
                        self.minmaxlist.append((int(self.mincutlist[i[:2]]), 'Max'))
                    else:
                        self.minmaxlist.append((int(self.mincutlist[i[:2]]), int(self.maxcutlist[i[:2]])))
                except:
                    tkMessageBox.showerror('Try again.', 'Please enter a valid integer cut off points for annotation file ' + i[:2] + '.')
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
            if self.graphtype.get() != 'None' and (self.leg.get() == 'Top' or self.leg.get() == 'Top & Bottom'):
                tkMessageBox.showerror('Try again.', 'Please Choose either the graph or the legend to be displayed above the figure.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            if self.leg.get() != 'None' and self.leg2.get() != 'None':
                tkMessageBox.showerror('Try again.', 'Please Choose either feature labels or a feature legend.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            else:
                if self.leg.get() == 'None':
                    self.theleg = self.leg2.get()
                else:
                    self.theleg = self.leg.get()
            self.inputlist = []
            self.graphlist = []
            getit = True
            nocompare = False
            if self.genlist.size() > 1 and self.blastlist.size() == 0:
                nocompare = tkMessageBox.askquestion('No blast files.', 'Only gene figures will be drawn, continue?\n(To create a comparison figure please generate or manually input a blast file)')
                if nocompare == 'no':
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
                else:
                    nocompare = True
            if self.genlist.size() > 0:
                if self.graphtype.get() == 'GC Content':
                    self.graphlist.append(self.getGCcontent(self.genlist.get(0)[4:], self.mincutlist[self.genlist.get(0)[:2]], self.maxcutlist[self.genlist.get(0)[:2]]))
                elif self.graphtype.get() == 'GC Skew':
                    self.graphlist.append(self.getGCskew(self.genlist.get(0)[4:], self.mincutlist[self.genlist.get(0)[:2]], self.maxcutlist[self.genlist.get(0)[:2]]))
                self.inputlist.append(self.genlist.get(0)[4:])
                tempfile = open(self.genlist.get(0)[4:])
                getline = True
                line = tempfile.readline()
                while getline and line != '':
                    if line.startswith('FT   source') or line.startswith('     source')\
                    or line.startswith('ORIGIN') or line.startswith('SQ   Sequence') or line.startswith('>'):
                        getline = False
                    line = tempfile.readline()
                if getline:
                    self.genlengths = [tkSimpleDialog.askinteger('Length not in file', 'Please enter the length of genome in file 1')]
                else:
                    self.genlengths = [None]
                tempfile.close()
            else:
                tkMessageBox.showerror('Try again.', 'Please enter at least one feature file.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            if self.genlist.size() - 1 == self.blastlist.size() or nocompare:
                for i in range(self.genlist.size() - 1):
                    self.inputlist.append(self.blastlist.get(i))
                    if self.graphtype.get() == 'GC Content' and self.allorone.get() == 1:
                        self.graphlist.append(self.getGCcontent(self.genlist.get(i + 1)[4:], self.mincutlist[self.genlist.get(i + 1)[:2]], self.maxcutlist[self.genlist.get(i + 1)[:2]]))
                    elif self.graphtype.get() == 'GC Skew' and self.allorone.get() == 1:
                        self.graphlist.append(self.getGCcontent(self.genlist.get(i + 1)[4:], self.mincutlist[self.genlist.get(i + 1)[:2]], self.maxcutlist[self.genlist.get(i + 1)[:2]]))
                    self.inputlist.append(self.genlist.get(i + 1)[4:])
                    tempfile = open(self.genlist.get(i + 1)[4:])
                    getline = True
                    line = tempfile.readline()
                    while getline and line != '':
                        if line.startswith('FT   source') or line.startswith('     source')\
                        or line.startswith('ORIGIN') or line.startswith('SQ   Sequence') or line.startswith('>'):
                            getline = False
                        line = tempfile.readline()
                    if getline:
                        self.genlengths.append(tkSimpleDialog.askinteger('Length not in file', 'Please enter the length of genome in file ' + str(i + 1) + '.'))
                    else:
                        self.genlengths.append(None)
                    tempfile.close()
            else:
                if self.blastlist.size() >= self.genlist.size():
                    tkMessageBox.showerror('Try again.', 'Too many blast files.')
                else:
                    tkMessageBox.showerror('Try again.', 'Too few blast files.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            try:
                self.drawfig2 = int(self.drawfig2var.get())
                if self.drawfig2 == 0:
                    self.drawfig2 = False
            except:
                tkMessageBox.showerror('Try again.', 'Please enter a valid integer for length of figure 2.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            self.compress = False
            if self.drawfig1.get() == 1:
                self.vardrawfig1 = True
            else:
                self.vardrawfig1 = False
            if self.blastoutline.get() == 1:
                self.varblastoutline = True
            else:
                self.varblastoutline = False

            if self.graphtype.get() == 'None':
                self.vargraphit = None
            elif self.graphtype.get() == 'GC Content':
                self.vargraphit = [self.graphlist, self.poscol, self.negcol, int(self.graphheight.get()),
                                   int(self.graphlinet.get()), self.histo.get(), self.maxy.get(), int(self.ggap.get())]
                if None in self.vargraphit[0]:
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
            elif self.graphtype.get() == 'GC Skew':
                self.vargraphit = [self.graphlist, self.poscol, self.negcol, int(self.graphheight.get()),
                                   int(self.graphlinet.get()), self.histo.get(), self.maxy.get(), int(self.ggap.get())]
                if None in self.vargraphit[0] == None:
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
            elif self.graphtype.get() == 'Coverage':
                self.vargraphit = [[self.getCoverage()], self.poscol, self.negcol, int(self.graphheight.get()),
                    int(self.graphlinet.get()), self.histo.get(), self.maxy.get(), int(self.ggap.get())]
                if None in self.vargraphit[0]:
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
            elif self.graphtype.get() == 'Custom':
                tempcustom = self.getCustom()
                if self.allorone.get() != 1:
                    tempcustom = [tempcustom[0]]
                self.vargraphit = [tempcustom, self.poscol, self.negcol, int(self.graphheight.get()),
                                   int(self.graphlinet.get()), self.histo.get(), self.maxy.get(), int(self.ggap.get())]
                if None in self.vargraphit[0]:
                    self.running = False
                    self.createFigure.config(text="Create Figure")
                    return None
            if self.cutstate != None and self.cutstate != (str(self.mincutlist), str(self.maxcutlist)):
                tkMessageBox.showerror('Try again.', 'Please generate blast files again, blast files do not match modified annotation files.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            if self.orderstate != None and self.orderstate != self.genlist.get(0, END):
                tkMessageBox.showerror('Try again.', 'Please generate blast files again, order of annotation files has been changed.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            getit = True
            for i in self.inputlist:
                if not os.path.exists(i):
                    if not i == '' and not nocompare:
                        getit = False
            if not getit:
                tkMessageBox.showerror('Try again.', 'A selected file does not exist.')
                self.running = False
                self.createFigure.config(text="Create Figure")
                return None
            else:
                self.thethread = threading.Thread(target=self.makeFigure2)
                self.thethread.start()
                self.thethread2 = threading.Thread(target=self.dotdotdot)
                self.thethread2.start()

    def dotdotdot(self):
        while self.thethread.isAlive():
            time.sleep(0.5)
            self.processLab.config(text='Drawing figure..')
            time.sleep(0.5)
            self.processLab.config(text='Drawing figure...')
            time.sleep(0.5)
            self.processLab.config(text='Drawing figure.')
        if self.theminblast == 101:
            self.processLab.config(text='Drawing figure...\ncomplete.')
        elif self.theminblast == None:
            self.processLab.config(text='Drawing figure...\nfailed.')
        else:
            self.processLab.config(text='Drawing figure...\ncomplete.')
        self.running = False
        self.createFigure.config(text="Create Figure")

    def makeFigure2(self):
        if self.filetype.get() == 'Bitmap (bmp)':
            if self.outfile.get()[-4:].lower() != '.bmp':
                theoutfile = self.outfile.get() + '.bmp'
            else:
                theoutfile = self.outfile.get()
            self.theminblast = draw(theoutfile, self.minlength, self.mineval, self.minIdent,
                            self.inputlist, self.figwidth, self.height1, self.height2,
                            self.minblastc, self.maxblastc, self.minblastci, self.maxblastci, self.vardrawfig1, self.drawfig2,
                            False, self.compress, self.reverseList, self.featDict, self.glt,
                            self.exont, self.genet, self.genlengths, self.aln.get(), self.vargraphit, self.varblastoutline,
                            self.minmaxlist, self.autodetect.get() == 1, self.theleg, self.legname.get())
        elif self.filetype.get() == 'Vector file (svg)':
            if self.outfile.get()[-4:].lower() != '.svg':
                theoutfile = self.outfile.get() + '.svg'
            else:
                theoutfile = self.outfile.get()
            self.theminblast = drawsvg(theoutfile, self.minlength, self.mineval, self.minIdent,
                            self.inputlist, self.figwidth, self.height1, self.height2,
                            self.minblastc, self.maxblastc, self.minblastci, self.maxblastci, self.vardrawfig1, self.drawfig2,
                            False, self.compress, self.reverseList, self.featDict, self.glt,
                            self.exont, self.genet, self.genlengths, self.aln.get(), self.vargraphit, self.varblastoutline,
                            self.minmaxlist, self.autodetect.get() == 1, self.theleg, self.legname.get())
        else:
            self.theminblast = self.getPreview()

    def getPreview(self):
        try:
            self.prevwindow.destroy()
        except:
            pass
        theoutfile = None
        if self.filetype.get() == 'Preview (1:1)':
            testit, self.theminblast, width, height = draw(theoutfile, self.minlength, self.mineval, self.minIdent,
                    self.inputlist, self.figwidth, self.height1, self.height2,
                    self.minblastc, self.maxblastc, self.minblastci, self.maxblastci, self.vardrawfig1, self.drawfig2,
                    False, self.compress, self.reverseList, self.featDict, self.glt,
                    self.exont, self.genet, self.genlengths, self.aln.get(), self.vargraphit, self.varblastoutline,
                    self.minmaxlist, self.autodetect.get() == 1, self.theleg, self.legname.get(), 1)
        else:
           testit, self.theminblast, width, height = draw(theoutfile, self.minlength, self.mineval, self.minIdent,
                    self.inputlist, self.figwidth, self.height1, self.height2,
                    self.minblastc, self.maxblastc, self.minblastci, self.maxblastci, self.vardrawfig1, self.drawfig2,
                    False, self.compress, self.reverseList, self.featDict, self.glt,
                    self.exont, self.genet, self.genlengths, self.aln.get(), self.vargraphit, self.varblastoutline,
                    self.minmaxlist, self.autodetect.get() == 1, self.theleg, self.legname.get(), 2)
        self.prevwindow = Toplevel()
        self.prevwindow.title('Preview')
        self.prevframe = Frame(self.prevwindow)
        self.prevwindow.grid_rowconfigure(0, weight=1)
        self.prevwindow.grid_columnconfigure(0, weight=1)
        self.prevwindow.geometry('+30+40')
        self.prevframe.grid(row=0, column=0, sticky=NSEW)
        self.prevframe.grid_rowconfigure(0, weight=1)
        self.prevframe.grid_columnconfigure(0, weight=1)
        xscrollbar = Scrollbar(self.prevframe, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)
        yscrollbar = Scrollbar(self.prevframe)
        yscrollbar.grid(row=0, column=1, sticky=N+S)
        self.canvas = Canvas(self.prevframe, bd=0, bg='#000000', scrollregion=(0, 0, width, height),
                        xscrollcommand=xscrollbar.set,
                        yscrollcommand=yscrollbar.set)
        test = PhotoImage(data=testit)
        self.canvas.create_image(0, 0, image=test, anchor=NW)
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        self.canvas.image = test
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)
        #label = Label(self.prevframe, image=test)
        #label.image = test
        #label.grid()
        #self.canvas.image = test
        return self.theminblast

    def gbk2fasta(self, genbank, out, mincut, maxcut):
        getseq = False
        getembl = False
        getmultifa = False
        seq = ''
        try:
            mincut = int(mincut)
            if mincut < 1: mincut = 1
            if maxcut != 'Max':
                maxcut = int(maxcut)
            if maxcut < 1: maxcut = 1
        except:
            tkMessageBox.showerror('Try again.', 'Annotation slice values not valid.')
        try:
            gen = open(genbank)
            outfile = open(out, 'w')
            for line in gen:
                if line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('SQ   Sequence'):
                    getembl = True
                elif line.startswith('>'):
                    if getmultifa:
                        seq += 'qqq'
                    else:
                        getmultifa = True
                elif line.startswith('//'):
                    getseq = False
                    getembl = False
                elif getseq:
                    seq += ''.join(line.split()[1:])
                elif getembl:
                    seq += ''.join(line.split()[:-1])
                elif getmultifa:
                    seq += line.rstrip()
            if getmultifa:
                getset = set(seq)
                rightchars = set('atgcATGCqnNuUyYkKmMsSwWbBdDhHvVxXrR-')
                isitgood = True
                for i in getset:
                    if not i in rightchars:
                        isitgood = False
                if not isitgood:
                    tkMessageBox.showerror('Try again.', 'Annotation file contains invalid characters.\
                                           Check genbank/EMBL contains no lines starting with > or that\
                                           fasta file contains only valid nucleotides')
                    return 0
            if '/' in out:
                outfile.write('>' + out.split('/')[1] + '\n')
            else:
                outfile.write('>' + out + '\n')
            if maxcut == 'Max':
                maxcut = len(seq)
            if mincut == 1 and maxcut == len(seq):
                if getmultifa:
                    seq = seq.replace('qqq', 'n' * (len(seq) / 500))
                outfile.write(seq)
            elif mincut < maxcut:
                seq = seq[mincut-1:maxcut]
                if getmultifa:
                    seq = seq.replace('qqq', 'n' * (len(seq) / 500))
                outfile.write(seq)
            else:
                seq = seq[mincut-1:] + seq[:maxcut]
                if getmultifa:
                    seq = seq.replace('qqq', 'n' * (len(seq) / 500))
                outfile.write(seq)
            if len(seq) == 0:
                tkMessageBox.showerror('Try again.', 'There is no sequence in ' + genbank + '.')
                return 0
            else:
                return 1
        except:
            tkMessageBox.showerror('Try again.', genbank + ' does not exist.')
            return 0

    def genBlast(self):
        try:
            if self.thegenblast.isAlive():
                tkMessageBox.showerror('Please wait', 'BLAST already running.')
                return None
        except:
            pass
        try:
            if self.thethread.isAlive():
                tkMessageBox.showerror('Please wait', 'easyfig creating figure.')
                return None
        except:
            pass
        try:
            if self.thedlblast.isAlive():
                tkMessageBox.showerror('Please wait', 'Blast is downloading.')
                return None
        except:
            pass
        self.processLab.config(text='Performing blastn...')
        self.workingDir = tkFileDialog.askdirectory(title='Please select a working directory.')
        if self.workingDir == ():
            self.processLab.config(text='Performing blastn...\nCancelled.')
            return None
        os.chdir(self.workingDir)
        index = 0
        if self.genlist.size() < 2:
            tkMessageBox.showerror('Try again.', 'easyfig needs at least 2 genbank files to create blast files.')
            self.processLab.config(text='Performing blastn...\nCancelled.')
            return None
        else:
            thegenlist = self.genlist.get(0, END)
            for i in thegenlist:
                index += 1
                temp = self.gbk2fasta(i[4:], str(index) + '.easyfig.fa', self.mincutlist[i[:2]], self.maxcutlist[i[:2]])
                if temp == 0:
                    return None
            self.cutstate = (str(self.mincutlist), str(self.maxcutlist))
            self.orderstate = self.genlist.get(0, END)
            if self.blastnDir == None:
                pass
            elif self.blastnDir[-11:] == 'tblastx.exe':
                if os.path.exists(self.blastnDir[:-11] + 'blastn.exe'):
                    self.blastnDir = self.blastnDir[:-11] + 'blastn.exe'
                else:
                    self.blastnDir = None
            elif self.blastnDir[-7:] == 'tblastx':
                if os.path.exists(self.blastnDir[:-7] + 'blastn'):
                    self.blastnDir = self.blastnDir[:-7] + 'blastn'
                else:
                    self.blastnDir = None
            if self.dbnDir != None:
                if not os.path.exists(self.dbnDir):
                    self.dbnDir = None
            if self.blastnDir != None:
                if not os.path.exists(self.blastnDir):
                    self.blastnDir = None
            if self.dbnDir != None:
                pass
            elif isNewBlastDB():
                self.dbnDir = 'makeblastdb'
            elif isLegBlastDB():
                self.dblDir = 'formatdb'
            elif os.path.exists('~/bin/makeblastdb'):
                self.dbnDir = '~/bin/makeblastdb'
            elif os.path.exists('/usr/local/ncbi/bin/makeblastdb'):
                self.blastnDir = '/usr/local/ncbi/bin/makeblastdb'
            elif os.path.exists('/usr/local/bin/makeblastdb'):
                self.dbnDir = '/usr/local/bin/makeblastdb'
            elif os.path.exists(self.pwd + '/makeblastdb'):
                self.dbnDir = self.pwd + '/makeblastdb'
            elif os.path.exists('/usr/local/ncbi/blast/bin/makeblastdb'):
                self.dbnDir = '/usr/local/ncbi/blast/bin/makeblastdb'
            elif os.path.exists('/usr/local/bin/formatdb'):
                self.dblDir = '/usr/local/bin/formatdb'
            elif os.path.exists('~/bin/formatdb'):
                self.dblDir = '~/bin/formatdb'
            elif os.path.exists(self.pwd + '/formatdb'):
                self.dblDir = self.pwd + '/formatdb'
            elif os.path.exists(self.pwd + '/makeblastdb.exe'):
                self.dbnDir = self.pwd + '/makeblastdb.exe'
            elif os.path.exists(self.pwd + '/formatdb.exe'):
                self.dblDir = self.pwd + '/formatdb.exe'
            else:
                folderlist = []
                for letter in string.uppercase:
                    if os.path.exists(letter + ':/program files/ncbi/'):
                        folders = os.listdir(letter + ':/program files/ncbi/')
                        for f in folders:
                            if f.upper().startswith('BLAST'):
                                folderlist.append(letter + ':/program files/ncbi/' + f)
                folderlist.sort(reverse=True)
                blastgot = False
                if len(folderlist) > 0:
                    for f in folderlist:
                        if not blastgot and os.path.exists(f + '/bin/makeblastdb.exe'):
                            blastgot = True
                            self.dblDir = '"' + f + '/bin/makeblastdb"'
            if self.blastnDir != None:
                pass
            elif isNewBlastn():
                self.blastnDir = 'blastn'
            elif isLegBlastall():
                self.blastlDir = 'blastall'
            elif os.path.exists('~/bin/blastn'):
                self.blastnDir = '~/bin/blastn'
            elif os.path.exists('/usr/local/ncbi/bin/blastn'):
                self.blastnDir = '/usr/local/ncbi/bin/blastn'
            elif os.path.exists('/usr/local/bin/blastn'):
                self.blastnDir = '/usr/local/bin/blastn'
            elif os.path.exists(self.pwd + '/blastn'):
                self.blastnDir = self.pwd + '/blastn'
            elif os.path.exists('/usr/local/ncbi/blast/bin/blastn'):
                self.blastnDir = '/usr/local/ncbi/blast/bin/blastn'
            elif os.path.exists('/usr/local/bin/blastall'):
                self.blastlDir = '/usr/local/bin/blastall'
            elif os.path.exists('~/bin/blastall'):
                self.blastlDir = '~/bin/blastall'
            elif os.path.exists(self.pwd + '/blastall'):
                self.blastlDir = self.pwd + '/blastall'
            elif os.path.exists(self.pwd + '/blastall.exe'):
                self.blastlDir = self.pwd + '/blastall.exe'
            elif os.path.exists(self.pwd + '/blastn.exe'):
                self.blastnDir = self.pwd + '/blastn.exe'
            else:
                folderlist = []
                for letter in string.uppercase:
                    if os.path.exists(letter + ':/program files/ncbi/'):
                        folders = os.listdir(letter + ':/program files/ncbi/')
                        for f in folders:
                            if f.upper().startswith('BLAST'):
                                folderlist.append(letter + ':/program files/ncbi/' + f)
                folderlist.sort(reverse=True)
                blastgot = False
                if len(folderlist) > 0:
                    for f in folderlist:
                        if not blastgot and os.path.exists(f + '/bin/blastn.exe'):
                            blastgot = True
                            self.blastnDir = '"' + f + '/bin/blastn"'
            if self.blastnDir == None and self.blastlDir == None or self.dbnDir == None and self.dblDir == None:
                dlblast = tkMessageBox.askquestion('Blast not found', 'Do you wish to download Blast?')
                if dlblast != 'no':
                    self.thedlblast = threading.Thread(target=self.downloadBlast)
                    self.thedlblast.start()
                    return None
                tempdir = tkFileDialog.askdirectory(title='Please select a directory with blastn and makeblastdb.')
                if tempdir == ():
                    tempdir = ''
                if os.path.exists(tempdir + '/blastn.exe') and os.path.exists(tempdir + '/makeblastdb.exe'):
                    self.blastnDir = tempdir + '/blastn.exe'
                    self.dbnDir = tempdir + '/makeblastdb.exe'
                elif os.path.exists(tempdir + '/blastn') and os.path.exists(tempdir + '/makeblastdb'):
                    self.blastnDir = tempdir + '/blastn'
                    self.dbnDir = tempdir + '/makeblastdb'
                else:
                    self.processLab.config(text='Performing blastn...\nInvadild directory.\nBlast not found.')
                    self.blastnDir = None
                    self.dbnDir = None
                    return None
            if self.workingDir == '':
                self.processLab.config(text='Performing blastn...\nCancelled.')
                return None
            self.thegenblast = threading.Thread(target=self.genBlast2)
            self.thegenblast.start()
            self.thegenblast2 = threading.Thread(target=self.genBlastDot)
            self.thegenblast2.start()


    def genBlastDot(self):
        while self.thegenblast.isAlive():
            time.sleep(0.5)
            self.processLab.config(text='Performing blastn.')
            time.sleep(0.5)
            self.processLab.config(text='Performing blastn..')
            time.sleep(0.5)
            self.processLab.config(text='Performing blastn...')
        if self.blastlist.size() == self.genlist.size() - 1:
            self.processLab.config(text='Performing blastn...\ncomplete.')
        else:
            self.processLab.config(text='Blast has failed, please check genbank files and rerun.')

    def genBlast2(self):
        self.blastlist.delete(0, END)
        the_tempdb_dir = os.path.abspath('.') + '/tempdb'
        for i in range(self.genlist.size() - 1):
            if self.dbnDir != None:
                subprocess.Popen(self.dbnDir + ' -dbtype nucl -out ' + the_tempdb_dir + ' -in ' + str(i + 2) +
                                 '.easyfig.fa', shell=True).wait()
            elif self.dblDir != None:
                subprocess.Popen(self.dblDir + ' -p F -t tempdb -n tempdb -i '
                                 + str(i + 2) + '.easyfig.fa', shell=True).wait()
            if self.blastnDir:
                subprocess.Popen(self.blastnDir + ' -task blastn -db ' + the_tempdb_dir + ' -outfmt 6 -query ' + str(i+1)
                                 + '.easyfig.fa -out ' + str(i + 1) + str(i+2) + '.easyfig.out',
                                 shell=True).wait()
            elif self.blastlDir:
                subprocess.Popen(self.blastlDir + ' -p blastn -d ' + the_tempdb_dir + ' -F F -m 8 -a 8 -i '
                             + str(i + 1) + '.easyfig.fa -o '
                             + str(i+1) + str(i+2) + '.easyfig.out', shell=True).wait()
            self.blastlist.insert(END, self.workingDir + '/' + str(i + 1) + str(i+2) + '.easyfig.out')
        self.blastlist.xview_moveto(1)
        if os.path.exists('tempdb.nhr'):
            os.remove('tempdb.nhr')
        if os.path.exists('tempdb.nin'):
            os.remove('tempdb.nin')
        if os.path.exists('error.log'):
            os.remove('error.log')
        if os.path.exists('tempdb.nsq'):
            os.remove('tempdb.nsq')
        if os.path.exists('formatdb.log'):
            os.remove('formatdb.log')
        os.chdir(self.pwd)

    def genBlastX(self):
        try:
            if self.thegenblast.isAlive():
                tkMessageBox.showerror('Please wait', 'BLAST already running.')
                return None
        except:
            pass
        try:
            if self.thethread.isAlive():
                tkMessageBox.showerror('Please wait', 'easyfig creating figure.')
                return None
        except:
            pass
        try:
            if self.thedlblast.isAlive():
                tkMessageBox.showerror('Please wait', 'Blast is downloading.')
                return None
        except:
            pass
        self.workingDir = tkFileDialog.askdirectory(title='Please select a working directory.')
        if self.workingDir == ():
            self.processLab.config(text='Performing tblastx...\nCancelled.')
            return
        os.chdir(self.workingDir)
        index = 0
        if self.genlist.size() < 2:
            tkMessageBox.showerror('Try again.', 'easyfig needs at least 2 genbank files to create blast files.')
        else:
            thegenlist = self.genlist.get(0, END)
            for i in thegenlist:
                index += 1
                temp = self.gbk2fasta(i[4:], str(index) + '.easyfig.fa', self.mincutlist[i[:2]], self.maxcutlist[i[:2]])
                if temp == 0:
                    return None
            self.cutstate = (str(self.mincutlist), str(self.maxcutlist))
            self.orderstate = self.genlist.get(0, END)
            if self.blastnDir == None:
                pass
            elif self.blastnDir[-10:] == 'blastn.exe':
                if os.path.exists(self.blastnDir[:-10] + 'tblastx.exe'):
                    self.blastnDir = self.blastnDir[:-10] + 'tblastx.exe'
                else:
                    self.blastnDir = None
            elif self.blastnDir[-6:] == 'blastn':
                if os.path.exists(self.blastnDir[:-6] + 'tblastx'):
                    self.blastnDir = self.blastnDir[:-6] + 'tblastx'
                else:
                    self.blastnDir = None
            if self.dbnDir != None:
                if not os.path.exists(self.dbnDir):
                    self.dbnDir = None
            if self.blastnDir != None:
                if not os.path.exists(self.blastnDir):
                    self.blastnDir = None
            if self.dbnDir != None:
                pass
            elif isNewBlastDB():
                self.dbnDir = 'makeblastdb'
            elif isLegBlastDB():
                self.dblDir = 'formatdb'
            elif os.path.exists('~/bin/makeblastdb'):
                self.dbnDir = '~/bin/makeblastdb'
            elif os.path.exists('/usr/local/bin/makeblastdb'):
                self.dbnDir = '/usr/local/bin/makeblastdb'
            elif os.path.exists('./makeblastdb'):
                self.dbnDir = './makeblastdb'
            elif os.path.exists('/usr/local/ncbi/bin/makeblastdb'):
                self.blastnDir = '/usr/local/ncbi/bin/makeblastdb'
            elif os.path.exists('/usr/local/ncbi/blast/bin/makeblastdb'):
                self.dbnDir = '/usr/local/ncbi/blast/bin/makeblastdb'
            elif os.path.exists('/usr/local/bin/formatdb'):
                self.dblDir = '/usr/local/bin/formatdb'
            elif os.path.exists('~/bin/formatdb'):
                self.dblDir = '~/bin/formatdb'
            elif os.path.exists('./formatdb'):
                self.dblDir = './formatdb'
            elif os.path.exists('./makeblastdb.exe'):
                self.dbnDir = './makeblastdb.exe'
            elif os.path.exists('./formatdb.exe'):
                self.dblDir = './formatdb.exe'
            else:
                folderlist = []
                for letter in string.uppercase:
                    if os.path.exists(letter + ':/program files/ncbi/'):
                        folders = os.listdir(letter + ':/program files/ncbi/')
                        for f in folders:
                            if f.upper().startswith('BLAST'):
                                folderlist.append(letter + ':/program files/ncbi/' + f)
                folderlist.sort(reverse=True)
                blastgot = False
                if len(folderlist) > 0:
                    for f in folderlist:
                        if not blastgot and os.path.exists(f + '/bin/makeblastdb.exe'):
                            blastgot = True
                            self.dblDir = '"' + f + '/bin/makeblastdb"'
            if self.blastnDir != None:
                pass
            elif isNewTblastx():
                self.blastnDir = 'tblastx'
            elif isLegBlastall():
                self.blastlDir = 'blastall'
            elif os.path.exists('~/bin/tblastx'):
                self.blastnDir = '~/bin/tblastx'
            elif os.path.exists('/usr/local/ncbi/bin/tblastx'):
                self.blastnDir = '/usr/local/ncbi/bin/tblastx'
            elif os.path.exists('/usr/local/bin/tblastx'):
                self.blastnDir = '/usr/local/bin/tblastx'
            elif os.path.exists('./tblastx'):
                self.blastnDir = './tblastx'
            elif os.path.exists('/usr/local/ncbi/blast/bin/tblastx'):
                self.blastnDir = '/usr/local/ncbi/blast/bin/tblastx'
            elif os.path.exists('/usr/local/bin/blastall'):
                self.blastlDir = '/usr/local/bin/blastall'
            elif os.path.exists('~/bin/blastall'):
                self.blastlDir = '~/bin/blastall'
            elif os.path.exists('./blastall'):
                self.blastlDir = './blastall'
            elif os.path.exists('./tblastx.exe'):
                self.blastnDir = './tblastx.exe'
            else:
                folderlist = []
                for letter in string.uppercase:
                    if os.path.exists(letter + ':/program files/ncbi/'):
                        folders = os.listdir(letter + ':/program files/ncbi/')
                        for f in folders:
                            if f.upper().startswith('BLAST'):
                                folderlist.append(letter + ':/program files/ncbi/' + f)
                folderlist.sort(reverse=True)
                blastgot = False
                if len(folderlist) > 0:
                    for f in folderlist:
                        if not blastgot and os.path.exists(f + '/bin/tblastx.exe'):
                            blastgot = True
                            self.blastnDir = '"' + f + '/bin/tblastx.exe"'
            if self.blastnDir == None and self.blastlDir == None or self.dbnDir == None and self.dbl == None:
                dlblast = tkMessageBox.askquestion('Blast not found', 'Do you wish to download Blast?')
                if dlblast:
                    self.thedlblast = threading.Thread(target=self.downloadBlast)
                    self.thedlblast.start()
                    return None
                tempdir = tkFileDialog.askdirectory(title='Please select a directory with tblastx and makeblastdb.')
                if os.path.exists(tempdir + '/tblastx.exe') and os.path.exists(tempdir + '/makeblastdb.exe'):
                    self.blastnDir = tempdir + '/tblastx.exe'
                    self.dbnDir = tempdir + '/makeblastdb.exe'
                elif os.path.exists(tempdir + '/tblastx') and os.path.exists(tempdir + '/makeblastdb'):
                    self.blastnDir = tempdir + '/tblastx'
                    self.dbnDir = tempdir + '/makeblastdb'
                else:
                    self.processLab.config(text='Performing blastn...\nInvadild directory.\nBlast not found.')
                    return None
            if self.workingDir == '':
                self.processLab.config(text='Performing blastn...\nCancelled.')
                return None
            self.thegenblast = threading.Thread(target=self.genBlastX2)
            self.thegenblast.start()
            self.thegenblast2 = threading.Thread(target=self.genBlastXdot)
            self.thegenblast2.start()

    def genBlastXdot(self):
        while self.thegenblast.isAlive():
            time.sleep(0.5)
            self.processLab.config(text='Performing tblastx.')
            time.sleep(0.5)
            self.processLab.config(text='Performing tblastx..')
            time.sleep(0.5)
            self.processLab.config(text='Performing tblastx...')
        self.processLab.config(text='Performing tblastx...\ncomplete.')


    def genBlastX2(self):
        self.blastlist.delete(0, END)
        for i in range(self.genlist.size() - 1):
            if self.dbnDir != None:
                subprocess.Popen(self.dbnDir + ' -dbtype nucl -out tempdb -in ' + str(i + 2) +
                                 '.easyfig.fa', shell=True).wait()
            elif self.dblDir != None:
                subprocess.Popen(self.dblDir + ' -p F -t tempdb -n tempdb -i '
                                 + str(i + 2) + '.easyfig.fa', shell=True).wait()
            if self.blastnDir:
                subprocess.Popen(self.blastnDir + ' -db tempdb -outfmt 6 -query ' + str(i+1)
                                 + '.easyfig.fa -out ' + str(i + 1) + str(i+2) + '.easyfig.out',
                                 shell=True).wait()
            elif self.blastlDir:
                subprocess.Popen(self.blastlDir + ' -p tblastx -d tempdb -F F -m 8 -a 8 -i '
                             + str(i + 1) + '.easyfig.fa -o '
                             + str(i+1) + str(i+2) + '.easyfig.out', shell=True).wait()
            self.blastlist.insert(END, self.workingDir + '/' + str(i + 1) + str(i+2) + '.easyfig.out')
        self.blastlist.xview_moveto(1)
        if os.path.exists('tempdb.nhr'):
            os.remove('tempdb.nhr')
        if os.path.exists('tempdb.nin'):
            os.remove('tempdb.nin')
        if os.path.exists('error.log'):
            os.remove('error.log')
        if os.path.exists('tempdb.nsq'):
            os.remove('tempdb.nsq')
        if os.path.exists('formatdb.log'):
            os.remove('formatdb.log')
        os.chdir(self.pwd)



    def annmod(self, event=None):
        try:
            self.annwindow.destroy()
        except:
            pass
        self.annwindow = Toplevel()
        self.frame6 = Frame(self.annwindow)
        self.annwindow.title('Subregions')
        self.frangelab = Label(self.frame6, text='Range', font='TkDefaultFont 13 bold')
        self.frangelab.grid(row=0, column=2, columnspan=3)
        self.ffilelab = Label(self.frame6, text='Ann. file', font='TkDefaultFont 13 bold')
        self.ffilelab.grid(row=1, column=1, pady=10)
        self.fminlab = Label(self.frame6, text='Min', font='TkDefaultFont 13 bold')
        self.fminlab.grid(row=1, column=2, pady=10)
        self.fdotdot = Label(self.frame6, text=' .. ')
        self.fdotdot.grid(row=1, column=3)
        self.fmaxlab = Label(self.frame6, text='Max', font='TkDefaultFont 13 bold')
        self.fmaxlab.grid(row=1, column=4, pady=10)
        self.frevlab = Label(self.frame6, text='Reverse', font='TkDefaultFont 13 bold')
        self.frevlab.grid(row=1, column=5, pady=10)
        self.scrollbar2 = Scrollbar(self.frame6, orient=VERTICAL)
        self.fgenlist = Listbox(self.frame6, yscrollcommand=self.scrollbar2.set, exportselection=0)
        self.fgenlist.bind('<Button-1>', self.setselectedcuts)
        self.fgenlist.bind('<Double-Button-1>', self.doublecuts)
        self.fgenlist.bind('<MouseWheel>', self.onmousewheel)
        self.fgenlist.bind('<Button-4>', self.onmousewheel)
        self.fgenlist.bind('<Button-5>', self.onmousewheel)
        self.fgenlist.grid(row=2, column=1)
        self.fgenminlist = Listbox(self.frame6, yscrollcommand=self.scrollbar2.set, exportselection=0)
        self.fgenminlist.config(width=7)
        self.fgenminlist.bind('<Button-1>', self.setselectedcuts)
        self.fgenminlist.bind('<Double-Button-1>', self.doublecuts)
        self.fgenminlist.bind('<MouseWheel>', self.onmousewheel)
        self.fgenminlist.bind('<Button-4>', self.onmousewheel)
        self.fgenminlist.bind('<Button-5>', self.onmousewheel)
        self.fgenminlist.grid(row=2, column=2)
        self.fgenmaxlist = Listbox(self.frame6, yscrollcommand=self.scrollbar2.set, exportselection=0)
        self.fgenmaxlist.config(width=7)
        self.fgenmaxlist.bind('<Button-1>', self.setselectedcuts)
        self.fgenmaxlist.bind('<Double-Button-1>', self.doublecuts)
        self.fgenmaxlist.bind('<MouseWheel>', self.onmousewheel)
        self.fgenmaxlist.bind('<Button-4>', self.onmousewheel)
        self.fgenmaxlist.bind('<Button-5>', self.onmousewheel)
        self.fgenmaxlist.grid(row=2, column=4)
        self.fgenrevlist = Listbox(self.frame6, yscrollcommand=self.scrollbar2.set, exportselection=0)
        self.fgenrevlist.config(width=5)
        self.fgenrevlist.bind('<Button-1>', self.setselectedcuts)
        self.fgenrevlist.bind('<Double-Button-1>', self.doublecuts)
        self.fgenrevlist.bind('<MouseWheel>', self.onmousewheel)
        self.fgenrevlist.bind('<Button-4>', self.onmousewheel)
        self.fgenrevlist.bind('<Button-5>', self.onmousewheel)
        self.fgenrevlist.grid(row=2, column=5)
        self.scrollbar2.config(command=self.yview2)
        self.scrollbar2.grid(row=2, column=0, sticky=NS)
        annlist = self.genlist.get(0, END)
        annlistpostemp = self.genlist.curselection()
        for i in annlist:
            self.fgenlist.insert(END, i)
            self.fgenminlist.insert(END, self.mincutlist[i[:2]])
            self.fgenmaxlist.insert(END, self.maxcutlist[i[:2]])
            if self.revlist[i[:2]]:
                self.fgenrevlist.insert(END, 'yes')
            else:
                self.fgenrevlist.insert(END, 'no')
        self.fgenlist.xview_moveto(1)
        self.genmincut = StringVar()
        self.genmaxcut = StringVar()
        self.genrev = IntVar()
        self.mincutentry = Entry(self.frame6, textvariable=self.genmincut)
        self.mincutentry.config(width=7)
        self.mincutentry.grid(row=3, column=2)
        self.maxcutentry = Entry(self.frame6, textvariable=self.genmaxcut)
        self.maxcutentry.config(width=7)
        self.maxcutentry.grid(row=3, column=4)
        self.genrentry = Checkbutton(self.frame6, variable=self.genrev)
        self.genrentry.grid(row=3, column=5)
        if len(annlist) > 0 and annlistpostemp != ():
            self.fgenlist.selection_set(annlistpostemp)
            self.fgenminlist.selection_set(annlistpostemp)
            self.fgenmaxlist.selection_set(annlistpostemp)
            self.fgenrevlist.selection_set(annlistpostemp)
            self.fgenlist.see(annlistpostemp)
            self.fgenminlist.see(annlistpostemp)
            self.fgenmaxlist.see(annlistpostemp)
            self.fgenrevlist.see(annlistpostemp)
            self.genmincut.set(self.fgenminlist.get(annlistpostemp))
            self.genmaxcut.set(self.fgenmaxlist.get(annlistpostemp))
            if self.fgenrevlist.get(annlistpostemp) == 'yes':
                self.genrev.set(1)
            else:
                self.genrev.set(0)
        self.changecutsbutton = Button(self.frame6, text='  change cutoffs  ', command=self.changecuts)
        self.changecutsbutton.grid(row=3, column=1, pady=10)
        self.annwindowclosebutton = Button(self.frame6, text='close', command=self.annwindowclose)
        self.annwindowclosebutton.grid(row=12, column=4, columnspan=2, sticky=E, pady=10)
        self.annwindow.geometry('+30+40')
        self.frame6.grid(padx=30, pady=10)


    def changecuts(self):
        thepost = self.fgenlist.curselection()
        if thepost == ():
            tkMessageBox.showerror('Try again.', 'Please select genome to change.')
            return
        else:
            thepost = int(thepost[0])
        self.fgenminlist.delete(thepost)
        self.fgenminlist.insert(thepost, self.genmincut.get())
        self.mincutlist[self.fgenlist.get(thepost)[:2]] = self.genmincut.get()
        self.fgenmaxlist.delete(thepost)
        self.fgenmaxlist.insert(thepost, self.genmaxcut.get())
        self.maxcutlist[self.fgenlist.get(thepost)[:2]] = self.genmaxcut.get()
        self.fgenrevlist.delete(thepost)
        if self.genrev.get() == 1:
            self.fgenrevlist.insert(thepost, 'yes')
            self.revlist[self.fgenlist.get(thepost)[:2]] = True
        else:
            self.fgenrevlist.insert(thepost, 'no')
            self.revlist[self.fgenlist.get(thepost)[:2]] = False
        if not thepost == self.fgenlist.size() - 1:
            self.fgenlist.selection_clear(0, END)
            self.fgenlist.selection_set(thepost + 1, thepost + 1)
            self.fgenlist.see(thepost + 1)
            self.fgenminlist.selection_clear(0, END)
            self.fgenminlist.selection_set(thepost + 1, thepost + 1)
            self.fgenminlist.see(thepost + 1)
            self.fgenmaxlist.selection_clear(0, END)
            self.fgenmaxlist.selection_set(thepost + 1, thepost + 1)
            self.fgenmaxlist.see(thepost+1)
            self.fgenrevlist.selection_clear(0, END)
            self.fgenrevlist.selection_set(thepost + 1, thepost + 1)
            self.fgenrevlist.see(thepost + 1)

    def yview2(self, *args):
        apply(self.fgenlist.yview, args)
        apply(self.fgenminlist.yview, args)
        apply(self.fgenmaxlist.yview, args)
        apply(self.fgenrevlist.yview, args)

    def onmousewheel(self, event):
        return "break"

    def setselectedcuts(self, event):
        selected = self.fgenlist.nearest(event.y)
        tempypos = self.fgenlist.yview()[0]
        self.fgenminlist.yview_moveto(tempypos)
        self.fgenmaxlist.yview_moveto(tempypos)
        self.fgenrevlist.yview_moveto(tempypos)
        self.fgenlist.selection_clear(0, END)
        self.fgenlist.selection_set(selected, selected)
        self.fgenminlist.selection_clear(0, END)
        self.fgenminlist.selection_set(selected, selected)
        self.fgenmaxlist.selection_clear(0, END)
        self.fgenmaxlist.selection_set(selected, selected)
        self.fgenrevlist.selection_clear(0, END)
        self.fgenrevlist.selection_set(selected, selected)
        self.genmincut.set(self.fgenminlist.get(selected))
        self.genmaxcut.set(self.fgenmaxlist.get(selected))
        if self.fgenrevlist.get(selected) == 'yes':
            self.genrev.set(1)
        else:
            self.genrev.set(0)

    def doublecuts(self, event):
        try:
            self.doublecutswin.destroy()
        except:
            pass
        self.doublecutsel = self.fgenlist.nearest(event.y)
        self.doublecutswin = Toplevel(self.frame6)
        self.doublecutswin.title('Change subregion')
        self.frame10 = Frame(self.doublecutswin)
        self.dublabel1 = Label(self.frame10, text='Modify file ' + self.fgenlist.get(self.doublecutsel)[:3], font='TkDefaultFont 13 bold')
        self.dublabel1.grid(row=0, column=0, pady=5)
        self.dublabel2 = Label(self.frame10, text='Min Cutoff:')
        self.dublabel2.grid(row=1, column=0)
        self.dublabel3 = Label(self.frame10, text='Max Cutoff:')
        self.dublabel3.grid(row=2, column=0)
        self.dublabel4 = Label(self.frame10, text='Reverse:')
        self.dublabel4.grid(row=3, column=0)
        self.dublabel2str = StringVar(value=self.fgenminlist.get(self.doublecutsel))
        self.dublabel3str = StringVar(value=self.fgenmaxlist.get(self.doublecutsel))
        if self.fgenrevlist.get(self.doublecutsel) == 'yes':
            self.dublabel4int = IntVar(value=1)
        else:
            self.dublabel4int = IntVar(value=0)
        self.dublabel2ent = Entry(self.frame10, textvariable=self.dublabel2str)
        self.dublabel2ent.grid(row=1, column=1)
        self.dublabel3ent = Entry(self.frame10, textvariable=self.dublabel3str)
        self.dublabel3ent.grid(row=2, column=1)
        self.dublabel4ent = Checkbutton(self.frame10, variable=self.dublabel4int)
        self.dublabel4ent.grid(row=3, column=1)
        self.doublecutsclosebut = Button(self.frame10, text='Save & Close', command=self.doublecutsclose)
        self.doublecutsclosebut.grid(row=4, column=1, sticky=E)
        self.doublecutswin.geometry('+40+50')
        self.frame10.grid(padx=20, pady=20)

    def doublecutsclose(self):
        self.fgenminlist.delete(self.doublecutsel)
        self.fgenminlist.insert(self.doublecutsel, self.dublabel2str.get())
        self.mincutlist[self.fgenlist.get(self.doublecutsel)[:2]] = self.dublabel2str.get()
        self.fgenmaxlist.delete(self.doublecutsel)
        self.fgenmaxlist.insert(self.doublecutsel, self.dublabel3str.get())
        self.maxcutlist[self.fgenlist.get(self.doublecutsel)[:2]] = self.dublabel3str.get()
        self.fgenrevlist.delete(self.doublecutsel)
        if self.dublabel4int.get() == 1:
            self.fgenrevlist.insert(self.doublecutsel, 'yes')
            self.revlist[self.fgenlist.get(self.doublecutsel)[:2]] = True
        else:
            self.fgenrevlist.insert(self.doublecutsel, 'no')
            self.revlist[self.fgenlist.get(self.doublecutsel)[:2]] = False
        self.doublecutswin.destroy()

    def annwindowclose(self):
        self.annwindow.destroy()



    def openFile1(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen1.set(filename)
    def openFile2(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen2.set(filename)
    def openFile3(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen3.set(filename)
    def openFile4(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen4.set(filename)
    def openFile5(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen5.set(filename)
    def openFile6(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen6.set(filename)
    def openFile7(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen7.set(filename)
    def openFile8(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen8.set(filename)
    def openFile9(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen9.set(filename)
    def openFile0(self):
        filename = tkFileDialog.askopenfilename(filetypes = [('genbank/embl/fasta', ('*.gbk', '*.embl', '*.gb', '*.fa', '*.fna', '*.dna', '*.fas', '*.fasta')), ('All files','*')])
        self.gen0.set(filename)

    def openBlast1(self):
        filename = tkFileDialog.askopenfilename()
        self.blast1.set(filename)
    def openBlast2(self):
        filename = tkFileDialog.askopenfilename()
        self.blast2.set(filename)
    def openBlast3(self):
        filename = tkFileDialog.askopenfilename()
        self.blast3.set(filename)
    def openBlast4(self):
        filename = tkFileDialog.askopenfilename()
        self.blast4.set(filename)
    def openBlast5(self):
        filename = tkFileDialog.askopenfilename()
        self.blast5.set(filename)
    def openBlast6(self):
        filename = tkFileDialog.askopenfilename()
        self.blast6.set(filename)
    def openBlast7(self):
        filename = tkFileDialog.askopenfilename()
        self.blast7.set(filename)
    def openBlast8(self):
        filename = tkFileDialog.askopenfilename()
        self.blast8.set(filename)
    def openBlast9(self):
        filename = tkFileDialog.askopenfilename()
        self.blast9.set(filename)

    def getoutfile(self):
        if self.filetype.get() == 'Bitmap (bmp)':
            filename = tkFileDialog.asksaveasfilename(filetypes = [('bmp', '*.bmp'), ('All files','*')])
        else:
            filename = tkFileDialog.asksaveasfilename(filetypes = [('svg', '*.svg'), ('All files','*')])
        self.outfile.set(filename)

    def handleDownload(self, block):
        self.downloadFile.write(block)
        if self.thecount * 100 / self.totalBytes != (self.thecount + len(block)) * 100 / self.totalBytes:
            try:
                self.processLab.config(text='Finding Blast... Done\nDownloading... ' + str((self.thecount + len(block)) * 100 / self.totalBytes) + '%')
            except:
                pass
        self.thecount += len(block)

    def downloadBlastAuto(self):
        self.thedlblast = threading.Thread(target=self.downloadBlast)
        self.thedlblast.start()

    def downloadBlastMan(self):
        theplatform = platform.system()
        architecture = platform.architecture()[0]
        if theplatform == 'Linux' and architecture == '32bit':
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand extracting\nncbi-blast-x.x.x+-ia32-linux.tar.gz\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')
        elif theplatform == 'Linux' and architecture == '64bit':
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand extracting\nncbi-blast-x.x.x+-x64-linux.tar.gz\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')
        elif theplatform == 'Windows' and architecture == '32bit':
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand running\nncbi-blast-x.x.x+-win32.exe\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')
        elif theplatform == 'Windows' and architecture == '64bit':
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand running\nncbi-blast-x.x.x+-win64.exe\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')
        elif theplatform == 'Darwin':
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand running\nncbi-blast-x.x.x+.dmg\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')
        else:
            ok = tkMessageBox.askokcancel('Downloading Blast Manually', 'Easyfig suggests downloading\nand compiling\nncbi-blast-x.x.x+.src.tar.gz\n\
clicking ok will bring up\nthe download location\nin your browser.')
            if ok:
                webbrowser.open_new('ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/')

    def chooseBlastDir(self):
        tempdir = tkFileDialog.askdirectory(title='Please select a directory with blastn and makeblastdb.')
        if tempdir == () or tempdir == '':
            return
        if os.path.exists(tempdir + '/blastn.exe') and os.path.exists(tempdir + '/makeblastdb.exe'):
            self.blastnDir = tempdir + '/blastn.exe'
            self.dbnDir = tempdir + '/makeblastdb.exe'
        elif os.path.exists(tempdir + '/blastn') and os.path.exists(tempdir + '/makeblastdb'):
            self.blastnDir = tempdir + '/blastn'
            self.dbnDir = tempdir + '/makeblastdb'
        else:
            tkMessageBox.showerror('Try again.', 'Blast not found in Directory.')
            self.blastnDir = None
            self.dbnDir = None

    def downloadBlast(self):
        theplatform = platform.system()
        architecture = platform.architecture()[0]
        self.processLab.config(text='Finding Blast...')
        try:
            ftp = FTP('ftp.ncbi.nlm.nih.gov')
            ftp.login()
            ftp.cwd('blast/executables/blast+/LATEST/')
            files = []
            ftp.dir(files.append)
        except:
            self.processLab.config(text='Unable to Create FTP \nconnection.\nPlease dowload manually.')
            return
        filename = None
        try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
            if true_platform == 'AMD64':
                architecture = '64bit'
        except KeyError:
            pass
        for line in files:
            if theplatform == 'Linux' and architecture == '32bit' and line.split()[8][-17:] == 'ia32-linux.tar.gz':
                filename = line.split()[8]
                self.totalBytes = int(line.split()[4])
            elif theplatform == 'Linux' and architecture == '64bit' and line.split()[8][-16:] == 'x64-linux.tar.gz':
                filename = line.split()[8]
                self.totalBytes = int(line.split()[4])
            elif theplatform == 'Windows' and architecture == '32bit' and line.split()[8][-17:] == 'ia32-win32.tar.gz':
                filename = line.split()[8]
                self.totalBytes = int(line.split()[4])
            elif theplatform == 'Windows' and architecture == '64bit' and line.split()[8][-16:] == 'x64-win64.tar.gz':
                filename = line.split()[8]
                self.totalBytes = int(line.split()[4])
            elif theplatform == 'Darwin' and line.split()[8][-23:] == 'universal-macosx.tar.gz':
                filename = line.split()[8]
                self.totalBytes = int(line.split()[4])
        if filename == None:
            self.processLab.config(text='Unable to download blast.\nPlease dowload manually.')
            return
        self.thecount = 0
        try:
            self.downloadFile = open(filename, 'wb')
        except:
            self.processLab.config(text='Unable to download blast.\nPlease dowload manually.')
            return
        ftp.retrbinary('RETR ' + filename, self.handleDownload)
        self.downloadFile.close()
        self.processLab.config(text='Downloading... Complete\nExtracting file...')
        try:
            tfile = tarfile.open(filename, 'r:gz')
            tfile.extractall()
        except:
            self.processLab.config(text='Unable to download blast.\nPlease dowload manually.')
            return
        filenamedir = filename.split('+')[0] + '+'
        if theplatform == 'Windows':
            try:
               shutil.move(filenamedir + '/bin/makeblastdb.exe', self.pwd)
            except:
               pass
            try:
                shutil.move(filenamedir + '/bin/blastn.exe', self.pwd)
            except:
                pass
            try:
                shutil.move(filenamedir + '/bin/tblastx.exe', self.pwd)
            except:
                pass
        else:
            try:
                shutil.move(filenamedir + '/bin/makeblastdb', self.pwd)
            except:
                pass
            try:
                shutil.move(filenamedir + '/bin/blastn', self.pwd)
            except:
                pass
            try:
                shutil.move(filenamedir + '/bin/tblastx', self.pwd)
            except:
                pass
        tfile.close()
        shutil.rmtree(filenamedir)
        os.remove(filename)
        if os.path.exists(self.pwd + '/blastn') or os.path.exists(self.pwd + '/blastn.exe'):
            self.processLab.config(text='Extracting file... Done\nBLAST+ installed.')
        else:
            self.processLab.config(text='Unable to download blast.\nPlease dowload manually.')

def gbk2fasta(genbank, out, mincut, maxcut):
    getseq = False
    getembl = False
    getmultifa = False
    seq = ''
    try:
        mincut = int(mincut)
        if mincut < 1: mincut = 1
        if maxcut != 'Max':
            maxcut = int(maxcut)
        if maxcut < 1: maxcut = 1
    except:
        print 'Annotation slice values not valid.'
    try:
        gen = open(genbank)
        outfile = open(out, 'w')
        for line in gen:
            if line.startswith('ORIGIN'):
                getseq = True
            elif line.startswith('SQ   Sequence'):
                getembl = True
            elif line.startswith('>'):
                if getmultifa:
                    seq += 'qqq'
                else:
                    getmultifa = True
            elif line.startswith('//'):
                getseq = False
                getembl = False
            elif getseq:
                seq += ''.join(line.split()[1:])
            elif getembl:
                seq += ''.join(line.split()[:-1])
            elif getmultifa:
                seq += line.rstrip()
        if getmultifa:
            getset = set(seq)
            rightchars = set('atgcATGCqnNuUyYkKmMsSwWbBdDhHvVxXrR-')
            isitgood = True
            for i in getset:
                if not i in rightchars:
                    isitgood = False
            if not isitgood:
                print 'Annotation file contains invalid characters. Check genbank/EMBL contains no lines starting with > or that fasta file contains only valid nucleotides'
                return 0
        if '/' in out:
            outfile.write('>' + out.split('/')[1] + '\n')
        else:
            outfile.write('>' + out + '\n')
        if maxcut == 'Max':
            maxcut = len(seq)
        if mincut == 1 and maxcut == len(seq):
            if getmultifa:
                seq = seq.replace('qqq', 'n' * (len(seq) / 500))
            outfile.write(seq)
        elif mincut < maxcut:
            seq = seq[mincut-1:maxcut]
            if getmultifa:
                seq = seq.replace('qqq', 'n' * (len(seq) / 500))
            outfile.write(seq)
        else:
            seq = seq[mincut-1:] + seq[:maxcut]
            if getmultifa:
                seq = seq.replace('qqq', 'n' * (len(seq) / 500))
            outfile.write(seq)
        if len(seq) == 0:
            print 'There is no sequence in ' + genbank + '.'
            return 0
        else:
            return 1
    except:
        print genbank + ' does not exist.'
        return 0

def getGCcontent(filename, windsize, step, mincut, maxcut):
    try:
        gen = open(filename)
        getseq = False
        getembl = False
        seq = ''
        for line in gen:
            if line.startswith('ORIGIN'):
                getseq = True
            elif line.startswith('SQ   Sequence'):
                getembl = True
            elif line.startswith('//'):
                getseq = False
                getembl = False
            elif getseq:
                seq += ''.join(line.split()[1:])
            elif getembl:
                seq += ''.join(line.split()[:-1])
        gen.close()
        seq = seq.upper()
    except:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    if len(seq) == 0:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    if maxcut == 'Max':
        seq = seq[int(mincut)-1:]
    elif int(maxcut) <= int(mincut):
        seq = seq[int(mincut)-1:] + seq[:int(maxcut)+1]
    else:
        seq = seq[int(mincut)-1:int(maxcut)+1]
    window1 = int(windsize) / 2
    window2 = int(windsize) - window1
    thearray = []
    for i in range(0, len(seq), int(step)):
        seqstring = seq[max([0, i-window1]):i+window2]
        thearray.append((seqstring.count('G') + seqstring.count('C')) * 1.0 / len(seqstring) - 0.5)
    return thearray

def getGCskew(filename, windsize, step, mincut, maxcut):
    try:
        getseq = False
        getembl = False
        seq = ''
        gen = open(filename)
        for line in gen:
            if line.startswith('ORIGIN'):
                getseq = True
            elif line.startswith('SQ   Sequence'):
                getembl = True
            elif line.startswith('//'):
                getseq = False
                getembl = False
            elif getseq:
                seq += ''.join(line.split()[1:])
            elif getembl:
                seq += ''.join(line.split()[:-1])
        gen.close()
        seq = seq.upper()
    except:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    if len(seq) == 0:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    if maxcut == 'Max':
        seq = seq[int(mincut)-1:]
    elif int(maxcut) <= int(mincut):
        seq = seq[int(mincut)-1:] + seq[:int(maxcut)+1]
    else:
        seq = seq[int(mincut)-1:int(maxcut)+1]
    window1 = int(windsize) / 2
    window2 = int(windsize) - window1
    thearray = []
    for i in range(0, len(seq), int(step)):
        seqstring = seq[max([0, i-window1]):i+window2]
        gcount = seqstring.count('G')
        ccount = seqstring.count('C')
        try:
            thearray.append((gcount - ccount) * 1.0 / (gcount + ccount))
        except:
            thearray.append(0)
    return thearray

def getCoverage(filename, filename2, mincut, maxcut):
# DEFNIITION: takes a file and reads in all contigs, their start positions and the reads located within the contig
# REQUIRES: a valid ace file
# RETURNS: A list of objects of class contig
    seq = ''
    getseq = False
    getembl = False
    try:
        gen = open(filename)
        for line in gen:
            if line.startswith('ORIGIN'):
                getseq = True
            elif line.startswith('SQ   Sequence'):
                getembl = True
            elif line.startswith('//'):
                getseq = False
                getembl = False
            elif getseq:
                seq += ''.join(line.split()[1:])
            elif getembl:
                seq += ''.join(line.split()[:-1])
        gen.close()
    except:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    if len(seq) == 0:
        print 'Annotation file ' + filename + ' not valid.'
        return None
    seq = seq.lower()
    if maxcut == 'Max':
        seq = seq[int(mincut)-1:]
    elif int(maxcut) <= int(mincut):
        seq = seq[int(mincut)-1:] + seq[:int(maxcut)+1]
    else:
        seq = seq[int(mincut)-1:int(maxcut)+1]
    outlist = [0 for i in range(len(seq))]
    readlist = [] # list of reads to be added to the contig class
    index = 0 # switches to 1 once program has dealt with the initial contig
    # iterates through the file determines what information is contained in each line then reads it to the
    # right locationregular expressions python
    transtab = string.maketrans('atgc', 'tacg')
    acefile = open(filename2)
    for line in acefile:
        # puts name in file and starts reading sequence below
        if line.startswith("CO "):
            if index != 0:
                freqDict = {}
                for j in readlist:
                    for k in range(j.startpos, (j.startpos + j.readLength)):
                        if k in freqDict:
                            freqDict[k] += 1
                        else:
                            freqDict[k] = 1
                coverageList = []
                for j in range(1, len(contigSeq) + 1):
                    if contigSeq[j - 1] != '*':
                        coverageList.append(freqDict[j])
                contigSeq = contigSeq.lower()
                thepos = seq.find(contigSeq)
                if thepos != -1:
                    outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
                else:
                    contigSeq = contigSeq[::-1]
                    contigSeq = contigSeq.translate(transtab)
                    thepos = seq.find(contigSeq)
                    if thepos != -1:
                        coverageList.reverse()
                        outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
                readlist = []
            index = 1
            contigSeq = ''
            contigName = line.split()[1] # splits the line into a list with elements seperated by whitespace characters
                                      # then returns the second element of that list (the name)
            readnumber = 0 # initiates the read number used to determine where the readsequence will be added
      # creates a object of class read with the name and location within the contig, leaves sequence as the
      # empty string to be read in later
        elif line.startswith('BQ'):
            index = 2
        elif line.startswith("AF "):
            readIt = line.split() # splits the line into a list of strings seperated by whitespace characters
            readName = readIt[1] # the name of the read
            readPos = int(readIt[3]) # the position of the read within the contig
            readInstance = read(readName, readPos, None) # creates an instance of class read
            readlist.append(readInstance) # appends to list
        elif index == 1:
            contigSeq += line[:-1]
        elif line.startswith("QA "):
            readlist[readnumber].startpos = readlist[readnumber].startpos + int(line.split()[1]) - 1
            readlist[readnumber].readLength = int(line.split()[2]) - int(line.split()[1]) + 1
            readnumber += 1
    freqDict = {}
    for j in readlist:
        for k in range(j.startpos, (j.startpos + j.readLength)):
            if k in freqDict:
                freqDict[k] += 1
            else:
                freqDict[k] = 1
    coverageList = []
    for j in range(1, len(contigSeq) + 1):
        if contigSeq[j - 1] != '*':
            coverageList.append(freqDict[j])
    contigSeq = contigSeq.lower()
    thepos = seq.find(contigSeq)
    if thepos != -1:
        outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
    else:
        contigSeq = contigSeq[::-1]
        contigSeq = contigSeq.translate(transtab)
        thepos = seq.find(contigSeq)
        if thepos != -1:
            coverageList.reverse()
            outlist = outlist[:thepos] + coverageList + outlist[thepos + len(coverageList):]
    return outlist

def getCustom(filename):
    try:
        thearray = []
        gen = open(filename)
        templine = gen.readline().rstrip().split('\t')
        linelen = len(templine)
        for i in templine:
            thearray.append([float(i)])
        for line in gen:
            templine = line.rstrip().split('\t')
            for i in range(len(templine)):
                if templine[i] != '':
                    thearray[i].append(float(templine[i]))
        return thearray
    except:
        print filename + ' not valid graph file.'
        return None



def genBlast(inlist, cutlist):
    try:
        os.mkdir('temp_easyfig')
    except:
        pass
    num = 1
    outlist = []
    for i in inlist:
        gbk2fasta(i, 'temp_easyfig/' + str(num) + '.easyfig.fa', cutlist[num-1][0], cutlist[num-1][1])
        num += 1
    for i in range(len(inlist) - 1):
        if isNewBlastDB():
            subprocess.Popen('makeblastdb -dbtype nucl -out temp_easyfig/tempdb -in temp_easyfig/' + str(i + 2) +
                             '.easyfig.fa', shell=True).wait()
            print 'makeblastdb -dbtype nucl -out temp_easyfig/tempdb -in temp_easyfig/' + str(i + 2) + '.easyfig.fa'
        elif isLegBlastDB():
            subprocess.Popen('formatdb -p F -t tempdb -n temp_easyfig/tempdb -i temp_easyfig/'
                             + str(i + 2) + '.easyfig.fa', shell=True).wait()
        else:
            print 'Could not find BLAST.'
            sys.exit()
        if isNewBlastn():
            subprocess.Popen('blastn -task blastn -db temp_easyfig/tempdb -outfmt 6 -query temp_easyfig/' + str(i+1)
                             + '.easyfig.fa -out temp_easyfig/' + str(i + 1) + str(i+2) + '.easyfig.out',
                             shell=True).wait()
        elif isLegBlastall():
            subprocess.Popen('blastall -p blastn -d temp_easyfig/tempdb -F F -m 8 -a 8 -i temp_easyfig/'
                         + str(i + 1) + '.easyfig.fa -o temp_easyfig/'
                         + str(i+1) + str(i+2) + '.easyfig.out', shell=True).wait()
        else:
            print 'Could not find BLAST.'
            sys.exit()
        outlist.append(inlist[i])
        outlist.append('temp_easyfig/' + str(i+1) + str(i+2) + '.easyfig.out')
    outlist.append(inlist[-1])
    return outlist

def genTBlastX(inlist, cutlist):
    pwd = os.getcwd()
    if os.path.exists('temp_easyfig'):
        print 'please run from a directory without the folder temp_easyfig'
        sys.exit()
    os.mkdir('temp_easyfig')
    os.chdir('temp_easyfig')
    num = 1
    outlist = []
    for i in inlist:
        if i[0] in ['/', '\\', '~']:
            thepath = i
        else:
            thepath = '../' + i
        gbk2fasta(thepath, str(num) + '.easyfig.fa', cutlist[num-1][0], cutlist[num-1][1])
        num += 1
    for i in range(len(inlist) - 1):
        if isNewBlastDB():
            subprocess.Popen('makeblastdb -dbtype nucl -out tempdb -in ' + str(i + 2) +
                             '.easyfig.fa', shell=True).wait()
        elif isLegBlastDB():
            subprocess.Popen('formatdb -p F -t tempdb -n tempdb -i '
                             + str(i + 2) + '.easyfig.fa', shell=True).wait()
        else:
            print 'Could not find BLAST.'
            sys.exit()
        if isNewTblastx():
            subprocess.Popen('tblastx -db tempdb -outfmt 6 -query ' + str(i+1)
                             + '.easyfig.fa -out ' + str(i + 1) + str(i+2) + '.easyfig.out',
                             shell=True).wait()
        elif isLegBlastall():
            subprocess.Popen('blastall -p tblastx -d tempdb -F F -m 8 -a 8 -i '
                         + str(i + 1) + '.easyfig.fa -o '
                         + str(i+1) + str(i+2) + '.easyfig.out', shell=True).wait()
        else:
            print 'Could not find BLAST.'
            sys.exit()
        outlist.append(inlist[i])
        outlist.append(os.getcwd() + '/' + str(i+1) + str(i+2) + '.easyfig.out')
    os.chdir(pwd)
    outlist.append(inlist[-1])
    return outlist


global abortCaptain



minlength = 0
mineval = 0.001
minIdent = 0
inputlist = []
width = 5000
height1 = 50
height2 = 100
minblastc = (200, 200, 200)
maxblastc = (100, 100, 100)
minblastci = (200, 200, 200)
maxblastci = (100, 100, 100)
drawfig1 = False
drawfig2 = False
drawfig3 = False
compress = True
reverseList = []
featDict = {}
glt = 5
exont = 2
genet = 1
featlengths = []
aln = 'centre'
graphit = None
blastoutline = True
minmaxlist = []
getgc = False
getgcskew = False
getcoverage = False
getcustom = False
windsize = 1000
step = 1000
graphit = None
multigraph = True
loggraph = False
gtype = 'Histogram'
axisthick = 1
pvc = (255, 0, 0)
nvc = (0, 0, 255)
ggap = 10
gheight = 50
blastit = True
tblastit = False
blastfiles = None
lastflag = 1
filename = None
svg = False
filter = False
keep_blast = False
nofeat = False
gmaxy = 'Auto'
legend = 'None'
legname = 'gene'
abortCaptain = False

if len(sys.argv) >= 2 and sys.argv[1] != '--help' and sys.argv[1] != '-h' and sys.argv[1] != '-help':
    for i in range(1,len(sys.argv)):
        if sys.argv[i][:1] == '-':
            lastflag = i + 2
        if sys.argv[i] == '-o':
            filename = sys.argv[i+1]
        elif sys.argv[i] == '-e':
            mineval = float(sys.arg[i+1])
        elif sys.argv[i] == '-min_length':
            minlength = int(sys.argv[i+1])
        elif sys.argv[i] == '-i':
            minIdent = float(sys.argv[i+1])
        elif sys.argv[i] == '-width':
            width = int(sys.argv[i+1])
        elif sys.argv[i] == '-ann_height':
            height1 = int((sys.argv[i+1]))
        elif sys.argv[i] == '-blast_height':
            height2 = int((sys.argv[i+1]))
        elif sys.argv[i] == '-f1':
            if sys.argv[i+1] == 'T' or sys.argv[i+1] == 't' or sys.argv[i+1] == 'True' or sys.argv[i+1] == 'true':
                drawfig1 = True
            elif sys.argv[i+1] == 'F' or sys.argv[i+1] == 'f' or sys.argv[i+1] == 'False' or sys.argv[i+1] == 'false':
                drawfig1 = False
        elif sys.argv[i] == '-f2':
            drawfig2 = int(sys.argv[i+1])
        elif sys.argv[i] == '-f3':
            drawfig3 = sys.argv[i+1]
        elif sys.argv[i] == '-uncomp':
            if sys.argv[i+1] == 'T' or sys.argv[i+1] == 't' or sys.argv[i+1] == 'True' or sys.argv[i+1] == 'true':
                compress = False
        elif sys.argv[i] == '-blastn':
            blastit = True
            lastflag -= 1
        elif sys.argv[i] == '-tblastx':
            tblastit = True
            blastit = False
            lastflag -= 1
        elif sys.argv[i] == '-blast_files':
            blastit = False
            blastfiles = i
        elif sys.argv[i] == '-blast_col':
            if sys.argv[i+ 1].isdigit():
                lastflag = i+7
                t1 = int(sys.argv[i+1])
                t2 = int(sys.argv[i+2])
                t3 = int(sys.argv[i+3])
                t4 = int(sys.argv[i+4])
                t5 = int(sys.argv[i+5])
                t6 = int(sys.argv[i+6])
            else:
                if sys.argv[i+1] == 'blue':
                    t1, t2, t3, t4, t5, t6 = 30, 144, 255, 25, 25, 112
                elif sys.argv[i+1] == 'red':
                    t1, t2, t3, t4, t5, t6 = 200, 100, 0, 255, 0, 0
            minblastc = (t1, t2, t3)
            maxblastc = (t4, t5, t6)
        elif sys.argv[i] == '-blast_col_inv':
            if sys.argv[i+ 1].isdigit():
                lastflag = i+7
                t1 = int(sys.argv[i+1])
                t2 = int(sys.argv[i+2])
                t3 = int(sys.argv[i+3])
                t4 = int(sys.argv[i+4])
                t5 = int(sys.argv[i+5])
                t6 = int(sys.argv[i+6])
            else:
                if sys.argv[i+1] == 'blue':
                    t1, t2, t3, t4, t5, t6 = 30, 144, 255, 25, 25, 112
                elif sys.argv[i+1] == 'red':
                    t1, t2, t3, t4, t5, t6 = 200, 100, 0, 255, 0, 0
            minblastci = (t1, t2, t3)
            maxblastci = (t4, t5, t6)
        elif sys.argv[i] == '-f':
            r, g, b = 64, 224, 208
            arrow = 'arrow'
            feat = sys.argv[i+1]
            if feat == 'F':
                nofeat = True
            if len(sys.argv) > i + 2 and sys.argv[i+2].isdigit():
                r = int(sys.argv[i+2])
                g = int(sys.argv[i+3])
                b = int(sys.argv[i+4])
                if len(sys.argv) > i + 5 and (sys.argv[i+5] == 'arrow' or sys.argv[i+5] == 'rect' \
                or sys.argv[i+5] =='frame' or sys.argv[i+5] == 'pointer'):
                    arrow = sys.argv[i+5]
                    lastflag = i + 6
                else:
                    lastflag = i + 5
            if len(sys.argv) > i + 2 and (sys.argv[i+2] == 'arrow' or sys.argv[i+2] == 'rect' \
            or sys.argv[i+2] =='frame' or sys.argv[i+2] == 'pointer'):
                arrow = sys.argv[i+2]
                lastflag = i + 3
            featDict[feat] = (arrow, (r, g, b))
        elif sys.argv[i] == '-glt':
            glt = int(sys.argv[i+1])
        elif sys.argv[i] == '-exont':
            exont = int(sys.argv[i+1])
        elif sys.argv[i] == genet:
            genet = int(sys.argv[i+1])
        elif sys.argv[i] == '-aln':
            aln = sys.argv[i+1]
            if aln == 'best':
                aln = 'best blast'
        elif sys.argv[i] == '-bo':
            if sys.argv[i+1] == 'T' or sys.argv[i+1] == 't' or sys.argv[i+1] == 'True' or sys.argv[i+1] == 'true':
                blastoutline = True
            else:
                blastoutline = False
        elif sys.argv[i] == '-G':
            if sys.argv[i+1] == 'GCContent':
                getgc = True
            elif sys.argv[i+1] == 'GCSkew':
                getgcskew = True
            elif sys.argv[i+1] == 'Coverage':
                getcoverage = True
                gfilename = sys.arv[i+2]
                lastflag += 1
            elif sys.argv[i+1] == 'Custom':
                getcustom = True
                gfilename = sys.argv[i+2]
                lastflag += 1
            else:
                print sys.argv[i+1] + ' not a valid graph type'
        elif sys.argv[i] == '-wind_size':
            windsize = int(sys.argv[i+1])
        elif sys.argv[i] == '-step':
            step = int(sys.argv[i+1])
        elif sys.argv[i] == '-line':
            if sys.argv[i+1] == 'T' or sys.argv[i+1] == 't' or sys.argv[i+1] == 'True' or sys.argv[i+1] == 'true':
                gtype = 'Line'
        elif sys.argv[i] == '-axis_t':
            axisthick = sys.argv[i+1]
        elif sys.argv[i] == '-pos_col':
            lastflag = i + 4
            r = int(sys.argv[i+1])
            g = int(sys.argv[i+2])
            b = int(sys.argv[i+3])
            pvc = (r, g, b)
        elif sys.argv[i] == '-neg_col':
            lastflag = i + 4
            r = int(sys.argv[i+1])
            g = int(sys.argv[i+2])
            b = int(sys.argv[i+3])
            nvc = (r, g, b)
        elif sys.argv[i] == '-g_height':
            gheight = int(sys.argv[i+1])
        elif sys.argv[i] == '-gap':
            ggap = int(sys.argv[i+1])
        elif sys.argv[i] == '-y_max':
            gmaxy = int(sys.argv[i+1])
        elif sys.argv[i] == '-A':
            if sys.argv[i+1] == 'T' or sys.argv[i+1] == 't' or sys.argv[i+1] == 'True' or sys.argv[i+1] == 'true':
                auto = True
            else:
                auto = False
        elif sys.argv[i] == '-svg':
            svg = True
            lastflag -= 1
        elif sys.argv[i] == '-keep':
            keep_blast = True
            lastflag -= 1
        elif sys.argv[i] == '-filter':
            filter = True
            lastflag -= 1
        elif sys.argv[i] == '-legend':
            if sys.argv[i+1] == 'single':
                legend = 'Single column'
            elif sys.argv[i+1] == 'double':
                legend = 'Two columns'
            elif sys.argv[i+1] == 'top':
                legend = 'Top'
            elif sys.argv[i+1] == 'bottom':
                legend = 'Bottom'
            elif sys.argv[i+1] == 'both':
                legend = 'Top & Bottom'
            else:
                print 'Legend options are <single/double/top/bottom/both/None> (case sensitive), using None.'
        elif sys.argv[i] == '-leg_name':
            legname = sys.argv[i+1]
    inlist = sys.argv[lastflag+1:]
    if blastfiles != None and lastflag == blastfiles + 2:
        allthestuff = sys.argv[blastfiles+1:]
        allthestuff2 = []
        for i in allthestuff:
            if i != 'R' and i != 'Max' and not i.isdigit():
                allthestuff2.append(i)
        inlist = allthestuff[len(allthestuff2)/2:]
        last = inlist[0]
        inlist = inlist[1:]
    else:
        last = sys.argv[lastflag]
    templist = []
    revlist = []
    cutlist = []
    rev = False
    cuts = [None, None]
    for i in inlist:
        if i == 'R' or i == 'Max' or i.isdigit():
            if os.path.exists(i):
                sys.stderr.write('Cannot tell if "' + i +
                                 '" is an file or argument (the file exists and this is also the argument to trim or reverse genome).\
            \nPlease rename file (if file) or remove file from directory (if argument).\n')
                sys.exit()
        if i == 'R':
            rev = True
            getit = True
        elif i.isdigit():
            if cuts[0] == None:
                cuts[0] = int(i)
            else:
                cuts[1] = int(i)
        elif i == 'Max':
            cuts[1] = i
        else:
            revlist.append(rev)
            if cuts == [None, None]:
                cuts = [1, 'Max']
            cutlist.append(tuple(cuts))
            templist.append(last)
            rev = False
            cuts = [None, None]
            last = i
    revlist.append(rev)
    if cuts == [None, None]:
        cuts = [1, 'Max']
    cutlist.append(tuple(cuts))
    for i in cutlist:
        if None in i:
            sys.stderr.write('Please provide a start coordinate and end coordinate for genome cuts. (Only a single coordinate was provided)\n')
            sys.exit()
    templist.append(last)
    if getgc:
        thearray = []
        for j in range(len(templist)):
            mincut, maxcut = cutlist[j]
            thearray.append(getGCcontent(templist[j], windsize, step, mincut, maxcut))
        graphit = [thearray, pvc, nvc, gheight, axisthick, gtype, gmaxy, ggap]
    elif getgcskew:
        thearray = []
        for j in range(len(templist)):
            mincut, maxcut = cutlist[j]
            thearray.append(getGCskew(templist[j], windsize, step, mincut, maxcut))
        graphit = [thearray, pvc, nvc, gheight, axisthick, gtype, gmaxy, ggap]
    elif getcustom:
        thearray = getcustom(gfilename)
        graphit = [thearray, pvc, nvc, gheight, axisthick, gtype, gmaxy, ggap]
    elif getcoverage:
        thearray = [getCoverage(templist[0], gfilename, cutlist[0][0], cutlist[0][1])]
        graphit = [thearray, pvc, nvc, gheight, axisthick, gtype, gmaxy, ggap]
    if blastit:
        inlist = genBlast(templist, cutlist)
    elif tblastit:
        inlist = genTBlastX(templist, cutlist)
    elif blastfiles != None:
        inlist = []
        tempfiles = sys.argv[blastfiles+1:]
        for i in templist[:-1]:
            inlist.append(i)
            inlist.append(tempfiles.pop(0))
        inlist.append(templist[-1])
    else:
        'Please choolse -blastn or -tblastx flags to generate blast files, or use -blast_files to use previously generated files.'
    if filename == None:
        print 'Please choose a file to write to (-o tag) and try agian.'
        sys.exit()
    if featDict == {} and not nofeat:
        featDict = {'CDS': ('arrow', (64, 224, 208))}
    if svg :
        x = drawsvg(filename, minlength, mineval, minIdent, inlist, width, height1, height2,
         minblastc, maxblastc, minblastci, maxblastci, drawfig1, drawfig2, drawfig3,
         compress, revlist, featDict, glt, exont, genet, featlengths, aln, graphit,
         blastoutline, cutlist, filter, legend, legname)
    else:
        x = draw(filename, minlength, mineval, minIdent, inlist, width, height1, height2,
         minblastc, maxblastc, minblastci, maxblastci, drawfig1, drawfig2, drawfig3,
         compress, revlist, featDict, glt, exont, genet, featlengths, aln, graphit,
         blastoutline, cutlist, filter, legend, legname)
    if (blastit or tblastit) and not keep_blast:
        shutil.rmtree('temp_easyfig')
    print "Minimum blast hit reported: " + str(x) + '%'

elif len(sys.argv) == 1:
    from Tkinter import *
    import tkFileDialog
    import tkMessageBox
    import tkSimpleDialog
    import tkColorChooser
    class DDlistbox(Listbox):
        def __init__(self, master, **kw):
            kw['selectmode'] = SINGLE
            Listbox.__init__(self, master, kw)
            self.bind('<Button-1>', self.setCurrent)
            self.bind('<B1-Motion>', self.shiftSelection)
            self.curIndex = None
        def setCurrent(self, event):
            self.curIndex = self.nearest(event.y)
        def shiftSelection(self, event):
            i = self.nearest(event.y)
            if i < self.curIndex:
                x = self.get(i)
                self.delete(i)
                self.insert(i+1, x)
                self.curIndex = i
            elif i > self.curIndex:
                x = self.get(i)
                self.delete(i)
                self.insert(i-1, x)
                self.curIndex = i
    abortCaptain = False
    root = Tk()
    root.title('Easyfig.py')
    root.option_add('*Font', 'TkDefaultFont 12')
    app = App(root)
    root.mainloop()
else:
    print '''
Easyfig.py   Written by: Mitchell Sullivan   mjsull@gmail.com
Supervisor: Dr. Scott Beatson   University of Queensland    03.12.2010

License: GPLv3

Version 2.2.3

Usage: Easyfig.py [options] GenBank/EMBL/fasta GenBank/EMBL/fasta GenBank/EMBL/fasta ...

This script should work on 1 to an infinite amount of GenBank/EMBL files (given enough memory)

Adding 2 integers after the annotation file will crop the annotation file.
Adding a R after the annotation file will reverse compliment it.

WARNING: Will overwrite output file without warning.
WARNING: Will delete temp_easyfig folder if -keep flag not given.

***************************************************************
GenBank or EMBL file must have source line, or Sequence.
'     source  1..<sequence length>' or 'FT   source    1..<sequence length>'

for GenBank / EMBL

***************************************************************

The GenBank file preceding the blast file should always be the query
the GenBank file after the blast file should always be the reference
In it's present state only 'CDS' features will be recorded

Options:
-o <string>   Specify output file. <REQUIRED!>
-blastn       Generate blastn files automatically. Requires blastall or blast+
              in the path, Annotation file must have nucleotide sequence. [Default]
-tblastx      Generate tblastx files automatically. Requires blastall or blast+
              in the path, Annotation file must have nucleotide sequence.
-blast_files  List of previously generated blast files, ordered. Query must be
              annotation file on top, reference annotation file on bottom.
-svg          Create Scalable Vector Graphics (svg) file instead of bmp.
-filter       Filter small blast hits or annotations (< 4 pixels wide). [F]


GENERAL OPTIONS:
-width <int>          width of figure in pixels. [5000]
-ann_height <int>     height of annotations in figure (pixels). [50]
-blast_height <int>   height of blast hits in figure (pixels). [100]
-f1 <T/F>             draw colour gradient figure for blast hits. [F]
-f2 <int>             draw scale figure <int> base pairs long. [0]
-uncomp <T/F>         Do not compress figure. [F]
-f  <string> [r g b] [arrow/rect/pointer/frame]
                      Draw features of type <string> (case sensitive) in the
                      color r g b with illustration type arrow, rectangle,
                      pointer or frame. Default light blue arrows.
                      EXAMPLE: -f CDS 255 0 0 rect will draw all CDS features as
                      a red rectangle.
                      if none specified easyFig automatically draws CDS features.
                      If you want a figure with no features drawn use -f F
-glt <int>            Genome line is <int> pixels thick [5]
-exont <int>          exon lines joining introns are <int> pixels thick. [1]
-genet <int>          outline of features is <int> pixels thick. [1]
-aln <best/left/right/centre> [centre]
                      Alignment of genomes
                      best aligns feature file perpendicular to best blast hit.
-legend <single/double/top/bottom/both/None>
                      Single: Gene names in single column
                      Double: Gene names in two columns
                      Top: Top feature file genes labelled above figure
                      Bottom: Bottom feature file genes labelled below figure
                      Both: Top and bottom feature files genes labelled above
                            and below genome.
                      None: No legend or gene labelling <default>
-leg_name             Where to get feature name from [gene]

BLAST OPTIONS:
-e <float>            maxmimum e value of blast hits to be drawn. [0.001]
-i <float>            minimum identity value of blast hits to be drawn. [0]
-min_length <int>     minimum length of blast hits to be drawn. [0]
-blast_col <red/blue> changes blast hits to gradient of red or blue
                      alternitively <int1 int2 int3 int4 int5 int6>
                      defines color gradient for blast hits
                      worst blast hit reported will be color int1 int2 int3
                      where int 1 2 3 is the RGB of color range[0-255]
                      100% identity blast hits will be color int4 int5 int6
                      [default 20 20 20 175 175 175] <gray>

-blast_col_inv        Colour for inverted blast hits.
-bo <T/F>             Black outline of blast hits. [T]
-keep                 Don't delete blast output (temp_easyfig/)

GRAPH OPTIONS:
-G <GCContent/GCSkew/Coverage/Custom [filename]>
                      Plot GC Content, GC Skew, Coverage or Custom graph.
                      if Coverage or Custom filename for ace or custom file needs
                      to be provided. Details on how to make custom graph files
                      in manual.
-wind_size <int>      Window size for calculating GC content/GC skew. [1000]
-step <int>           Step size for calculating GC content/GC skew. [1000]
-line <T/F>           Draw graph as a line graph. [T]
-axis_t               Thickness of X axis. [1]
-pos_col <int int int> RGB colour of positive values in graph. [Red]
-neg_col <int int int> RGB colour of negative values in graph. [Blue]
-g_height <int>       height of graph in pixels. [50]
-gap                  gap between graph and annotations. [10]
-y_max                Maximum y value [Default: max Y calculated.]


EXAMPLES:

Easyfig.py -filter -o outfile.bmp genbank1.gbk genbank2.gbk genbank3.gbk

Easiest way to generate a simple comparison file between three (or more) annotation
files. Shows CDS features as red arrows.

Easyfig.py -o outfile.bmp -e 0.00001 -f gene frame 0 0 255 -G GCContent ann1.embl ann2.gbk ann3.gbk ann4.embl

Generate a blastn comparison between 4 annotation files, Display genes as blue
arrows in frame. Only report blast hits under 0.00001 expect value.
Display the GC content of each file as a graph.

Easyfig.py -tblastx -o outfile.svg -svg ann1.embl 1 10000 ann2.embl 1 10000 R

Show a tblastx comparison of the first 10000 base pairs of ann1.embl and ann2.embl
Reverse compliment ann2.embl. Writes as a SVG file.


this script uses a modified version of Paul McGuire's (http://www.geocities.com/ptmcg/ RIP (geocities, not paul))
bmp.py - module for constructing simple BMP graphics files
'''