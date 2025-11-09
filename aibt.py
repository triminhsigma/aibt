import streamlit as st
import random
import time
import json
import os
import base64
import re
import math
from fractions import Fraction

st.set_page_config(page_title="Quiz Toán", page_icon="📘", layout="centered")

@st.cache_data
def load_audio_b64(filepath: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_filepath = os.path.join(script_dir, filepath)
    if not os.path.exists(absolute_filepath):
        return None, None
    with open(absolute_filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    mime_type = "audio/mp3"
    if filepath.endswith(".wav"): mime_type = "audio/wav"
    elif filepath.endswith(".ogg"): mime_type = "audio/ogg"
    return b64, mime_type

@st.cache_data
def load_audio_bytes(filepath: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_filepath = os.path.join(script_dir, filepath)
    if not os.path.exists(absolute_filepath):
        return None, None
    with open(absolute_filepath, "rb") as f:
        data = f.read()
    mime_type = "audio/mp3"
    if filepath.endswith(".wav"): mime_type = "audio/wav"
    elif filepath.endswith(".ogg"): mime_type = "audio/ogg"
    return data, mime_type

@st.cache_data
def load_font_css(font_path: str, font_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_font_path = os.path.join(script_dir, font_path)
    if not os.path.exists(absolute_font_path):
        return None
    with open(absolute_font_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    @font-face {{
        font-family: '{font_name}';
        src: url(data:font/ttf;base64,{b64}) format('truetype');
    }}
    html, body, .stApp, [class*="css"] {{
        font-family: '{font_name}', sans-serif !important;
    }}
    .quiz-container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }}
    .question-box {{
        background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(250,250,255,0.9));
        padding: 16px;
        border-radius: 10px;
    }}
    .small-muted {{ color: #666; font-size:12px; }}
    </style>
    """
    return css

def play_audio_sfx(filepath: str):
    b64, mime_type = load_audio_b64(filepath)
    if b64 and mime_type:
        audio_html = f"""<audio autoplay><source src="data:{mime_type};base64,{b64}" type="{mime_type}"></audio>"""
        st.markdown(audio_html, unsafe_allow_html=True)

def safe_float(val):
    try:
        return float(val)
    except:
        return None

def random_number():
    t = random.choice(["int", "float", "frac"])
    if t == "int":
        return random.randint(-20, 20)
    elif t == "float":
        return round(random.uniform(-10, 10), 1)
    else:
        n, d = random.randint(1, 10), random.randint(2, 10)
        return Fraction(n, d)

def num_str(n):
    if isinstance(n, Fraction):
        if n.denominator == 1:
            return f"{n.numerator}"
        return f"({n.numerator}/{n.denominator})"
    if isinstance(n, float):
        return f"{n:.1f}"
    return f"{n}"

def generate_question(mode, level):
    if mode == "Số hữu tỉ":
        if level == "Rất Dễ":
            a, b = random.randint(-20,20), random.randint(-20,20)
            op = random.choice(["+","-"])
            expr = f"({a}) {op} ({b})"
            ans = eval(expr)
        elif level == "Dễ":
            a,b = random_number(), random_number()
            op = random.choice(["+","-","*"])
            expr = f"{num_str(a)} {op} {num_str(b)}"
            ans = eval(f"{float(a)} {op} {float(b)}")
        elif level == "Bình Thường":
            a,b = random_number(), random_number()
            op = random.choice(["+","-","*","/"])
            fb = float(b)
            if op == "/" and abs(fb) < 1e-6:
                b = 1 if fb >= 0 else -1
                fb = float(b)
            expr = f"{num_str(a)} {op} {num_str(b)}"
            ans = eval(f"{float(a)} {op} {fb}")
        elif level == "Khó":
            a,b,c = random_number(), random_number(), random_number()
            ops = random.choices(["+","-","*"], k=2)
            expr = f"{num_str(a)} {ops[0]} ({num_str(b)} {ops[1]} {num_str(c)})"
            ans = eval(f"{float(a)} {ops[0]} ({float(b)} {ops[1]} {float(c)})")
        else:
            if random.choice([True,False]):
                a,b = random.randint(1,9), random.randint(2,9)
                c = random_number()
                fa = Fraction(a,b)
                fc = float(c)
                expr = f"({a}/{b})**2 + {num_str(c)}"
                ans = float(fa)**2 + fc
            else:
                n = random.choice([4,9,16,25,36,49,64,81])
                c = random_number()
                fc = float(c)
                expr = f"sqrt({n}) * {num_str(c)}"
                ans = math.sqrt(n) * fc
        return expr, ans

    elif mode == "Tìm x":
        if level == "Rất Dễ":
            a,b = random_number(), random_number()
            fa,fb = float(a), float(b)
            op = random.choice(['+','-'])
            if op=='+':
                expr = f"x + {num_str(a)} = {num_str(b)}"
                ans = fb - fa
            else:
                expr = f"x - {num_str(a)} = {num_str(b)}"
                ans = fb + fa
        elif level == "Dễ":
            a,b,c = [random.randint(-10,10) for _ in range(3)]
            a = a if a!=0 else 1
            op = random.choice(['+','-'])
            if op=='+':
                expr = f"{a}x + {b} = {c}"
                ans = (c - b) / a
            else:
                expr = f"{a}x - {b} = {c}"
                ans = (c + b) / a
        elif level == "Bình Thường":
            a,b,c = [random_number() for _ in range(3)]
            a = a if float(a)!=0 else 1
            fa,fb,fc = float(a), float(b), float(c)
            op = random.choice(['+','-'])
            if op=='+':
                expr = f"{num_str(a)}x + {num_str(b)} = {num_str(c)}"
                ans = (fc - fb) / fa
            else:
                expr = f"{num_str(a)}x - {num_str(b)} = {num_str(c)}"
                ans = (fc + fb) / fa
        elif level == "Khó":
            a,b,c = [random_number() for _ in range(3)]
            a = a if float(a)!=0 else 1
            fa,fb,fc = float(a), float(b), float(c)
            expr = f"{num_str(a)} * (x + {num_str(b)}) = {num_str(c)}"
            ans = (fc / fa) - fb
        else:
            if random.choice([True,False]):
                a,b,c = [random_number() for _ in range(3)]
                b = b if float(b)!=0 else 1
                c = c if float(c)!=0 else 1
                fa,fb,fc = float(a), float(b), float(c)
                expr = f"{num_str(a)} / x = {num_str(b)} / {num_str(c)}"
                ans = (fa * fc) / fb
            else:
                a,b,c = [random_number() for _ in range(3)]
                b = b if float(b)!=0 else 1
                fa,fb,fc = float(a), float(b), float(c)
                expr = f"(x + {num_str(a)}) / {num_str(b)} = {num_str(c)}"
                ans = (fc * fb) - fa
        return expr, round(ans,6)

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        try:
            with open("leaderboard.json","r",encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_leaderboard(data):
    with open("leaderboard.json","w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

css = load_font_css("SJ Pancake Pen.ttf", "SJ Pancake Pen")
if css:
    st.markdown(css, unsafe_allow_html=True)

load_audio_b64("correct.mp3")
load_audio_b64("wrong.mp3")
music_data, music_mime = load_audio_bytes("your_song.mp3")

if "screen" not in st.session_state: st.session_state.screen = "start"
if "questions" not in st.session_state: st.session_state.questions = []
if "index" not in st.session_state: st.session_state.index = 0
if "correct" not in st.session_state: st.session_state.correct = 0
if "start_time" not in st.session_state: st.session_state.start_time = 0
if "player" not in st.session_state: st.session_state.player = ""
if "mode" not in st.session_state: st.session_state.mode = ""
if "difficulty" not in st.session_state: st.session_state.difficulty = ""
if "num_questions" not in st.session_state: st.session_state.num_questions = 0
if "answered" not in st.session_state: st.session_state.answered = False
if "play_sfx" not in st.session_state: st.session_state.play_sfx = None
if "music_on" not in st.session_state: st.session_state.music_on = True
if "seed" not in st.session_state: st.session_state.seed = None

container = st.container()
with container:
    st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)

placeholder = st.empty()

if st.session_state.screen == "start":
    with placeholder.container():
        st.title("📘 Quiz Toán")
        cols = st.columns([3,1])
        with cols[0]:
            name = st.text_input("Tên người chơi")
            mode = st.selectbox("Chế độ", ["Số hữu tỉ","Tìm x"])
            level = st.selectbox("Độ khó", ["Rất Dễ","Dễ","Bình Thường","Khó","Rất Khó"])
            num_q = st.number_input("Số câu", min_value=1, max_value=30, value=5)
        with cols[1]:
            seed_input = st.text_input("Seed (để lặp lại phiên)", value="")
            if seed_input and st.button("Áp dụng seed"):
                try:
                    st.session_state.seed = int(seed_input)
                except:
                    st.session_state.seed = sum(ord(c) for c in seed_input)
                st.success("Seed đã được đặt")
        if st.button("Bắt đầu") and name.strip():
            st.session_state.player = name.strip()
            st.session_state.mode = mode
            st.session_state.difficulty = level
            st.session_state.num_questions = num_q
            if st.session_state.seed is not None:
                random.seed(st.session_state.seed)
            st.session_state.questions = [generate_question(mode, level) for _ in range(num_q)]
            st.session_state.index = 0
            st.session_state.correct = 0
            st.session_state.start_time = time.time()
            st.session_state.screen = "quiz"
            st.session_state.answered = False
            st.session_state.play_sfx = None
            st.rerun()

elif st.session_state.screen == "quiz":
    if st.session_state.play_sfx:
        if st.session_state.play_sfx == "correct":
            play_audio_sfx("correct.mp3")
            st.success("✅ Chính xác!")
        elif st.session_state.play_sfx == "wrong":
            play_audio_sfx("wrong.mp3")
            st.error(f"❌ Sai!")
        st.session_state.play_sfx = None

    with placeholder.container():
        idx = st.session_state.index
        if idx >= len(st.session_state.questions):
            st.session_state.screen = "result"
            st.rerun()
        q, ans = st.session_state.questions[idx]
        st.subheader(f"Câu {idx+1}/{st.session_state.num_questions}")
        st.markdown(f"**Người chơi:** {st.session_state.player}  ·  **Chế độ:** {st.session_state.mode}  ·  **Độ khó:** {st.session_state.difficulty}")
        progress = int((idx / st.session_state.num_questions) * 100)
        st.progress(progress)
        q_latex = str(q).replace("x", r" \mathbf{x} ").replace("*", r"\times").replace("sqrt", r"\sqrt").replace("**2", "^2")
        q_latex = re.sub(r"\((-?\d+)/(\d+)\)", r"\\frac{\1}{\2}", q_latex)
        q_latex = re.sub(r"(-?\d+)/(\d+)", r"\\frac{\1}{\2}", q_latex)
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.latex(q_latex)
        if st.session_state.mode == "Tìm x":
            user_ans_str = st.text_input("Nhập đáp án (x = ?):", key=f"q_{idx}")
        else:
            user_ans_str = st.text_input("Nhập đáp án:", key=f"q_{idx}")
        st.markdown("</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        if not st.session_state.answered:
            with col_a:
                if st.button("Trả lời", key=f"btn_{idx}"):
                    if user_ans_str:
                        try:
                            if "/" in user_ans_str:
                                ua = float(Fraction(user_ans_str))
                            else:
                                ua = float(user_ans_str.replace(",", "."))
                            if abs(float(ans) - ua) < 1e-6:
                                st.session_state.correct += 1
                                st.session_state.play_sfx = "correct"
                            else:
                                st.session_state.play_sfx = "wrong"
                        except Exception:
                            st.error("⚠️ Đáp án không hợp lệ.")
                            st.session_state.play_sfx = "wrong"
                        st.session_state.answered = True
                        st.rerun()
                    else:
                        st.warning("Vui lòng nhập đáp án!")
            with col_b:
                if st.button("Bỏ qua", key=f"skip_{idx}"):
                    st.info("Đã bỏ qua câu này")
                    st.session_state.answered = True
                    st.session_state.play_sfx = None
                    st.rerun()
        else:
            st.markdown("---")
            if st.session_state.index < st.session_state.num_questions - 1:
                if st.button("Câu tiếp theo ➡️", key=f"next_{idx}"):
                    st.session_state.index += 1
                    st.session_state.answered = False
                    st.rerun()
            else:
                if st.button("🏁 Xem kết quả", key=f"result_{idx}"):
                    st.session_state.screen = "result"
                    st.rerun()

elif st.session_state.screen == "result":
    with placeholder.container():
        st.balloons()
        st.title("🎉 Kết quả")
        total_time = time.time() - st.session_state.start_time
        avg_time = total_time / max(1, st.session_state.num_questions)
        st.metric("Điểm số", f"{st.session_state.correct}/{st.session_state.num_questions}")
        st.metric("Tổng thời gian (s)", f"{total_time:.2f}")
        st.metric("Thời gian trung bình (s/câu)", f"{avg_time:.2f}")
        leaderboard = load_leaderboard()
        key = f"{st.session_state.mode} ({st.session_state.difficulty})"
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
        st.subheader(f"🏆 Bảng xếp hạng: {key}")
        rows = []
        for i, entry in enumerate(leaderboard[key], 1):
            emoji = "🏅" if i==1 else "🥈" if i==2 else "🥉" if i==3 else ""
            rows.append({"#": f"{i} {emoji}", "Tên": entry["player"], "Điểm": f"{entry['score']}/{entry['total']}", "Thời gian (s)": f"{entry['time']:.2f}"})
        st.table(rows)
        cols = st.columns(3)
        with cols[0]:
            if st.button("🔁 Chơi lại"):
                st.session_state.screen = "start"
                st.session_state.questions = []
                st.session_state.index = 0
                st.session_state.correct = 0
                st.session_state.answered = False
                st.session_state.play_sfx = None
                st.rerun()
        with cols[1]:
            if st.button("🏠 Trang chủ"):
                st.session_state.screen = "start"
                st.session_state.questions = []
                st.session_state.index = 0
                st.session_state.correct = 0
                st.session_state.answered = False
                st.session_state.play_sfx = None
                st.rerun()
        with cols[2]:
            if st.button("📁 Xuất JSON"):
                fname = f"result_{st.session_state.player}_{int(time.time())}.json"
                with open(fname, "w", encoding="utf-8") as f:
                    json.dump({"player": st.session_state.player, "score": st.session_state.correct, "total": st.session_state.num_questions, "time": total_time}, f, ensure_ascii=False, indent=2)
                with open(fname, "rb") as f:
                    st.download_button("Tải kết quả (.json)", f, file_name=fname)
