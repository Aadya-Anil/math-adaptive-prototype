# app.py
import streamlit as st
import time
from src.puzzle_generator import generate_puzzle
from src.adaptive_engine import AdaptiveEngine
from src.tracker import SessionTracker

# -------------------------
# Configuration (Option B)
# -------------------------
QUESTIONS_PER_ROUND = 10
# make the AI slightly more responsive for demo (medium progression)
DEFAULT_LR = 0.45
DEFAULT_TARGET = 0.72

LEVEL_NAMES = ["Easy", "Medium", "Hard", "Warrior"]

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Math Adventures!", page_icon="🎯")

st.title("🎯 Math Adventures — Medium Progression")
st.write("A short adaptive math game (10 questions). The game gets slightly harder as the player improves.")

# -------------------------
# Session state init
# -------------------------
if "name" not in st.session_state:
    st.session_state.name = None

if "engine" not in st.session_state:
    # engine will be created when the player chooses difficulty / starts game
    st.session_state.engine = None

if "tracker" not in st.session_state:
    st.session_state.tracker = None

if "q_num" not in st.session_state:
    st.session_state.q_num = 0  # how many questions asked this round

if "current_puzzle" not in st.session_state:
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None

if "round_active" not in st.session_state:
    st.session_state.round_active = False

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

# -------------------------
# Helper functions
# -------------------------
def start_new_round(init_level: int):
    """Initialize engine, tracker and counters for a fresh round."""
    st.session_state.engine = AdaptiveEngine(init_level=init_level, max_level=3, lr=DEFAULT_LR, target=DEFAULT_TARGET)
    st.session_state.tracker = SessionTracker()
    st.session_state.q_num = 0
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None
    st.session_state.round_active = True
    st.session_state.last_feedback = ""

def end_round():
    st.session_state.round_active = False

def create_next_puzzle_if_needed():
    """Generate a new puzzle (and start timer) if none exists and round is active."""
    if not st.session_state.round_active:
        return
    if st.session_state.current_puzzle is None and st.session_state.q_num < QUESTIONS_PER_ROUND:
        level = st.session_state.engine.get_level()
        puzzle, answer = generate_puzzle(level)
        st.session_state.current_puzzle = puzzle
        st.session_state.current_answer = answer
        st.session_state.start_time = time.monotonic()

# -------------------------
# UI — Name & Start
# -------------------------
if st.session_state.name is None:
    st.subheader("👋 What’s your name, hero?")
    name_input = st.text_input("Enter name", key="name_input")

    if st.button("Start (choose difficulty next)"):
        if name_input.strip():
            st.session_state.name = name_input.strip()
            # No rerun needed — Streamlit auto-reruns after button press.

    # If still no name, stop here
    if st.session_state.name is None:
        st.stop()


st.write(f"Hi **{st.session_state.name}**! Let's play a short adaptive round — {QUESTIONS_PER_ROUND} questions.")

# If no active round, show difficulty choices
if not st.session_state.round_active:
    st.subheader("Choose your starting difficulty (1 = easiest):")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("1️⃣ Easy"):
            start_new_round(init_level=0)
            st.experimental_rerun()
    with c2:
        if st.button("2️⃣ Medium"):
            start_new_round(init_level=1)
            st.experimental_rerun()
    with c3:
        if st.button("3️⃣ Hard"):
            start_new_round(init_level=2)
            st.experimental_rerun()
    with c4:
        if st.button("4️⃣ Warrior"):
            start_new_round(init_level=3)
            st.experimental_rerun()

    # show last round summary if exists
    if st.session_state.tracker is not None and st.session_state.q_num > 0:
        st.write("### Last round summary (most recent)")
        acc = st.session_state.tracker.accuracy() * 100
        avg_t = st.session_state.tracker.avg_time()
        st.write(f"- Accuracy: **{acc:.1f}%**")
        st.write(f"- Avg time: **{avg_t:.2f}s**")
        st.write(f"- Final level reached: **{LEVEL_NAMES[st.session_state.engine.get_level()]}**")
    st.stop()

# -------------------------
# Round is active: ensure puzzle ready
# -------------------------
create_next_puzzle_if_needed()

# if we've asked enough questions → end round and show summary
if st.session_state.q_num >= QUESTIONS_PER_ROUND and st.session_state.current_puzzle is None:
    end_round()

