# Quantum Singular Value Transformation (QSVT) in Qiskit (2021 Qiskit Europe Hackathon)

QSVT is a relatively new framework that allows one to apply arbitrary polynomial transformations to the singular values of a block-encoded matrix, a method first coherently introduced by Gilyen et. al in a 2018 paper. This work is subsequent to work on Quantum Signal Processing. About a year later, Prof. Isaac Chuang has given an overview of Gilyen's ideas, and has clearly shown how QSVT serves as a unification scheme for many quantum algorithms. Recently, Seth Lloyd and colleagues published a preprint on 'Hamiltonian Singular Value Transformation and Inverse Block Encoding' for NISQ-era devices.

One of the most important challenges in the broad field of Quantum Information is implementing non-unitary operations and finding useful NISQ-era applications that offer some valuable speed-up or make otherwise intractable problems solvable. The QSVT effort is an emerging and potentially-groundbreaking development towards these NISQ-applicability as it also allows one to fundamentally re-cast any complex circuitry as the iteration of a single, simple circuit structure that can also construct arbitrary non-unitary operations.

QSVT also hints at novel algorithms via. the so-called Quantum Signal Processing phases. Each different set of phases corresponds to a different transformation. Hence, exploring this space is invaluable.

In this project, we aim to create a QSVT mopdule for Qiskit and develop a useful library dedicated to the general QSVT framework where different algorithms can be expressed as the manifestation of a single fundamental idea with the corresponding encoding and polynomial transformation.

# General Overview of How QSVT works

Say you have an object (operator/scalar value/matrix-representation etc.) of interest in your algorithm that you want to apply a particular transformation to;

1-Block encode this object of interest into the upper-left corner of a a well-behaving Unitary (ex. block encode the Hamiltonian (non-unitary) into a Unitary)

2-Figure out what transformation you want to apply to this object, and what function corresponds to this transformation (ex. we want cos(Ht) and sin(Ht) for simulation, so the functions of interest are cos(x) and sin(x)). This function needs to satisfy some constraints, most important ones being, its absolute value should be bounded by 1 in [-1,1] and should be smooth.

3-Find the Chebyshev expansion of this function, and store the coefficients (this can be done via. FFT or Remez-Exchange algorithm)

4-Using these coefficients, solve for the Quantum Signal Processing phases (can be efficiently done by the QSP_solver by Dong et al, which we have translated from Matlab to Python for use in Qiskit).

5-Build a simple circuit that uses a fixed number of ancilla qubits, the Unitary, rotations around the Z-axis with the found phases, and an 'projector-controlled NOTs' as elements.

6-Obtain the unitary embedding of the arbitrary transformation you desired.

7-Extract results!

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

# Team
| Bartu Bisgin  | Jiri Guth Jarkovsky | Martin Mauser | Nagme Oruz | Erfan Abedi | 
| ------------- | ------------- | ------------- | ------------- | ------------- |
| (Circuit Design / Algorithm) | (Circuit Design / Algorithm) | (Testing) | (Testing) | (Software Development) |

# References

- [A. Gilyén, Y. Su, G. H. Low, and N. Wiebe. Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics. In Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing, pages 193–204, 2019](https://dl.acm.org/doi/10.1145/3313276.3316366)

- [Isaac Chuang: Grand Unification of Quantum Algorithms](https://www.youtube.com/watch?v=GFRojXdrVXI&t=2002s)

- [Low, G. H., Yoder, T. J. & Chuang, I. L. The methodology of resonant equiangular composite quantum gates. Phys. Rev. X 6, 041067 (2016)](http://arxiv.org/abs/1603.03996)

- [T. J. Yoder, G. H. Low, I. L. Chuang, Fixed-point quantum search with an optimal number of queries. 10.1103/PhysRevLett.113.210501](https://arxiv.org/pdf/1409.3305.pdf)

- [Y. Dong, X. Meng, K. B. Whaley, and L. Lin. Efficient Phase Factor Evaluation in Quantum Signal Processing. arXiv: 2002.11649](https://arxiv.org/abs/2002.11649)

- [Low, G. H. & Chuang, I. L. Optimal Hamiltonian Simulation by Quantum Signal Processing. Phys. Rev. Lett. 118, 010501 (2017)](http://arxiv.org/abs/1606.02685)

- [Harrow, A. W., Hassidim, A. & Lloyd, S. Quantum algorithm for solving linear systems of equations. Phys. Rev. Lett. 103, 150502 (2009)](http://arxiv.org/abs/0811.3171)

- https://github.com/qsppack
