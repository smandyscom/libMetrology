from frame_def import frame_c_dictionary, T_s0_r, T_s_s0, P_r
import sympy
import unittest

# CCD error analysis
def ccd_error_analysis(Ax, key='C1'):
    T_ci_r, T_ci_cireal, ERROR_VECTOR_Ci = frame_c_dictionary[key]
    #
    S_AXIS_VECTOR = ('Sx', 'Sy', 'Sz', 0, 0, 0)
    P_ci_real = T_ci_cireal*T_ci_r.inv()*T_s0_r(Ax)*T_s_s0(S_AXIS_VECTOR)*P_r
    P_ci_nominal = T_ci_r.inv()*T_s0_r(Ax)*T_s_s0(S_AXIS_VECTOR)*P_r
    P_ci_error = P_ci_nominal[0:2, :] - P_ci_real[0:2, :]

    error_gain_p_ci  = P_ci_error.jacobian(ERROR_VECTOR_Ci)
    return error_gain_p_ci


class TestAnalysisFunction(unittest.TestCase):
    def setUp(self):
        sympy.init_printing()

    def test_c1(self):
        print ccd_error_analysis('Ax', 'C1')



