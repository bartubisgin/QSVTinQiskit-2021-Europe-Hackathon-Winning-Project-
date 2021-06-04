import numpy as np

# Evaluate function based on Chebyshev expansion coefficients
#
# ----------------------------------------------------------------------
#
# Input:
#       x, coef
#       parity  -- 0 for even, 1 for odd
#  partialcoef  -- true: only include even/odd coefficiennts
# Output:
#       wult     -- function at x

def ChebyCoef2Func(x, coeff, parity, partialcoeff):
    try:
        result = np.zeros((len(x), 1))
    except TypeError:
        result = np.zeros((1, 1))
    y = np.arccos(x)
    len_coeff = len(coeff)
    if partialcoeff:
        if parity == 0:
            for k in range(len_coeff):
                result += coeff[k] * np.cos(2*k*y)
        else:
            for k in range(len_coeff):
                result += coeff[k] * np.cos((2 * (k+1) - 1) * y)
    else:
        if parity == 0:
            for k in range(0, len_coeff, 2):
                result += coeff[k] * cos(k * y)
        else:
            for k in range(1, len_coeff, 2):
                result += coeff[k] * cos(k * y)
    return result