from sympy import *
import unittest

def HomogenousTransformationSymbol(subscript):
    R = MatrixSymbol('R' + subscript,3,3)
    P = MatrixSymbol('P' + subscript,3,1)
    zero = ZeroMatrix(1,3)
    one = Identity(1)
    return Matrix([[R,P],[zero,one]])

def PositionSymbol(subscript):
    pass

def VectorSymbol(subscript):
    pass

if __name__ == '__main__':
    print Matrix(HomogenousTransformationSymbol('cs') * HomogenousTransformationSymbol('sr'))
