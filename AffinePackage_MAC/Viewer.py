#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Viewer.py: The purpose of this script is to view a PolyVector by passing just a few parameters"""

__author__      = "Raymond Friend"
__copyright__   = "Copyright 2019, Penn State University"
__credits__ = ["Raymond Friend", "Sergei Tabachnikov"]
__version__ = "2.0.1"
__maintainer__ = "Raymond Friend"
__email__ = "rayjfriend@gmail.com"
__status__ = "Production"

import sys
from PVector import *
import Shape
from Tkinter import *
from math import floor, cos, sin, pi
from random import uniform
import colorsys
import os
from PolyVector import *

fileName = sys.argv[1]
shapeName = fileName[fileName.rfind('/') + 1:]
initial = open(fileName, "r")

N = int(initial.readline()) # number of vertices
vertices = [] # will be list of PVectors

# read the .txt file to reconstruct shape
for i in range(0, N):
	x = float(initial.readline())
	y = float(initial.readline())
	vertices.append(PVector(x, y))

shape = PolyVector(vertices) # PolyVector object made from vertices[]

# booleans for display
beams = True
edges = True
initials = True

c = pi / 180.0 # conversion to radians
t0 = float(initial.readline()) # initial time
angle = float(initial.readline()) # initial angle (assumed to arrive in deg)
u0 = PVector(cos(angle), sin(angle)) # initial velocity

initial.close()

# compute average position and half-diameter of set from the average position
C = shape.average()
R = shape.maxDistanceTo(C)
m = 0.1 # the proportion of R used as a margin in the canvas
w = 2 * (1 + m) * R # width of screen in geometrical units
h = w # height of screen in geometrical units

canvas_width = 500 # absolute width of screen in drawing units
canvas_height = 500 # absolute height of screen in drawing units
centerPos = PVector(canvas_width / 2, canvas_height / 2) # center position on canvas

def drawX(x):
	"""Transforms coordinates in the shape to coordinates in the canvas (x-component)"""
	return canvas_width / w * (x - C.x) + centerPos.x

def drawY(y):
	"""Transforms coordinates in the shape to coordinates in the canvas (y-component)"""
	return canvas_height / h * (y - C.y) + centerPos.y


# setting up some variables
O = None # combination of timeOrbit and code generated
code = -1 # code generated
timeOrbit = None # time orbit generated
positionOrbit = None # corresponding position Orbit
odd = "#9494b8" # how to color odd numbered beams (which connect 2n + 1 with 2n + 3 in orbit)
even = "#ffff66" # how to color even numbered beams (which connect 2n with 2n + 2 in orbit)
message = "" # reported on screen
shapeMessage = "{" # always include exact coordinates of shape in message
for i in range(N):
	shapeMessage += "(" + str(shape.V[i].x) + "," + str(shape.V[i].y) + "), " 
shapeMessage = shapeMessage[:-2] + "}"
error = 0.01
maxOrbit = 1000

def HSVtoRGB(h, s, v):
	"""Returns a string of the form '#xxxxxx' in RGB corresponding to the provided HSV color. Arguments expected as decimals 0 to 1"""
	rgb = colorsys.hsv_to_rgb(h, s, v)
	s = "#"
	for i in rgb:
		bits = hex(int(floor(255.0 * i)))[2:]
		if len(bits) == 1:
			bits = "0" + bits
		s += bits 
	return s

def update(event):
	"""called every time that a command is activated in popup"""

	# editing these global variables
	global O
	global timeOrbit
	global code
	global positionOrbit
	global message
	global text
	global t0
	global u0
	global angle
	global parameterSlider
	global uSlider
	global discrepancySlider
	global maxOrbitSlider
	
	# update from sliders
	t0 = float(parameterSlider.get())
	angle = uSlider.get()
	u0.x = cos(angle * c)
	u0.y = sin(angle * c)
	error = pow(10, discrepancySlider.get())
	maxOrbit = int(pow(10, maxOrbitSlider.get()))
	
	# retrieving the orbit for the conditions
	O = shape.orbit(t0, u0, maxOrbit, error, error)
	timeOrbit = O[0]
	code = O[1]
	positionOrbit = shape.getPositions(timeOrbit)
	print "\tTemporal Orbit: ", str(timeOrbit)

	# update the text that will appear on screen
	message = "|O| = " + str(len(timeOrbit) - 1) + "\nDiscrepancy between points: " + str(error) + "\nMax Orbit Length allowed: " + str(maxOrbit) + "\n" + PolyVector.report(int(code), {}, False) + "\nVertices = " + shapeMessage
	text.config(state=NORMAL)
	text.delete(1.0, END)
	text.insert(END, message, "center")
	text.config(state=DISABLED)

	# display the result
	display()
	
	return

