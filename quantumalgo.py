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

def multiply_segments(segment1, segment2):
    """
    Multiplies two segments of the form 'ABC' where each letter represents a term.
    Multiplication here is simply concatenation in this specific context.
    """
    return ' '.join([s1 + s2 for s1, s2 in zip(segment1.split(), segment2.split())])

def apply_distributive_law(expression):
    """
    Applies the distributive law to an expression that includes addition within brackets.
    Assumes the expression is in the specific form given.
    """
    # Split the expression into its components
    parts = expression.split(')(')
    
    
    # Remove the enclosing brackets for easier manipulation
    parts = [part.strip('()') for part in parts]
    print("parts", parts)
    
    # Apply distributive law specifically for the given structure
    left_segment = parts[0].split(' + ')
    right_segments = parts[1].split(' + ')
    
    # Multiply left_segment with each part of right_segments
    distributed_parts = []
    for left_term in left_segment:
        for right_term in right_segments:
            distributed_parts.append(multiply_segments(left_term, right_term))
    print("dist", distributed_parts)
    distributed_parts = simplify_expressions(distributed_parts)
    distributed_parts = [element for element in distributed_parts if '0' not in element.split() and '-0' not in element.split()]
    print("sim", distributed_parts)
    
    # Reconstruct the distributed expression
    distributed_expression = '(' + ' + '.join(distributed_parts) + ')'
    
    # Append the remaining parts of the original expression if there are any
    if len(parts) > 2:
        distributed_expression += '(' + ')('.join(parts[2:]) + ')'
    
    return distributed_expression

def apply_rules(expression, rules):
    """Apply predefined rules to the expression."""
    for rule, identity in rules.items():
        expression = expression.replace(rule, identity)
    return expression

def simplify_identity(expression):
    """Simplify expressions involving the identity element 'I'."""
    simplified_parts = []
    for part in expression.split():
        # Simplify 'I' with other characters, but ensure 'I.I' remains 'I'
        if len(part) > 1:
            part = part.replace('I', '')
        # Append the simplified or original part
        simplified_parts.append(part if part else 'I')
    return ' '.join(simplified_parts)

def simplify_expressions(expressions):
    """Simplify each expression in the array based on defined rules."""
    # Define rules, including handling for 'I' as an identity element
    rules = {
        "X.X": "I", "Y.Y": "I", "Z.Z": "I", "H.H": "I", "T.T": "S",
        "H.Z": "XH", "Z.H": "HX", "D0.Z": "D0", "D1.Z": "-D1",
        "D0.D1": "0", "D0+D1": "I", "H.Z.H": "X", "D0.D0": "D0", "D1.D1": "D1", "D1.D0": "0", "H.X.Z": "X",
        "I.I": "I", "I.X": "X", "X.I": "X", "XH.XH": "I",
    }

    # Adjust the rules for format (removing dots)
    corrected_rules = {rule.replace('.', ''): identity for rule, identity in rules.items()}

    # Apply rules and simplify identity for each expression
    simplified = [simplify_identity(apply_rules(expr, corrected_rules)) for expr in expressions]
    return simplified

# Construct the algebraic expression for the quantum circuit slice
ex = ''
for i in range(count+1):
    ex = ex + '('
    algebraic_expression = ' + '.join(create_term(state, control_target_pairs[i], target_operations[i], not_control[i], gate[i]) for state in binary_states[i])
    ex = ex + algebraic_expression
    ex = ex + ')'
print("converted",ex)

terms = ex.split(')(')

# Adjusting for the first and last terms which may not be split correctly due to the absence of surrounding brackets
if terms[0].startswith('('):
    terms[0] = terms[0][1:]
if terms[-1].endswith(')'):
    terms[-1] = terms[-1][:-1]

# Counting the number of terms
number_of_terms = len(terms)

expression = ex.upper()

while(number_of_terms >1):
    expression = apply_distributive_law(expression)
    print("After applying distributive law:", expression)
    terms = expression.split(')(')

    # Adjusting for the first and last terms which may not be split correctly due to the absence of surrounding brackets
    if terms[0].startswith('('):
        terms[0] = terms[0][1:]
    if terms[-1].endswith(')'):
        terms[-1] = terms[-1][:-1]

    # Counting the number of terms
    number_of_terms = len(terms)

expression = expression.replace(" + -", " - ")
print("final simplified version:", expression)
