from numpy import *
from ikpy import geometry_utils
#import numpy

class HomogenousTransformation(matrix):
    def __new__(self,tx=0,ty=0,tz=0,alpha=0,beta=0,gamma=0):
        #Fix me : use keyword args , xyzabc , RP(Rotation,Translation) , 
        #
        # Euler sequence : translate xyz -> rotate about x alpha radians -> rotate about y 
        # 
        self = identity(4)
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

    def __force_R_unity(self):
        cols = [self[0:3,0:3][:,i] for i in range(0,3)]
        #lens = map(lambda x: x.norm(),cols)
        lens = [x.norm() for x in cols] 
        return reduce(lambda x : x==1,lens)
        
    def __is_R_orthogonal(self):
        QTQ = self.__R * self.__R.T
        fill_diagonal(QTQ,0)
        return not QTQ.any() 

class PositionVector(matrix):
    def __new__(self,px=0.,py=0.,pz=0.,scale=1.):
        self = matrix([px,py,pz,scale])
        return self.T

if __name__ == '__main__':
    H = HomogenousTransformation()
    print H 
    P = PositionVector(0,0,0,1)
    print P 