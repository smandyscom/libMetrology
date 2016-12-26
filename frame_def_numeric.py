import numpy
import random

ERROR_SCALE = 0.0001
NOISE_SCALE = 0.1 * ERROR_SCALE

class htm(numpy.matrix):
    @property
    def R(self):
        return self[0:3, 0:3]

    @R.setter
    def R(self, value):
        self[0:3, 0:3] = value

    @property
    def P(self):
        # return position vector
        return self[:, 3]

    @P.setter
    def P(self, value):
        self[:, 3] = value

VECTOR_C = (95.823, 203.615, 58.255)
VECTOR_S0 = (95.823 + 65, 163.5, 120.002)
VECTOR_P = (0, 0, 120.002 - 58.255)
C_FRAME = numpy.matrix(([0, 0, 1],
                           [-1, 0, 0],
                           [0, 1, 0]))
S_FRAME = numpy.matrix(([-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, -1]))

Cx, Cy, Cz = VECTOR_C
S0x, S0y, S0z = VECTOR_S0
Px, Py, Pz = VECTOR_P
# __chain = T_c_creal*T_c_r.inv()*T_s0_r*T_s_s0

#simulating small angle error
# __error_pos = tuple([random.random() for x in range(0, 3)])
# __error_angle = tuple([random.uniform(0, 3.14 * ERROR_SCALE) for x in range(0, 3)])
# T_c_creal = numeric_def.HomogenousTransformation(xyzabc=__error_pos + __error_angle)
# error_vector_answer = (T_c_creal.item((2,1)),
                       # T_c_creal.item((0,2)),
                       # T_c_creal.item((1,0)),
                       # T_c_creal.item((0,3)),
                       # T_c_creal.item((1,3)),
                       # T_c_creal.item((2,3)))

# T_c1_r = numeric_def.HomogenousTransformation(RP=(numpy.matrix(([0, 0, 1],
                                                                # [-1, 0, 0],
                                                                # [0, 1, 0])),
                                                  # numpy.matrix(VECTOR_C).T))

# T_s0_r = numeric_def.HomogenousTransformation(RP=(S_FRAME, numpy.matrix(VECTOR_S0).T))


