from numpy import *
from ikpy import geometry_utils as gu

def is_Orthogonal(m):
    QTQ = m.T*m
    QQT = m*m.T
    print "QTQ{0}QQT{1}".format(QTQ,QQT)
    return allclose(QTQ,identity(QTQ.shape[0]))

def force_vector_unity(vec):
    return (1/linalg.norm(vec)) * vec


class HomogenousTransformation(matrix):
    def __new__(self,**kwargs):
        self = identity(4)
        if 'RP' in kwargs:
            R,P = kwargs['RP']
            for i in range(0,3):
                R[:,i]=force_vector_unity(R[:,i])
            if not is_Orthogonal(R):
                raise ValueError('R is not orthogonal')
            self[0:3,0:3]=R
            self[0:3,3]=P
        elif 'xyzabc' in kwargs:
            x,y,z,a,b,c = kwargs['xyzabc']
            R = matrix(gu.Rz_matrix(c)*gu.Ry_matrix(b)*gu.Rx_matrix(a))
            P = matrix([x,y,z])
            self = HomogenousTransformation(RP=(R,P))
        else:
            pass
        #
        # Euler sequence : translate xyz -> rotate about x alpha radians -> rotate about y
        #
        return self

    def __init__(self):
        self.__R=self[0:3,0:3]
        self.__P=self[0:3,3]
    #def __init__(self,*args,**kwargs):
        #super(HomogenousTransformation,self).__init__(*args,**kwargs)
        #given artibary matrix , check properties of HTM

    def is_valid(self):
        #check out if the matrix satisfied HTM properties
        return self.__is_R_unity() and self.__is_R_rank3()


class PositionVector(matrix):
    def __new__(self,px=0.,py=0.,pz=0.,scale=1.):
        self = matrix([px,py,pz,scale])
        return self.T

if __name__ == '__main__':
    print is_Orthogonal(matrix([[1,0],[0,1]]))
    print force_vector_unity(matrix([1,1,1]))
    R = identity(3) *2
    P = matrix([1,1,1])
    print HomogenousTransformation(RP=(R,P))
    print HomogenousTransformation(xyzabc=(1,2,3,3.14,1.57,0))
    P = PositionVector(0,0,0,1)
    print P
    P = matrix([1,1,1])
    # R = matrix([[1,0,0],[0,1,1],[0,0,1]])
    R=identity(3)
    R[1:2]=1
    print 'R{0}'.format(R)
    print 'RT{0}'.format(R.T)
    print 'RTR{0}'.format(R.T*R)
    print is_Orthogonal(R)
    # print HomogenousTransformation(RP=(R,P))
