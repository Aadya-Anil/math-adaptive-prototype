class AdaptiveEngine:

    #Here we will maintain a difficulty score and update it based on performance. Score is mapped to difficulty levels 0–3, 0 being easy level. 
    # I have adopted a streak approach in this reinforcement-style update, so consecutive correct answers will increase performance score and hence increase the level.

    def __init__(self, start_level=0):
        self.score = float(start_level)
        self.max_score = 3.0
        self.lr = 0.8   # learning rate
        self.target = 0.7  # desired performance, if score is higher than this we will increade difficulty
        # to track streaks
        self.correct_streak = 0
        self.wrong_streak = 0

    def compute_performance(self, correct, time_taken): #Returns a performance score between 0 and 1 using the number of correct answers and time taken to answer each.
        base = 1.0 if correct else 0.0 #ie. Correct = +1, if then incorrect = 0.
        speed_bonus = max(0, 1.5 - time_taken) / 10  # small bonus for answering quickly too
        perf = min(1.0, base + speed_bonus)
        return perf

    def update(self, correct, time_taken):
        perf = self.compute_performance(correct, time_taken)
        change = self.lr * (perf - self.target) # the learning rule
        self.score += change
        self.score = max(0.0, min(self.score, self.max_score)) # Clamps score between 0 and max

        # Streak adjustments
        if correct:
            self.correct_streak += 1
            self.wrong_streak = 0
        else:
            self.wrong_streak += 1
            self.correct_streak = 0

        # 3 correct answers then level up 1 step
        if self.correct_streak >= 3:
            self.score = min(self.score + 1.0, self.max_score)
            self.correct_streak = 0

        # 2 consecutive wrong then level down 1 step
        if self.wrong_streak >= 2:
            self.score = max(self.score - 1.0, 0.0)
            self.wrong_streak = 0


    def get_level(self): #maps continuous score to discrete level 0 to 3
        if self.score < 1.0:
            return 0
        elif self.score < 2.0:
            return 1
        elif self.score < 3.0:
            return 2
        else:
            return 3
