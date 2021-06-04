# Define projectors.
# Note that p_left is actually p_right from above because the order
# of operations are reversed when equations are turned into circuits
# due to how time-flow is defined in circuit structures

# In the Qiskit implementation qubit indexes start from 0
# and the most significant qubit is the highest index
# keeping this in mind e.g for 4 nqubits = {q0,q1,q2,q3}
# q0 and q1 are the system qubits
# q2 is the signal qubit
# q3 is the ancillary rotation qubit
# nqubits-1 = 4-1 = 3 below, then corresponds to q3

def p_left(q, phi): #right projector
    qc = QuantumCircuit(q)
    n = q
    ctrl_range = list(range(0,n-1))
    
    for qubit in range(n-1): # Implement a simple multi 0-controlled
        qc.x(qubit)
    qc.mcx(ctrl_range , n-1) # 0-Controlled on all but the last qubits, acts on the last qubit
    for qubit in range(n-1):
        qc.x(qubit)
        
    
    qc.rz(phi, n-1) # RZ(phi) on the last qubit
    
    
    for qubit in range(n-1): # Reverse the effect of the first multi-control
        qc.x(qubit)
    qc.mcx(ctrl_range ,n-1) 
    for qubit in range(n-1):
        qc.x(qubit)
    
    p_left_gate = qc.to_gate() # Compiles all this into a gate
    p_left_gate.name = "P$_l$(Φ)"
    return p_left_gate

def p_right(phi): # Left projector acts just on the signal and the ancillary qubit
    qc = QuantumCircuit(2)
    
    qc.cx(0, 1)
    qc.rz(phi, 1)
    qc.cx(0 ,1)
    
    p_right_gate = qc.to_gate()
    p_right_gate.name = "P$_r$(Φ)"
    return p_right_gate