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




def QSP_Solver(coeff, parity, options: dict) -> (object, object):
    if not "criteria" in options:
        options["criteria"] = 1e-12

    out = dict()

    tot_len = len(coeff)
    # pi_n = np.array([np.pi / 2 / (2*tot_len) for _ in range(tot_len)])
    delta = np.cos(np.arange(1, 2*tot_len, 2) * np.pi/2/(2*tot_len)).conj()
    options["target"] = lambda x: ChebyCoef2Func(x, coeff, parity, True)
    options["parity"] = parity
    obj = QSPObj_sym
    grad = QSPGrad_sym

    start_time = time.time()
    # (tot_len, 1) or (tot_len, ) ?
    [phi, obj_value, out] = QSP_LBFGS(obj, grad, delta, np.zeros((tot_len, )), options)
    phi[-1] += np.pi/4

    # The : indexes are 99# problematic, not sure how to convert them yet

    if parity == 0:
        phi_proc = np.zeros((2 * len(phi) - 1, ))
        phi_proc[:len(phi) - 1] = phi[1:][::-1]
        phi_proc[len(phi) - 1:] = phi
    else:
        phi_proc = np.zeros((2 * len(phi) ))
        phi_proc[:len(phi)] = phi[::-1]
        phi_proc[len(phi):] = phi

    lapsed_time = time.time() - start_time
    out["time"] = lapsed_time
    out["value"] = obj_value

    return phi_proc, out

