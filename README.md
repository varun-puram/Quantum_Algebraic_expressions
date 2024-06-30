The Python script provided interprets and converts an IBM OpenQASM code, which is a textual representation of a quantum circuit, into an algebraic expression. This script processes the specified quantum gates on qubits with the possibility of control-target relationships, thereby building and simplifying the corresponding algebraic expression by applying circuit identities representing the operations applied to the qubits over the sequence of gates.

Puram, V., Karuppasamy, K., Thomas, J.P. (2024). Optimizing Quantum Circuits Using Algebraic Expressions. ICCS 2024. Lecture Notes in Computer Science, vol 14837. Springer, Cham.  https://doi.org/10.1007/978-3-031-63778-0_19
<img width="965" alt="image" src="https://github.com/varun-puram/Quantum_Algebraic_expressions/assets/71292221/6fe9af96-1371-4ea4-aaba-af6aab535b23">


## Input

The input to this script is an OpenQASM file named "input.txt", which must be formatted correctly to represent the quantum circuit. OpenQASM is a hardware-agnostic description language used to write quantum circuits. Below is an example of how such a file might look:

```qasm
qreg q[3];
barrier q[0], q[1], q[2];
h q[2];
barrier q[0], q[1], q[2];
cz q[1], q[2];
barrier q[0], q[1], q[2];
h q[2];
barrier q[0], q[1], q[2];
cz q[1], q[0];
cx q[1], q[2];
barrier q[0], q[1], q[2];
```
