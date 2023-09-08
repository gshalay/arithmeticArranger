# Filename: arithmetic_arranger.py
# Description: Function that will take a series of equations and format them in a readable way. Will optionally output the answers.
# Author: Greg Shalay
# Requirements:
# 1. Handle the following error situations:
#   a) If more than 5 problems exist, return "Error: Too many problems"
#   b) Valid operators are addition and subtraction. Invalid operators return "Error: Operator must be '+' or '-'."
#   c) Numbers should only contain digits. Entries that don't return "Error: Numbers must only contain digits."
#   d) Numbers should only be a max of four digits in length. Return "Error: Numbers cannot be more than four digits." if true.
#
# 2. If conditions are met, then the output should be formatted in accordance with these rules:
#   a) A single space between the operator and the longest of the two operands.
#   b) The operator is on the same line as the second operand.
#   c) Operands are written in the same order that they were provided. (first on top, second on bottom).
#   d) Numbers should be right-aligned.
#   e) Four spaces between each problem.
#   f) There should be dashes at the bottom of each problem individually.

import sys

# Define constants
PROBLEM_LIMIT: int = 5
DIGIT_LIMIT: int = 10000
DIGIT_LENGTH_LIMIT: int = 4
OP1_IDX: int = 0
SIGN_IDX: int = 1
OP2_IDX: int = 2

# Line constants
TAB: str = "    "
NEW_LINE: str = "\n"

# Error Messages
ERR_TOO_MANY_PROBLEMS = "Error: Too many problems."
ERR_INVALID_OPERATOR = "Error: Operator must be '+' or '-'."
ERR_NON_DIGITS_PRESENT = "Error: Numbers must only contain digits."
ERR_NUMBER_TOO_LONG = "Error: Numbers cannot be more than four digits."
ERR_NUMBER_OF_TOKENS_MISMATCH = "Error: Expected 3 tokens (two operands and an operator), but got a different amount."
ERR_GENERIC = "Error: An unexpected error occurred."

# Return codes
# Errors - Named using the prefix of ERR_ then the following characters are the first letter in each word of the respective error message variable name.
ERR_IO: int = 1
ERR_NDP: int = 2
ERR_NTL: int = 3
ERR_NOTM: int = 4

# Success
PASS: int = 0


class Equation:
    def __init__(self, operand1, operator, operand2, solution):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
        self.solution = solution


def arithmetic_arranger(problems: list, show_solutions: bool = False):
    if (len(problems) > PROBLEM_LIMIT):
        return ERR_TOO_MANY_PROBLEMS

    equations = []

    # Start by parsing each equation.
    for string_equation in problems:
        ret_val = parse_equation(string_equation)

        if (isinstance(ret_val, Equation)):
            equations.append(ret_val)
        else:
            match str(ret_val):
                case str("1"):
                    return ERR_INVALID_OPERATOR
                case str("2"):
                    return ERR_NON_DIGITS_PRESENT
                case str("3"):
                    return ERR_NUMBER_TOO_LONG
                case str("4"):
                    return ERR_NUMBER_OF_TOKENS_MISMATCH
                case _:
                    return ERR_GENERIC

    return format_equations_string(equations, show_solutions)


def parse_equation(string_equation: str):
    tokens = string_equation.split()

    # Check error case 1c.
    if (not tokens[OP1_IDX].isnumeric() or not tokens[OP2_IDX].isnumeric()):
        return ERR_NDP

    # Check error case 1d
    if (len(tokens[OP1_IDX]) > int(DIGIT_LENGTH_LIMIT) or len(tokens[OP2_IDX]) > int(DIGIT_LENGTH_LIMIT)):
        return ERR_NTL

    # Check error case 1b
    if (tokens[SIGN_IDX] != "+" and tokens[SIGN_IDX] != "-"):
        return ERR_IO

    op1 = int(tokens[OP1_IDX])
    op2 = int(tokens[OP2_IDX])

    return Equation(str(op1), str(tokens[SIGN_IDX]), str(op2), calculate_solution(op1, tokens[SIGN_IDX], op2))


def calculate_solution(op1: int, sign: str, op2: int):
    return (op1 + op2) if (sign == "+") else (op1 - op2)


def format_equations_string(equations: list, show_solutions: bool):
    equations_string = ""

    r = range(1, 5) if (
        show_solutions) else range(1, 4)

    for current_line in r:
        line = ""

        for equation_idx in range(0, len(equations)):
            longest_operand_len = get_longest_operand_len(
                equations[equation_idx])

            match str(current_line):
                case "1":
                    line += equations[equation_idx].operand1.rjust(
                        longest_operand_len + 2)
                case "2":
                    line += equations[equation_idx].operator + " " + equations[equation_idx].operand2.rjust(
                        longest_operand_len)
                case "3":
                    line += "".rjust(longest_operand_len + 2, "-")
                case "4":
                    line += str(equations[equation_idx].solution).rjust(
                        longest_operand_len + 2)
                case _:
                    return ERR_GENERIC

            if (not equation_idx == len(equations) - 1):
                line += TAB
            else:
                line += NEW_LINE

        equations_string += line

    return equations_string


def get_longest_operand_len(eq: Equation):
    return max(len(eq.operand1), len(eq.operand2))


# print(arithmetic_arranger(['3801 - 2', '123 + 49']))
# print()
# print(arithmetic_arranger(['1 + 2', '1 - 9380']))
# print()
# print(arithmetic_arranger(['3 + 855', '3801 - 2', '45 + 43', '123 + 49']))
# print()
# print(arithmetic_arranger(['11 + 4', '3801 - 2999', '1 + 2', '123 + 49', '1 - 9380']))
# print()
# print(arithmetic_arranger(['44 + 815', '909 - 2', '45 + 43', '123 + 49', '888 + 40', '653 + 87']))
# print()
# print(arithmetic_arranger(['3 / 855', '3801 - 2', '45 + 43', '123 + 49']))
# print()
print(arithmetic_arranger(['24 + 85215', '3801 - 2', '45 + 43', '123 + 49']))
# print()
# print(arithmetic_arranger(['98 + 3g5', '3801 - 2', '45 + 43', '123 + 49']))
# print()
# print(arithmetic_arranger(['3 + 855', '988 + 40'], True))
# print()
# print(arithmetic_arranger(['32 - 698', '1 - 3801', '45 + 43', '123 + 49', '988 + 40'], True))
