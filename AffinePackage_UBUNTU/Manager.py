#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manager.py: The purpose of this script is to greet the user with a GUI and offer the Load and Create options for many types of shapes."""

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
import Tkinter, Tkconstants, tkFileDialog
import colorsys
import os
import errno
from PolyVector import *
import subprocess
import shlex
from threading import Thread
from math import sin, cos, pi
import random

# In the Manager, if trying to create, we will construct a shape. Defaults to Shape.default()
shape = Shape.Default()
N = shape.length	# number of vertices in default shape

# To be updated as shape updates
shapeMessage = ""	# reported on screen, including exact coordinates of vertices of shape
C = None 		# average position
R = 0 			# max distance of the set of vertices from their average position
m = 0.1 		# canvas margin term, proportion of R
w = 0 			# width of screen in geometrical units
h = w 			# height of screen in geometrical units
canvas_width = 300 	# absolute width of screen in drawing units
canvas_height = 300 	# absolute height of screen in drawing units
centerPos = PVector(canvas_width / 2, canvas_height / 2)

# Where to store any generated files. Creates this directory if it does not already exist
dirName = sys.argv[1]

def drawX(x):
	"""Transforms coordinates in the shape to coordinates in the canvas (x-component)"""
	return canvas_width / w * (x - C.x) + centerPos.x

def drawY(y):
	"""Transforms coordinates in the shape to coordinates in the canvas (y-component)"""
	return canvas_height / h * (y - C.y) + centerPos.y


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

def OPEN(dirName, fileName):
        """opens the requested file using Viewer.py"""
	subprocess.call(shlex.split("python " + dirName + "/Viewer.py " + fileName))


def threaded_run(dirName, fileName):
	"""called to run each pop-up window in parallel"""
        t = Thread(target=OPEN, args=(dirName, fileName))
	t.daemon = True
	t.start()

def update():
	"""called every time that a command is activated in popup"""

	# using these global variables
	global N
	global shapeMessage
	global text
	global C
	global R
	global w
	global h

	N = shape.length
	updateCoordinatesArray()	

	# updated canvas parameters
	C = shape.average()
	R = shape.maxDistanceTo(C)
	w = 2 * (1 + m) * R 
	h = w 

	# update the text that will appear on screen
	shapeMessage += "Vertices = {"
	for i in range(N):
		shapeMessage += "(" + str(shape.V[i].x) + "," + str(shape.V[i].y) + "), " 
	shapeMessage = shapeMessage[:-2] + "}"
        text.config(state=NORMAL)
	text.delete(1.0, END)
	text.insert(END, shapeMessage, "center")
        text.config(state=DISABLED)

	# display the result
	display()
	
	return

def display():
	"""How to display the canvas"""

	# using these global variables
	global shape
	global canvas

	canvasV = [] 	# vertices' positions on canvas
	# transform coordinates to canvas coordinates
	for i in range(N):
		canvasV.append(PVector(drawX(shape.V[i].x), drawY(shape.V[i].y)))
	
	# background
	canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill = "white")
	
	# polygon border
	for i in range(N):
		canvas.create_line(canvasV[i].x, canvasV[i].y, canvasV[(i + 1) % N].x, canvasV[(i + 1) % N].y, fill = "black", width = 2)
	
	# labels for the vertices
	alpha = 0.1
	extra = PVector.mult(centerPos, alpha)
	for i in range(N):
		textPos = PVector.sub(PVector.mult(canvasV[i], 1 + alpha), extra)
		canvas.create_text(textPos.x, textPos.y, fill="black",font="Times 15",text=str(i))

	return

def updateLoadButton():
	"""Called as the loadButton command"""
	
	fileName = tkFileDialog.askopenfilename(initialdir = dirName + "/files", title = "Select Shape File (.txt)", filetypes = [("text files", "*.txt")]) # show an "open" dialog box and return the path to the selected file
	shapeName = fileName[fileName.rfind('/') + 1:]
	print '\n' + shapeName + " has been loaded\n"
	############subprocess.call(shlex.split("python " + dirName + "/Viewer.py " + fileName))
	threaded_run(dirName, fileName)
	return

def updateGenerateButton():
	"""Called as the generateButton command"""
	global shape
	shapeName = ""
	if v.get() == "Default":
		shapeName = "Default"
	elif v.get() == "Regular N-gon":
		shapeName = str(N) + "gon" + str(nGonSlider.get())
	elif v.get() == "Trapezoid":
		shapeName = "Trapezoid" + str(trapezoidSlider.get())
	elif v.get() == "Parallelogram":
		shapeName = "Parallelogram" + str(parallelogramSlider.get())
	elif v.get() == "Kite":
		shapeName = "Kite" + str(kiteSlider.get())
	elif v.get() == "General":
		shapeName = "General" + str(random.randint(100000000,999999999))
	fileName = dirName + "/files/" + shapeName + ".txt"
	shape.updateFile(fileName, 0.5, 45)
	print "\nGenerated " + shapeName + ".txt in " + dirName + "/files\n"
	##################subprocess.call(shlex.split("python " + dirName + "/Viewer.py " + fileName))
	threaded_run(dirName, fileName)
	return

