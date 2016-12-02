import numpy
import unittest
import numeric_def

def pod_fixed_inverse(htm):
    #a->b->c->x->y->z
    x, y, z = htm[0, 3], htm[1, 3], htm[2, 3]
    _sinb, _cosb_cosc, _cosa_cosb = -htm[2, 0], htm[0, 0], htm[2, 2]
    #solve a,b,c
    b = numpy.arcsin(_sinb)
    c = numpy.arccos(_cosb_cosc/numpy.cos(b))
    a = numpy.arccos(_cosa_cosb/numpy.cos(b))
    #
    return a, b, c, x, y, z


class TestKinematicFunction(unittest.TestCase):
    def setUp(self):
        pass
        # numpy.init_printing()

    def test_1(self):
        __input = numeric_def.HomogenousTransformation(xyzabc=(1, 2, 3, 0.5, 0.5, 0.5))
        print __input
        print pod_fixed_inverse(__input)
