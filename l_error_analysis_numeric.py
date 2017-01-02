from frame_def_numeric import T_lreal_l, T_y0real_y0, T_c4_y0real, T_l_c4, T_y0_s0
from frame_def_numeric import htm, error_matrix
from frame_def_numeric import T_s0_r, T_c4_y0real
import numpy
from numpy import eye, vstack, hstack
from numpy.linalg import pinv
import random
from circle_fit import circle_fit_3d

#prepare cicle points
RADIUS = 1
PARTS = 10
RADS = [x*(numpy.pi/PARTS) for x in range(0, PARTS)]
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
    return T_l_r_real(Ax, Ay) * numpy.matrix((0, 0, Mz, 1)).T

def P_r_by_l_known(Ax, Ay, Mz):
    return T_l_r_nominal(Ax, Ay) * numpy.matrix((0, 0, Mz, 1)).T

def T_l_r_nominal(Ax, Ay):
    return T_s0_r(Ax) * T_y0real_s0 * T_c4_y0real(Ay) * T_l_c4

def T_l_r_real(Ax, Ay):
    return T_l_r_nominal(Ax, Ay) * T_lreal_l

verification = [map(lambda x: (P_r_by_l(x[0], x[1], x[2])), axis_value_set) for axis_value_set in axis_values ]
estimation = [map(lambda x: (P_r_by_l_known(x[0], x[1], x[2])), axis_value_set) for axis_value_set in axis_values ]

fitted_center_axis_values_answer =  [numpy.vstack((solve_Ax_Ay_Mz((center[:, 0:3]).T), eye(1))) for center in CENTERS]
fitted_center_axis_values = [circle_fit_3d(map(lambda x: x.T, axis_value_set)) for axis_value_set in axis_values]
fitted_center_laser_observe = [circle_fit_3d(map(lambda x: (x[0:3, :]).T, point_set)) for point_set in estimation]
# print fitted_center_axis_values
# print fitted_center_axis_values_answer
diff_fitted_center = [fitted_center_axis_values_answer[index] - fitted_center_axis_values[index] for index in range(0, len(CENTERS))]
# print diff_fitted_center
# print fitted_center_laser_observe

center_l_l = [((T_l_r_nominal(0, 0)).I * point)[0:2, :] for point in fitted_center_laser_observe]
center_l_r = [((T_l_r_nominal(0, 0)).I * point.T)[0:2, :] for point in CENTERS]
center_error_xy = reduce(lambda y, z: vstack((y, z)), [center_l_l[index] - center_l_r[index] for index in range(0, len(center_l_l))])

def coe_xy(Mz):
    return numpy.matrix(([0, -Mz, 0, -1, 0, 0],
                         [Mz, 0, 0, 0, -1, 0]))

__coe_xy = reduce(lambda y, z: vstack((y, z)), [coe_xy(x[2, 0]) for x in fitted_center_axis_values])

solved_error_vector = pinv(__coe_xy) * center_error_xy

print solved_error_vector
print T_lreal_l.error_vector
