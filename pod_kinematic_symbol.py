import sympy
import symbol_def

sympy.init_printing()
X,Y,Z = sympy.symbols("X Y Z")

xyz_translation = sympy.eye(4)
xyz_translation[:3,3] = sympy.Matrix([X,Y,Z])

abc_rotation = sympy.eye(4)
abc_rotation[:3,:3] = symbol_def.Rz_Matrix('c')* symbol_def.Ry_Matrix('b') * symbol_def.Rx_Matrix('a')

# translation comes before rotation
pod_fixed = abc_rotation * xyz_translation
#rotation comes before translation
pod_relative = xyz_translation * abc_rotation


