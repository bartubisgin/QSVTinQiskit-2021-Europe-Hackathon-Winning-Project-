import numpy as np
import time

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
    pi_n = [pi / 2 / (2*tot_len) for _ in range(2*tot_len)]
    delta = np.conj(np.cos(np.dot(np.arange(1, 2*tot_len, 2), pi_n)))
    options["target"] = lambda x, opts: ChebyCoef2Func(x, coeff, parity, True)
    options["parity"] = parity
    obj = QSPObj_sym
    grad = QSPGrad_sym

    start_time = time.time()
    [phi, obj_value, out] = QSP_LBFGS(
        obj, grad, delta, np.zeros((tot_len, 1)), options)
    phi[end] += np.pi/4

    # The : indexes are 99# problematic, not sure how to convert them yet

    if parity == 0:
        phi_proc = np.zeros((2 * len(phi) - 1, 1))
        phi_proc[1: len(phi) - 1] = phi[end: 2: -1]
        phi_proc(len(phi): end) = phi

    else:
        phi_proc = np.zeros((2 * len(phi, 1))
        phi_proc[1: len(phi)]=phi[end: 1: -1]
        phi_proc[len(phi) + 1: end]=phi

    lapsed_time=time.time() - start_time
    out["time"]=lapsed_time
    out["value"]=obj_value

    return phi_proc, out
