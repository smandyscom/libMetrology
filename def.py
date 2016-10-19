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

def Rz_Matrix(theta):
    return Matrix([[1,theta,0],
    [sin(theta),cos(theta),0],
    [0,0,1]])

def Ry_Matrix(theta):
    return Matrix([[cos(theta),0,sin(theta)],
    [0,1,0],
    [-sin(theta),0,cos(theta)]])
    

def Rx_Matrix(theta):
    return Matrix([[1,0,0],
    [0,cos(theta),-sin(theta)],
    [0,sin(theta),cos(theta)]])


if __name__ == '__main__':
    print Matrix(HomogenousTransformationSymbol('cs') * HomogenousTransformationSymbol('sr'))
    print Rz_Matrix('c')*Ry_Matrix('b')*Rx_Matrix('a')
    H = Ry_Matrix('b')*Rx_Matrix('a')
    print H 
    print simplify(H)
    print trigsimp(simplify(H))
    # small angle approch
    for ch in ['a','b']:
        H = H.subs(sin(ch),ch)
        H = H.subs(cos(ch),1)
    print simplify(H)
    for ch in ['a','b']:
        H = H.subs(ch,3.14/180)
    print H
    print type(H)
    print H.evalf()
    print type(H.evalf())