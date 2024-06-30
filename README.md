The Python script interprets IBM OpenQASM code—a textual format for describing quantum circuits. It processes the script to identify and organize information about quantum gates, including control-target relationships, into structured data. This structured data captures the sequence and conditions of operations performed on the qubits.

The script functions by reading through the OpenQASM code line-by-line, distinguishing between different types of operations such as control gates (c prefix), regular gates, and barrier commands that indicate segmentation of the circuit for modular processing. Each gate operation and its associated qubits are stored in dictionaries, enabling the script to map out the entire circuit in a format suitable for further computational analysis.

Puram, V., Karuppasamy, K., Thomas, J.P. (2024). Optimizing Quantum Circuits Using Algebraic Expressions. ICCS 2024. Lecture Notes in Computer Science, vol 14837. Springer, Cham.  https://doi.org/10.1007/978-3-031-63778-0_19



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
