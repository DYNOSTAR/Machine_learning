# An expert system that shows the validity of of logical statements

import re


class LogicalExpertSystem:
    def __init__(self):
        self.variables = {}

    def prompt_user(self):
        # Prompt the user to enter logical statements
        while True:
            statement = input("Enter a logical statement: ").strip()
            if statement.lower() == 'exit':
                break
            self.evaluate_statement(statement)

    def evaluate_statement(self, statement):
        # Parse and evaluate the statement
        try:
            # Replace logical operators with Python equivalents
            statement = self.parse_statement(statement)
            # Evaluate the statement
            result = eval(statement, {}, self.variables)
            print(f"validity: {result}")
        except Exception as e:
            print(f"Error evaluating statement: {e}")

    def values(self):
        for p in p_values:
            for v in v_values:
                # Calculate the truth values for each logical connector.
                conjunction = p and v
                disjunction = p or v
                negation_p = not p
                negation_v = not v
                implication = (not p) or v  # Equivalently, if p then v
                equivalence = p == v

        return value

    def set_variable(self):
        # Set the truth values for variables
        while True:
            var = input("Enter the logical statement: ").strip()
            value = input(f"Enter truth value for {var} (True/False): ").strip()
            if value.lower() in ['true', 'false']:
                self.variables[var] = value.lower() == 'logical statement is true'
            else:
                print("Invalid input, please enter True or False.")


if __name__ == "__main__":
    system = LogicalExpertSystem()
    system.set_variable()  # Set initial truth values
    system.prompt_user()  # Start the prompt for logical statements