def display():

	# editing these global variable(s)
	global canvas
	
	canvasV = [] # vertices' positions on canvas
	canvasP = [] # positionOrbit's positions on canvas
	# transform coordinates to canvas coordinates
	for i in range(N):
		canvasV.append(PVector(drawX(shape.V[i].x), drawY(shape.V[i].y)))
	for i in range(len(positionOrbit)):
		canvasP.append(PVector(drawX(positionOrbit[i].x), drawY(positionOrbit[i].y)))
	
	# background
	canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill = "white")
	
	# polygon border
	if edges:
		for i in range(0, N):
			canvas.create_line(canvasV[i].x, canvasV[i].y, canvasV[(i + 1) % N].x, canvasV[(i + 1) % N].y, fill = "black", width = 2)

	# support lines
	if beams:
		for i in range(2, len(positionOrbit)):
			canvas.create_line(canvasP[i].x, canvasP[i].y, canvasP[i - 2].x, canvasP[i - 2].y, fill = (even if i % 2 == 0 else odd), width = 1)

	# trajectory
	if len(positionOrbit) > 2:
		for i in range(1, len(positionOrbit)):
			canvas.create_line(canvasP[i].x, canvasP[i].y, canvasP[i - 1].x, canvasP[i - 1].y, fill = HSVtoRGB(float(i - 1) / float(len(positionOrbit) - 2), 1, 1), width = 2)
	elif len(positionOrbit) > 1:
		canvas.create_line(canvasP[1].x, canvasP[1].y, canvasP[0].x, canvasP[0].y, fill = "red", width = 2)
	
	# initial point and initial vector
	r = canvas_width / 100
	if initials:
		u = PVector.mult(PVector.normalize(u0), max(r * 2, canvas_width / 20))
		canvas.create_line(canvasP[0].x, canvasP[0].y, canvasP[0].x + u.x, canvasP[0].y + u.y, fill = "green", width = 3)
		canvas.create_oval(canvasP[0].x - r, canvasP[0].y - r, canvasP[0].x + r, canvasP[0].y + r, fill = "cyan")

	return

def updateSaveButton():
	global shape
	shape.updateFile(fileName, t0, angle)
	print "\nUpdated File: " + shapeName + '\n'

def updateDisplays():
	global displays
	global edges
	global beams
	global initials
	states = displays.state()
	edges = states[0]
	beams = states[1]
	initials = states[2]
	display()
	return

def clicked(event):
	return

master = Tk()
master.title(shapeName)

canvas = Canvas(master, width = canvas_width, height = canvas_height)
canvas.bind("<Button-1>", clicked)
canvas.pack()

textSize = 13
text = Text(master, width = int(canvas_width / textSize * 1.5), height = 5)
text.insert(END, message)
text.tag_configure("center", justify = 'center')
text.tag_add("center", 3.0, "end")
text.configure(font = ("Courier", textSize))
text.config(state=DISABLED)
text.pack()

parameterSlider = Scale(master, from_ = 0, to = N, length = 360, orient = HORIZONTAL, resolution = 0.0001, command = update, label="Temporal", variable=DoubleVar(value=t0))
parameterSlider.pack()

uSlider = Scale(master, from_ = 0, to = 360, length = 360, orient = HORIZONTAL, resolution = 1, command = update, label="Angular", variable=DoubleVar(value=angle))
uSlider.pack()

discrepancySlider = Scale(master, from_ = -10, to = 0, length = 360, orient = HORIZONTAL, resolution = 0.001, command = update, label="Error or Discrepancy (log)", variable=DoubleVar(value=-7.))
discrepancySlider.pack()

maxOrbitSlider = Scale(master, from_ = 2, to = 5, length = 360, orient = HORIZONTAL, resolution = 0.001, command = update, label="Max Orbit (log)", variable=DoubleVar(value=3.))
maxOrbitSlider.pack()

class Checkbar(Frame):
	def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
		Frame.__init__(self, parent)
		self.width = canvas_width / 2
		self.vars = []
		for pick in picks:
			var = IntVar(value=1)
			chk = Checkbutton(self, text=pick, variable=var, command=updateDisplays)
			chk.pack(side=side, anchor=anchor, expand=YES)
			self.vars.append(var)
	def state(self):
		return map((lambda var: var.get()), self.vars)

displays = Checkbar(master, ['Edges', 'Beams', 'Initials'])
displays.pack(side=TOP)

saveButton = Button(master, text = "Save", command = updateSaveButton, width = 25, pady = 10)
saveButton.pack()

update(None)
mainloop()
