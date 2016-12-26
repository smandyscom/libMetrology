import numeric_def
import frame_def_numeric
import numpy
import random

#prepare cicle points
RADIUS = 2
PARTS = 10
RADS = [x*(numpy.pi/PARTS) for x in range(0, 10)]
ROUNDS = map((lambda rad: (RADIUS*numpy.cos(rad), RADIUS*numpy.sin(rad), 0, 1)),
             RADS)
ROUNDS = map(lambda __rounds : numpy.matrix(__rounds), ROUNDS)
CENTERS = ((0, 0, 0, 1),
           (10, 0, 0, 1),
           (20, 0, 0, 1),
           (0, 10, 0, 1),
           (0, 20, 0, 1))
CENTERS = map(lambda __center: numpy.matrix(__center), CENTERS)

#circle round points to corresponding Ax,Ay , according to revealed chain
circle_points = [map(lambda round_point: round_point + __center, ROUNDS)  for __center in CENTERS ]
#Ax,Ay fitted center Ax_bar,Ay_bar

#real center represented in L

#measured center represeted in L_real (0,0,Mz,1)

#  real center=T_lreal_l(0,0,Mz,1)

