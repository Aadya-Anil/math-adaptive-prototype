# src/puzzle_generator.py

import random

def generate_puzzle(level):
    """
    Returns (expression_string, correct_answer)
    Difficulty grows mainly by expression complexity.
    """

    if level == 0:
        # Easy: one operation
        a, b = random.randint(1, 9), random.randint(1, 9)
        op = random.choice(["+", "-"])
        if op == "-" and b > a:
            a, b = b, a
        expr = f"{a} {op} {b}"

    elif level == 1:
        # Medium: + or - with 2 steps
        a, b, c = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        expr = f"{a} + {b} - {c}"

    elif level == 2:
        # Hard: includes multiplication
        a, b, c = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        expr = f"{a} * {b} + {c}"

    else:
        # Level 3: two small expressions combined
        a, b = random.randint(1, 9), random.randint(1, 9)
        c, d = random.randint(1, 9), random.randint(1, 9)
        expr = f"({a} + {b}) * ({c} - 1)"

    ans = eval(expr)
    return expr, ans
