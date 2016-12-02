import numpy
import unittest
import numeric_def
import random

def pod_relative_inverse(htm):
    #a->b->c->x->y->z
    x, y, z = htm[0, 3], htm[1, 3], htm[2, 3]
    #solve a,b,c
    a = numpy.arctan2(htm[2, 1], htm[2, 2])
    b = numpy.arcsin(-htm[2, 0])
    c = numpy.arctan2(htm[1, 0], htm[0, 0])
    #
    return x, y, z, a, b, c


class TestKinematicFunction(unittest.TestCase):
    def setUp(self):
        pass
        # numpy.init_printing()

    def test_1(self):
        __tuple_pos = tuple([random.random() for x in range(0,3)])
        __tuple_angle = tuple([random.uniform(0, 3.14) for x in range(0,3)])

        __input = numeric_def.HomogenousTransformation(xyzabc=__tuple_pos+__tuple_angle)

        __tuple_answer = pod_relative_inverse(__input)

        __forward = numeric_def.HomogenousTransformation(xyzabc=__tuple_answer)

        self.assertTrue(numpy.allclose(__forward, __input),
                        '__input:{0},__forward:{1}'.format(__input,__forward))

        self.assertTrue(numpy.allclose(numpy.matrix(__tuple_pos + __tuple_angle),numpy.matrix(__tuple_answer)),
                        '\nanswer:{0}\nrefer:{1}\n__input:\n{2}\n__forward:\n{3}'.format(__tuple_answer,
                                                                                __tuple_pos + __tuple_angle,
                                                                                __input,
                                                                                __forward))
