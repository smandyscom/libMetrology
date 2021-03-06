from numpy import matlib,linalg
import numpy
from ikpy import geometry_utils as gu

def is_Orthogonal(m):
    QTQ = m.T*m
    QQT = m*m.T
    # print "QTQ{0}QQT{1}".format(QTQ,QQT)
    return numpy.allclose(QTQ, matlib.identity(QTQ.shape[0]))

def force_vector_unity(vec):
    return (1/linalg.norm(vec)) * vec

class ErrorTransformation(numpy.matrix):
    def __new__(self, ERROR_VECTOR):
        #unpack
        ex, ey, ez, sx, sy, sz = ERROR_VECTOR
        self = matlib.identity(4)
        self[0:3, 3] = numpy.matrix([sx, sy, sz]).T
        self[2, 1] = ex
        self[1, 2] = -ex
        self[0, 2] = ey
        self[2, 0] = -ey
        self[1, 0] = ez
        self[0, 1] = -ez
        return self

    def __init__(self):
        pass

class HomogenousTransformation(numpy.matrix):
    def __new__(self, **kwargs):
        self = matlib.identity(4)
        if 'RP' in kwargs:
            R, P = kwargs['RP']
            for i in range(0, 3):
                R[:, i] = force_vector_unity(R[:, i])
            if not is_Orthogonal(R):
                raise ValueError('R is not orthogonal')
            self[0:3, 0:3] = R
            self[0:3, 3] = P
        elif 'xyzabc' in kwargs:
            x, y, z, a, b, c = kwargs['xyzabc']
            R = numpy.matrix(gu.Rz_matrix(c))*numpy.matrix(gu.Ry_matrix(b))*numpy.matrix(gu.Rx_matrix(a))
            P = numpy.matrix([x, y, z]).T
            self = HomogenousTransformation(RP=(R, P))
        else:
            pass
        #
        # Euler sequence : translate xyz -> rotate about x alpha radians -> rotate about y
        #
        return self

    def __init__(self):
        pass

    #FIXME: R,P is able to be edited after initialized

    @property
    def R(self):
        return self[0:3, 0:3]

    @property
    def P(self):
        return self[0:3, 3]



class PositionVector(numpy.matrix):
    def __new__(self, px=0., py=0., pz=0., scale=1.):
        self = numpy.matrix([px, py, pz, scale], dtype=float)
        return self.T



if __name__ == '__main__':
    print is_Orthogonal(numpy.matrix([[1,0],[0,1]]))
    print force_vector_unity(numpy.matrix([1,1,1]))
    R = matlib.identity(3) *2
    P = numpy.matrix([1,1,1])
    P = P.T
    print 'P{0}'.format(P)
    print HomogenousTransformation(RP=(R,P))
    print HomogenousTransformation(xyzabc=(1,2,3,3.14,1.57,0))
    P = PositionVector(0,0,0,1)
    print P
    P = numpy.matrix([1,1,1])
    # R = matrix([[1,0,0],[0,1,1],[0,0,1]])
    #Note : ndarray * as element multiplication , rather matlib * as matrix multiplication
    R=matlib.identity(3)
    R[1:2]=1
    print 'R{0}'.format(R)
    print 'RT{0}'.format(R.T)
    print 'RTR{0}'.format(R.T*R)
    print is_Orthogonal(R)
    # print HomogenousTransformation(RP=(R,P))
    print HomogenousTransformation(xyzabc=(1,2,3,0,0,0)) * PositionVector(1,1,1,1)
    seed=(1,1,1,3.14,3.14,3.14)
    __htm = HomogenousTransformation(xyzabc=seed) * HomogenousTransformation(xyzabc=seed).I
    print HomogenousTransformation(xyzabc=seed) * HomogenousTransformation(xyzabc=seed).I
    # print HomogenousTransformation(xyzabc=seed).R
    print ("E:", ErrorTransformation((0.1, 0.2, 0.3, 0.4, 0.5, 0.6)))
    print __htm.P

