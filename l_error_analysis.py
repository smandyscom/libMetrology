from frame_def import T_lreal_l, T_l_c4, T_c4_y0real, T_y0real_y0, T_y0_s0, T_s0_r, P_r, ERROR_VECTOR_L, ERROR_VECTOR_Y0
import sympy
import unittest

#measured by L-Frame , represented in R-Frame
def P_r_by_l_real(Ax, Ay, Mz):
    return T_s0_r(Ax)*T_y0_s0*T_y0real_y0*T_c4_y0real(Ay)*T_l_c4*T_lreal_l*sympy.Matrix(([0, 0, Mz, 1]))

def P_r_by_l_real_2():
    # simplified
    Txy, Tyy, Tzy = sympy.symbols('Txy,Tyy,Tzy')
    ex, ey, ez  = ERROR_VECTOR_Y0[0:3]
    T_y0real_s0 = sympy.Matrix(([1, -ez, ey, Txy],
                                [ez, 1, -ex, Tyy],
                                [-ey, ex, 1, Tzy],
                                [0, 0, 0, 1]))

    Txl, Tyl, Tzl = sympy.symbols('Txl,Tyl,Tzl')
    ex, ey, ez  = ERROR_VECTOR_L[0:3]
    T_lreal_c4 = sympy.Matrix(([1, -ez, ey, Txl],
                               [ez, 1, -ex, Tyl],
                               [-ey, ex, 1, Tzl],
                               [0, 0, 0, 1]))
    Ax, Ay, Mz = sympy.symbols('Ax,Ay,Mz')
    P_r = T_s0_r(Ax)*T_y0real_s0*T_c4_y0real(Ay)*T_lreal_c4*sympy.Matrix(([0, 0, Mz, 1]))
    P_r_jacobian = P_r.jacobian((Ax, Ay, Mz))
    P_r_offset = P_r - P_r_jacobian * sympy.Matrix(([Ax, Ay, Mz]))
    return sympy.simplify(P_r_jacobian), sympy.simplify(P_r_offset)


# Laser measure error analysis(without sz)
def l_error_analysis_1():
    # fitted ellipse center , measured by laser,  represented in R-Frames
    Ax_fitted_center, Ay_fitted_center = sympy.symbols(['Ax_fitted_center', 'Ay_fitted_center'])
    # fitted ellipse center , z-value
    Mz = sympy.Symbol('Mz')
    P_l = sympy.Matrix(([0, 0, Mz, 1]))
    T_l_r = T_s0_r(Ax_fitted_center)*T_y0_s0*T_y0real_y0*T_c4_y0real(Ay_fitted_center)*T_l_c4
    #T_l_r is fully known
    P_r_nominal = T_l_r*P_l
    P_r_real = T_l_r*T_lreal_l*P_l
    # where P_r_real_l , mearused by top_view @
    # Ax_fitted_center,Ay_fitted_center
    P_r_error = P_r_nominal[0:2, :] - P_r_real[0:2, :]

    error_gain_p_r = P_r_error.jacobian(ERROR_VECTOR_L)

    return sympy.simplify(error_gain_p_r)

def l_error_analysis_2():
    Mz = sympy.Symbol('Mz')
    P_l_nominal = sympy.Matrix(([0, 0, Mz, 1]))
    P_l_real = T_lreal_l*P_l_nominal
    P_l_error = P_l_nominal - P_l_real

    error_gain_p_l = P_l_error.jacobian([ERROR_VECTOR_L])

    return P_l_error, error_gain_p_l

def l_ax_ay_profile_analysis():
    __coeff = iter(sympy.symbols(['C{0}'.format(x) for x in range(0, 20)]))
    Ax, Ay, Mz = sympy.symbols(['Ax', 'Ay', 'Mz'])
    __x = (Ax, Ay, Mz)
    P_r = P_r_by_l_real(Ax, Ay, Mz)
    # take some organizing
    new_entity = []
    for entity in P_r[:, :]:
        expr = entity.expand().collect(__x)
        # print expr
        record = []
        for factor in __x:
            expr = expr.subs(expr.coeff(factor), __coeff.next())
            record.append(factor*expr.coeff(factor))
        #replace constant as simplified symbol
        expr = expr.subs(expr - sum(record),
                         __coeff.next())
        new_entity.append(expr)

    P_r = sympy.Matrix(new_entity)
    P_r = P_r[0:3, :]
    # since going to scan a circle profile, a conoical form established
    circle_expr = sum([x**2 for x in P_r[:, :]])
    # generate ellipse form
    ellipse_coff_2 = (sympy.Matrix([circle_expr.expand()]).jacobian(__x)).jacobian(__x)
    ellipse_expr_2 = (sympy.Matrix(__x).T * (ellipse_coff_2/2).T * sympy.Matrix(__x))[0, 0]
    ellipse_coff_1 = sympy.Matrix([circle_expr.expand() - ellipse_expr_2.expand()]).jacobian(__x)
    ellipse_expr_1 =  (ellipse_coff_1 * sympy.Matrix(__x))[0, 0]
    ellipse_expr_0 = circle_expr.expand() - ellipse_expr_2.expand() - ellipse_expr_1.expand()
    return ellipse_coff_2, ellipse_coff_1,  ellipse_expr_0


class TestAnalysisFunction(unittest.TestCase):
    def setUp(self):
        sympy.init_printing()

    def test_c1(self):
        pass