def updateNGonSlider(event):
	"""Called as the nGonSlider command"""
	global shape
	global shapeMessage
	shape = Shape.NGon(nGonSlider.get(), 100, PVector(0, 0))
	shapeMessage = "Regular " + str(nGonSlider.get()) + "-gon\n"
	update()
        return

def updateTrapezoidSlider(event):
	"""Called as the trapezoidSlider command"""
	global shape
	global shapeMessage
	shape = Shape.Trapezoid(trapezoidSlider.get(), PVector(0, 0), 100)
	shapeMessage = "Trapezoid of Modulus [" + str((float(trapezoidSlider.get()) / (float(trapezoidSlider.get()) - 1))) + "] = " + str(int(floor(float(trapezoidSlider.get()) / (float(trapezoidSlider.get()) - 1)))) + ", the ratio of the long horizontal edge to the difference in lengths between the two horizontal edges\n" # Modulus = floor{|AB| / (|AB| - |CD|)} = floor{s / (s - 1)}, where s = float(trapezoidSlider.get())
	update()
        return

def updateParallelogramSlider(event):
	"""Called as the parallelogramSlider command"""	
	global shape
	global shapeMessage
	shape = Shape.Parallelogram(parallelogramSlider.get(), PVector(0, 0), 100)
	shapeMessage = "Parallelogram with shearing " + str(parallelogramSlider.get()) + ", the ratio of the distance between midpoints of the horizontal sides and the height of the parallelogram\n"
	update()
        return

def updateKiteSlider(event):
	"""Called as the kiteSlider command"""	
	global shape
	global shapeMessage
	shape = Shape.Kite(kiteSlider.get(), PVector(0, 0), 100)
	shapeMessage = "Kite with droop " + str(kiteSlider.get()) + ", the ratio of the vertical distance between the bottom and horizontal beam, and the top and the horizontal beam\n"
	update()
        return

def updateGeneralSlider(event):
	"""Called as the generalSlider command"""
	global shape
	global shapeMessage
	shapeMessage = "General shape\n"
	newN = generalSlider.get()

	if shape.length < newN: # adding vertices, harder
		newVertices = []
		for i in range(shape.length):
			newVertices.append(PVector(shape.V[i].x, shape.V[i].y))
		for i in range(shape.length, newN):
			theta = random.uniform(0, 2 * pi)
			newVertices.append(PVector.add(C, PVector(100 * cos(theta), 100 * sin(theta))))
		shape = PolyVector(newVertices)
	
	if shape.length > newN: # removing vertices, easy!
		newVertices = []
		for i in range(newN):
			newVertices.append(PVector(shape.V[i].x, shape.V[i].y))
		shape = PolyVector(newVertices)
	update()
        return

def updateTypeMenu(event):	
	"""Called as the typeMenu command"""

	nGonSlider.grid_remove()
	trapezoidSlider.grid_remove()
	parallelogramSlider.grid_remove()
	kiteSlider.grid_remove()
	generalSlider.grid_remove()

	global shape
	global shapeMessage
	global v

	r = 2
	c = 0
	
	if v.get() == 'Default':
		shape = Shape.Default()
		shapeMessage = "Default shape: a square\n"
		update()
	elif v.get() == 'Regular N-gon':
		nGonSlider.grid(row=r,column=c)
		updateNGonSlider(None)
	elif v.get() == 'Trapezoid':
		trapezoidSlider.grid(row=r,column=c)
		updateTrapezoidSlider(None)
	elif v.get() == 'Parallelogram':
		parallelogramSlider.grid(row=r,column=c)
		updateParallelogramSlider(None)
	elif v.get() == 'Kite':
		kiteSlider.grid(row=r,column=c)
		updateKiteSlider(None)
	elif v.get() == 'General':
		generalSlider.grid(row=r,column=c)
		generalSlider.set(shape.length)
		updateGeneralSlider(None)

