import numpy as np
from scipy.special import jv as besselj
from Solvers.QSP_solver import QSP_Solver
from math import ceil

# --------------------------------------------------------------------------
# Test case 1: Hamiltonian simulation
#
# Here we want to approxiamte e^{-i\tau x} by Jacobi-Anger expansion:
#
# e^{-i\tau x} = J_0(\tau)+2\sum_{k even} (-1)^{k/2}J_{k}(\tau)T_k(x)+2i\sum_{k odd} (-1)^{(k-1)/2}J_{k}(\tau) T_k(x)
#
# We truncate the series up to N = 1.4\tau+log(10^{14}), which gives an polynomial approximation of e^{-i\tau x} with
# accuracy 10^{-14}. Besides, we deal with real and imaginary part of the truncated series seperatly and divide them
# by a constant factor 2 to enhance stability.
#
# parameters
#     tau: the duration \tau in Hamiltonian simulation
#     criteria: stop criteria, default 1e-12
#     plot_phase: whether plot phase factors
#
# --------------------------------------------------------------------------
#
# Reference: Yulong Dong, Xiang  Meng, K.Birgitta Whaley and Lin Lin
#            Efficient Phase Factor Evaluation in Quantum Signal Processing
#
# Author: Yulong Dong, Xiang Meng
# Version 1.0
# Last Update 06/2020
#
# --------------------------------------------------------------------------
# setup parameters

tau = 1000
criteria = 1e-12
plot_phase = True
opts = dict()

# --------------------------------------------------------------------------
# find phase factors

opts["criteria"] = criteria
max_order = ceil(1.4 * tau + np.log(1e14))
if np.mod(max_order, 2) == 1:
    max_order -= 1

# --------------------------------------------------------------------------
# even part

coeff = np.zeros((max_order//2 + 1, 1))
for i in range(len(coeff)):
    coeff[i] = (-1)**(i) * besselj(2*i, tau)

coeff[0] /= 2
[phi1, out1] = QSP_Solver(coeff, 0, opts)

print("- Info: \t\tQSP phase factors --- solved by L-BFGS\n")
print("- Parity: \t\t%s\n- Degree: \t\t%d\n", "even", max_order)
print("- Iteration times: \t%d\n", out1["iter"])
print("- CPU time: \t%.1f s\n", out1["time"])

#--------------------------------------------------------------------------
# odd part

coeff = np.zeros((max_order/2 + 1, 1))
for i in range(len(coeff)):
    coeff[i] = (-1)**(i) * besselj(2*i + 1, tau)
[phi2,out2] = QSP_Solver(coeff, 1, opts)

#--------------------------------------------------------------------------
# output

print("- Info: \t\tQSP phase factors --- solved by L-BFGS\n")
print("- Parity: \t\t%s\n- Degree: \t\t%d\n", "odd", max_order + 1)
print("- Iteration times: \t%d\n", out2["iter"])
print("- CPU time: \t%.1f s\n", out2["time"])
#--------------------------------------------------------------------------
# plot phase factors

## Won't plot until necessary
