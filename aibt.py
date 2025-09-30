import streamlit as st
import random, time, json, os
from fractions import Fraction

def generate_question(mode, level):
    if mode == "Số hữu tỉ":
        if level == "Rất Dễ":
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(["+", "-"])
            expr = f"{a}{op}{b}"
            ans = eval(expr)
        elif level == "Dễ":
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(["+", "-", "*", "/"])
            if op == "/":
                while b == 0:
                    b = random.randint(1, 20)
            expr = f"{a}{op}{b}"
            ans = eval(expr)
        elif level == "Bình Thường":
            a, b, c = random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)
            ops = random.choices(["+", "-", "*"], k=2)
            expr = f"{a}{ops[0]}{b}{ops[1]}{c}"
            ans = eval(expr)
        elif level == "Khó":
            a = random.choice([random.randint(1, 9), round(random.uniform(1, 9), 1), Fraction(random.randint(1, 9), random.randint(1, 9))])
            b = random.choice([random.randint(1, 9), round(random.uniform(1, 9), 1), Fraction(random.randint(1, 9), random.randint(1, 9))])
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and b == 0:
                b = 1
            expr = f"({a}){op}({b})"
            ans = eval(expr)
        else:  # Rất Khó
            a = random.choice([random.randint(1, 9), round(random.uniform(1, 9), 1), Fraction(random.randint(1, 9), random.randint(1, 9))])
            b = random.choice([random.randint(1, 9), round(random.uniform(1, 9), 1), Fraction(random.randint(1, 9), random.randint(1, 9))])
            c = random.choice([random.randint(1, 9), round(random.uniform(1, 9), 1), Fraction(random.randint(1, 9), random.randint(1, 9))])
            ops = random.choices(["+", "-", "*", "/"], k=2)
            expr = f"({a}){ops[0]}({b}){ops[1]}({c})"
            ans = eval(expr)
        return expr, ans
    elif mode == "Tìm x":
        a, b = random.randint(1, 20), random.randint(1, 20)
        expr = f"x + {a} = {b}"
        ans = b - a
        return expr, ans

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    return {}

def save_leaderboard(data):
    with open("leaderboard.json", "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Quiz Toán", page_icon="📘")

if "screen" not in st.session_state:
    st.session_state.screen = "start"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "player" not in st.session_state:
    st.session_state.player = ""
if "mode" not in st.session_state:
    st.session_state.mode = ""
if "difficulty" not in st.session_state:
    st.session_state.difficulty = ""
if "num_questions" not in st.session_state:
    st.session_state.num_questions = 0

# -------------------------------
# Màn hình Start
# -------------------------------
if st.session_state.screen == "start":
    st.title("📘 Quiz Toán")
    name = st.text_input("Nhập tên người chơi:")
    mode = st.selectbox("Chọn chế độ", ["Số hữu tỉ", "Tìm x"])
    level = st.selectbox("Chọn độ khó", ["Rất Dễ", "Dễ", "Bình Thường", "Khó", "Rất Khó"])
    num_q = st.number_input("Số câu", min_value=1, max_value=20, value=5)

    if st.button("Bắt đầu") and name.strip():
        st.session_state.player = name.strip()
        st.session_state.mode = mode
        st.session_state.difficulty = level
        st.session_state.num_questions = num_q
        st.session_state.questions = [generate_question(mode, level) for _ in range(num_q)]
        st.session_state.index = 0
        st.session_state.correct = 0
        st.session_state.start_time = time.time()
        st.session_state.screen = "quiz"
        st.rerun()

# -------------------------------
# Màn hình Quiz
# -------------------------------
elif st.session_state.screen == "quiz":
    idx = st.session_state.index
    q, ans = st.session_state.questions[idx]

    st.subheader(f"Câu {idx+1}/{st.session_state.num_questions}")
    st.markdown(f"👤 Người chơi: **{st.session_state.player}**")
    st.markdown(f"📌 Câu hỏi: **{q} = ?**")

    user_ans = st.text_input("Nhập đáp án", key=f"ans_{idx}")

    if st.button("Trả lời"):
        try:
            ua = Fraction(user_ans) if "/" in user_ans else float(user_ans)
            if abs(float(ua) - float(ans)) < 1e-6:
                st.success("Đúng!")
                st.session_state.correct += 1
            else:
                st.error(f"Sai! Đáp án: {ans}")
        except:
            st.error(f"Đáp án không hợp lệ! Đúng: {ans}")
        st.session_state.index += 1
        if st.session_state.index >= st.session_state.num_questions:
            st.session_state.screen = "result"
        st.rerun()

# -------------------------------
# Màn hình Kết quả
# -------------------------------
elif st.session_state.screen == "result":
    total_time = time.time() - st.session_state.start_time
    avg_time = total_time / st.session_state.num_questions
    st.success(f"Hoàn thành! Điểm: {st.session_state.correct}/{st.session_state.num_questions}")
    st.write(f"Tổng TG: {total_time:.2f}s | TG TB: {avg_time:.2f}s")

    leaderboard = load_leaderboard()
    key = f"{st.session_state.mode}-{st.session_state.difficulty}"
    if key not in leaderboard:
        leaderboard[key] = []
    leaderboard[key].append({
        "player": st.session_state.player,
        "score": st.session_state.correct,
        "total": st.session_state.num_questions,
        "time": total_time,
        "avg": avg_time
    })
    leaderboard[key] = sorted(leaderboard[key], key=lambda x: (-x["score"], x["time"]))[:10]
    save_leaderboard(leaderboard)

    st.subheader("🏆 Top 3 (chế độ hiện tại)")
    for i, entry in enumerate(leaderboard[key][:3], 1):
        st.write(f"{i}. {entry['player']} | {entry['score']}/{entry['total']} | TG:{entry['time']:.2f}s")

    all_scores = []
    for k in leaderboard:
        all_scores.extend(leaderboard[k])
    all_scores = sorted(all_scores, key=lambda x: (-x["score"], x["time"]))[:3]

    st.subheader("🌍 Top 3 Toàn Cầu")
    for i, entry in enumerate(all_scores, 1):
        st.write(f"{i}. {entry['player']} | {entry['score']}/{entry['total']} | TG:{entry['time']:.2f}s")

    if st.button("Chơi lại"):
        st.session_state.screen = "start"
        st.rerun()
