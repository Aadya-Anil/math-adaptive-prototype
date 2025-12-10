import streamlit as st
import time
from src.puzzle_generator import generate_puzzle
from src.adaptive_engine import AdaptiveEngine
from src.tracker import SessionTracker

# ---------------------------------------
# STREAMLIT PAGE SETUP
# ---------------------------------------
st.set_page_config(
    page_title="Math Adventures!",
    page_icon="🎉",
)

st.title("🎉 Math Adventures!")
st.write("A fun math game that gets *smarter* as you play! ✨")


# ---------------------------------------
# INITIAL SESSION STATE SETUP
# ---------------------------------------
if "name" not in st.session_state:
    st.session_state.name = None

if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False

if "engine" not in st.session_state:
    st.session_state.engine = None

if "tracker" not in st.session_state:
    st.session_state.tracker = None

if "current_puzzle" not in st.session_state:
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None


# ---------------------------------------
# STEP 1 → ASK NAME
# ---------------------------------------
if st.session_state.name is None:
    st.subheader("👋 What’s your name, hero?")
    name_input = st.text_input("Enter your name")

    if st.button("Start Game"):
        if name_input.strip():
            st.session_state.name = name_input.strip()
            st.rerun()

    st.stop()

st.write(f"Hi **{st.session_state.name}**! Ready for your math adventure? 🦸")


# ---------------------------------------
# STEP 2 → CHOOSE DIFFICULTY
# ---------------------------------------
if not st.session_state.difficulty_chosen:
    st.subheader("Choose your difficulty:")

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("1️⃣ Easy"):
        st.session_state.engine = AdaptiveEngine(init_level=0, max_level=3)
        st.session_state.tracker = SessionTracker()
        st.session_state.difficulty_chosen = True
        st.rerun()

    if col2.button("2️⃣ Medium"):
        st.session_state.engine = AdaptiveEngine(init_level=1, max_level=3)
        st.session_state.tracker = SessionTracker()
        st.session_state.difficulty_chosen = True
        st.rerun()

    if col3.button("3️⃣ Hard"):
        st.session_state.engine = AdaptiveEngine(init_level=2, max_level=3)
        st.session_state.tracker = SessionTracker()
        st.session_state.difficulty_chosen = True
        st.rerun()

    if col4.button("4️⃣ Warrior ⚔️"):
        st.session_state.engine = AdaptiveEngine(init_level=3, max_level=3)
        st.session_state.tracker = SessionTracker()
        st.session_state.difficulty_chosen = True
        st.rerun()

    st.stop()


engine = st.session_state.engine
tracker = st.session_state.tracker


# ---------------------------------------
# STEP 3 → GENERATE PUZZLE
# ---------------------------------------
if st.session_state.current_puzzle is None:
    level = engine.get_level()
    puzzle, answer = generate_puzzle(level)

    st.session_state.current_puzzle = puzzle
    st.session_state.current_answer = answer
    st.session_state.start_time = time.time()

level_names = ["Easy", "Medium", "Hard", "Warrior"]
curr_level = engine.get_level()

st.subheader(f"🎯 Solve this ({level_names[curr_level]})")
st.write(f"## {st.session_state.current_puzzle} = ?")


# ---------------------------------------
# STEP 4 → GET ANSWER
# ---------------------------------------
user_input = st.text_input("Your answer")

if st.button("Submit"):
    try:
        user_answer = int(user_input)
    except:
        st.error("❌ Please enter a valid number!")
        st.stop()

    elapsed = time.time() - st.session_state.start_time
    correct = (user_answer == st.session_state.current_answer)

    # Log attempt
    tracker.log_attempt(
        curr_level,
        correct,
        elapsed,
        user_answer
    )

    # Update difficulty
    engine.update(correct, elapsed)

    # Feedback
    if correct:
        st.success("🎉 Correct! Well done!")
    else:
        st.error(f"❌ Oops! The correct answer was **{st.session_state.current_answer}**.")

    st.write(f"⏱️ Time taken: **{elapsed:.2f}s**")
    st.write(f"✨ Next difficulty: **{level_names[engine.get_level()]}**")

    # Reset puzzle for next round
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None

    st.button("Next Problem", on_click=st.rerun)
