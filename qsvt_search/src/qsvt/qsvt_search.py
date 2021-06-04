from qsvt import *
from qsvt.oracle_unitary import U, reverse_gate
from qsvt.projectors import p_left, p_right

def qsvt_search(target): # target = marked element, is a bit-string!
    
    systemqubits = len(target)
    nqubits = systemqubits + 2
    q = QuantumRegister(nqubits, 'q')
    circuit = QuantumCircuit(q)  

    d = (2*systemqubits) - 1

    if systemqubits > 6 and systemqubits < 10:
        for i in range(1, systemqubits - 6 + 1):
            d += 2 * i
    
    u = U(nqubits-1)
    u_dag = reverse_gate(u)
    
    p_right_range = [nqubits-2, nqubits-1]
    u_range = list(range(0, nqubits-1))
    p_left_range = list(range(0, nqubits))

    circuit.append(p_left(nqubits,(1-d)*pi), p_left_range)
    circuit.append(U(nqubits-1), u_range)

    for i in range((d-1)//2):
        circuit.append(p_right(pi), p_right_range) #debug this, doesnt work just as a 2 qubit gate
        circuit.append(u_dag, u_range)
        circuit.append(p_left(nqubits,pi), p_left_range)
        circuit.append(u, u_range)

    for i in range(len(target)): # The operation for acquiring arbitrary marked element
        bts = target [::-1]      # bitstring is reversed to be compatible with the reverse qubit order in Qiskit
        if bts[i] == '0':
            circuit.x(i)

    circuit.measure_all()
    return circuit