from frame_def_numeric import T_lreal_l, T_y0real_y0, T_c4_y0real, T_l_c4, T_y0_s0
from frame_def_numeric import htm, error_matrix
from frame_def_numeric import T_s0_r, T_c4_y0real
import numpy
import random
import circle_fit

#prepare cicle points
RADIUS = 2
PARTS = 10
RADS = [x*(numpy.pi/PARTS) for x in range(0, 10)]
ROUNDS = map((lambda rad: (RADIUS*numpy.cos(rad), RADIUS*numpy.sin(rad), 0, 0)),
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
#Ax, Ay , Mz analysing
T_y0real_s0 = T_y0_s0 * T_y0real_y0
T_lreal_c4 = T_l_c4 * T_lreal_l

T_s0_r_zero = T_s0_r(0)
Rs0 = T_s0_r_zero[0:3, 0:3]
Ps0 = T_s0_r_zero[0:3, 3]
Ry0 = T_y0_s0[0:3, 0:3]
offset_value =  T_y0real_y0[0:3, 0:3] * T_lreal_c4[0:3, 3] + Rs0 * T_y0real_s0[0:3, 3] + Ps0
exy0, eyy0, ezy0 = T_y0real_y0.error_vector[0:3]

exl, eyl = T_lreal_l.error_vector[0:2]
coeff = numpy.matrix(([1, -ezy0, exl * ezy0 + eyl + eyy0],
                      [0, 1, -exl - exy0 + eyl*ezy0],
                      [0, exy0, -exl * exy0 - eyl * eyy0 + 1]))

def solve_Ax_Ay_Mz(P_r):
    # P_r , 3x1 vector
    return coeff.I * (P_r - offset_value)

#the axis value measured
axis_values = [map(lambda x: (coeff.I * (x[:, 0:3].T - offset_value)), circle_point_set) for circle_point_set in circle_points]

def P_r_by_l(Ax, Ay, Mz):
    return T_s0_r(Ax) * T_y0real_s0 * T_c4_y0real(Ay) * T_lreal_c4 * numpy.matrix((0, 0, Mz, 1)).T

def P_r_by_l_known(Ax, Ay, Mz):
    return T_s0_r(Ax) * T_y0real_s0 * T_c4_y0real(Ay) * T_l_c4 * numpy.matrix((0, 0, Mz, 1)).T

verification = [map(lambda x: (P_r_by_l(x[0], x[1], x[2])), axis_value_set) for axis_value_set in axis_values ]

print solve_Ax_Ay_Mz((numpy.matrix((0, 0, 0))).T)
print circle_fit.circle_fit_3d(map(lambda x: x.T, axis_values[0]))

# verification : take Ax, Ay, Mz forward kinematic to verify P_r
#Ax,Ay fitted center Ax_bar,Ay_bar

#real center represented in L

#measured center represeted in L_real (0,0,Mz,1)

#  real center=T_lreal_l(0,0,Mz,1)

