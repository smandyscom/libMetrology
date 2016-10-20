import def2
import numpy
from numpy import random as rd
PI=numpy.pi

#given 4-point , generate vector/postion  set respect to p0
def vp_set(p_set):
    vp_set_ = numpy.hstack(tuple([p_set[:,i]-p_set[:,0] for i in range(1,4)]))
    vp_set_ = numpy.matrix(numpy.hstack((vp_set_,p_set[:,0])))
    return vp_set_

p_s = def2.PositionVector(0, 0, 10)


def T_s_s0(axes_coordinate):
    return def2.HomogenousTransformation(xyzabc=axes_coordinate)


def T_s0_r(X, Y=10, Z=10, a=0, b=0, c=0):
    return def2.HomogenousTransformation(xyzabc=(X, Y, Z, a, b, c))

T_c_r_nominal = def2.HomogenousTransformation(xyzabc=(100,100,100,0,0,0))

#take artribary ex,ey,ez,ea,eb,ec
position_error_magnitude = 5 #10 mm
position_error= tuple([rd.sample()*position_error_magnitude for x in range(0,3)])
angle_error_magnitude = numpy.deg2rad(5)# rad
angle_error = tuple([rd.sample()*angle_error_magnitude for x in range(0,3)])
error_vector = position_error+angle_error # tuple join
print 'Error vector:{0}'.format(error_vector)

T_c_r_error = def2.HomogenousTransformation(xyzabc=error_vector)
T_c_r = T_c_r_error * T_c_r_nominal

#generate 4-points able to construct orthogonal vector, respect to frame-r
p_set_r = numpy.hstack(tuple([T_s0_r(0)*T_s_s0(p+(0,0,0))*p_s for p in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]]))
# [p1-p0 , p2-p0 , p3-p0 , p0 ]r
vp_set_r = vp_set(p_set_r) 
# observed by frame-C
p_set_c = T_c_r.I * p_set_r
# [p1-p0 , p2-p0 , p3-p0 , p0 ]
vp_set_c = vp_set(p_set_c)

assert numpy.allclose(T_c_r.I*vp_set_r,vp_set_c) , 'vp_set_c equals T_c_r.I* vp_set_r'
assert numpy.allclose(vp_set_c*vp_set_r.I,T_c_r.I) , 'T_c_r.I equals vp_set_c * vp_set_r.I'

#take x,y part only , since it is CCD
p_set_c_xy = p_set_c[0:2,:]
vp_set_c_xy = vp_set(p_set_c_xy)

#Object : given vp_set_c_xy , restore T_c_r
# algorithm need to test :Start

# due to property of orthogonal , cross product Vx,Vy part to generate Vz
vx = vp_set_c_xy[0,0:3]
vy = vp_set_c_xy[1,0:3]
vz = numpy.matrix(numpy.cross(vx,vy))
vx_vy_vz = numpy.matrix(numpy.vstack((vx,vy,vz)))
assert def2.is_Orthogonal(vx_vy_vz)

vp_set_c_answer = numpy.matlib.identity(4)
vp_set_c_answer[0:3,0:3] = vx_vy_vz
#Fix me : how to get z value
vp_set_c_answer[:,3]=p_set_c[:,0]
assert numpy.allclose(vp_set_c,vp_set_c_answer)
#approach 1: direct inverse
T_c_r_answer = (vp_set_c_answer*vp_set_r.I).I
assert numpy.allclose(T_c_r_answer,T_c_r)
#approach 2 : solve elements
T_r_c = numpy.matlib.identity(4)
T_r_c[0:3,0:3] = vp_set_c[0:3,0:3] * vp_set_r[0:3,0:3].I
T_r_c[0:3,3] = vp_set_c[0:3,3] - T_r_c[0:3,0:3] * vp_set_r[0:3,3]
T_c_r_answer2 = T_r_c.I
assert numpy.allclose(T_c_r_answer2,T_c_r_answer) , T_c_r_answer2-T_c_r_answer

#examine error calculation
T_c_r_error_answer = T_c_r_answer * T_c_r_nominal.I 
assert numpy.allclose(T_c_r_error_answer,T_c_r_error) , T_c_r_error_answer-T_c_r_error

