from numpy import *
#import numpy

class HomogenousTransformation(type(array)):
    def is_valid(self):
        #check out if the matrix satisfied HTM properties
        return self.__is_R_unity() and self.__is_R_rank3()          
    def __is_R_unity(self):
        cols = [self[0:3,0:3][:,i] for i in range(0,3)]
        #lens = map(lambda x: x.norm(),cols)
        lens = [x.norm() for x in cols] 
        return reduce(lambda x : x==1,lens)
        
    def __is_R_rank3(self):
        return (self.extract([0,1,2],[0,1,2]).rank() == 3)


if __name__ == '__main__':
    H = HomogenousTransformation([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
    print H.is_valid()
    print H