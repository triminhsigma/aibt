import streamlit as st
import random
import time
import json
import os
import base64
from fractions import Fraction

def local_font(font_path: str, font_name: str):
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

def random_value():
    r = random.choice([0, 1, 2])
    if r == 0:
        return random.randint(1, 9)
    if r == 1:
        return round(random.uniform(1, 9), 2)
    return Fraction(random.randint(1, 9), random.randint(1, 9))

def format_value(v):
    if isinstance(v, Fraction):
        return f"{v.numerator}/{v.denominator}"
    if isinstance(v, float):
        s = f"{v:.2f}"
        if s.endswith(".00"):
            return s[:-3]
        return s
    return str(v)

def to_fraction(v):
    if isinstance(v, Fraction):
        return v
    if isinstance(v, float):
        return Fraction(str(v))
    return Fraction(v)

def to_eval_literal(v):
    if isinstance(v, Fraction):
        return f"Fraction({v.numerator},{v.denominator})"
    if isinstance(v, float):
        return repr(v)
    return str(v)

def generate_question(mode, level):
    if mode == "Số hữu tỉ":
        if level == "Rất Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-"])
            expr = f"{a} {op} {b}"
            ans_frac = to_fraction(eval(f"{a}{op}{b}"))
            return expr, ans_frac

        if level == "Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and b == 0:
                b = 1
            expr = f"{a} {op} {b}"
            ans_frac = to_fraction(eval(f"{a}{op}{b}"))
            return expr, ans_frac

        if level == "Bình Thường":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            c = random.randint(1, 20)
            ops = random.choices(["+", "-", "*"], k=2)
            expr = f"{a} {ops[0]} {b} {ops[1]} {c}"
            ans_frac = to_fraction(eval(expr))
            return expr, ans_frac

        if level == "Khó":
            a = random_value()
            b = random_value()
            op = random.choice(["+", "-", "*", "/"])
            if op == "/" and to_fraction(b) == 0:
                b = 1
            disp = f"({format_value(a)}) {op} ({format_value(b)})"
            eval_expr = f"({to_eval_literal(a)}){op}({to_eval_literal(b)})"
            ans_frac = to_fraction(eval(eval_expr, {"Fraction": Fraction}))
            return disp, ans_frac

        if level == "Rất Khó":
            a = random_value()
            b = random_value()
            c = random_value()
            ops = random.choices(["+", "-", "*", "/"], k=2)
            if ops[0] == "/" and to_fraction(b) == 0:
                b = 1
            if ops[1] == "/" and to_fraction(c) == 0:
                c = 1
            disp = f"({format_value(a)}) {ops[0]} ({format_value(b)}) {ops[1]} ({format_value(c)})"
            eval_expr = f"({to_eval_literal(a)}){ops[0]}({to_eval_literal(b)}){ops[1]}({to_eval_literal(c)})"
            ans_frac = to_fraction(eval(eval_expr, {"Fraction": Fraction}))
            return disp, ans_frac

    if mode == "Tìm x":
        if level == "Rất Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            left = f"x + {format_value(a)}"
            right = format_value(b)
            ans_frac = to_fraction(b) - to_fraction(a)
            return (left, right), ans_frac

        if level == "Dễ":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            left = f"{format_value(a)} + x"
            right = format_value(b)
            ans_frac = to_fraction(b) - to_fraction(a)
            return (left, right), ans_frac

        if level == "Bình Thường":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 20)
            left = f"{format_value(a)} * x + {format_value(b)}"
            right = format_value(c)
            ans_frac = (to_fraction(c) - to_fraction(b)) / to_fraction(a)
            return (left, right), ans_frac

        if level == "Khó":
            a = random_value()
            b = random_value()
            op = random.choice(["+", "-", "*", "/"])
            if op == "+":
                left = f"x + ({format_value(a)})"
                right = format_value(b)
                ans_frac = to_fraction(b) - to_fraction(a)
                return (left, right), ans_frac
            if op == "-":
                left = f"x - ({format_value(a)})"
                right = format_value(b)
                ans_frac = to_fraction(b) + to_fraction(a)
                return (left, right), ans_frac
            if op == "*":
                if to_fraction(a) == 0:
                    a = 1
                left = f"x * ({format_value(a)})"
                right = format_value(b)
                ans_frac = to_fraction(b) / to_fraction(a)
                return (left, right), ans_frac
            if op == "/":
                if to_fraction(a) == 0:
                    a = 1
                left = f"x / ({format_value(a)})"
                right = format_value(b)
                ans_frac = to_fraction(b) * to_fraction(a)
                return (left, right), ans_frac

        if level == "Rất Khó":
            pattern = random.choice([0, 1, 2, 3, 4])
            a = random_value()
            b = random_value()
            c = random_value()
            if pattern == 0:
                left = f"({format_value(a)}) * x + ({format_value(b)})"
                right = format_value(c)
                if to_fraction(a) == 0:
                    a = 1
                ans_frac = (to_fraction(c) - to_fraction(b)) / to_fraction(a)
                return (left, right), ans_frac
            if pattern == 1:
                left = f"(x + ({format_value(a)})) * ({format_value(b)})"
                right = format_value(c)
                if to_fraction(b) == 0:
                    b = 1
                ans_frac = (to_fraction(c) / to_fraction(b)) - to_fraction(a)
                return (left, right), ans_frac
            if pattern == 2:
                left = f"x / ({format_value(a)}) - ({format_value(b)})"
                right = format_value(c)
                if to_fraction(a) == 0:
                    a = 1
                ans_frac = (to_fraction(c) + to_fraction(b)) * to_fraction(a)
                return (left, right), ans_frac
            if pattern == 3:
                left = f"{format_value(a)} * (x - ({format_value(b)}))"
                right = format_value(c)
                if to_fraction(a) == 0:
                    a = 1
                ans_frac = (to_fraction(c) / to_fraction(a)) + to_fraction(b)
                return (left, right), ans_frac
            left = f"(x + ({format_value(a)})) / ({format_value(b)}) + ({format_value(c)})"
            right = format_value(random_value())
            denom = to_fraction(b)
            if denom == 0:
                b = 1
                denom = to_fraction(b)
            rhs = to_fraction(right)
            ans_frac = (rhs - to_fraction(c)) * denom - to_fraction(a)
            return (left, right), ans_frac

    return "0 + 0", Fraction(0, 1)

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
            qs = []
            for _ in range(num_q):
                q, a = generate_question(mode, level)
                qs.append((q, a))
            st.session_state.questions = qs
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
        if isinstance(q, tuple):
            left, right = q
            st.markdown(f"📌 Câu hỏi: **{left} = {right}, x = ?**")
        else:
            st.markdown(f"📌 Câu hỏi: **{q} = ?**")
        if f"answered_{idx}" not in st.session_state:
            st.session_state[f"answered_{idx}"] = False
            st.session_state[f"feedback_{idx}"] = ""
        if not st.session_state[f"answered_{idx}"]:
            user_ans = st.text_input("Nhập đáp án", key=f"ans_{idx}")
            if st.button("Trả lời"):
                try:
                    ua = Fraction(user_ans)
                except Exception:
                    try:
                        ua = Fraction(str(float(user_ans)))
                    except Exception:
                        ua = None
                if ua is None:
                    if isinstance(ans, Fraction):
                        st.session_state[f"feedback_{idx}"] = ("error", f"Đáp án không hợp lệ! Đúng: {ans.numerator}/{ans.denominator} ≈ {float(ans):.6f}")
                    else:
                        st.session_state[f"feedback_{idx}"] = ("error", f"Đáp án không hợp lệ! Đúng: {float(ans):.6f}")
                else:
                    if abs(float(ua) - float(ans)) < 1e-6:
                        st.session_state[f"feedback_{idx}"] = ("success", "Đúng!")
                        st.session_state.correct += 1
                    else:
                        if isinstance(ans, Fraction):
                            st.session_state[f"feedback_{idx}"] = ("error", f"Sai! Đáp án: {ans.numerator}/{ans.denominator} ≈ {float(ans):.6f}")
                        else:
                            st.session_state[f"feedback_{idx}"] = ("error", f"Sai! Đáp án: {float(ans):.6f}")
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
