The Python script provided interprets and converts an IBM OpenQASM code, which is a textual representation of a quantum circuit, into an algebraic expression. This script processes the specified quantum gates on qubits with the possibility of control-target relationships, thereby building and simplifying the corresponding algebraic expression by applying circuit identities representing the operations applied to the qubits over the sequence of gates.

The script follows the algorithm specified in the paper "Optimizing Quantum Circuits using Algebraic Expressions" by Johnson P Thomas, Varun Puram, and Krishnageetha Karuppasamy.

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
