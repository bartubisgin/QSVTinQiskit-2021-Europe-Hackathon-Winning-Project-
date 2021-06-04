#Define Oracle and the reverse-gate for
#constructing dagger later

from qsvt import *

def U(q): 
    qc = QuantumCircuit(q)
    n = q + 1
    
    for qubit in range(n-2):
        qc.h(qubit)
    
    qc.mcx(list(range(0,n-2)), n-2)
    
    U_gate = qc.to_gate()
    U_gate.name = "U"
    return U_gate

def reverse_gate(gate):
    gate_rev = gate.reverse_ops()
    gate_rev.name = gate.name + "$^†$"
    return gate_rev