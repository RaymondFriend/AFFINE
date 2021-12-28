# AFFINE
GUI tool for exploring polygonal affine billiard dynamics. Made for Sergei Tabachnikov after completing my Honors Undergraduate Thesis for Penn State in Mathematics in 2019. 

## Installation

Installing the Affine Package. You only have to do this once.

### macOS

Give AFFINE.command permission to execute

1. Press CMD + SPACE
2. Type ``Terminal`` and hit ENTER
3. Type ``cd `` (with a space). (Don't hit ENTER yet.)
4. Drag the ``AffinePackage_MAC`` folder onto the terminal window, which will add a directory onto the current line
5. Hit ENTER
6. Type ``chmod u+x AFFINE.command``
7. Close the Terminal window
8. CTRL + Click on ``AFFINE.command``
9.  Click ``Open``
10  Click ``Open``

### Linux

1. Right click the shortcut called ``AFFINE`` 
2. Click ``Properties``
3. Click the ``Permissions`` tab
4. Make sure the ``Allow executing file as program`` box is checked
5. Close the pop-up

## Usage

Instructions for using Affine Package.

### macOS

1. To get started, simply double-click the shortcut called ``AFFINE.command``
2. Select from the dropdown on the left the type of shape
3. When available, use the slider on the left to adjust the dimensions of the shape
4. Either select `General' from the dropdown, or alter the coordinates of your shape using the sliders on the right to create a general polygon. The slider on the left either adds or subtracts vertices from the shape
5. Generate the shape with the ``Generate`` button
6. In the pop-up window:
    1. Adjust the Temporal and Angular sliders to see symplectic orbits along the shape
    2. Adjust the Error slider to alter how strict the computer is when comparing the equality of coordinates along the orbit. This slider is logarithmic (10^pow). A smaller power means the computer will distinguish more finely between points.
    3. Adjust the Max Orbit slider to alter how long the computer is willing to perpetuate its test orbit until declaring the orbit has maxed-out. This slider is logarithmic (10^pow). A larger power means the computer is willing to calculate more steps in the orbit if necessary.
    4. Refer to the textbox and terminal window for information about this orbit
    5. Adjust whether the edges of the shape, support beams (drawn between every other point along the orbit), or initial point and velocity are drawn with the checkboxes
    6. To save your temporal and angular choices, click the ``Save`` button
    7. Close the pop-up window when you are done viewing the shape
7. You may load a previously-generated shape using the "Load" button.
    1. Select the file you would like to load
    2. Click ``Open``
    3. Pop-up window will appear, and refer to step 6
8. Much of the background-steps taken by the program can be viewed on the terminal window
9. Close the window called ``Affine Billiards Manager`` to end the program
10. You may move the ``AFFINE`` shortcut to anywhere on your machine, such as your Desktop. However, avoid changing the name of the folder ``AffinePackage_UBUNTU`` or else the ``AFFINE`` shortcut will not execute. Moreover, avoid duplicating this folder, even in your Trash, or else the shortcut will have trouble deciding to which folder to refer. 


### Linux

1. To get started, simply double-click the shortcut called ``AFFINE``
2. Select from the dropdown on the left the type of shape
3. When available, use the slider on the left to adjust the dimensions of the shape
4. Either select `General' from the dropdown, or alter the coordinates of your shape using the sliders on the right to create a general polygon. The slider on the left either adds or subtracts vertices from the shape
5. Generate the shape with the ``Generate`` button
6. In the pop-up window:
    1. Adjust the Temporal and Angular sliders to see symplectic orbits along the shape  
    2. Adjust the Error slider to alter how strict the computer is when comparing the equality of coordinates along the orbit. This slider is logarithmic (10^pow). A smaller power means the computer will distinguish more finely between points.  
    3. Adjust the Max Orbit slider to alter how long the computer is willing to perpetuate its test orbit until declaring the orbit has maxed-out. This slider is logarithmic (10^pow). A larger power means the computer is willing to calculate more steps in the orbit if necessary.  
    4. Refer to the textbox and terminal window for information about this orbit  
    5. Adjust whether the edges of the shape, support beams (drawn between every other point along the orbit), or initial point and velocity are drawn with the checkboxes  
    6. To save your temporal and angular choices, click the ``Save`` button 
    7. Close the pop-up window when you are done viewing the shape 
7. You may load a previously-generated shape using the "Load" button.
    1. Select the file you would like to load 
    2. Click ``Open``. 
    3. Pop-up window will appear, and refer to step 6 
8. Much of the background-steps taken by the program can be viewed on the terminal window
9. Close the window called ``Affine Billiards Manager`` to end the program
10. You may move the ``AFFINE`` shortcut to anywhere on your machine, such as your Desktop. However, avoid changing the name of the folder ``AffinePackage_UBUNTU`` or else the ``AFFINE`` shortcut will not execute. Moreover, avoid duplicating this folder, even in your Trash, or else the shortcut will have trouble deciding to which folder to refer. 


*Created by Raymond Friend, May 19, 2019*  
*Advisor: Sergei Tabachnikov*  
*As part of an undergraduate honors thesis in Mathematics **Symplectic Billiards**, April 9, 2019*  
*Penn State University*.  
*Version: 2.0*

