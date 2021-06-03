# QSVT in Qiskit
Quantum algorithms re-imagined as the iteration of a single 'simple' circuit through Quantum Singular Value Transformation that can implement vast class of non-unitaries, implemented in Qiskit.

# Grand Unification and Efficient Implementation of Non-Unitaries
Quantum Singular Value Transformation is a promising new framework that allows one to apply an arbitrary polynomial transformation (bound by some constraints) to the singular values of a block-encoded unitary transformation, a method first coherently introduced by Gilyen et. al in a 2018 paper. This work is subsequent to work on Quantum Signal Processing. Later, about 4 months ago, Prof. Isaac Chuang has given an overview of Gilyen's ideas, and how QSVT serves as a unification schemes for many quantum algorithms as something more fundamental. Even more recently, Seth Lloyd and colleagues published a preprint on 'Hamiltonian Singular Value Transformation and Inverse Block Encoding' for NISQ-era devices.

One of the most important challenges in the broad field of Quantum Information is implementing non-unitary operations and finding useful NISQ-era applications that offer some valuable speed-up or are simply intractable. The QSVT effort is an emerging and potentially-impactful development towards these NISQ-applicability as it allows one to fundamentally re-cast any complex circuitry as the iteration of a single, simple circuit structure that can also construct arbitrary non-unitary operations.

QSVT also hints at novel algorithms via. the tune-able parameters, that are the Quantum Signal Processing phases. As each different set of phases corresponds to a different transformation, exploring this space is invaluable.

In this project, the aim is to apply QSVT hands-on in Qiskit and develop a useful library dedicated to general QSVT framework where different algorithms can be expressed as the manifestation of a single fundamental idea with the corresponding encoding and polynomial transformation.

# General Overview of How QSVT works

Say you have an object (operator/scalar value/matrix-representation etc.) of interest in your algorithm that you want to apply a particular transformation to;

1-Block encode this object of interest into the upper-left corner of a a well-behaving Unitary (ex. block encode the Hamiltonian (non-unitary) into a Unitary)

2-Figure out what transformation you want to apply to this object, and what function corresponds to this transformation (ex. we want cos(Ht) and sin(Ht) for simulation, so the functions of interest are cos(x) and sin(x)). This function needs to satisfy some constraints, most important ones being, its absolute value should be bounded by 1 in [-1,1] and should be smooth.

3-Find the Chebyshev expansion of this function, and store the coefficients (this can be done via. FFT or Remez-Exchange algorithm)

4-Using these coefficients, solve for the Quantum Signal Processing phases.

5-Build a simple circuit that uses a fixed number of ancilla qubits, and just has the Unitary, a rotation around the Z-axis with the found phases, and an ancilla Controlled-projector as elements.

6-Build another simple circuit with the same elements, just a little tweaking. Take hermitian conjugate of the Unitary and the projector (ie. due to its Unitary nature, its inverse).

7-Add these circuits end to end as many times needed with different values for the found phases (so add the circuit block to the end with something similar of a for statement with different phase values).

8-Obtain the unitary embedding of the arbitrary transformation you desired.

9-Extract results!

For example, given a Hamiltonian, and given that you can block-encode it properly in the first step; you can EXACTLY extract cos(Ht)-isin(Ht) to build your time-evolution operator exp(-iHt) EXACTLY, without having to deal with any approximations! THIS IS AMAZING!

Notice how this framework is independent of the type of algorithm we want to use! This is remarkable for NISQ-era devices because now we don't need to construct different types of sub-routines for all kinds of different algorithms. We can simply create this circuit, and given that we can properly block-encode our desired operator and that we can obtain the phases by some routine, we can implement different algorithms from across the board with the same circuit architecture! It should be noted that the depth of the circuit depends on the degree of the polynomial expansion, however, the circuit itself being simple, somehow compensates for this. Further work is being done on this topic.

# Algorithms That Are Confirmed to be QSVT-expressable

* Quantum Search

* Hamiltonian Simulation and Quantum Walks

* Something similar to 'Shor's Algorithm'

* Matrix Inversion / HHL (for solving linear systems of equations)

* Several QML applications

# Short-term Goals

Implement Fixed-point Amplitude Amplification (FPAA) with QSVT in Qiskit. FPAA uses the whole Bloch sphere for answers instead of the mere 2D plane by Grover's and can be used for efficient search, state preparation and/or as a sub-routine to other algorithms. Create functions that are readily-callable for FPAA and can be compared to 2 and 3 qubit cases with original Grover's. This requires delicate documentation on inner workings, implementation and efficiency, preparing of which is also a part of short-term goals.

# Long-term Goals

We want to keep implementing different algorithms in the QSVT framework and add them to this initial module to create a rich QSVT library for Qiskit, making QSVT more accesible to the community, bridging the gap between cutting-edge research and developers. We hope to contribute to research on QSVT and the development of novel algorithms through this work.

# References

- [A. Gilyén, Y. Su, G. H. Low, and N. Wiebe. Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics. In Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing, pages 193–204, 2019](https://dl.acm.org/doi/10.1145/3313276.3316366)

- [Isaac Chuang: Grand Unification of Quantum Algorithms](https://www.youtube.com/watch?v=GFRojXdrVXI&t=2002s)

- [T. J. Yoder, G. H. Low, I. L. Chuang, Fixed-point quantum search with an optimal number of queries. 10.1103/PhysRevLett.113.210501](https://arxiv.org/pdf/1409.3305.pdf)

- [Y. Dong, X. Meng, K. B. Whaley, and L. Lin. Efficient Phase Factor Evaluation in Quantum Signal Processing. arXiv: 2002.11649](https://arxiv.org/abs/2002.11649)

- https://github.com/qsppack
