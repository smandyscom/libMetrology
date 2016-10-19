import def2
import numpy
from numpy import random as rd
PI=numpy.pi

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
error_vector = position_error+angle_error
print 'Error vector:{0}'.format(error_vector)
T_c_r_error = def2.HomogenousTransformation(xyzabc=error_vector)
T_c_r = T_c_r_error * T_c_r_nominal

#generate 4-points able to construct orthogonal vector, respect to frame-r
p_set_r = numpy.hstack(tuple([T_s0_r(0)*T_s_s0(p+(0,0,0))*p_s for p in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]]))
print p_set_r

vp_set_r = numpy.hstack(tuple([p_set_r[:,i]-p_set_r[:,0] for i in range(1,4)]))
vp_set_r = numpy.matrix(numpy.hstack((vp_set_r,p_set_r[:,0])))
print vp_set_r

# observed by frame-C
p_set_c = T_c_r.I * p_set_r
print 'p_set_c{0}'.format(p_set_c)
#
vp_set_c_reveal = numpy.hstack(tuple([p_set_c[:,i]-p_set_c[:,0] for i in range(1,4)]))
vp_set_c_reveal = numpy.matrix(numpy.hstack((vp_set_c_reveal,p_set_c[:,0])))
#take x,y part only , since it is CCD
p_set_c_xy = p_set_c[0:2,:]
vp_set_c_xy = numpy.hstack(tuple([p_set_c_xy[:,i]-p_set_c_xy[:,0] for i in range(1,4)]))
vp_set_c_xy = numpy.hstack((vp_set_c_xy,p_set_c_xy[:,0]))
print vp_set_c_xy

# due to property of orthogonal , cross product Vx,Vy part to generate Vz
vx = vp_set_c_xy[0,0:3]
vy = vp_set_c_xy[1,0:3]
vz = numpy.matrix(numpy.cross(vx,vy))
print vx,vy,vz
vx_vy_vz = numpy.matrix(numpy.vstack((vx,vy,vz)))
print vx_vy_vz
print def2.is_Orthogonal(vx_vy_vz)

vp_set_c = numpy.matlib.identity(4)
vp_set_c[0:3,0:3] = vx_vy_vz
vp_set_c[0:2,3] = vp_set_c_xy[:,3]
#use nominal parameter
vp_set_c[2,3] = -1 * T_c_r_nominal[2,3]
print vp_set_c

# T_c_r_answer = def2.HomogenousTransformation(RP=(vp_set_r[0:3, 0:3] * vx_vy_vz.I ,
                                                          # numpy.matrix([0,0,0]).T))
T_r_c = numpy.matlib.identity(4)
T_r_c[0:3,0:3] = vp_set_c[0:3,0:3] * vp_set_r[0:3,0:3].T
T_r_c[0:3,3] = vp_set_c[0:3,3] - T_r_c[0:3,0:3].T * vp_set_r[0:3,3]
T_c_r_answer = T_r_c.I
# T_c_r_answer[0,3] = vp_set_c[0,3] - (T_c_r_answer[0:3,0:3]*vp_set_r[0:3,3])[0,:]
# T_c_r_answer[1,3] = vp_set_c[1,3] - (T_c_r_answer[0:3,0:3]*vp_set_r[0:3,3])[1,:]

#Compare the R matrix
print vp_set_r[0:3,0:3] * vx_vy_vz.I
print T_c_r[0:3,0:3]

print 'reveal{0}'.format(vp_set_c_reveal)
print 'calculate{0}'.format(vp_set_c)

print T_c_r_answer
print T_c_r
print T_c_r_nominal

print vp_set_c * (T_c_r_nominal.I*vp_set_r).I
print T_c_r_error.I

