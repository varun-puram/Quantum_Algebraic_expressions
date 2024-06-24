from itertools import product

num_qubits = None
control_target_pairs = {}
target_operations = {}
not_control = False
gate = {}
with open("input.txt", "r") as file:
    for line in file:
        tokens = line.strip().split()
        if line.startswith("qreg"):
            num_qubits = int(tokens[1][2:-2])
        elif line.startswith("c"):
            control_qubit = int(tokens[1][2:-2])
            target_qubit = int(tokens[2][2:-2])  # Extract the last integer as the key
            if control_qubit not in control_target_pairs:
                control_target_pairs[control_qubit] = []
            control_target_pairs[control_qubit].append(target_qubit)
            target_operation = tokens[0][1:]  # Extract the next character as the value
            target_operations[target_qubit] = target_operation
        else:
            not_control = True
            gate_qubit = int(tokens[1][2:-2])
            gate[tokens[0]] = gate_qubit
sorted_control_target_pairs = {k: control_target_pairs[k] for k in sorted(control_target_pairs, reverse=True)}

control_target_pairs = dict(sorted_control_target_pairs)

# Function to determine if a qubit is a control qubit for any target
def is_control_for_any(qubit, control_target_pairs):
    for targets in control_target_pairs.values():
        if qubit in targets:
            return True
    return False

# Generate binary states for the control qubits
binary_states = list(product([0, 1], repeat=len(control_target_pairs)))
# binary_states = [(1, 0)]

# Create the term based on the control qubits' state
def rev_create_term(state, control_target_pairs, target_operations):
    term = ['I'] * num_qubits  # Start with identity for all qubits

    for control_state, (control_qubit, targets) in zip(state, control_target_pairs.items()):
        if control_state == 1:  # Control qubit is active
            # Apply the target operation
            for target in targets:
                term[(num_qubits-1) - (target)%(num_qubits)] = target_operations[target]
            # Mark the control qubit as active
            term[(num_qubits-1) - (control_qubit)%(num_qubits)] = 'D1'
        else:
            # Control qubit is inactive
            # Ensure that target operations are set to identity unless they are also a control qubit
            for target in targets:
                if not is_control_for_any(target, control_target_pairs):
                    term[(num_qubits-1) - (target)%(num_qubits)] = 'I'
            # Mark the control qubit as inactive
            term[(num_qubits-1) - (control_qubit)%(num_qubits)] = 'D0'

    return '  '.join(term)

def create_term(state, control_target_pairs, target_operations, not_control, gate):

    term = ['I'] * num_qubits  # Start with identity for all qubits

    if not_control:
        for gates in gate.keys():
            term [gate[gates]] = gates

    for control_state, (control_qubit, targets) in zip(state, control_target_pairs.items()):
        if control_state == 1:  # Control qubit is active
            # Apply the target operation
            for target in targets:
                term[target] = target_operations[target]
            # Mark the control qubit as active
            term[control_qubit] = 'D1'
        else:
            # Control qubit is inactive
            # Ensure that target operations are set to identity unless they are also a control qubit
            for target in targets:
                if not is_control_for_any(target, control_target_pairs):
                    term[target] = 'I'
            # Mark the control qubit as inactive
            term[control_qubit] = 'D0'

    return '  '.join(term)

# Construct the algebraic expression for the quantum circuit slice
ex = ''
ex = '('
algebraic_expression = ' + '.join(create_term(state, control_target_pairs, target_operations, not_control, gate) for state in binary_states)
ex = ex + algebraic_expression
ex = ex + ')'
print(ex)
