import numpy as np
import time
from .QSPObj_sym import QSPObj_sym
from .QSPGrad_Sim import QSPGrad_sym
from .ChebyCoef2Func import ChebyCoef2Func
from .QSP_LBFGS import QSP_LBFGS

# --------------------------------------------------------------------------
# Given coefficients of a polynomial P, yield corresponding phase factors
#
# The reference chose the first half of the phase factors as the
# optimization variables, while in the code we used the second half of the
# phase factors. These two formulations are equivalent.
#
# To simplify the representation, a constant pi/4 is added to both sides of
# the phase factors when evaluating the objective and the gradient. In the
# output, the FULL phase factors with pi/4 are given.
#
# Input:
#       coef --- Coefficients of polynomial P under Chevyshev basis, P
#                should be even/odd, only provide non-zero coefficients
#     parity --- Parity of polynomial P (0 -- even, 1 -- odd)
#       opts --- Options structure with fields
#                criteria: stop criteria
#
# Output:
#    phi_proc --- Solution of optimization problem, FULL phase factors
#         out --- Information of solving process
#
# --------------------------------------------------------------------------
#


# coeff = [-4.85722573e-17,  1.15635132e+00, -1.11022302e-16, -3.82434639e-01,
#          -1.04083409e-16,  2.25911198e-01,  9.71445147e-17, -1.57682407e-01,
#          -2.77555756e-17,  1.18990330e-01, -4.16333634e-17, -9.38298349e-02,
#          -4.68375339e-17,  7.60566958e-02, -2.77555756e-17, -6.28092870e-02,
#          6.93889390e-18,  5.25742336e-02,  -2.77555756e-17, -4.44744041e-02,
#          1.38777878e-17,  3.79644735e-02,  -2.77555756e-17, -3.26859974e-02,
#          5.03069808e-17,  2.83926438e-02,  -2.77555756e-17, -2.49091444e-02,
#          1.73472348e-18,  2.21076246e-02, -1.04083409e-16]


def QSP_Solver(coeff, parity, options: dict) -> (object, object):
    if not "criteria" in options:
        options["criteria"] = 1e-12

    out = dict()

    tot_len = len(coeff)
    # pi_n = np.array([np.pi / 2 / (2*tot_len) for _ in range(tot_len)])
    delta = np.conj(np.cos(np.arange(1, 2*tot_len, 2) * np.pi/2/(2*tot_len)))
    options["target"] = lambda x: ChebyCoef2Func(x, coeff, parity, True)
    options["parity"] = parity
    obj = QSPObj_sym
    grad = QSPGrad_sym

    start_time = time.time()
    # (tot_len, 1) or (tot_len, ) ?
    [phi, obj_value, out] = QSP_LBFGS(
        obj, grad, delta, np.zeros((tot_len, 1)), options)
    phi[-1] += np.pi/4

    # The : indexes are 99# problematic, not sure how to convert them yet

    if parity == 0:
        phi_proc = np.zeros((2 * len(phi) - 1, 1))
        phi_proc[:len(phi) - 1] = phi[1:][::-1]
        phi_proc[len(phi):] = phi

    else:
        phi_proc = np.zeros((2 * len(phi, 1)))
        phi_proc[:len(phi)] = phi[::-1]
        phi_proc[len(phi) + 1:] = phi

    lapsed_time = time.time() - start_time
    out["time"] = lapsed_time
    out["value"] = obj_value

    return phi_proc, out


# a, b = QSP_Solver(coeff, 1, dict())

# print(a, b)
