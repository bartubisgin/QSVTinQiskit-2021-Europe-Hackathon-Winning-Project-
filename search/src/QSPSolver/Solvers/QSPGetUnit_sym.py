import numpy as np

#--------------------------------------------------------------------------
# Get the QSP unitary matrix based on given phase vector and point 
# x \in [-1, 1]
#
# Input:
#       phi --- The phase factors 
#         x --- Point to be evaluated
#    parity --- Parity of phi (0 -- even, 1 -- odd)
#
# Output:
#     qspmat--- The QSP unitary matrix
#
#--------------------------------------------------------------------------
#

def QSPGetUnit_sym(phi, x, parity):
    Wx = np.array([[x, 1j*np.sqrt(1-x**2)],
          [1j*np.sqrt(1-x**2), x]])

    gate = np.array([[np.exp(1j * np.pi/4), 0],
            [0, np.exp(-1j * np.pi/4)]])
    
    exp_phi = np.exp(1j * phi)

    # Caused a problem here ?
    # sqrt(1-x^2) becomes a problem here because x = 0.99999 instead of 1
    if parity == 1:
        result = np.array([[exp_phi[0], 0], 
                            [0, exp_phi[0].conj()]])
        for k in range(1, len(exp_phi)):
            result = result @ Wx @ np.array([[exp_phi[k], 0],
                                            [0, exp_phi[k].conj()]])
        result = result @ gate
        qspmat = result.T @ Wx @ result
    
    else:
        result = np.eye(2)
        for k in range(1, len(exp_phi)):
            # @= is not yet supported (why?)
            result = result @ Wx * np.array([[exp_phi[k], 0],
                                            [0, exp_phi[k].conj()]])
        result = result @ gate
        qspmat = result.T @ np.array([[exp_phi[0], 0],
                          [0, exp_phi[1].conj()]]) @ result
    return qspmat
        