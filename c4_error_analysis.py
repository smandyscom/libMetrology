from frame_def import T_c4_y0real, T_y0_y0real, T_y0_s0, T_s0_r, P_r, ERROR_VECTOR_Y0
import sympy
import unittest


#CCD4 measure error analysis
def ccd4_error_analysis(Ax, Ay):
    P_c4_real = T_c4_y0real(Ay).inv()*T_y0_y0real*T_y0_s0.inv()*T_s0_r(Ax).inv()*P_r
    P_c4_nominal = T_c4_y0real(Ay).inv()*T_y0_s0.inv()*T_s0_r(Ax).inv()*P_r
    P_c4_error = P_c4_nominal[0:2, :] - P_c4_real[0:2, :]

    # print '{0}\n{1}'.format(P_c4_real, P_c4_nominal, P_c4_error)

    error_gain_p_c4 = P_c4_error.jacobian(ERROR_VECTOR_Y0)
    return error_gain_p_c4

class TestAnalysisFunction(unittest.TestCase):
    def setUp(self):
        sympy.init_printing()

    def test_c1(self):
        print ccd4_error_analysis('Ax', 'Ay')


