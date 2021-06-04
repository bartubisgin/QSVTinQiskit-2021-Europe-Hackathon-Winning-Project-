import numpy as np

# Get QSP unitary matrix based on given phase vector and point x \in [-1, 1]
#
# ----------------------------------------------------------------------
#
# Input:
#       phase, x
# Output:
#       targ    -- QSP approximation of target, real(result(1, 1))
#

def QSPGetUnitary(phase, x):
    Wx = np.array([[x, 1j * np.sqrt(1 - x**2)],
          [1j * np.sqrt(1 - x ** 2), x]])
    
    exp_phi = np.exp(1j * phase)
    result = np.array([[exp_phi[0], 0],
           [0, exp_phi[0].conj()]])

    for k in range(1, exp_phi.size):
        temp = np.array([[exp_phi[k], 0], 
                [0, exp_phi[k].conj()]])
        result = result @ Wx @ temp
    
    return np.real(result[0, 0])