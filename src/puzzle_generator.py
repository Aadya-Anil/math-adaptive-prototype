import random

def generate_puzzle(level):
    
    if level == 0:  # Easy level
        a, b = random.randint(1, 9), random.randint(1, 9)
        op = random.choice(["+", "-","*","/"])
        if op == "-" and b > a: # to avoid negative numbers because this is for ages 5-10
            a, b = b, a
        expr = f"{a} {op} {b}"
        if op == "/": #avoids fraction answers
            dividend = a * b
            expr= f"{dividend} / {a}"

    elif level == 1: # Medium : longer expressions
        a, b, c = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        op = random.choice(["+", "-"])
        expr = f"{a} {op} {b} {op} {c}"

    elif level == 2: # Hard: much longer expressions , includes multiplication and division
        a, b, c = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        op = random.choice(["+", "-","*","/"])
        expr = f"{a} {op} {b} {op} {c}"
        if op == "/":
            dividend = a * b
            expr= f"{dividend} / a"

    else: # Warrior level : combines two small expressions 
        a, b = random.randint(1, 9), random.randint(1, 9)
        c, d = random.randint(1, 9), random.randint(1, 9)
        expr = f"({a} + {b}) * ({c} - {d})"

    ans = eval(expr)
    return expr, ans
