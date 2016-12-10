import symbol_def
import sympy
# C_FRAME = sympy.Matrix(([0, 0, 1],
                           # [-1, 0, 0],
                           # [0, 1, 0]))
ERROR_VECTOR = sympy.Matrix(['ex', 'ey', 'ez', 'sx', 'sy', 'sz'])

# Fixed Parameters (nominals)
S_FRAME = sympy.Matrix(([-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, -1]))

#Head ball position in S-Frame
Px, Py, Pz = sympy.symbols(['Px', 'Py', 'Pz'])
P_s = sympy.Matrix([Px, Py, Pz, 1])

#Y0 Frame in S0-Frame
Y0X, Y0Y, Y0Z = sympy.symbols(['Y0X', 'Y0Y', 'Y0Z'])
T_y0_s0 = symbol_def.Transformation_Matrix(sympy.eye(3),
                                           symbol_def.Translation_Vector(Y0X, Y0Y, Y0Z))
#L Frame = (Y Frame)
C4X, C4Y, C4Z = sympy.symbols(['C4X', 'C4Y', 'C4Z'])
T_c4_l = symbol_def.Transformation_Matrix(sympy.eye(3),
                                          symbol_def.Translation_Vector(C4X, C4Y, C4Z))

#Variable Frames
S0Y, S0Z = sympy.symbols(['S0Y', 'S0Z'])
#Translation X-Frame
def T_s0_r(Ax):
    return symbol_def.Transformation_Matrix(S_FRAME,
                                            symbol_def.Translation_Vector(Ax, S0Y, S0Z))
#SmarPod 6-Degree Frame
def T_s_s0(axis_tuple):
    x, y, z, a, b, c = axis_tuple
    return symbol_def.Transformation_Matrix(symbol_def.Rz_Matrix(c) *
                                            symbol_def.Ry_Matrix(b) *
                                            symbol_def.Rx_Matrix(a),
                                            symbol_def.Translation_Vector(x, y, z))
#Translation Y-Frame
def T_y0_c4(Ay):
    return symbol_def.Transformation_Matrix(sympy.eye(3),
                                            symbol_def.Translation_Vector(0, Ay, 0))

#CCD real frame to ideal frame
T_c_creal = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('ex', 'ey', 'ez'),
                                             symbol_def.Translation_Vector('sx', 'sy','sz'))

# CCD error analysis
def ccd_error_analysis_1(C_FRAME, Ax):
    T_c_r = symbol_def.Transformation_Matrix(C_FRAME,
                                            symbol_def.Translation_Vector('Cx','Cy','Cz'))
    # P_c = T_c_creal*T_c_r.inv()*T_s0_r*T_s_s0*P_s
    #fixed rotation(reference frame)
    P_c = T_c_creal*T_c_r.inv()*T_s0_r(Ax)*T_s_s0(('SX', 'SY', 'SZ', 0, 0, 0))*P_s
    P_c = P_c[0:2, :]

    error_gain_p_c  = P_c.jacobian(ERROR_VECTOR)
    return P_c, error_gain_p_c

# Laser error analysis
def laser_error_analysis_2(Ax, Ay):
    #Y0 real frame to ideal frame
    T_y0_y0real = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('exy', 'eyy', 'ezy'),
                                                    symbol_def.Translation_Vector('sxy', 'syy','szy'))
    #L real frame to ideal frame
    T_l_lreal = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('exl', 'eyl', 'ezl'),
                                                    symbol_def.Translation_Vector('sxl', 'syl','szl'))
    #Contact position in L-Frame
    P_l = sympy.Matrix([0, 0, Plz, 1])
    P_r = T_s0_r(Ax)*T_y0_s0*T_y0_y0real*T_l_s0(Ay)*T_l_lreal*P_l
    #Approximation , vanish second order error

