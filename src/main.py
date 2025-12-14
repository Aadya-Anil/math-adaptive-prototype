import time
from src.puzzle_generator import generate_puzzle
from src.adaptive_engine import AdaptiveEngine
from src.tracker import SessionTracker

LEVELS = ["Easy", "Medium", "Hard", "Warrior Mode"]

def main():
    print("\n====== Math Adventures =====\n")

    name = input("Hello fellow adventurer! What's your name ->> ").strip() or "Player"
    print(f"\nHello, {name}! Let's find out how much you can tackle the world of MATH.\n")

    print("Choose your difficulty:")
    print("1) Easy\n2) Medium\n3) Hard\n4) Warrior Mode")

    while True:
        choice = input("Enter 1-4: ")
        if choice in ["1", "2", "3", "4"]:
            break
        print(f"You can only choose a number from 1 to 4. TRY AGAIN, {name}")

    start_level = int(choice) - 1
    engine = AdaptiveEngine(start_level=start_level) # applies our adaptive rule
    tracker = SessionTracker() #calls tracker.py to record performance

    NUM_QUESTIONS = 8

    for i in range(NUM_QUESTIONS):
        level = engine.get_level()
        expr, ans = generate_puzzle(level) 

        print(f"\nQ{i+1}/{NUM_QUESTIONS} | Level: {LEVELS[level]}")
        print(f"Solve: {expr} = ?")

        start = time.monotonic() #starts timer 
        try:
            user_ans = int(input("Your answer: "))
        except:
            user_ans = None
        elapsed = time.monotonic() - start #calculates how much time is taken for that perticular question

        correct = (user_ans == ans)
        tracker.log(level, correct, elapsed, user_ans, ans)
        engine.update(correct, elapsed)

        if correct:
            print(" ✓ That is Correct!")
        else:
            print(f" ✗ Oops, that's not right. Correct answer was {ans}")
        print(f"You took {elapsed:.2f}s to answer that!")

    # summary at end of session
    print("\n====== Session Statistics ====== \n Let's see how well you did...\n")
    print(f"Correct answers: {tracker.total_correct()}")
    print(f"Wrong answers:   {tracker.total_wrong()}")
    print(f"Accuracy: {tracker.accuracy()*100:.1f}%")
    print(f"Average time: {tracker.avg_time():.2f}s")
    if tracker.accuracy() > 0.6:
        next_level = min(engine.get_level(), 3) 
    print(f"Recommended next level: {LEVELS[next_level]}")
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
