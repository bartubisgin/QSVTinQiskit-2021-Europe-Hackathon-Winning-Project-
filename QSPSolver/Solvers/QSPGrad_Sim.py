import numpy as np

#--------------------------------------------------------------------------
# Evalute the gradient and objective of QSP function, provided that 
# phi is symmetric
#
# Input:
#        phi --- Variables
#      delta --- Samples
#       opts --- Options structure with fields
#         target: target function
#         parity: parity of phi (0 -- even, 1 -- odd)
#
# Output:
#        grad --- Gradient of obj function
#         obj --- Objective function value
#

def QSPGrad_sym(phi, delta, options):
    m = len(delta)
    d = len(phi)
    obj = np.zeros((m, 1))
    grad = np.zeros((m, d))
    gate = np.array([[np.exp(1j * np.pi / 4), 0],
                    [np.exp(-1j * np.pi / 4), 0]])

    exp_theta = np.exp(1j * phi)
    targetx = options["target"]
    parity = options["parity"]

    for i in range(m):
        x = delta[i]
        Wx = np.array([[x, 1j*np.sqrt(1 - x**2)],
                        [1j * np.sqrt(1 - x**2), x]])
        temp_save_1 = np.zeros((2, 2, d))
        temp_save_2 = np.zeros((2, 2, d))

        temp_save_1[:, :, 0] = np.eye(2)
        temp_save_2[:, :, 0] = np.array([[exp_theta[d - 1, 0], 0],
                                        [0, np.conj(exp_theta[d - 1, 0])]]) @ gate
        
        for j in range(1, d):
            temp_save_1[:, :, j] = temp_save_1[:, :, j - 1] * np.array([exp_theta[j], np.conj(exp_theta[j])]) @ Wx
            temp_save_2[:, :, j] = np.array([exp_theta[d - j], np.conj(exp_theta[d - j])]) * Wx @ temp_save_2[:, :, j-1]
        
        if parity == 1:
            qspmat = np.transpose(temp_save_2[:, :, d - 1]) @ Wx @ temp_save_2[:, :, d - 1]
            gap = np.real(qspmat[0, 0]) - targetx(x)
            leftmat = np.transpose(temp_save_2[:, :, d - 2]) @ Wx

            for j in range(d):
                grad_temp = leftmat @ temp_save_1[:, :, j] * np.array([1j, -1j]) @ temp_save_2[:, :, d - 1 - j]
                grad[i][j] = 2 * np.real(grad_temp[0, 0]) * gap
            
            grad[i][0] /= 2

            obj[i] = 0.5 * (np.real(qspmat[0, 0]) - targetx(x)) ** 2

    return grad, obj

