import sympy
from sympy import polys

import symbol_def

sympy.init_printing()

#Error factors for Frame Y0 to Frame S0
eyx,eyy,eyz,syx,syy,syz = sympy.symbols(('eyx','eyy','eyz','syx','syy','syz'))
#Nominal Frame L translation respect to Y0
LX,LY,LZ = sympy.symbols(('LX','LY','LZ'))
#Error factors for Frame L to Frame Y0
elx,ely,slx,sly,slz = sympy.symbols(('elx','ely','slx','sly','slz'))

# Mearsure frame = YE = L , yaw is dont cared , since it is distance meter
T_YE_Y = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('elx', 'ely', 0),
                                                symbol_def.Translation_Vector('slx', 'sly','slz'))
T_Y_Y0E = symbol_def.Transformation_Matrix(sympy.eye(3),
                                                  symbol_def.Translation_Vector(0, 'LY', 0))
T_Y0E_Y0 = symbol_def.Transformation_Matrix(symbol_def.Error_Matrix('eyx', 'eyy','eyz'),
                                                 symbol_def.Translation_Vector('syx', 'syy', 'syz'))

p_l_measure = symbol_def.Translation_Vector(0,0,'zl').col_join(sympy.Matrix([1]))
p_s0_known = symbol_def.Translation_Vector('rx','ry','rz').col_join(sympy.Matrix([1]))

p_s0_measure = T_Y0E_Y0 *T_Y_Y0E *T_YE_Y *p_l_measure

linkage = sympy.Eq(T_Y0E_Y0 *T_Y_Y0E *T_YE_Y *p_l_measure,p_s0_known)
print linkage

#ignore any second error, take all of them as zero
elimiation_table = [x*y for y in [elx,ely,slx,sly,slz] for x in (eyx,eyy,eyz,syx,syy,syz)]
#approximation : set second error as zero
for var in elimiation_table:
    linkage = linkage.subs(var,0)
    #p_s0_measure = p_s0_measure.subs(var,0)
    
#print linkage

#collect coefficient for unknowns
coeffX = polys.polytools.poly(p_s0_measure[0],(eyx,eyy,eyz,syx,syy,syz,elx,ely,slx,sly,slz)).coeffs()
coeffY = polys.polytools.poly(p_s0_measure[1],(eyx,eyy,eyz,syx,syy,syz,elx,ely,slx,sly,slz)).coeffs()
coeffZ = polys.polytools.poly(p_s0_measure[2],(eyx,eyy,eyz,syx,syy,syz,elx,ely,slx,sly,slz)).coeffs()
print coeffX
print coeffY
print coeffZ

print p_s0_measure
for var in elimiation_table:
    p_s0_measure = p_s0_measure.subs(var,0)
print p_s0_measure

#11 unkowns , at least need 4 point = 12 equations to solve
#coeff_matrix = sympy.Matrix([coeffX,coeffY,coeffZ])
#print coeff_matrix


#estimate the condition
#p_l_measures = sympy.Matrix([[0,0,'zl'+str(x),1] for x in range(0,4)]).T
#p_s0_knowns = sympy.Matrix([['rx'+str(x),'ry'+str(x),'rz'+str(x),1] for x in range(0,4)]).T
#p_s0_measures= T_Y0E_Y0 *T_Y_Y0E *T_YE_Y *p_l_measures 
#print p_s0_measures
#coeff_matrix = [polys.polytools.poly(p_s0_measures[i,j],(eyx,eyy,eyz,syx,syy,syz,elx,ely,slx,sly,slz)).coeffs() for i in range(0,4) for j in range(0,4)]
#print sympy.Matrix(coeff_matrix)