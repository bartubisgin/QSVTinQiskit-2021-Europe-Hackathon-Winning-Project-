from Solvers.QSP_solver import QSP_Solver
from Solvers.ChebyCoef2Func import ChebyCoef2Func
from Solvers.QSPGetUnitary import QSPGetUnitary
import numpy as np
import matplotlib.pyplot as plt

coeff = [-4.85722573e-17,  1.15635132e+00, -1.11022302e-16, -3.82434639e-01,
         -1.04083409e-16,  2.25911198e-01,  9.71445147e-17, -1.57682407e-01,
         -2.77555756e-17,  1.18990330e-01, -4.16333634e-17, -9.38298349e-02,
         -4.68375339e-17,  7.60566958e-02, -2.77555756e-17, -6.28092870e-02,
         6.93889390e-18,  5.25742336e-02,  -2.77555756e-17, -4.44744041e-02,
         1.38777878e-17,  3.79644735e-02,  -2.77555756e-17, -3.26859974e-02,
         5.03069808e-17,  2.83926438e-02,  -2.77555756e-17, -2.49091444e-02,
         1.73472348e-18,  2.21076246e-02, -1.04083409e-16]

options = dict()

parity = 0
tau = 1000
criteria = 1e-12
plot_phase = True

options["criteria"] = criteria
options["maxiter"] = 100
max_order = np.ceil(1.4*tau + np.log(1e14))
if np.mod(max_order, 2) == 1:
    max_order -= 1

phi, out = QSP_Solver(coeff, parity, options)


parity_label = ["even", "odd"]
print("- Info: \t\tQSP phase factors --- solved by L-BFGS\n")
print("- Parity: \t\t%s\n- Degree: \t\t%d\n" % (parity_label[parity+1], max_order))
print("- Iteration times: \t%d\n" % out["iter"])
print("- CPU time: \t%.1f s\n" % out["time"])


if plot_phase:
    plt.figure(1)
    temp = phi.copy()
    # why?
    temp[0] -= np.pi/4
    temp[-1] -= np.pi/4
    plt.plot(range(1, len(temp) + 1), temp)

    x = np.linspace(0, 1, 1000)
    def targ(x): return ChebyCoef2Func(x, coeff, parity, True)
    y = np.zeros((x.size))
    yqsp = np.zeros((x.size))
    for jj in range(len(x)):
        y[jj] = targ(x[jj])
        yqsp[jj] = QSPGetUnitary(phi, x[jj])
    yqsp_full = yqsp[~np.isnan(yqsp)]
    scale_fac = np.mean(np.divide(yqsp_full, y))
    print("- Linf approximation error: \t%.2e\n" %
          np.linalg.norm(y*scale_fac - yqsp, np.inf))
    plt.show()