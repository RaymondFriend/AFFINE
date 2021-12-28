#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PVector.py: a module defining the PVector class, acting as vectors in a two-dimensional space with multiple class methods and instance methods"""

__author__      = "Raymond Friend"
__copyright__   = "Copyright 2019, Penn State University"
__credits__ = ["Raymond Friend", "Sergei Tabachnikov"]
__version__ = "2.0.1"
__maintainer__ = "Raymond Friend"
__email__ = "rayjfriend@gmail.com"
__status__ = "Production"

from numpy import interp
from math import sqrt

#-----------PARAMTERS-----------
POINT_EQUALITY_DISCREPANCY = 1e-11
SLOPE_EQUALITY_DISCREPANCY = 1e-11
#-------------------------------

class PVector:
	"""object meant to store two-dimensional data"""
	def __init__(self, x, y):
		"""Constructor"""
		self.x = float(x)
		self.y = float(y)
	
	def __repr__(self):
		"""How the PVector looks in interactive prompt"""
		return "PVector()"

	def __str__(self):
		"""How the PVector prints"""
		return "(" + str(self.x) + " ," + str(self.y) + ")" 
	
	@classmethod
	def add(cls, A, B):
		"""Returns the sum of two PVector objects"""
		return PVector(A.x + B.x, A.y + B.y)
	
	@classmethod
	def sub(cls, A, B):
		"""Returns the difference of two PVector objects: A - B"""
		return PVector(A.x - B.x, A.y - B.y)
	
	@classmethod
	def mult(cls, A, r):
		"""Returns the scaled version of a PVector by r"""
		r_ = float(r)
		return PVector(A.x * r_, A.y * r_)

	@classmethod
	def div(cls, A, r):
		"""Returns the inversely scaled version of a PVector by r"""
		r_ = float(r)
		if r_ == 0:
			return PVector(0, 0)
		return PVector(A.x / r_, A.y / r_)
	
	@classmethod
	def normalize(cls, A):
		"""Returns a normalized PVector in the same direction as A"""
		r = PVector.mod(A)
		if r == 0:
			return PVector(0, 0)
		return PVector.div(A, r)

	@classmethod
	def dot(cls, A, B):
		"""Returns the dot product of two PVector objects"""
		return (A.x * B.x + A.y * B.y)
	
	@classmethod
	def map(cls, s, a, b, A, B):
		"""Outputs PVector parameterized linearly with s in (a,b)"""
		s_ = float(s)
		return PVector(interp(s_, [a, b], [A.x, B.x]), interp(s_, [a, b], [A.y, B.y]))	
	
	@classmethod
	def mod(cls, A):
		"""Returns modulus of PVector"""
		return sqrt(A.x ** 2 + A.y ** 2)

	@classmethod
	def dist(cls, A, B):
		"""Returns distance between PVectors A and B"""
		return PVector.mod(PVector.sub(A, B))

	@classmethod
	def parallel(cls, A, B):
		"""Returns True for Parallel, False otherwise"""
		return abs(A.x * B.y - A.y * B.x) < sqrt((A.x ** 2 + A.y ** 2) * (B.x ** 2 + B.y ** 2)) * SLOPE_EQUALITY_DISCREPANCY

	@classmethod
	def onLine(cls, X, A, B):
		"""Returns True if X lies on AB, False otherwise"""
		return abs((X.x - B.x) * (A.y - B.y) - (X.y - B.y) * (A.x - B.x)) < sqrt((B.y - A.y) ** 2 + (A.x - B.x) ** 2) * POINT_EQUALITY_DISCREPANCY
	
	@classmethod
	def unmap(cls, X, A, B, a, b):
		"""Returns parameter of X along AB within the interval [a,b]. Designed for when onLine(X, A, B) == True"""
		a_ = float(a); b_ = float(b)
		if A.x == B.x:
			#Resort to using the y components since they are only distinct vertically
			return a_ + (X.y - A.y) * (b_ - a_) / (B.y - A.y)
		else:
			#Perhaps not different in y components, so use horizontal components
			return a_ + (X.x - A.x) * (b_ - a_) / (B.x - A.x)

	@classmethod
	def equals(cls, A, B):
		"""Returns True if A equals B, False otherwise"""
		return PVector.mod(PVector.sub(A, B)) < POINT_EQUALITY_DISCREPANCY

	def addto(self, X):
		"""Add PVector to self"""
		self.x += X.x
		self.y += X.y
	
	def subfrom(self, X):
		"""Subtract PVector from self"""
		self.x -= X.x
		self.y -= X.y	
	
	def multby(self, r):
		"""Scale self by r"""
		r_ = float(r)
		self.x *= r_
		self.y *= r_

	def divby(self, r):
		"""Scale self inversely by r"""
		r_ = float(r)
		if r_ == 0:
			return PVector(0, 0)
		self.x /= r_
		self.y /= r_

	def modof(self):
		"""Returns modulus of self"""
		return sqrt(self.x ** 2 + self.y ** 2)
	
	def normalizethis(self):
		"""Rescale self to be of unit modulus"""
		r = self.modof()
		if r == 0:
			return
		self.divby(r)
