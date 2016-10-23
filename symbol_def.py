#!/usr/bin/env python
from sympy import *
import unittest

global aa
aa = 5

def Transformation_Matrix(*args):
    R,P = args
    htm = eye(4)
    htm[0:3,0:3] = R
    htm[0:3,3] = P
    return htm


def Translation_Vector(*args):
    x,y,z = symbols(args)
    return Matrix([x,y,z])


def Rz_Matrix(theta):
    return Matrix([[cos(theta),-sin(theta),0],
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

#3-axis rotation pitch-row-yaw error is
#simplified by small angle approch
def Error_Matrix(*args):
    epsilon_x,epsilon_y,epsilon_z = symbols(args)
    expr = Rz_Matrix(epsilon_z)*Ry_Matrix(epsilon_y)*Rx_Matrix(epsilon_x)
    # small angle appoximation
    for var in args:
        expr = expr.subs(sin(var),var)
        expr = expr.subs(cos(var),1)
    # generate cross couplings
    expr = expr.subs(epsilon_x*epsilon_y,0)
    expr = expr.subs(epsilon_y*epsilon_z,0)
    expr = expr.subs(epsilon_z*epsilon_x,0)
    return expr

if __name__ == '__main__':
    init_session()

class TestSymbolFunction(unittest.TestCase):
    def setUp(self):
        init_printing()
    def test_ad_hoc(self):
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

    def test_Error_Matrix(self):
        print Error_Matrix('a','b','c')
    def test_Translation_Vector(self):
        print Translation_Vector('x','y','z')
    def test_Transformation_Matrix(self):
        print Transformation_Matrix(Error_Matrix('a','b','c'),
                                    Translation_Vector('x','y','z'))
