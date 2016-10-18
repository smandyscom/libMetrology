from numpy import *
#import numpy

class HomogenousTransformation(matrix):
    def __init__(self,*args,**kwargs):
        super(HomogenousTransformation,self).__init__(*args,**kwargs)
        #given artibary matrix , check properties of HTM
#        self.__R=self[0:3,0:3]
#        self.__P=self[0:3,3]
        
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
    def __init__(self,*args,**kwargs):
        super(PositionVector,self).__init__(*args,**kwargs)

if __name__ == '__main__':
    H = HomogenousTransformation([[1,2],[3,4]])
    print H 
    P = PositionVector([0,0,0,1])
    print P