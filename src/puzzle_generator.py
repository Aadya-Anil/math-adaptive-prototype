import random

def generate_simple_term():
    """
    A simple 1-operation expression: a + b, a - b, or a * b.
    Difficulty suitable for kids (no negative subtraction).
    """
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    op = random.choice(["+", "-", "*"])

    # avoid negative subtraction for kids
    if op == "-" and b > a:
        a, b = b, a

    return f"{a} {op} {b}"


def generate_puzzle(level):
    """
    Kid-friendly difficulty levels:
      0 → Easy:       single-operation
      1 → Medium:     two_terms op simple number
      2 → Hard:       three numbers, two operations
      3 → Warrior:    (term) + (term)
    """

    # -------------------------
    # Easy
    # -------------------------
    if level == 0:
        expr = generate_simple_term()

    # -------------------------
    # Medium
    # -------------------------
    elif level == 1:
        t1 = generate_simple_term()
        op = random.choice(["+", "-", "*"])
        t2 = random.randint(1, 9)
        expr = f"{t1} {op} {t2}"

    # -------------------------
    # Hard (kid-friendly)
    # -------------------------
    elif level == 2:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)

        op1 = random.choice(["+", "-", "*"])
        op2 = random.choice(["+", "-", "*"])

        # avoid negative subtraction
        if op1 == "-" and b > a:
            a, b = b, a
        if op2 == "-" and c > b:
            b, c = c, b

        expr = f"{a} {op1} {b} {op2} {c}"

    # -------------------------
    # Warrior (Option B version)
    # -------------------------
    else:
        t1 = generate_simple_term()
        t2 = generate_simple_term()
        expr = f"({t1}) + ({t2})"

    # Evaluate safely
    ans = eval(expr)

    return expr, ans
