import numpy as np
from .QSPGetUnit_sym import QSPGetUnit_sym

#--------------------------------------------------------------------------
# Evalute the objective of QSP function, provided that phi is symmetric.
#
# Input:
#        phi --- Variables
#      delta --- Samples
#       opts --- Options structure with fields
#         target: target function
#         parity: parity of phi (0 -- even, 1 -- odd)
#
# Output:
#         obj --- Objective function value
#
#--------------------------------------------------------------------------

def QSPObj_sym(phi, delta, options):
    m = len(delta)
    obj = np.zeros((m, 1))

    for i in range(m):
        qspmat = QSPGetUnit_sym(phi, delta[i], options["parity"])
        obj[i] = 0.5 * (np.real(qspmat[0, 0]) - options["target"](delta[i])) ** 2
    
    return obj