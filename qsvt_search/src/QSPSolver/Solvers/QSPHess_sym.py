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
#--------------------------------------------------------------------------

def QSPHess_sym(phi, delta, options) -> (object, object, object):
    m = len(delta)
    d = len(phi)
    obj = np.zeros((m, 1))
    grad = np.zeros((m, d))
    hess = np.zeros((d, d, m))
    sigmaz = np.array([[1, 0], 
                        [0, -1]])
    temp_sig = 1j * sigmaz
    gate = np.array([[np.exp(1j * pi / 4), 0],
                    [0, np.exp(-1j * pi / 4)]])
    
    exp_theta = np.exp(1j * phi)
    targetx = options["target"]
    parity = options["parity"]

    # Start Hessian

    for i in range(m):
        x = delta[i]
        Wx = np.array([[x, 1j * np.sqrt(1 - x**2)], 
                        [1j * np.sqrt(1 - x**2), x]])
        temp_save = np.zeros((2, 2, d, d+1))
        temp_lef_save = np.zeros((2, 2, d+1))

        for j in range(d):
            temp_save[:, :, j, j] = np.eye(2)

        thetawx = np.zeros((2, 2, d))

        for j in range(d):
            thetawx[:, :, j]  = np.array([[exp_theta[j], 0], 
                                            [0, exp_theta[j].conj()]]) @ Wx

        for j in range(d):
            for k in range(j+1, d+1):
                if (k < d):
                    temp_save[:, :, j, k] = temp_save[:, :, j, k - 1] @ thetawx[:, :, k - 1]
                else:
                    temp_save[:, :, j, k] = temp_save[:, :, j, k - 1] @ np.array([[exp_theta[d - 1], 0],
                                                                                [0, exp_theta[d - 1].conj()]]) @ gate
        if parity == 1:
            qspmat = temp_save[:, :, 0, d].T @ Wx @ temp_save[:, :, 0, d]
            gap = np.real(qspmat[0, 0]) - targetx(x)
            leftmat = temp_save[:, :, 0, d].T @ Wx
            for j in range(d + 1):
                temp_lef_save[:, :, j] = leftmat @ temp_save[:, :, 0, j]
            
            grad_temp = np.zeros((2, 2, d))
            grad_lef_temp = np.zeros((2, 2, d))
            grad_Wtemp = np.zeros((2, 2, d))

            for j in range(d):
                grad_temp[:, :, j] = temp_save[:, :, 0, j] @ temp_sig @ temp_save[:, :, j, d]
                grad_lef_temp[:, :, j] = 2 * leftmat @ grad_temp[:, :, j]
                grad[i, j] = np.real(grad_lef_temp[0, 0, j]) * gap

            for j in range(d):
                grad_Wtemp[:, :, j] = Wx @ grad_temp[:, :, j]
            
            for j in range(d):
                for k in range(j, d):
                    hesst = temp_lef_save[:, :, j] * np.array([1, -1]) @ temp_save[:, :, j, k] * np.array([-1, 1]) @ temp_save[:, :, k, d]
                    hesst_temp = 2 * np.real(hesst[0, 0]) * gap
                    hesst_2 = (grad_temp[:, :, j] @ grad_Wtemp[:, :, k]).T
                    hess_temp_2 = 2 * np.real(hesst_2[0, 0]) * gap
                    hess[j, k, i] = np.real(grad_lef_temp[0, 0, j]) * np.real(grad_lef_temp[0, 0, k]) + hesst_temp + hess_temp_2
                    hess[k, j, i] = hess[j, k, i]
            obj[i] = 0.5 * (np.real(qspmat[0, 0,]) - targetx(x)) ** 2
        else:
            qspmat = temp_save[:, :, 1, d].T @ Wx @ temp_save[:, :, 0, d]
            gap = np.real(qspmat[0, 0] - targetx(x))
            leftmat = temp_save[:, : 1, d].T @ Wx
            for j in range(d+1):
                temp_lef_save[:, :, j] = leftmat @ temp_save[:, :, 0, j]
            
            grad_temp = np.zeros((2, 2, d))
            grad_temp_2 = np.zeros((2, 2, d))
            grad_lef_temp = np.zeros((2, 2, d))
            grad_Wtemp = np.zeros((2, 2, d))

            for j in range(d):
                if j != 0:
                    grad_temp_2[:, :, j] = temp_save[:, :, 1, j] @ temp_sig @ temp_save[:, :, j, d]

                grad_temp[:, :, j] = temp_save[:, :, 0, j] @ temp_sig @ temp_save[:, :, j, d]
                grad_lef_temp[:, :, j] = 2 * leftmat @ grad_temp[:, :, j]
                if j == 0:
                    grad_lef_temp[:, :, j] /= 2
                grad[i, j] = np.real(grad_lef_temp[0, 0, j]) * gap
            
            for j in range(d):
                grad_Wtemp[:, :, j] = Wx @ grad_temp[:, :, j]
            
            for k in range(d):
                hesst = leftmat * np.array([1, -1]) @ temp_save[:, :, 0, k] * np.array([-1, 1]) @ temp_save[:, :, k, d]
                hesst_temp = np.real(hesst[0, 0] @ gap)
                if k == 0:
                    hesst_2 = np.zeros((2,2))
                else:
                    hesst_2 = (temp_save[:, :, 0, d] @ temp_save @ Wx @ grad_temp_2[:, :, k]).T
                
                hesst_temp_2 = np.real(hesst[0, 0]) @ gap
                hess[0, k, i] = np.real(grad_lef_temp[0, 0, 0]) @ np.real(grad_lef_temp[0, 0, k]) + hesst_temp + hesst_temp_2
                hess[k, 0, i] = hess[0, k, i]
            
            for j in range(1, d):
                for k in range(j, d):
                    hesst = temp_lef_save[:, :, j] * np.array([1, -1]) @ temp_save[:, :, j, k] * np.array([-1, 1]) @ temp_save[:, :, k, d]
                    hesst_temp = 2 * np.real(hesst[0, 0]) @ gap
                    hesst2 = grad_temp_2[:, :, j].T @ grad_Wtemp[:, :, k]
                    hesst_temp_2 = 2 * np.real(hesst2[0, 0]) @ gap
                    hess[j, k, i] = np.real(grad_lef_temp[0, 0, j]) @ np.real(grad_lef_temp[0, 0, k]) + hesst_temp + hesst_temp_2
                    hess[k, j, i] = hess[j, k, i]

            obj[i] = 0.5 * (np.real(qspmat[0, 0]) - targetx(x)) ** 2
    return hess, grad, obj




























