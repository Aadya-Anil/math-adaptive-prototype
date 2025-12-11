# src/adaptive_engine.py

class AdaptiveEngine:
    """
    Maintains a difficulty score and updates it based on performance.
    Score is mapped to difficulty levels 0–3.
    """

    def __init__(self, start_level=0):
        self.score = float(start_level)
        self.max_score = 3.0
        self.lr = 0.8   # learning rate
        self.target = 0.7  # desired performance
        # Track streaks
        self.correct_streak = 0
        self.wrong_streak = 0

    def compute_performance(self, correct, time_taken):
        """
        Returns a performance score between 0 and 1.
        Correct = 1, incorrect = 0.
        Slight bonus for answering quickly.
        """
        base = 1.0 if correct else 0.0
        speed_bonus = max(0, 1.5 - time_taken) / 10  # small bonus
        perf = min(1.0, base + speed_bonus)
        return perf

    def update(self, correct, time_taken):
        perf = self.compute_performance(correct, time_taken)

        # Reinforcement-style update
        change = self.lr * (perf - self.target)
        self.score += change

        # Clamp score between 0 and max
        self.score = max(0.0, min(self.score, self.max_score))

        # -----------------------------
        # Streak-based adjustments
        # -----------------------------
        if correct:
            self.correct_streak += 1
            self.wrong_streak = 0
        else:
            self.wrong_streak += 1
            self.correct_streak = 0

        # 3 correct answers → level up 1 step
        if self.correct_streak >= 3:
            self.score = min(self.score + 1.0, self.max_score)
            self.correct_streak = 0

        # 2 consecutive wrong → level down 1 step
        if self.wrong_streak >= 2:
            self.score = max(self.score - 1.0, 0.0)
            self.wrong_streak = 0


    def get_level(self):
        """Map continuous score to discrete level 0–3."""
        if self.score < 1.0:
            return 0
        elif self.score < 2.0:
            return 1
        elif self.score < 3.0:
            return 2
        else:
            return 3
