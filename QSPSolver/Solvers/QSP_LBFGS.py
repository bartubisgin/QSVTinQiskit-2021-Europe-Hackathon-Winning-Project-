import numpy as np

# Solving phase factors optimization via L-BFGS
#
# Input:
#        obj --- Objective function L(phi) (Should also be given in grad)
#       grad --- Gradient of obj function
#      delta --- Samples
#        phi --- Initial value
#       opts --- Options structure with fields
#              maxiter: max iteration
#              gamma: linesearch retraction rate
#              accrate: linesearch accept ratio
#              minstep: minimal stepsize
#              criteria: stop criteria for obj value on Chevyshev points
#              lmem: L-BFGS memory size
#              print: whether to output
#              itprint: print frequency
#              parity: parity of polynomial (0 -- even, 1 -- odd)
#              target: target polynomial
#
# Output:
#         phi --- Solution of phase factors optimization
#   obj_value --- Objection value at optimal point L(phi^*)
#         out --- Information about solving process
#


def QSP_LBFGS(obj, grad, delta, phi, options) -> (object, object, object):
    if "maxiter" not in options:
        options["maxiter"] = 5e4
    if "gamma" not in options:
        options["gamma"] = 0.5
    if "accrate" not in options:
        options["accrate"] = 1e-3
    if "minstep" not in options:
        options["minstep"] = 1e-5
    if "criteria" not in options:
        options["criteria"] = 1e-12
    if "lmem" not in options:
        options["lmem"] = 200
    if "print" not in options:
        options["print"] = 1
    if "itprint" not in options:
        options["itprint"] = 1

    out = dict()

    # Copy values to parameters
    maxiter = options["maxiter"]
    gamma = options["gamma"]
    accrate = options["accrate"]
    lmem = options["lmem"]
    minstep = options["minstep"]
    pri = options["print"]
    itprint = options["itprint"]
    crit = options["criteria"]

    iter_ = 0
    d = len(phi)
    mem_size = 0
    mem_now = 0
    mem_grad = np.zeros((lmem, d))
    mem_obj = np.zeros((lmem, d))
    mem_dot = np.zeros((lmem, ))
    [grad_s, obj_s] = grad(phi, delta, options)
    obj_value = np.mean(obj_s)
    GRAD = np.mean(grad_s, axis=0)

    # Start L-BFGS
    if (pri):
        print("L-BFGS solver started")

    while(True):
        iter_ += 1
        theta_d = GRAD.copy()
        alpha = np.zeros((mem_size, 1))
        for i in range(mem_size):
            subsc = np.mod(mem_now - i, lmem)
            alpha[i] = mem_dot[i] * (mem_obj[subsc, :] @ theta_d)
            theta_d -= alpha[i] * np.conj(mem_grad[subsc, :])
            # print(i, iter_)

        theta_d *= 0.5
        if (options["parity"] == 0):
            theta_d[0] *= 2
            
            for i in range(mem_size):
                subsc = np.mod(mem_now - (mem_size - i) - 1, lmem)
                beta = mem_dot[subsc] * (mem_grad[subsc, :] @ theta_d)
                theta_d += (alpha[mem_size - i - 1] - beta) * np.conj(mem_obj[subsc, :])
            
        step = 1
        exp_des = np.conj(GRAD) @ theta_d
        
        while(True):
            theta_new = phi - step * theta_d
            obj_snew = obj(theta_new, delta, options)
            obj_valuenew = np.mean(obj_snew)
            ad = obj_value - obj_valuenew
            if (ad > exp_des * accrate * step or step < minstep):
                break
            step *= gamma

        phi = theta_new
        obj_value = obj_valuenew
        obj_max = np.max(obj_snew)
        [grad_s, _] = grad(phi, delta, options)
        GRAD_new = np.mean(grad_s, axis=0)
        mem_size = np.min([lmem, mem_size + 1])
        mem_now = np.mod(mem_now, lmem)
        mem_grad[mem_now, :] = GRAD_new - GRAD
        mem_obj[mem_now, :] = - step * theta_d
        mem_dot[mem_now] = 1/(mem_grad[mem_now, :] @ np.conj(mem_obj[mem_now, :]))
        GRAD = GRAD_new
        if pri and np.mod(iter_, itprint) == 0:
            if (iter_ == 1 or np.mod(iter_ - itprint, itprint * 10) == 0):
                print("str_head")
        
        if iter_ >= maxiter:
            print("Max iteration reached")
            break

        if obj_max < crit ** 2:
            print("Stop criteria satisfied")
            break
    
    out["iter"] = iter_

    return phi, obj_value, out



