from sympy import *
import unittest

def HomogenousTransformation(subscript):
    R = MatrixSymbol('R' + subscript,3,3)
    P = MatrixSymbol('P' + subscript,3,1)
    zero = ZeroMatrix(1,3)
    one = Identity(1)
    return Matrix([[R,P],[zero,one]])

# init_session()
print Matrix(HomogenousTransformation('cs') * HomogenousTransformation('sr'))

