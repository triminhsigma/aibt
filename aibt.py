import streamlit as st
import random
import time
import json
import os
import base64
from fractions import Fraction

def local_font(font_path: str, font_name: str):
    if not os.path.exists(font_path):
        return
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

local_font("SJ Pancake Pen.ttf", "SJ Pancake Pen")

def random_number():
    kind = random.choice(["int", "float", "frac"])
    if kind == "int":
        value = random.randint(1, 9)
        return value
    elif kind == "float":
        value = round(random.uniform(1, 9), 1)
        return value
    else:
        numerator = random.randint(1, 9)
        denominator = random.randint(1, 9)
        if denominator == 0:
            denominator = 1
        value = Fraction(numerator, denominator)
        return value

def generate_question(mode, level):
    if mode == "Số hữu tỉ":
        if level == "Rất Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-"])
            expr = f"{a} {op} {b}"
            ans = eval(expr)
            return expr, ans
        elif level == "Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and b == 0:
                b = 1
            expr = f"{a} {op} {b}"
            ans = eval(expr)
            return expr, ans
        elif level == "Bình Thường":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            c = random.randint(1, 20)
            op1 = random.choice(["+", "-", "*"])
            op2 = random.choice(["+", "-", "*"])
            expr = f"{a} {op1} {b} {op2} {c}"
            ans = eval(expr)
            return expr, ans
        elif level == "Khó":
            a = random_number()
            b = random_number()
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and float(b) == 0:
                b = 1
            expr = f"({a}) {op} ({b})"
            if op == "+":
                ans = float(a) + float(b)
            elif op == "-":
                ans = float(a) - float(b)
            elif op == "*":
                ans = float(a) * float(b)
            elif op == "/":
                ans = float(a) / float(b)
            return expr, ans
        else:
            a = random_number()
            b = random_number()
            c = random_number()
            op1 = random.choice(["+", "-", "*", "/"])
            op2 = random.choice(["+", "-", "*", "/"])
            if op1 == "/" and float(b) == 0:
                b = 1
            if op2 == "/" and float(c) == 0:
                c = 1
            expr = f"({a}) {op1} ({b}) {op2} ({c})"
            if op1 == "+":
                temp = float(a) + float(b)
            elif op1 == "-":
                temp = float(a) - float(b)
            elif op1 == "*":
                temp = float(a) * float(b)
            elif op1 == "/":
                temp = float(a) / float(b)
            if op2 == "+":
                ans = temp + float(c)
            elif op2 == "-":
                ans = temp - float(c)
            elif op2 == "*":
                ans = temp * float(c)
            elif op2 == "/":
                ans = temp / float(c)
            return expr, ans

    elif mode == "Tìm x":
        if level == "Rất Dễ" or level == "Dễ" or level == "Bình Thường":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            expr = f"x + {a} = {b}"
            ans = b - a
            return expr, ans
        elif level == "Khó":
            a = random_number()
            b = random_number()
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and float(b) == 0:
                b = 1
            if op == "+":
                result = float(a) + float(b)
                expr = f"x + {b} = {result}"
                ans = result - float(b)
            elif op == "-":
                result = float(a) - float(b)
                expr = f"x - {b} = {result}"
                ans = result + float(b)
            elif op == "*":
                result = float(a) * float(b)
                expr = f"x * {b} = {result}"
                ans = result / float(b)
            elif op == "/":
                result = float(a) / float(b)
                expr = f"x / {b} = {result}"
                ans = result * float(b)
            return expr, ans
        else:
            a = random_number()
            b = random_number()
            c = random_number()
            op1 = random.choice(["+", "-", "*", "/"])
            op2 = random.choice(["+", "-", "*", "/"])
            if op1 == "/" and float(b) == 0:
                b = 1
            if op2 == "/" and float(c) == 0:
                c = 1
            if op1 == "+":
                temp1 = float(a) + float(b)
            elif op1 == "-":
                temp1 = float(a) - float(b)
            elif op1 == "*":
                temp1 = float(a) * float(b)
            elif op1 == "/":
                temp1 = float(a) / float(b)
            if op2 == "+":
                result = temp1 + float(c)
            elif op2 == "-":
                result = temp1 - float(c)
            elif op2 == "*":
                result = temp1 * float(c)
            elif op2 == "/":
                result = temp1 / float(c)
            expr = f"x {op1} {b} {op2} {c} = {result}"
            if op1 == "+":
                ans = result - eval(str(float(b)) + op2 + str(float(c)))
            elif op1 == "-":
                ans = result + eval(str(float(b)) + op2 + str(float(c)))
            elif op1 == "*":
                ans = result / eval(str(float(b)) + op2 + str(float(c)))
            elif op1 == "/":
                ans = result * eval(str(float(b)) + op2 + str(float(c)))
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

placeholder = st.empty()

if st.session_state.screen == "start":
    with placeholder.container():
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

elif st.session_state.screen == "quiz":
    with placeholder.container():
        idx = st.session_state.index
        q, ans = st.session_state.questions[idx]
        st.subheader(f"Câu {idx+1}/{st.session_state.num_questions}")
        st.markdown(f"👤 Người chơi: **{st.session_state.player}**")
        if st.session_state.mode == "Tìm x":
            st.markdown(f"📌 Câu hỏi: **{q}, x = ?**")
        else:
            st.markdown(f"📌 Câu hỏi: **{q} = ?**")
        if f"answered_{idx}" not in st.session_state:
            st.session_state[f"answered_{idx}"] = False
            st.session_state[f"feedback_{idx}"] = ""
        if not st.session_state[f"answered_{idx}"]:
            user_ans = st.text_input("Nhập đáp án", key=f"ans_{idx}")
            if st.button("Trả lời"):
                try:
                    if "/" in user_ans:
                        ua = Fraction(user_ans)
                        ua_val = float(ua)
                    else:
                        ua_val = float(user_ans)
                    if abs(float(ans) - ua_val) < 1e-6:
                        st.session_state[f"feedback_{idx}"] = ("success", "Đúng!")
                        st.session_state.correct += 1
                    else:
                        st.session_state[f"feedback_{idx}"] = ("error", f"Sai! Đáp án: {ans}")
                except:
                    st.session_state[f"feedback_{idx}"] = ("error", f"Đáp án không hợp lệ! Đúng: {ans}")
                st.session_state[f"answered_{idx}"] = True
                st.rerun()
        else:
            typ, msg = st.session_state[f"feedback_{idx}"]
            if typ == "success":
                st.success(msg)
            else:
                st.error(msg)
            if st.button("Tiếp tục"):
                st.session_state.index += 1
                if st.session_state.index >= st.session_state.num_questions:
                    st.session_state.screen = "result"
                st.rerun()

elif st.session_state.screen == "result":
    with placeholder.container():
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
