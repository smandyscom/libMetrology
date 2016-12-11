import symbol_def
import sympy
ERROR_VECTOR = sympy.Matrix(['ex', 'ey', 'ez', 'sx', 'sy', 'sz'])


#Head ball position in S-Frame
Px, Py, Pz = sympy.symbols(['Px', 'Py', 'Pz'])
P_r = sympy.Matrix([Px, Py, Pz, 1])

#C1 Frame in R-Frame
C1x, C1y, C1z = sympy.symbols(['C1x', 'C1y', 'C1z'])
T_c1_r = symbol_def.Transformation_Matrix(sympy.Matrix(([1, 0, 0],
                                                        [0, 1, 0],
                                                        [0, 0, 1])),
                                          symbol_def.Translation_Vector(C1x, C1y, C1z))
ERROR_VECTOR_C1 = sympy.symbols(['exc1', 'eyc1', 'ezc1', 'sxc1', 'syc1', 'szc1'])
T_c1_c1real = symbol_def.Error_Matrix(ERROR_VECTOR_C1)

#C2 Frame in R-Frame
C2x, C2y, C2z = sympy.symbols(['C2x', 'C2y', 'C2z'])
T_c2_r = symbol_def.Transformation_Matrix(sympy.Matrix(([1, 0, 0],
                                                        [0, 1, 0],
                                                        [0, 0, 1])),
                                          symbol_def.Translation_Vector(C2x, C2y, C2z))
ERROR_VECTOR_C2 = sympy.symbols(['exc2', 'eyc2', 'ezc2', 'sxc2', 'syc2', 'szc2'])
T_c2_c2real = symbol_def.Error_Matrix(ERROR_VECTOR_C2)

#C3 Frame in R-Frame
C3x, C3y, C3z = sympy.symbols(['C3x', 'C3y', 'C3z'])
T_c3_r = symbol_def.Transformation_Matrix(sympy.Matrix(([1, 0, 0],
                                                        [0, 1, 0],
                                                        [0, 0, 1])),
                                          symbol_def.Translation_Vector(C3x, C3y, C3z))
ERROR_VECTOR_C3 = sympy.symbols(['exc3', 'eyc3', 'ezc3', 'sxc3', 'syc3', 'szc3'])
T_c3_c3real = symbol_def.Error_Matrix(ERROR_VECTOR_C3)

#
#L Frame to C4-Frame
LX, LY, LZ = sympy.symbols(['LX', 'LY', 'LZ'])
T_l_c4 = symbol_def.Transformation_Matrix(sympy.eye(3),
                                          symbol_def.Translation_Vector(LX, LY, LZ))
ERROR_VECTOR_L = sympy.symbols(['exL', 'eyL', 'ezL', 'sxL', 'syL', 'szL'])
T_Lreal_L = symbol_def.Error_Matrix(ERROR_VECTOR_L)

#Variable Frames
#S0-Frame in R-Frame
S0Y, S0Z = sympy.symbols(['S0Y', 'S0Z'])
def T_s0_r(Ax):
    return symbol_def.Transformation_Matrix(sympy.Matrix(([-1, 0, 0],
                                                          [0, 1, 0],
                                                          [0, 0, -1])),
                                            symbol_def.Translation_Vector(Ax, S0Y, S0Z))
#S-Frame in S0-Frame (6-DOF)
def T_s_s0(axis_tuple):
    x, y, z, a, b, c = axis_tuple
    return symbol_def.Transformation_Matrix(symbol_def.Rz_Matrix(c) *
                                            symbol_def.Ry_Matrix(b) *
                                            symbol_def.Rx_Matrix(a),
                                            symbol_def.Translation_Vector(x, y, z))
#Y0-Frame in S0-Frame
Y0X, Y0Y, Y0Z = sympy.symbols(['Y0X', 'Y0Y', 'Y0Z'])
T_y0_s0 = symbol_def.Transformation_Matrix(sympy.eye(3),
                                           symbol_def.Translation_Vector(Y0X, Y0Y, Y0Z))

#Y0REAL-Frame in Y-Frame
ERROR_VECTOR_Y0 = sympy.symbols(['exy0', 'eyy0', 'ezy0', 'sxy0', 'syy0', 'szy0'])
T_y0real_y0 = symbol_def.Error_Matrix(ERROR_VECTOR_Y0)

#C4-Frame in Y0REAL-Frame
C4x, C4y, C4z = sympy.symbols(['C4x', 'C4y', 'C4z'])
def T_c4_y0real(Ay):
    return symbol_def.Transformation_Matrix(sympy.Matrix(([1, 0, 0],
                                                          [0, 1, 0],
                                                          [0, 0, 1])),
                                            symbol_def.Translation_Vector(C4x, C4y + Ay, C4z))

# CCD error analysis
def ccd_error_analysis_1(Ax, key='C1'):
    #establish frames
    frame_c_dictionary = {}
    frame_c_dictionary['C1'] = (T_c1_r, T_c1_c1real, ERROR_VECTOR_C1)
    frame_c_dictionary['C2'] = (T_c2_r, T_c2_c2real, ERROR_VECTOR_C2)
    frame_c_dictionary['C3'] = (T_c3_r, T_c3_c3real, ERROR_VECTOR_C3)
    #
    T_ci_r, T_ci_cireal, ERROR_VECTOR_Ci = frame_c_dictionary[key]
    #
    S_AXIS_VECTOR = ('Sx', 'Sy', 'Sz', 0, 0, 0)
    P_ci_real = T_ci_cireal*T_ci_r.inv()*T_s0_r(Ax)*T_s_s0(S_AXIS_VECTOR)*P_r
    P_ci_nominal = T_ci_r.inv()*T_s0_r(Ax)*T_s_s0(S_AXIS_VECTOR)*P_r
    P_ci_error = P_ci_nominal[0:2, :] - P_ci_real[0:2, :]

    error_gain_p_ci  = P_ci_error.jacobian(ERROR_VECTOR_Ci)
    return error_gain_p_ci


#CCD4 measure error analysis
def ccd4_error_analysis(Ax, Ay):
    P_c4_real = T_c4_y0real(Ay).inv()*T_y0real_y0.inv()*T_y0_s0.inv()*T_s0_r(Ax).inv()*P_r
    P_c4_nominal = T_c4_y0real(Ay).inv()*T_y0_s0.inv()*T_s0_r(Ax).inv()*P_r
    P_c4_error = P_c4_nominal[0:2, :] - P_c4_real[0:2, :]

    error_gain_p_c4 = P_c4_error.jacobian(ERROR_VECTOR_Y0)
    return error_gain_p_c4


