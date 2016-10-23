import symbol_def
import sympy

sympy.init_printing()

#Error factors for Frame Y0 to Frame S0
eyx,eyy,eyz,syx,syy,syz = sympy.symbols(('eyx','eyy','eyz','syx','syy','syz'))
#Nominal Frame L translation respect to Y0
LX,LY,LZ = sympy.symbols(('LX','LY','LZ'))
#Error factors for Frame L to Frame Y0
elx,ely,slx,sly,slz = sympy.symbols(('elx','ely','slx','sly','slz'))

T_L_Y0_error = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('elx', 'ely', 0),
                                                symbol_def.Translation_Vector('slx', 'sly','slz'))
T_L_Y0_nominal = symbol_def.Transformation_Matrix(sympy.eye(3),
                                                  symbol_def.Translation_Vector('LX', 'LY', 'LZ'))
T_Y0_S0_error = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('eyx', 'eyy','eyz'),
                                                 symbol_def.Translation_Vector('syx', 'syy', 'syz'))

p_l_measure = symbol_def.Translation_Vector(0,0,'zl').col_join(sympy.Matrix([1]))
p_s0_known = symbol_def.Translation_Vector('rx','ry','rz').col_join(sympy.Matrix([1]))

linkage = sympy.Eq(T_Y0_S0_error *T_L_Y0_nominal *T_L_Y0_error *p_l_measure,p_s0_known)
print linkage
#ignore any second error, take all of them as zero


