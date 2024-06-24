from itertools import product

num_qubits = None
control_target_pairs = [{} for _ in range(1000)]
target_operations = [{} for _ in range(1000)]
not_control = [False]*100
gate = [{} for _ in range(100)]
count = -1
i = -1
flag = False
first = False
with open("input.txt", "r") as file:
    for line in file:
        tokens = line.strip().split()
        # print("t",tokens)
        if line.startswith("qreg"):
            flag = False
            num_qubits = int(tokens[1][2:-2])
            # print(num_qubits)
        elif line.startswith("c"):
            flag = False
            first = True
            control_qubit = int(tokens[1][2:-2])
            target_qubit = int(tokens[2][2:-2])  # Extract the last integer as the key
            if control_qubit not in control_target_pairs[i]:
                control_target_pairs[i][control_qubit] = []
            control_target_pairs[i][control_qubit].append(target_qubit)
            # print("CTP", control_target_pairs)
            target_operation = tokens[0][1:]  # Extract the next character as the value
            target_operations[i][target_qubit] = target_operation
        elif line.startswith("id"):
            flag = False
            first = True
            continue
        elif line.startswith("barrier"):
            if not flag:
                count+=1
                i+=1
                flag = True
        else:
            flag = False
            first = True
            not_control[i] = True
            gate_qubit = int(tokens[1][2:-2])
            gate[i][tokens[0]] = gate_qubit
            # print("gq", gate_qubit, gate)


if flag == True:
    count-=1
    i-=1
        
control_target_pairs = control_target_pairs[:count + 1]
target_operations = target_operations[:count + 1]
gate = gate[:count + 1]
# Assuming control_target_pairs is your list of dictionaries



for i in range(len(control_target_pairs)):
    # Sort each dictionary by keys in reverse order
    control_target_pairs[i] = {k: control_target_pairs[i][k] for k in sorted(control_target_pairs[i], reverse=True)}


# Function to determine if a qubit is a control qubit for any target
def is_control_for_any(qubit, control_target_pairs):
    for targets in control_target_pairs.values():
        if qubit in targets:
            return True
    return False

binary_states = [[]]*100
# Generate binary states for the control qubits
for i in range(len(control_target_pairs)):
    # print(len(control_target_pairs))
    binary_states[i] = list(product([0, 1], repeat=len(control_target_pairs[i])))
# binary_states = [(1, 0)]


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
for i in range(count+1):
    ex = ex + '('
    algebraic_expression = ' + '.join(create_term(state, control_target_pairs[i], target_operations[i], not_control[i], gate[i]) for state in binary_states[i])
    ex = ex + algebraic_expression
    ex = ex + ')'
print(ex)
