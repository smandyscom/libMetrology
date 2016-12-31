import numpy
from numpy import cos, sin
import random


ERROR_SCALE_DEG = 5
ERROR_SCALE_MM = 5
# NOISE_SCALE = 0.1 * ERROR_SCALE

#defines
EX = 0
EY = 1
EZ = 2
SX = 3
SY = 4
SZ = 5
TX = 0
TY = 1
TZ = 2

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


class error_matrix(numpy.matrix):
    @property
    def error_vector(self):
        # ex,ey,ez,sx,sy,ez
        return (self[2, 1],
                self[0, 2],
                self[1, 0],
                self[0, 3],
                self[1, 3],
                self[2, 3])

    @error_vector.setter
    def error_vector(self, value):
        ex, ey, ez, sx, sy, sz = value
        self[0:3, 3] = numpy.matrix([sx, sy, sz]).T
        self[2, 1] = ex
        self[1, 2] = -ex
        self[0, 2] = ey
        self[2, 0] = -ey
        self[1, 0] = ez
        self[0, 1] = -ez


T_c1_r, T_c2_r, T_c3_r, T_y0_s0, T_l_c4 = tuple([htm(numpy.eye(4)) for x in range(0, 5)])

T_c1_r.R = numpy.matrix(([0, 0, -1],
                         [-1, 0, 0],
                         [0, 1, 0]))
T_c1_r.P = numpy.matrix((95.823, 213.615, 58.255, 1)).T

T_c2_r.R = numpy.matrix(([1, 0, 0],
                         [0, 0, -1],
                         [0, 1, 0]))
T_c2_r.P = numpy.matrix((95.823, 213.615, 58.255, 1)).T

T_c3_r.R = numpy.matrix(([1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]))
T_c1_r.P = numpy.matrix((95.823, 213.615, 58.255, 1)).T

T_y0_s0.R = numpy.matrix(([-1, 0, 0],
                          [0, 1, 0],
                          [0, 0, -1]))
T_y0_s0.P = numpy.matrix((95.823, 213.615, 58.255, 1)).T

T_l_c4.R = numpy.matrix(([1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]))
T_l_c4.P = numpy.matrix((95.823, 213.615, 58.255, 1)).T

def T_s0_r(Ax):
    __htm = htm(numpy.eye(4))
    __htm.R = numpy.matrix(([-1, 0, 0],
                            [0, 1, 0],
                            [0, 0, -1]))
    __htm.P = numpy.matrix((Ax, 163.5, 120.002, 1)).T
    return __htm


def T_s_s0(a, b, c, x, y, z):
    __rot = numpy.matrix(([1, 0, 0],
                          [0, cos(a), -sin(a)],
                          [0, sin(a), cos(a)]))
    __rot = __rot * numpy.matrix(([cos(b), 0, sin(b)],
                                  [0, 1, 0],
                                  [-sin(b), 0, cos(b)]))
    __rot = __rot * numpy.matrix(([cos(c), -sin(c), 0],
                                  [sin(c), cos(c), 0],
                                  [0, 0, 1]))
    __htm = htm(numpy.eye(4))
    __htm.R = __rot
    __htm.P = numpy.matrix((x, y, z, 1)).T
    return __htm


def T_c4_y0real(Ay):
    # z align to working height
    __htm = htm(numpy.eye(4))
    __htm.R = numpy.matrix(([1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]))
    __htm.P = numpy.matrix((0, Ay, 0, 1)).T
    return __htm

# error matrice


def gen_error_vector():
    return (tuple([random.uniform(-numpy.deg2rad(ERROR_SCALE_DEG), numpy.deg2rad(ERROR_SCALE_DEG)) for x in range(0, 3)]) +
            tuple([random.uniform(-ERROR_SCALE_MM, ERROR_SCALE_MM) for x in range(0, 3)]))

T_c1real_c1, T_c2real_c2, T_c3real_c3, T_y0real_y0, T_lreal_l = tuple([error_matrix(numpy.eye(4)) for x in range(0, 5)])

T_c1real_c1.error_vector = gen_error_vector()
T_c2real_c2.error_vector = gen_error_vector()
T_c3real_c3.error_vector = gen_error_vector()
T_y0real_y0.error_vector = gen_error_vector()
T_lreal_l.error_vector = gen_error_vector()


