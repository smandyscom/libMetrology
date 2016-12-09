import symbol_def
import sympy
# C_FRAME = sympy.Matrix(([0, 0, 1],
                           # [-1, 0, 0],
                           # [0, 1, 0]))
# S_FRAME = sympy.Matrix(([-1, 0, 0],
                        # [0, 1, 0],
                        # [0, 0, -1]))

ERROR_VECTOR = sympy.Matrix(['ex', 'ey', 'ez', 'sx', 'sy', 'sz'])
Px, Py, Pz = sympy.symbols(['Px', 'Py', 'Pz'])
#CCD real frame to ideal frame
T_c_creal = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('ex', 'ey', 'ez'),
                                                symbol_def.Translation_Vector('sx', 'sy','sz'))

def generate_analysis(C_FRAME, S_FRAME):
    T_c_r = symbol_def.Transformation_Matrix(C_FRAME,
                                            symbol_def.Translation_Vector('Cx','Cy','Cz'))
    T_s0_r = symbol_def.Transformation_Matrix(S_FRAME,
                                            symbol_def.Translation_Vector('S0X','S0Y','S0Z'))
    #fixed rotation(reference frame)
    T_s_s0 = symbol_def.Transformation_Matrix(sympy.eye(3),
                                            symbol_def.Translation_Vector('SX','SY','SZ'))
    #
    P_s = sympy.Matrix([Px, Py, Pz, 1])
    P_c = T_c_creal*T_c_r.inv()*T_s0_r*T_s_s0*P_s
    P_c = P_c[0:2, :]

    error_gain_p_c  = P_c.jacobian(ERROR_VECTOR)
    return P_c, error_gain_p_c


