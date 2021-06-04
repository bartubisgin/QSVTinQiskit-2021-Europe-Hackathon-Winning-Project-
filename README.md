# Quantum Singular Value Transformation (QSVT) in Qiskit (2021 Qiskit Europe Hackathon)

Quantum Singular Value Transformation (QSVT) is a relatively new and promising framework for gate-based quantum computation, which allows for efficientcircuit representations of a large class of polynomial transformations, including non-unitary operations. This significantly expands the potential range of NISQ-era applications and quantum algorithms in general. QSVT also serves as a unification scheme for many quantum algorithms by showing that they can all be expressed in terms of the same circuit structure. The simple universal circuit structure that realizes the polynomial transformations generally uses only a constant number of ancilla qubits, regardless of the size of the input. Given the previous works on Quantum Signal Processing (QSP), it also has the potential to result in novel algorithms

One of the most important challenges in the broad field of Quantum Information is implementing non-unitary operations and finding useful NISQ-era applications that offer some valuable speed-up or make otherwise intractable problems solvable. The QSVT effort is an emerging and potentially-groundbreaking development towards these NISQ-applicability as it also allows one to fundamentally re-cast any complex circuitry as the iteration of a single, simple circuit structure that can also construct arbitrary non-unitary operations.


In this project, we aimed to create a QSVT mopdule for Qiskit and develop a useful library dedicated to the general QSVT framework where different algorithms can be expressed as the manifestation of a single fundamental idea with the corresponding encoding and polynomial transformation. 

With search implemented, we hope that we have begun to bridge the gap between academia and the Qiskit community for QSVT.


# Quantum Search with QSVT

In current form, the repository contains QSVT-implemented Search utilizing Fixed-point Amplitude Amplification. This search works fundamentally different from the original Grover's Search. It transforms the value of the inner product of the initial and the target states from whatever value it is, to the value of 1, meaning complete overlap! The qsvt_search function can find any marked state up to 9 qubit space very efficiently as of now, and can also demonstrate arbitrary transformations.

All the details about QSVT-search can be found in the documentation. We have tried our best to prepare a very detailed and informative documentation to make all this much more intuitive. We hope it helps!

# Algorithms That Are Confirmed to be QSVT-expressable

* Quantum Search
* Hamiltonian Simulation and Quantum Walks
* Something similar to 'Shor's Algorithm' (Kitaev's Factoring Algorithm)
* Matrix Inversion / HHL (for solving linear systems of equations)
* Several QML applications

# Short-term Goals (ACHIEVED)

Implement Fixed-point Amplitude Amplification (FPAA) with QSVT in Qiskit. FPAA uses the whole Bloch sphere for answers instead of the mere 2D plane by Grover's and can be used for efficient search, state preparation and/or as a sub-routine to other algorithms. Create functions that are readily-callable for FPAA and can be compared to 2 and 3 qubit cases with original Grover's. This requires delicate documentation on inner workings, implementation and efficiency, preparing of which is also a part of short-term goals.

# Long-term Goals

We want to keep implementing different algorithms in the QSVT framework and add them to this initial module to create a rich QSVT library for Qiskit, making QSVT more accesible to the community, bridging the gap between cutting-edge research and developers. We hope to contribute to research on QSVT and the development of novel algorithms through this work.

# Team
| Bartu Bisgin  | Jiri Guth Jarkovsky | Martin Mauser | Nagme Oruz | Erfan Abedi | 
| ------------- | ------------- | ------------- | ------------- | ------------- |


# References

- [A. Gilyén, Y. Su, G. H. Low, and N. Wiebe. Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics. In Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing, pages 193–204, 2019](https://dl.acm.org/doi/10.1145/3313276.3316366)

- [Isaac Chuang: Grand Unification of Quantum Algorithms](https://www.youtube.com/watch?v=GFRojXdrVXI&t=2002s)

- [Low, G. H., Yoder, T. J. & Chuang, I. L. The methodology of resonant equiangular composite quantum gates. Phys. Rev. X 6, 041067 (2016)](http://arxiv.org/abs/1603.03996)

- [T. J. Yoder, G. H. Low, I. L. Chuang, Fixed-point quantum search with an optimal number of queries. 10.1103/PhysRevLett.113.210501](https://arxiv.org/pdf/1409.3305.pdf)

- [Y. Dong, X. Meng, K. B. Whaley, and L. Lin. Efficient Phase Factor Evaluation in Quantum Signal Processing. arXiv: 2002.11649](https://arxiv.org/abs/2002.11649)

- [Low, G. H. & Chuang, I. L. Optimal Hamiltonian Simulation by Quantum Signal Processing. Phys. Rev. Lett. 118, 010501 (2017)](http://arxiv.org/abs/1606.02685)

- [Harrow, A. W., Hassidim, A. & Lloyd, S. Quantum algorithm for solving linear systems of equations. Phys. Rev. Lett. 103, 150502 (2009)](http://arxiv.org/abs/0811.3171)

- https://github.com/qsppack
