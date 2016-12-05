import symbol_def
import sympy

#CCD real frame to ideal frame
T_c_cerror = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('ex', 'ey', 'ez'),
                                                symbol_def.Translation_Vector('sx', 'sy','sz'))
T_c_r = symbol_def.Transformation_Matrix(sympy.eye(3),
                                         symbol_def.Translation_Vector('Cx','Cy','Cz'))
T_s0_r = symbol_def.Transformation_Matrix(sympy.eye(3),
                                          symbol_def.Translation_Vector('S0X','S0Y','S0Z'))
#fixed rotation(reference frame)
T_s_s0 = symbol_def.Transformation_Matrix(sympy.eye(3),
                                         symbol_def.Translation_Vector('SX','SY','SZ'))

__chain = T_c_cerror*T_c_r.inv()*T_s0_r*T_s_s0
# print T_c_r.inv()
print __chain[0,3]
print __chain[2,3]
__chain_p = __chain[0:2,3]
sympy.init_printing()
print __chain_p.jacobian(sympy.Matrix(['ex','ey','ez','sx','sy','sz']))

