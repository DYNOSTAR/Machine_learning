# prompt: expert system that shows the validity of logical statements

import re

def is_valid_logical_statement(statement):

    # Basic checks for common logical operators and symbols
    pattern = r"^(?:[a-zA-Z]+(?:\s*[=><]\s*[a-zA-Z0-9]+|\s*(?:and|or|not|implies)\s*[a-zA-Z]+)+)$"

    if re.match(pattern, statement):
      return True
    else:
      return False


# Example Usage
statements = [
    "p and q",
    "p or q",
    "not p",
    "p implies q",
    "p = q",
    "p and q or r",

]


for statement in statements:
    validity = is_valid_logical_statement(statement)
    print(f"'{statement}' is valid: {validity}")