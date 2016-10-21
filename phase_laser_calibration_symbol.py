from sympy import *

# pitch error along X-axis about ideal laser inferometer coordiante
a=Symbol('a')
# raw error along Y-axis about ideal laser inferometer coordiante
b=Symbol('b')
# translation from X-axis
tx=Symbol('tx')
ty=Symbol('ty')
tz=Symbol('tz')

#the individual factor of position respect to reference frame
r1x = Symbol('r1x')
r2x = Symbol('r2x')
r1y = Symbol('r1y')
r2y = Symbol('r2y')
r1z = Symbol('r1z')
r2z = Symbol('r2z')


zl1 = Symbol('zl1')
zl1 = Symbol('zl2')
#contact point 1 , sensed by laser inferometer
p_l1 = Matrix([0,0,zl1])
#contact point 2 , sensed by laser inferometer
p_l1 = Matrix([0,0,zl2])
#p1 p2 , sensed by laser inferometer
p_l1_l2 = p_l1.row_join(p_l2)

# the transform matrix from real-inferometer-frame to reference frame 
# was simplified by small angle approch
H_l_r = Matrix([[1,a*b,b,tx],[0,1,-a,ty],[-b,a,1,tz],[0,0,0,1]])

#p1 p2 , the sense point respect to reference frame
p_r1_r2 = Matrix([[r1x,r2x],[r1y,r2y],[r1z,r2z],[1,1]])

#
l_r_relation = Eq(H*p_l1_l2,p_r1_r2)

#the coefficient matrix for above relation
cof = Matrix([[1,0,0,0,zl1,0],\
	      [0,1,0,-zl1,0,0],\
	      [0,0,1,0,0,zl1],\
	      [1,0,0,0,zl2,0],\
	      [0,1,0,-zl2,0,0],\
	      [0,0,1,0,0,zl2]])
#the matrix form for system
cofb = cof.row_join(Matrix([r1x,r1y,r1z,r2x,r2y,r2z]))

linsolve(system,tx,ty,tz,a,b,1)