import symbol_def
import sympy

#given fixed DOF(z-axis) , evaluate all orthognal vector lengths

a = sympy.Symbol('a',real=True)
v1 = sympy.Matrix([a,0,0])
v2 = symbol_def.Rz_Matrix(120)*v1
v3 = symbol_def.Rz_Matrix(120)*v2
print v1,v2,v3
v1_v2_v3 = v1.col_insert(1,v2).col_insert(2,v3)
print sympy.trigsimp(v1_v2_v3)

v1_v2_v3[2,:] = v1_v2_v3[0,:].cross(v1_v2_v3[1,:])

v1_v2_v3_simp = sympy.trigsimp(v1_v2_v3)
v1_v2_v3_evaif = v1_v2_v3_simp.evalf()

print v1_v2_v3_evaif

candinates = [v1_v2_v3_evaif[2,i] for i in range(0,3)]
candinates = map(sympy.Abs,candinates)
# __max = sympy.Max(tuple(candinates))
# print __max

print v1_v2_v3_evaif.subs(a,1)

