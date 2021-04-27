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
    Wx = [[x, 1j*np.sqrt(1-x**2)],
          [1j*np.sqrt(1-x**2), x]]

    gate = [[np.exp(1j * np.pi/4, 0)],
            [0, np.exp(-1j * np.pi/4)]]
    
    exp_phi = np.exp(1j * phi)

    if parity == 1:
        result = [[exp_phi[0], 0], 
                  [0, np.conj(exp_phi[0])]]
        for k in range(1, len(exp_phi)):
            result @= Wx @ [[exp_phi[k], 0],
                            [0, np.conj(exp_phi[k])]]
        result @= gate
        qspmat = result.T @ Wk @ result
    
    else:
        result = np.eye(2)
        for k in range(1, len(exp_phi)):
            result @= np.multiply(Wx, [[exp_phi[k], 0],
                            [0, np.conj(exp_phi[k])]])
        result @= gate
        qspmat = ret.T @ [[exp_phi[0], 0],
                          [0, np.conj(exp_phi[1])]] @ result
    return qspmat
        