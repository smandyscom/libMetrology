from frame_def import T_lreal_l, T_l_c4, T_c4_y0real, T_y0_y0real, T_y0_s0, T_s0_r, P_r, ERROR_VECTOR_L
import sympy
import unittest

#measured by L-Frame , represented in R-Frame
def P_r_by_l_real(Ax, Ay, Mz):
    return T_s0_r(Ax)*T_y0_s0*T_y0_y0real*T_c4_y0real(Ay)*T_l_c4*T_lreal_l*sympy.Matrix(([0, 0, Mz, 1]))

# Laser measure error analysis(without sz)
def l_error_analysis_1():
    # fitted ellipse center , measured by laser,  represented in R-Frames
    Ax_fitted_center, Ay_fitted_center = sympy.symbols(['Ax_fitted_center', 'Ay_fitted_center'])
    # fitted ellipse center , z-value
    Mz = sympy.Symbol('Mz')
    P_l = sympy.Matrix(([0, 0, Mz, 1]))
    T_l_r = T_s0_r(Ax_fitted_center)*T_y0_s0*T_y0_y0real.inv()*T_c4_y0real(Ay_fitted_center)*T_l_c4
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

class TestAnalysisFunction(unittest.TestCase):
    def setUp(self):
        sympy.init_printing()

    def test_c1(self):
        pass

