# src/adaptive_engine.py
import math

class AdaptiveEngine:
    """
    Reinforcement-style adaptive engine.
    difficulty_score is continuous in [0, max_level].
    Update rule: difficulty_score += lr * (perf - target)
    """

    def __init__(self, init_level: int = 0, max_level: int = 3, lr: float = 0.35, target: float = 0.7):
        self.difficulty_score = float(init_level)
        self.max_level = max_level
        self.lr = lr
        self.target = target

    def _performance_score(self, correct: bool, time_taken: float, time_threshold: float = 7.0):
        """
        Returns perf in [0,1]. correctness is 1 or 0.
        Adds small speed bonus (up to 0.2) if faster than time_threshold.
        """
        base = 1.0 if correct else 0.0
        speed_bonus = 0.0
        if time_taken < time_threshold and time_taken > 0:
            speed_bonus = ((time_threshold - time_taken) / time_threshold) * 0.2
        raw = base + speed_bonus      # up to 1.2
        return min(1.0, raw / 1.2)

    def update(self, correct: bool, time_taken: float):
        perf = self._performance_score(correct, time_taken)
        delta = self.lr * (perf - self.target)
        self.difficulty_score += delta
        # clamp
        self.difficulty_score = max(0.0, min(float(self.max_level), self.difficulty_score))

    def get_level(self) -> int:
        """Map continuous score to discrete 0..max_level (4 buckets)."""
        # split [0, max_level] into max_level+1 equal buckets
        if self.max_level <= 0:
            return 0
        bucket = self.max_level / (self.max_level + 1)  # not used directly
        chunk = (self.max_level) / 4.0  # 4 levels
        s = self.difficulty_score
        if s < chunk:
            return 0
        elif s < 2 * chunk:
            return 1
        elif s < 3 * chunk:
            return 2
        else:
            return 3
