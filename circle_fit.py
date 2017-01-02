import numpy
import unittest

def circle_fit(point_set):
    # turns point to coefficient row
    def gen_coeff_vector(axis_value):
        # print axis_values.flat
        # print (axis_value.flat)[0:3]
        X, Y, Z = axis_value.flat
        return numpy.matrix((X**2 + Y**2 , X, Y, 1))

    coeff = reduce(lambda y, z : numpy.vstack((y, z)), map(gen_coeff_vector, point_set))
    u, s, v_star = numpy.linalg.svd(coeff)
    smallest_value_index =  (tuple(s)).index(min(s))
    print s
    print smallest_value_index
    v = v_star.H
    smallest_singular_vector = v[:, smallest_value_index]
    print smallest_singular_vector
    a, b1, b2, c = smallest_singular_vector.flat
    # print a, b1, b2, b3, c
    return -b1/(2*a), -b2/(2*a), c

class TestCircleFunction(unittest.TestCase):
    def setUp(self):
        # prepare cicle points
        RADIUS = 2
        PARTS = 10
        RADS = [x * (numpy.pi/PARTS) for x in range(0, 10)]
        self.ROUNDS = map((lambda rad: (RADIUS*numpy.cos(rad) + 30, RADIUS*numpy.sin(rad) + 5, 20)), RADS)
        self.ROUNDS = map(lambda __rounds : numpy.matrix(__rounds), self.ROUNDS)

    def test_circle(self):
        print self.ROUNDS
        print circle_fit(self.ROUNDS)



