#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PolyVector.py: a module defining the PolyVector class, acting as vertices of planar polygons. Offers multiple instance methods."""

__author__      = "Raymond Friend"
__copyright__   = "Copyright 2019, Penn State University"
__credits__ = ["Raymond Friend", "Sergei Tabachnikov"]
__version__ = "2.0.1"
__maintainer__ = "Raymond Friend"
__email__ = "rayjfriend@gmail.com"
__status__ = "Production"


from PVector import *
from math import floor, pi, cos, sin
from random import uniform

#--------------PARAMTERS--------------
TEMPORAL_EQUALITY_DISCREPANCY = 1e-7
TEMPORAL_EQUALITY_DISCREPANCY_CORNERS = 1e-7
MAX_ORBIT_LENGTH = 4e2
#-------------------------------------

class PolyVector:
        """an object meant to store a list of PVectors"""
        def __init__(self, V): 
                """Constructor"""
                self.V = V 		# a list of PVectors describing the vertices of polygon
		self.length = len(V)	
		self.U = []		# a list of direction PVectors for edges of polygon
		for i in range(self.length):
			self.U.append(PVector.sub(self.V[(i + 1) % self.length], self.V[i]))
    
        def __repr__(self):
                """How the PolyVectors looks in interactive prompt"""
                return "PolyVector()"
 
       	def __str__(self):
                """How the PolyVector prints"""
		S = "["
		for X in self.V:
			S += str(X) + ","
                return S[:len(S) - 1] + "]"
	
	#currently not being used
	def findIndex(self, W):
		"""Searches for edge where W satisfies onLine of the two endpoints and outputs index in self.V"""
		for i in range(self.length - 1):
			if PVector.onLine(W, self.V[i], self.V[i + 1]):
				return i
		return self.length - 1 if PVector.onLine(W, self.V[self.length - 1], self.V[0]) else - 1
	
	#currently not being used
	def findParameter(self, W):
		"""W being a PVector along the PolyVector, return parameter on PolyVector corresponding to that that PVector"""
		k = findIndex(W) # an integer describing on which edge the PVector is found
		return PVector.unmap(W, self.V[k], self.V[(k + 1) % self.length], 0, 1)

	def findPosition(self, t):
		"""t being a real parameter, return position along PolyVector corresponding to that this parameter"""
		t %= self.length
		T = int(floor(t))
		return PVector.map(t - T, 0, 1, self.V[T], self.V[(T + 1) % self.length])
	

	def findIntersection(self, t, u, TEMPORAL_EQUALITY_DISCREPANCY_CORNERS):
		"""Finds the next point of intersection along the boundary of the PolyVector polygon given time t and PVector u"""
		x = self.findPosition(t)
		i = int(floor(t))                  
		I = 0; uI = PVector(0, 0); xI = PVector(0, 0); r = 0.0 # initializing values
		for j in range(1, self.length):
			I = (i + j) % self.length
			xI = self.V[I]
			uI = self.U[I]
			if PVector.parallel(u, uI):
				continue # next j
			r = (u.x * (x.y - xI.y) - u.y * (x.x - xI.x)) / (u.x * uI.y - u.y * uI.x) # calculates parameter along the segment self.V[I] to self.V[I + 1] where the line through x of direction u would intersect
			if 0 < r and r > TEMPORAL_EQUALITY_DISCREPANCY_CORNERS and 1 - r > TEMPORAL_EQUALITY_DISCREPANCY_CORNERS:
				return r + I # found an intersection that happens on the edge of the polygon
			elif 0 <= r and r < 1 and (r <= TEMPORAL_EQUALITY_DISCREPANCY_CORNERS or 1 - r <= TEMPORAL_EQUALITY_DISCREPANCY_CORNERS):
				return -((r + I) % self.length) # found a singularity (vertex), reporting error
		return None # found no intersection, likely because was between two parallel edges initially


	def findIntersection2(self, t, u, TEMPORAL_EQUALITY_DISCREPANCY_CORNERS):
		"""Finds the next point of intersection along the boundary of the PolyVector polygon given time t and PVector u"""
		x = self.findPosition(t)
		i = int(floor(t))                  
		I = 0; uI = PVector(0, 0); xI = PVector(0, 0); r = 0.0; v = 0.0; w = 0.0 # initializing values
		for j in range(1, self.length):
			I = (i + j) % self.length
			xI = self.V[I]
			uI = self.U[I]
			if PVector.parallel(u, uI):
				continue # next j
			if uI.x == 0: # use y component
				w = (u.y * uI.y * (xI.x - x.x) + u.x * uI.y * x.y - u.y * uI.x * xI.y) / (u.x * uI.y - u.y * uI.x)
				r = (w - xI.y) / uI.y
			else:
				v = (u.x * uI.x * (xI.y - x.y) + u.y * uI.x * x.x - u.x * uI.y * xI.x) / (u.y * uI.x - u.x * uI.y)
				r = (v - xI.x) / uI.x
				 # calculates parameter along the segment self.V[I] to self.V[I + 1] where the line through x of direction u would intersect
			if 0 < r and r > TEMPORAL_EQUALITY_DISCREPANCY_CORNERS and 1 - r > TEMPORAL_EQUALITY_DISCREPANCY_CORNERS:
				return r + I # found an intersection that happens on the edge of the polygon
			elif 0 <= r and r < 1 and (r <= TEMPORAL_EQUALITY_DISCREPANCY_CORNERS or 1 - r <= TEMPORAL_EQUALITY_DISCREPANCY_CORNERS):
				return -((r + I) % self.length) # found a singularity (vertex), reporting error
		return None # found no intersection, likely because was between two parallel edges initially
	
	
	def orbit(self, t0, u0, MAX_ORBIT_LENGTH, TEMPORAL_EQUALITY_DISCREPANCY, TEMPORAL_EQUALITY_DISCREPANCY_CORNERS):
		"""Primary logic for symplectic billiards. Returns the orbit, represented by an array of times where the orbit hits along the PolyVector boundary"""
		orbit = [t0] 					# starts the array of parameter positions
		orbit[-1] = t0 					# to make the process consistent 
		u = u0 						# acts as the direction vector
		i = 1						# acts as index of orbit array
		t = self.findIntersection2(orbit[i - 2], u, TEMPORAL_EQUALITY_DISCREPANCY_CORNERS) 	# calls next on orbit[-1] with initial u0, which must exist
		while i < MAX_ORBIT_LENGTH:
			t = self.findIntersection2(orbit[i - 2], u, TEMPORAL_EQUALITY_DISCREPANCY_CORNERS)
			if t > 0: # found a next point along boundary \ vertices
				orbit.append(t)
				if abs(t - orbit[0]) < TEMPORAL_EQUALITY_DISCREPANCY:
					nextT = self.findIntersection2(orbit[i - 1], self.U[int(floor(t))], TEMPORAL_EQUALITY_DISCREPANCY_CORNERS)
					if abs(nextT - orbit[1]) < TEMPORAL_EQUALITY_DISCREPANCY:
						PolyVector.report(3, {"Orbit Size" : i})
						return [orbit, 3]
				u = self.U[int(floor(t))]
				i += 1; continue
			elif t == None: # no intersection found, a problem
				PolyVector.report(2, {"Preceding Time" : orbit[i - 2], "Preceding Vector" : u})
				return [orbit, 2]
			else: # t < 0, meaning found singularity
				PolyVector.report(1, {"Preceding Time" : orbit[i - 2], "Preceding Vector" : u})
				return [orbit, 1]
		PolyVector.report(0, {"Max orbit size is" : MAX_ORBIT_LENGTH})
		return [orbit, 0]

	def average(self):
		"""Computes average position of all PVectors"""
		X = 0.
		Y = 0.
		for i in range(self.length):
			X += self.V[i].x
			Y += self.V[i].y
		return PVector(X / self.length, Y / self.length)

	def maxDistanceTo(self, V):
		"""Computes maximum distance between a specified PVector V and all PVectors in self.V"""
		d = 0.
		for i in range(self.length):
			D = PVector.dist(self.V[i], V)
			if D > d:
				d = D
		return d

	@classmethod
	def report(cls, code, message = {}, toPrint = True):
		"""Generates reports to print out based on behavior of orbit"""
		codeDict = {
			0 : "Reached maximum orbit length",
			1 : "Singularity found",
			2 : "No next point found",
			3 : "Periodic orbit detected"
		}
		s = "Code " + str(code) + ": " + codeDict[code]
		for key,val in message.items():
			s += "\n\t" + str(key) + ": " + str(val)
		if toPrint:
			print s
		return s

	def getPositions(self, orbit):
		positions = []
		for t in orbit:
			positions.append(self.findPosition(t))
		return positions

	def updateFile(self, fileName, time, angle):
		initial = open(fileName, "w+")
		initial.truncate(0)
		initial.write(str(self.length) + "\n")
		for i in range(self.length):
			initial.write(str(self.V[i].x) + "\n")
			initial.write(str(self.V[i].y) + "\n")
		initial.write(str(time) + "\n")
		initial.write(str(angle) + "\n")
		initial.close()
