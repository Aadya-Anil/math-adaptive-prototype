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
    if op
