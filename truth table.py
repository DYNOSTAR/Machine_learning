# prompt: an expert system generating a truth table of logical connectors between P and V and, or, negation, implication and equivalence

def generate_truth_table(p_values, v_values):
    """Generates a truth table for logical connectors."""

    # Initialize the truth table as a list of dictionaries.
    truth_table = []

    # Iterate over all possible combinations of P and V values.
    for p in p_values:
        for v in v_values:
            # Calculate the truth values for each logical connector.
            conjunction = p and v
            disjunction = p or v
            negation_p = not p
            negation_v = not v
            implication = (not p) or v  # Equivalently, if p then v
            equivalence = p == v

            # Append a row to the truth table.
            truth_table.append({
                'P': p,
                'V': v,
                'P and V': conjunction,
                'P or V': disjunction,
                'not P': negation_p,
                'not V': negation_v,
                'P implies V': implication,
                'P equivalent to V': equivalence
            })

    return truth_table


def print_truth_table(truth_table):
    """Prints the given truth table in a formatted way"""

    # Print table header
    header_format = "{:<5} {:<5} {:<10} {:<10} {:<10} {:<10} {:<15} {:<20}"
    print(header_format.format("P", "V", "P and V", "P or V", "not P", "not V", "P implies V", "P equivalent to V"))
    print("-" * 80)  # separator line

    # Print rows
    row_format = "{:<5} {:<5} {:<10} {:<10} {:<10} {:<10} {:<15} {:<20}"
    for row in truth_table:
        print(row_format.format(row['P'], row['V'], row['P and V'], row['P or V'], row['not P'], row['not V'],
                                row['P implies V'], row['P equivalent to V']))


# Example usage:
p_values = [True, False]
v_values = [True, False]
table = generate_truth_table(p_values, v_values)
print_truth_table(table)