import numeric_def
import numpy
import random

ERROR_SCALE = 0.0001
VECTOR_C = (10, 10, 10)
VECTOR_S0 = (10, 10, 10)
VECTOR_P = (0, 0, 10)
Cx, Cy, Cz = VECTOR_C
S0x, S0y, S0z = VECTOR_S0
Px, Py, Pz = VECTOR_P
# __chain = T_c_creal*T_c_r.inv()*T_s0_r*T_s_s0

#simulating small angle error
__error_pos = tuple([random.random() for x in range(0, 3)])
__error_angle = tuple([random.uniform(0, 3.14 * ERROR_SCALE) for x in range(0, 3)])
T_c_creal = numeric_def.HomogenousTransformation(xyzabc=__error_pos + __error_angle)
error_vector_answer = (T_c_creal.item((2,1)),
                       T_c_creal.item((0,2)),
                       T_c_creal.item((1,0)),
                       T_c_creal.item((0,3)),
                       T_c_creal.item((1,3)),
                       T_c_creal.item((2,3)))

T_c_r = numeric_def.HomogenousTransformation(RP=(numpy.eye(3), numpy.matrix(VECTOR_C).T))

T_s0_r = numeric_def.HomogenousTransformation(RP=(numpy.eye(3), numpy.matrix(VECTOR_S0).T))

#fixed pose
def T_s_s0(translation):
    return numeric_def.HomogenousTransformation(RP=(numpy.eye(3), numpy.matrix(translation).T))

def coefficien_matrix(vector_S):
    Sx, Sy, Sz = vector_S
    return numpy.matrix(([0, -Cz+Pz+S0z+Sz, Cy-Py-S0y-Sy, 1, 0],
                         [Cz-Pz-S0z-Sz, 0, -Cx+Px+S0x+Sx, 0, 1]))

#the end ball used to do calibration
P_s = numeric_def.PositionVector(Px, Py, Pz)

VECTOR_S_SET = [(0, 0, 0),
                (10, 10, 1),
                (-10, 10, 1),
                (10, -10, 1),
                (-10, -10, 1)]


P_c_offseted = []
Coefficients = []

for index in range(0, len(VECTOR_S_SET)):
    # print VECTOR_S_SET[index]
    Sx, Sy, Sz = VECTOR_S_SET[index]
    P_c = T_c_creal * T_c_r.I * T_s0_r * T_s_s0((Sx, Sy, Sz)) * P_s
    # offset
    P_c = P_c - numpy.matrix((-Cx+S0x+Sx+Px,
                              -Cy+S0y+Sy+Py,
                              0,
                              1)).T
    # print P_c
    P_c_offseted.append(P_c[0:2, :])
    # print P_c_offseted
    Coefficients.append(coefficien_matrix((Sx, Sy, Sz)))

P_c_offseted =  numpy.vstack(tuple(P_c_offseted))
Coefficients =  numpy.vstack(tuple(Coefficients))

print P_c_offseted
print Coefficients

error_vector = numpy.linalg.pinv(Coefficients) * P_c_offseted

# print numpy.linalg.pinv(Coefficients)
print error_vector
print error_vector_answer
