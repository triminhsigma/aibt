import streamlit as st
import random
import time
import json
import os
import base64
from fractions import Fraction

def local_font(font_path: str, font_name: str):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
            <style>
            @font-face {{
                font-family: '{font_name}';
                src: url(data:font/ttf;base64,{b64}) format('truetype');
            }}
            html, body, [class*="css"] {{
                font-family: '{font_name}' !important;
            }}
            </style>
        """, unsafe_allow_html=True)

local_font("fonts/SJ-Pancake-Pen.ttf", "SJ Pancake Pen")

def random_number():
    t = random.choice(["int", "float", "frac"])
    if t == "int":
        return random.randint(1, 9)
    elif t == "float":
        return round(random.uniform(1, 9), 2)
    else:
        n, d = random.randint(1, 9), random.randint(1, 9)
        if d == 0:
            d = 1
        return Fraction(n, d)

def generate_question(mode, level):
    if mode == "Số hữu tỉ":
        if level == "Rất Dễ":
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(["+", "-"])
            expr = f"{a} {op} {b}"
            ans = eval(expr)
        elif level == "Dễ":
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and b == 0:
                b = 1
            expr = f"{a} {op} {b}"
            ans = eval(expr)
        elif level == "Bình Thường":
            a, b, c = random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)
            ops = random.choices(["+", "-", "*"], k=2)
            expr = f"{a} {ops[0]} {b} {ops[1]} {c}"
            ans = eval(expr)
        elif level == "Khó":
            a, b = random_number(), random_number()
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and float(b) == 0:
                b = 1
            expr = f"({a}) {op} ({b})"
            ans = eval(expr)
        else:
            a, b, c = random_number(), random_number(), random_number()
            ops = random.choices(["+", "-", "*", "/"], k=2)
            if ops[0] == "/" and float(b) == 0:
                b = 1
            if ops[1] == "/" and float(c) == 0:
                c = 1
            expr = f"({a}) {ops[0]} ({b}) {ops[1]} ({c})"
            ans = eval(expr)
        return expr, ans

    elif mode == "Tìm x":
        if level in ["Rất Dễ", "Dễ", "Bình Thường"]:
            a, b = random.randint(1, 20), random.randint(1, 20)
            expr = f"x + {a} = {b}"
            ans = b - a
            return expr, ans
        elif level == "Khó":
            a, b = random_number(), random_number()
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and float(b) == 0:
                b = 1
            if op == "+":
                res = float(a) + float(b)
                expr = f"x + {b} = {res}"
                ans = res - float(b)
            elif op == "-":
                res = float(a) - float(b)
                expr = f"x - {b} = {res}"
                ans = res + float(b)
            elif op == "*":
                res = float(a) * float(b)
                expr = f"x * {b} = {res}"
                ans = res / float(b)
            else:
                res = float(a) / float(b)
                expr = f"x / {b} = {res}"
                ans = res * float(b)
            return expr, ans
        else:
            a, b, c = random_number(), random_number(), random_number()
            op1, op2 = random.choice(["+", "-", "*", "/"]), random.choice(["+", "-", "*", "/"])
            if op1 == "/" and float(b) == 0:
                b = 1
            if op2 == "/" and float(c) == 0:
                c = 1
            res = eval(f"float(a) {op1} float(b) {op2} float(c)")
            expr = f"x {op1} {b} {op2} {c} = {res}"
            ans = float(a)
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
if "answered" not in st.session_state:
    st.session_state.answered = False

placeholder = st.empty()

if st.session_state.screen == "start":
    with placeholder.container():
        st.title("📘 Quiz Toán")
        name = st.text_input("Nhập tên người chơi:")
        mode = st.selectbox("Chọn chế độ", ["Số hữu tỉ", "Tìm x"])
        level = st.selectbox("Chọn độ khó", ["Rất Dễ", "Dễ", "Bình Thường", "Khó", "Rất Khó"])
        num_q = st.number_input("Số câu hỏi", min_value=1, max_value=20, value=5)
        if st.button("Bắt đầu chơi") and name.strip():
            st.session_state.player = name.strip()
            st.session_state.mode = mode
            st.session_state.difficulty = level
            st.session_state.num_questions = num_q
            st.session_state.questions = [generate_question(mode, level) for _ in range(num_q)]
            st.session_state.index = 0
            st.session_state.correct = 0
            st.session_state.start_time = time.time()
            st.session_state.screen = "quiz"
            st.session_state.answered = False
            st.rerun()

elif st.session_state.screen == "quiz":
    with placeholder.container():
        idx = st.session_state.index
        q, ans = st.session_state.questions[idx]
        st.subheader(f"Câu {idx + 1}/{st.session_state.num_questions}")
        st.markdown(f"👤 Người chơi: **{st.session_state.player}**")

        if st.session_state.mode == "Tìm x":
            st.markdown(f"📌 Câu hỏi: **{q}, x = ?**")
        else:
            st.markdown(f"📌 Câu hỏi: **{q} = ?**")

        if not st.session_state.answered:
            user_ans = st.text_input("Nhập đáp án của bạn:")
            if st.button("Trả lời"):
                try:
                    if "/" in user_ans:
                        ua = float(Fraction(user_ans))
                    else:
                        ua = float(user_ans)
                    if abs(float(ans) - ua) < 1e-6:
                        st.success("✅ Chính xác!")
                        st.session_state.correct += 1
                    else:
                        st.error(f"❌ Sai! Đáp án đúng là {ans}")
                except:
                    st.error(f"⚠️ Đáp án không hợp lệ! Đúng: {ans}")
                st.session_state.answered = True
        else:
            if st.button("Tiếp tục sang câu tiếp theo"):
                st.session_state.index += 1
                st.session_state.answered = False
                if st.session_state.index >= st.session_state.num_questions:
                    st.session_state.screen = "result"
                st.rerun()

elif st.session_state.screen == "result":
    with placeholder.container():
        total_time = time.time() - st.session_state.start_time
        avg_time = total_time / st.session_state.num_questions
        st.success(f"🎉 Hoàn thành! Điểm: {st.session_state.correct}/{st.session_state.num_questions}")
        st.write(f"⏱️ Tổng thời gian: {total_time:.2f}s | TB mỗi câu: {avg_time:.2f}s")

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

        st.subheader("🏆 Top 3 (Chế độ hiện tại)")
        for i, entry in enumerate(leaderboard[key][:3], 1):
            st.write(f"{i}. {entry['player']} | {entry['score']}/{entry['total']} | ⏱️ {entry['time']:.2f}s")

        all_scores = []
        for k in leaderboard:
            all_scores.extend(leaderboard[k])
        all_scores = sorted(all_scores, key=lambda x: (-x["score"], x["time"]))[:3]
        st.subheader("🌍 Top 3 Toàn Cầu")
        for i, entry in enumerate(all_scores, 1):
            st.write(f"{i}. {entry['player']} | {entry['score']}/{entry['total']} | ⏱️ {entry['time']:.2f}s")

        if st.button("🔁 Chơi lại"):
            st.session_state.screen = "start"
            st.rerun()