def updateCoordinatesArray():
	"""Called when the number of vertices is set in order to have the sliders on the right reflect the coordinates of the vertices properly"""
	global N
	global shape
	global coordinateSliders
	global coordinateSliderValues
	
	N = shape.length
	# too few sliders, append two steps at a time
	while len(coordinateSliders) < 2 * N:
		xValue = DoubleVar()
		yValue = DoubleVar()
		
		x = Scale(right, label=("x" + str(len(coordinateSliders) / 2)), from_=-200, to_=200, length=canvas_width * 3 / 4, variable=xValue, orient = HORIZONTAL, resolution = 0.001, command=updateCoordinates)
		y = Scale(right, label=("y" + str(len(coordinateSliders) / 2)), from_=-200, to_=200, length=canvas_width * 3 / 4, variable=yValue, orient = HORIZONTAL, resolution = 0.001, command=updateCoordinates)
		
		M = 8
		c = len(coordinateSliders) / M
		r = len(coordinateSliders) - M * c		
		x.grid(row=r,column=c)
		y.grid(row=r+1,column=c)
		
		coordinateSliderValues.append(xValue)
		coordinateSliderValues.append(yValue)
		
		coordinateSliders.append(x)
		coordinateSliders.append(y)
	
	# too many sliders, remove one step at a time
	while len(coordinateSliders) > 2 * N:
		coordinateSliders[len(coordinateSliders) - 1].grid_remove()
		coordinateSliders.pop()
		coordinateSliderValues.pop()

	for i in range(N):
		coordinateSliderValues[2 * i].set(shape.V[i].x)
		coordinateSliderValues[2 * i + 1].set(shape.V[i].y)

def updateCoordinates(event):
	"""Called as the coordinateSliders[i] command for each i"""	
	
	global v
	global shape
	global N
	
	# Alter the shape being displayed by the values of the sliders
	for i in range(N):
		shape.V[i].x = coordinateSliderValues[2 * i].get()
		shape.V[i].y = coordinateSliderValues[2 * i + 1].get()

	# update the dropdown to be General now	
	v.set('General')
	updateTypeMenu(None)

def clicked(event):
	return

# master frame contains all frames and components
master = Tk()
master.title("Affine Billiards Manager")

# left frame contains the canvas and 'frame'
left = Frame(master)
left.grid(row=0, column=0)

# right contians list of sliders for coordinates
right = Frame(master)
right.grid(row=0,column=1)

# displays shape
canvas = Canvas(left, width = canvas_width, height = canvas_height)
canvas.bind("<Button-1>", clicked)
canvas.grid(row=0,column=0)

# contains typeMenu and sliders for parameters, as well as Load and Generate buttons
frame = Frame(left)
frame.grid(row=2,column=0)

textSize = 13
text = Text(master, width = int(canvas_width / textSize * 2), height = 5)
text.insert(END, shapeMessage, "center")
text.tag_configure("center", justify = 'center')
text.tag_add("center", 3.0, "end")
text.configure(font = ("Courier", textSize))
text.config(state=DISABLED)
text.grid(row=1,column=0)

# Buttons on the right to control coordinates
coordinateSliders = []
coordinateSliderValues = []

# Type Menu widget
types = {'Default', 'Regular N-gon', 'Trapezoid', 'Parallelogram', 'Kite', 'General'}
v = StringVar(frame)
typeMenu = OptionMenu(frame, v, *types, command=updateTypeMenu)
Label(frame, text="Choose a type of shape").grid(row=0, column=0)
typeMenu.grid(row=1,column=0)

# Generate Button widget
generateButton = Button(frame, text = "Generate", command = updateGenerateButton, width=25, pady = 10)
generateButton.grid(row=2, column=1)

# Load Button widget
loadButton = Button(frame, text = "Load", command = updateLoadButton, width=25, pady = 10)
loadButton.grid(row=3, column=1, padx=80)

# N-Gon Slider widget
nGonSlider = Scale(frame, from_ = 3, to = 24, length = canvas_width * 3 / 4, orient = HORIZONTAL, resolution = 1, command = updateNGonSlider, label="Number of Sides")
nGonSlider.set(3)

# Trapezoid Slider widget
trapezoidSlider = Scale(frame, from_ = 1.001, to = 10, length = canvas_width * 3 / 4, orient = HORIZONTAL, resolution = 0.001, command = updateTrapezoidSlider, label="Trapezoid Parameter")
trapezoidSlider.set(2.0)

# Parallelogram Slider widget
parallelogramSlider = Scale(frame, from_ = 0, to = 10, length = canvas_width * 3 / 4, orient = HORIZONTAL, resolution = 0.001, command = updateParallelogramSlider, label="Parallelogram Parameter")
nGonSlider.set(0.5)

# Kite Slider widget
kiteSlider = Scale(frame, from_ = 1, to = 20, length = canvas_width * 3 / 4, orient = HORIZONTAL, resolution = 0.001, command = updateKiteSlider, label="Kite Parameter")
nGonSlider.set(2.5)

# General Slider widget
generalSlider = Scale(frame, from_ = 3, to = 12, length = canvas_width * 3 / 4, orient = HORIZONTAL, resolution = 1, command = updateGeneralSlider, label="Number of Sides")
generalSlider.set(3)

print "*******************************\nAffine Billiards Manager loaded\n*******************************\n"
updateCoordinatesArray()
v.set('Default')
updateTypeMenu(None)
mainloop()
