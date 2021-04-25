# QSVT in Qiskit
Quantum algorithms re-imagined as the iteration of a 'simple' circuit through Quantum Singular Value Transformation and implemented in Qiskit.

# Demonstrating the Grand Unification of Quantum Algorithms and Making Them More NISQ-friendly
Quantum Singular Value Transformation is a promising new framework that allows one to apply an arbitrary polynomial transformation (bound by some constraints) to the singular values of a block-encoded unitary transformation, a method first coherently introduced by Gilyen et. al in a 2018 paper. This work is subsequent to work on Quantum Signal Processing. Later, about 4 months ago, Prof. Isaac Chuang has given an overview of Gilyen's ideas, and how QSVT serves as a unification schemes for many quantum algorithms as something more fundamental. Even more recently, last week, Seth Lloyd and colleagues published a preprint on 'Hamiltonian Singular Value Transformation and Inverse Block Encoding' for NISQ-era devices.

One of the most important challenges in the broad field of Quantum Information is finding useful, NISQ-era applications that offer some valuable speed-up to their classical counterparts, which can be employed in academic research and industry today. The QSVT effort is an emerging and potentially-impactful development towards these NISQ-applicability as it allows one to fundamentally re-cast any complex circuitry as the iteration of a single, simple circuit structure that can also construct arbitrary non-unitary operations.

In this project, the aim is to apply QSVT hands-on in Qiskit and develop a useful libarary dedicated to general QSVT framework where different algorithms can be expressed as the manifestation of a single fundamental idea with the corresponding encoding and polynomial transformation.

# General Overview of How QSVT works

Say you have an object (operator/scalar value/matrix-representation etc.) of interest in your algorithm that you want to apply a particular transformation to;

1-Block encode this object of interest into the upper-left corner of a a well-behaving Unitary (ex. block encode the Hamiltonian (non-unitary) into a Unitary)

2-Figure out what transformation you want to apply to this object, and what function corresponds to this transformation (ex. we want cos(Ht) and sin(Ht) for simulation, so the functions of interest are cos(x) and sin(x)). This function needs to satisfy some constraints, most important ones being, its absolute value should be bounded by 1 in [-1,1] and should be smooth.

3-Find the Chebyshev expansion of this function, and store the coefficients (this can be done via. FFT or Remez-Exchange algorithm)

4-Using these coefficients, solve for the Quantum Signal Processing phases.

5-Build a simple circuit that uses a fixed number of ancilla qubits, and just has the Unitary, a rotation around the Z-axis with the found phases, and an ancilla Controlled-projector as elements.

6-Build another simple circuit with the same elements, just a little tweaking. Take hermitian conjugate of the Unitary and the projector (ie. due to its Unitary nature, its inverse).

7-Add these circuits end to end as many times needed with different values for the found phases (so add the circuit block to the end with something similar of a for statement with different phase values).

8-Obtain the unitary embedding of the transformation you desired.

9-Extract results!

For example, given a Hamiltonian, and given that you can block-encode it properly in the first step; you can EXACTLY extract cos(Ht)-isin(Ht) to build your time-evolution operator exp(-iHt) EXACTLY, without having to deal with any approximations! THIS IS AMAZING!

Notice how this framework is independent of the type of algorithm we want to use! This is remarkable for NISQ-era devices because now we don't need to construct different types of sub-routines for all kinds of different algorithms. We can simply create this circuit, and given that we can properly block-encode our desired operator and that we can obtain the phases by some routine, we can implement different algorithms from across the board with the same circuit architecture! It should be noted that the depth of the circuit depends on the degree of the polynomial expansion, however, the circuit itself being simple, somehow compensates for this. Further work is being done on this topic.

# Algorithms That Are Confirmed to be QSVT-expressable

Amplitude Amplification

Hamiltonian Simulation and Quantum Walks

Something similar to 'Shor's Algorithm'

HHL (for solving linear systems of equations)

Several QML algorithms

# Short-term Goals

Implement FPAA with QSVT in Qiskit and prepare a user-friendly library/repository Qiskit users.

# Long-term Goals

Keep implementing different algorithms in the repository to create a rich QSVT library for Qiskit, demonstrating the unification of different quantum algorithms and potentially creating more NISQ-era friendly forms.
