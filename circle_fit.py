import numpy
from numpy.linalg import svd, norm
from numpy import eye
import unittest
from frame_def_numeric import htm

def solve_right_singular_vector(A):
    u, s, v_star = svd(A)
    smallest_value_index =  (tuple(s)).index(min(s))
    v = v_star.H
    smallest_singular_vector = v[:, smallest_value_index]
    return smallest_singular_vector

def circle_fit_3d(point_set):
    # turns point to coefficient row
    def gen_coeff_vector(xy_axis_value):
        xy_axis_value_flat = xy_axis_value.flat
        # print xy_axis_value_flat
        xy_axis_value_flat = xy_axis_value_flat[0:2]
        X, Y = (xy_axis_value_flat[0, 0], xy_axis_value_flat[0, 1])
        return numpy.matrix((X**2 + Y**2 , X, Y, 1))

    # find the best fit plane for those point
    frame_origin = reduce(lambda x, y: (x + y), point_set)
    frame_origin = frame_origin / len(point_set)

    vectors = map(lambda x : x - frame_origin, point_set)
    # print vectors
    coeff  = reduce(lambda y, z : numpy.vstack((y, z)), vectors)
    vector_z = solve_right_singular_vector(coeff)
    vector_z = vector_z / norm(vector_z)
    vector_z = vector_z.T

    # print vectors[0], vector_z
    vector_x = numpy.cross(vectors[0], vector_z)
    vector_x = vector_x / norm(vector_x)

    vector_y = numpy.cross(vector_z, vector_x)
    vector_y = vector_y / norm(vector_y)

    # print vector_x, vector_y, vector_z

    # so , the htm generated
    T_new_origin = htm(eye(4))
    T_new_origin.P = numpy.vstack((frame_origin.T, eye(1)))
    T_new_origin.R = numpy.hstack((vector_x.T, vector_y.T, vector_z.T))

    # transformate all point to new frame
    point_set_new_frame = map(lambda x: numpy.vstack((x.T, eye(1))), point_set)
    point_set_new_frame = map(lambda x: T_new_origin.I * x , point_set_new_frame)

    # solve circle
    coeff = reduce(lambda y, z : numpy.vstack((y, z)), map(gen_coeff_vector, point_set_new_frame))
    coeff_vector = solve_right_singular_vector(coeff)
    a, b1, b2, c = tuple([coeff_vector[_index, 0] for _index in range(0, 4)])

    center_new_frame = (numpy.matrix((-b1/(2*a), -b2/(2*a), 0, 1))).T
    center_origin_frame = T_new_origin * center_new_frame

    return center_origin_frame

class TestCircleFunction(unittest.TestCase):
    def setUp(self):
        # prepare cicle points
        RADIUS = 2
        PARTS = 10
        RADS = [x * (numpy.pi/PARTS) for x in range(0, 10)]
        self.ROUNDS = map((lambda rad: (RADIUS*numpy.cos(rad) + 30, RADIUS*numpy.sin(rad) + 5, 20)), RADS)
        self.ROUNDS = map(lambda __rounds : numpy.matrix(__rounds), self.ROUNDS)

    def test_circle(self):
        print circle_fit_3d(self.ROUNDS)



