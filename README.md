# Math Adventures — AI-Powered Adaptive Learning Prototype

## Content
### [Overview](#overview-1)
### Project Structure
### System Flow
### Adaptive Logic
### Difficulty Representation
### Performance Signal
### Stability Rules
### Puzzle Generation
### Metrics tracked
### Session Summary
### Why This Approach
### Requirements
### Conclusion

## Overview

This repository contains aminimal adaptive learning prototype designed to demonstrate how difficulty can be adjusted dynamically based on a learner’s performance.
The system presents a short sequence of math problems and adapts the difficulty in real time using performance feedback.

The goal of this project is to demonstrate:

- adaptive logic
- performance tracking
- simple, clean and readable code with clear system design

## Project Structure

src/
  |-- main.py              # Session flow and user interaction
  |--puzzle_generator.py  # Difficulty-based math question generation
  |-- adaptive_engine.py   # Adaptive difficulty logic
  |-- tracker.py           # Performance tracking and session statistics


Each module has a single responsibility, making the system easy to understand and extend.

## System Flow
Start session
   ↓
Enter user name
   ↓
Choose starting difficulty
   ↓
Generate math question
   ↓
User submits answer (timed)
   ↓
Track correctness and time
   ↓
Update difficulty level
   ↓
Repeat for fixed number of questions
   ↓
Display session summary and next-level recommendation

Adaptive Logic
Type of Adaptation

The system uses a reinforcement-style adaptive approach with rule-based constraints.

It is not purely rule-based, as difficulty is adjusted using a continuous performance signal.

It is not full machine learning, as no model is trained and no dataset is required.

This hybrid approach provides adaptive behavior while remaining transparent and predictable.

Difficulty Representation

Difficulty is tracked internally as a continuous score:

score ∈ [0.0, 3.0]


Mapped to discrete levels:

Score Range	Difficulty
0.0 – 0.99	Easy
1.0 – 1.99	Medium
2.0 – 2.99	Hard
≥ 3.0	Warrior

This prevents abrupt jumps between difficulty levels.

Performance Signal

Each question produces a performance signal based on:

Correctness (primary factor)

Response time (small bonus for faster answers)

The difficulty score is updated using:

score += learning_rate × (performance − target)


This moves difficulty up when the learner performs well and down when they struggle.

Stability Rules

To keep the experience learner-friendly, additional rules are applied:

3 consecutive correct answers → increase difficulty

2 consecutive wrong answers → decrease difficulty

Difficulty is clamped within valid bounds

These rules simulate how a human tutor would adapt in real time.

Puzzle Generation

Math problems are generated based on the current difficulty level:

Level	Characteristics
Easy	Single arithmetic operation
Medium	Two simple operations
Hard	Multiplication combined with addition
Warrior	Parenthesized expressions

All division problems are generated using integer-only division, ensuring answers are always whole numbers and age-appropriate.

Metrics Tracked

During each session, the system tracks:

Total correct and incorrect answers

Accuracy percentage

Time taken per question

Average response time

These metrics influence both the adaptive difficulty updates and the final session recommendation.

Session Summary

At the end of the session, the system displays:

Number of correct and wrong answers

Accuracy percentage

Average response time

Recommended next difficulty level

Users are promoted only if performance exceeds a defined threshold.

Why This Approach

This design was chosen because it is:

Explainable – easy to understand and reason about

Lightweight – no external dependencies or training data

Real-time – adapts immediately after each question

Educationally appropriate – avoids sudden difficulty spikes

Extensible – can be upgraded to ML-based adaptation in the future

Running the Project
Requirements

Python 3.8 or higher

No external dependencies

Run Command
python -m src.main

Conclusion

This project demonstrates how adaptive learning behavior can be implemented using a small, well-structured system with reinforcement-style updates and meaningful performance metrics, without relying on heavy machine-learning frameworks.

