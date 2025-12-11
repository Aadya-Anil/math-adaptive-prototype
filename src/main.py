# src/main.py

import time
from src.puzzle_generator import generate_puzzle
from src.adaptive_engine import AdaptiveEngine
from src.tracker import SessionTracker

LEVELS = ["Easy", "Medium", "Hard", "Warrior"]

def main():
    print("\n=== Adaptive Math Prototype ===\n")

    name = input("Enter your name: ").strip() or "Player"
    print(f"\nHello, {name}! Let's begin.\n")

    print("Choose starting difficulty:")
    print("1) Easy\n2) Medium\n3) Hard\n4) Warrior")

    while True:
        choice = input("Enter 1–4: ")
        if choice in ["1", "2", "3", "4"]:
            break
        print("Please enter a valid option.")

    start_level = int(choice) - 1
    engine = AdaptiveEngine(start_level=start_level)
    tracker = SessionTracker()

    NUM_QUESTIONS = 8

    for i in range(NUM_QUESTIONS):
        level = engine.get_level()
        expr, ans = generate_puzzle(level)

        print(f"\nQ{i+1}/{NUM_QUESTIONS} | Level: {LEVELS[level]}")
        print(f"Solve: {expr} = ?")

        start = time.monotonic()
        try:
            user_ans = int(input("Your answer: "))
        except:
            user_ans = None
        elapsed = time.monotonic() - start

        correct = (user_ans == ans)
        tracker.log(level, correct, elapsed, user_ans, ans)
        engine.update(correct, elapsed)

        if correct:
            print("✓ Correct!")
        else:
            print(f"✗ Wrong. Correct answer: {ans}")
        print(f"Time taken: {elapsed:.2f}s")

    # summary
    print("\n=== Session Summary ===")
    print(f"Accuracy: {tracker.accuracy()*100:.1f}%")
    print(f"Average time: {tracker.avg_time():.2f}s")
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
