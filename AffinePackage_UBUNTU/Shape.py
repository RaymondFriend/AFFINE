#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shape.py: a module that generates the planar shapes called for in main.py. Instance methods."""

__author__      = "Raymond Friend"
__copyright__   = "Copyright 2019, Penn State University"
__credits__ = ["Raymond Friend", "Sergei Tabachnikov"]
__version__ = "2.0.1"
__maintainer__ = "Raymond Friend"
__email__ = "rayjfriend@gmail.com"
__status__ = "Production"


from PVector import *
from PolyVector import *
from math import floor, sin, cos, pi

def NGon(N, R, centerPos):
	"""Generates regular N-gon, of vertex radius r, centered at centerPos, returning PolyVector"""
	r = float(R)
	vertices = []
        angleShift = - pi / 2 if N % 2 == 1 else (-pi / float(N) if N % 4 == 0 else -2 * pi / float(N))
        for n in range(0, N): 
                vertices.append(PVector.add(PVector.mult(PVector(cos(pi * 2 * float(n) / float(N) + angleShift), sin(pi * 2 * float(n) / float(N) + angleShift)), r), centerPos))
	return PolyVector(vertices)

def Trapezoid(S, centerPos, width):
	"""Generates isosceles Trapezoid, with ratio long:short = s:1, with center of trapezoid at centerPos, and all drawing maximum width of `width' (s >= 1)"""
	s = float(S)
	w = float(width)
	vertices = [
		PVector(centerPos.x - w / 2, centerPos.y + w / 2),
		PVector(centerPos.x + w / 2, centerPos.y + w / 2),
		PVector(centerPos.x + w / (2 * s), centerPos.y - w / 2),
		PVector(centerPos.x - w / (2 * s), centerPos.y - w / 2)
	]
	return PolyVector(vertices)

def Parallelogram(S, centerPos, width):
	"""Generates a parallelogram, subtended by maximum width of `width', centered at centerPos, and with s acting as the shearing (s >= 0)"""
	s = float(S)
	w = float(width) / (s + 1)
	vertices = [
		PVector(centerPos.x - w * (s + 1) / 2, centerPos.y + w / 2),
		PVector(centerPos.x - w * (s - 1) / 2, centerPos.y + w / 2),
		PVector(centerPos.x + w * (s + 1) / 2, centerPos.y - w / 2),
		PVector(centerPos.x + w * (s - 1) / 2, centerPos.y - w / 2)
	]
	return PolyVector(vertices)

def Kite(S, centerPos, height):
	"""Generates a kite, subtended by a maximum height of `height', centered at centerPos, and with s acting as the vertical stretch (s >= 1)"""
	s = float(S)
	h = 2 * float(height) / (s + 1)
	vertices = [
		PVector(centerPos.x - h / 2, centerPos.y - h * (s - 1) / 4),
		PVector(centerPos.x, centerPos.y + h * (s + 1) / 4),
		PVector(centerPos.x + h / 2, centerPos.y - h * (s - 1) / 4),
		PVector(centerPos.x, centerPos.y - h * (s + 1) / 4)
	]
	return PolyVector(vertices)

def Quadrilateral(S, centerPos, P):
	"""Generates a quadrilateral, with unit vectors as two sides, and P as the fourth vertex. """
	"""S will specify length of unit vectors (recommend 100), centerPos will specify origin coordinates (recommend (0,0)), and P will be provided as if S = 1, centerPos = (0,0)"""
	s = float(S)
	newP = PVector.add(centerPos, PVector.mult(P, s))
	vertices = [
		PVector(centerPos.x + S, centerPos.y),
		PVector(centerPos.x, centerPos.y),
		PVector(centerPos.x, centerPos.y + S),
		PVector(centerPos.x + S * P.x, centerPos.y + S * P.y)
	]
	return PolyVector(vertices)

def Default():
    """Returns default shape in case of none-specified"""
    return NGon(4, 100, PVector(0, 0))