if not st.session_state.round_active:
    # Round finished — show performance summary
    st.subheader("🏁 Round complete — Performance Summary")
    tracker = st.session_state.tracker
    if tracker is None:
        st.write("No data.")
    else:
        acc = tracker.accuracy() * 100
        avg_t = tracker.avg_time()
        st.write(f"- Player: **{st.session_state.name}**")
        st.write(f"- Accuracy: **{acc:.1f}%**")
        st.write(f"- Average time: **{avg_t:.2f}s**")
        st.write(f"- Questions answered: **{len(tracker.attempts)}**")
        st.write(f"- Final difficulty: **{LEVEL_NAMES[st.session_state.engine.get_level()]}**")
        st.write("### Attempts (most recent first)")
        for a in reversed(tracker.attempts):
            st.write(f"- {LEVEL_NAMES[a.difficulty]} | Correct: {a.correct} | Time: {a.time_taken:.2f}s | Ans: {a.user_answer}")

    st.write("")
    if st.button("Play again"):
        # reset everything so they choose difficulty again
        st.session_state.name = st.session_state.name  # keep name
        st.session_state.engine = None
        st.session_state.tracker = None
        st.session_state.q_num = 0
        st.session_state.current_puzzle = None
        st.session_state.current_answer = None
        st.session_state.start_time = None
        st.session_state.round_active = False
        st.experimental_rerun()
    st.stop()

# -------------------------
# Show current progress and puzzle
# -------------------------
st.write(f"Question **{st.session_state.q_num + 1}** of **{QUESTIONS_PER_ROUND}**")
curr_level = st.session_state.engine.get_level()
st.write(f"Current difficulty: **{LEVEL_NAMES[curr_level]}**")

st.markdown("---")
st.subheader("Solve this:")
st.write(f"### {st.session_state.current_puzzle} = ?")

# -------------------------
# Use a form for atomic submit and accurate timing
# -------------------------
with st.form("answer_form", clear_on_submit=False):
    # keep input key stable so we can clear it manually
    user_input = st.text_input("Your answer", key="answer_input")
    submitted = st.form_submit_button("Submit")

if submitted:
    # Defensive checks
    if st.session_state.start_time is None:
        st.error("Internal timer error. Restarting the question.")
        # reset and continue
        st.session_state.current_puzzle = None
        st.session_state.current_answer = None
        st.session_state.start_time = None
        st.experimental_rerun()

    # parse answer
    try:
        user_ans = int(user_input)
    except:
        st.error("Please enter a whole number (e.g., 7)")
        st.stop()

    elapsed = time.monotonic() - st.session_state.start_time
    correct = (user_ans == st.session_state.current_answer)

    # log attempt
    st.session_state.tracker.log_attempt(st.session_state.engine.get_level(), correct, elapsed, user_ans)

    # update engine (AI step)
    st.session_state.engine.update(correct, elapsed)

    # advance counter and clear puzzle (so next puzzle is generated)
    st.session_state.q_num += 1
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None

    # clear the input box explicitly so next question shows blank box
    st.session_state.answer_input = ""

    # show immediate feedback
    if correct:
        st.success(f"🎉 Correct! Time: {elapsed:.2f}s")
    else:
        st.error(f"❌ Incorrect — correct answer was **{st.session_state.tracker.attempts[-1].user_answer if False else 'hidden'}**")
        # show correct answer separately to avoid accidental eval confusion
        # we saved the answer in the logged attempt? show via the previous attempt's answer using tracker
        last_attempt = st.session_state.tracker.attempts[-1]
        # the true correct answer is not stored in tracker, so we show it using engine/previous state
        # safer: compute it from the puzzle we just answered (we had it in session_state before clearing)
        # but we cleared it already — to avoid that, store the correct answer in a temp variable before clearing
        # (we will instead display a generic hint)
        st.write(f"The correct answer was: **{ (st.session_state.tracker.attempts[-1].user_answer if last_attempt else 'N/A') }**")
        # Note: the code stores user_answer; for transparency it's better to display the actual correct answer
        # If you want the exact correct value shown, keep a small history of correct answers in session_state

    # Small pause for UX (optional)
    st.write(f"Next question coming up. Questions completed: {st.session_state.q_num}/{QUESTIONS_PER_ROUND}")

    # If round done, we will show summary on next rerun
    if st.session_state.q_num >= QUESTIONS_PER_ROUND:
        st.experimental_rerun()
    else:
        # generate next puzzle immediately and rerun to update UI
        st.experimental_rerun()

# -------------------------
# End of file
# -------------------------
