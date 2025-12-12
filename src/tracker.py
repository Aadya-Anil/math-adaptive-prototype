from dataclasses import dataclass, field

@dataclass
class Attempt:
    level: int
    correct: bool
    time_taken: float
    user_answer: int
    true_answer: int

@dataclass
class SessionTracker:
    attempts: list = field(default_factory=list)

    def log(self, level, correct, time_taken, user_answer, true_answer):
        self.attempts.append(Attempt(level, correct, time_taken, user_answer, true_answer))

    def total_correct(self): #number of wrong answers in the current session
        return sum(a.correct for a in self.attempts)

    def total_wrong(self): #number of wrong answers in the current session
        return len(self.attempts) - self.total_correct()
        
    def accuracy(self): #accuracy 
        if not self.attempts:
            return 0
        return sum(a.correct for a in self.attempts) / len(self.attempts)

    def avg_time(self): #average time
        if not self.attempts:
            return 0
        return sum(a.time_taken for a in self.attempts) / len(self.attempts)
