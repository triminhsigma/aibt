import streamlit as st
from fractions import Fraction
import random, time, json, os, base64, sys

def local_font(path, name="CustomFont"):
    if hasattr(sys, "_MEIPASS"):
        path = os.path.join(sys._MEIPASS, path)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"""
        <style>
        @font-face {{ font-family: '{name}'; src: url(data:font/ttf;base64,{b64}) format('truetype'); }}
        * {{ font-family: '{name}', sans-serif !important; }}
        </style>
        """
    return ""

st.set_page_config(page_title="Quiz Toán", layout="centered")
st.markdown(local_font("SJ Pancake Pen.ttf", "PancakePen"), unsafe_allow_html=True)
st.title("📘 Quiz Toán")

for key, default in {
    "started": False, "player_name": "", "dokho": "Rất Dễ", "so_cau": 10,
    "index": 0, "so_dung": 0, "start_time": None, "cauhoi": None, "dap_an": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def rand_nonzero(a,b):
    n=0
    while n==0:
        n=random.randint(a,b)
    return n

def _apply_op(x:Fraction, op:str, y:Fraction):
    if op=="+": return x+y
    if op=="-": return x-y
    if op=="*": return x*y
    if op=="/": return x/y if y!=0 else Fraction(0)
    return x

def tao_cau_hoi(dokho):
    if dokho=="Rất Dễ":
        a,b=random.randint(1,10),random.randint(1,10)
        op="+"
    elif dokho=="Dễ":
        a,b=random.randint(1,20),random.randint(1,20)
        op=random.choice(["+","-"])
    elif dokho=="Bình Thường":
        a,b=random.randint(1,50),random.randint(1,50)
        op=random.choice(["+","-","*"])
    elif dokho=="Khó":
        a,b=random.randint(1,100),rand_nonzero(1,100)
        op=random.choice(["+","-","*","/"])
    else:
        a,b=random.randint(1,200),rand_nonzero(1,200)
        op=random.choice(["+","-","*","/"])
    expr=f"{a}{op}{b}=?"
    result=_apply_op(Fraction(a),op,Fraction(b))
    return expr,result

def parse_answer(ans):
    try:
        if "/" in ans: return Fraction(ans)
        return Fraction(float(ans)).limit_denominator(10000)
    except: return None

HS_FILE="highscores.json"

def save_highscore(score, so_cau, total_time, avg_time, difficulty, player_name):
    highscores=[]
    if os.path.exists(HS_FILE):
        try: highscores=json.load(open(HS_FILE,"r",encoding="utf-8"))
        except: highscores=[]
    highscores.append({
        "player":player_name,
        "score":score,
        "total_questions":so_cau,
        "total_time":round(total_time,2),
        "avg_time":round(avg_time,2),
        "difficulty":difficulty
    })
    with open(HS_FILE,"w",encoding="utf-8") as f:
        json.dump(highscores,f,indent=2,ensure_ascii=False)

def get_highscore_text(difficulty):
    if not os.path.exists(HS_FILE): return "Chưa có điểm cao."
    try:
        highscores=json.load(open(HS_FILE,"r",encoding="utf-8"))
        f=[x for x in highscores if x["difficulty"]==difficulty]
        if not f: return f"Chưa có điểm cao cho {difficulty}."
        f=sorted(f,key=lambda x:(-x["score"],x["avg_time"]))[:3]
        return "🏆 Top 3\n"+"\n".join(
            f"{i+1}. {e['player']} | {e['score']}/{e['total_questions']} | TG:{e['total_time']}s | TB:{e['avg_time']}s"
            for i,e in enumerate(f))
    except: return "Không thể đọc bảng điểm."

def get_player_progress(player_name):
    if not os.path.exists(HS_FILE): return "Chưa có tiến trình nào."
    try:
        highscores=json.load(open(HS_FILE,"r",encoding="utf-8"))
        f=[x for x in highscores if x["player"]==player_name]
        if not f: return "Chưa có tiến trình nào."
        f=sorted(f,key=lambda x:(-x["score"],x["avg_time"]))[:5]
        return f"📊 Tiến trình 5 lần chơi tốt nhất của {player_name}\n"+"\n".join(
            f"{i+1}. {e['score']}/{e['total_questions']} | TG:{e['total_time']}s | TB:{e['avg_time']}s"
            for i,e in enumerate(f))
    except: return "Không thể đọc tiến trình người chơi."

if not st.session_state.started:
    player_name = st.text_input("Nhập tên người chơi:", st.session_state.player_name)
    dokho = st.selectbox("Chọn độ khó", ["Rất Dễ","Dễ","Bình Thường","Khó","Rất Khó"], index=["Rất Dễ","Dễ","Bình Thường","Khó","Rất Khó"].index(st.session_state.dokho))
    so_cau = st.number_input("Số câu", min_value=1, max_value=50, value=st.session_state.so_cau)
    if st.button("Bắt đầu"):
        if player_name.strip():
            st.session_state.started=True
            st.session_state.player_name=player_name
            st.session_state.dokho=dokho
            st.session_state.so_cau=so_cau
            st.session_state.index=0
            st.session_state.so_dung=0
            st.session_state.start_time=time.time()
            st.session_state.cauhoi,st.session_state.dap_an=tao_cau_hoi(dokho)
        else:
            st.warning("Vui lòng nhập tên!")

if st.session_state.started and st.session_state.index < st.session_state.so_cau:
    st.subheader(f"Câu {st.session_state.index+1}/{st.session_state.so_cau}")
    st.write(st.session_state.cauhoi)
    ans = st.text_input("Nhập đáp án", key=f"ans_input_{st.session_state.index}", value="")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Trả lời", key=f"btn_{st.session_state.index}_ok"):
            parsed = parse_answer(ans)
            if parsed is not None:
                if parsed == st.session_state.dap_an:
                    st.success("🎉 Đúng!")
                    st.session_state.so_dung += 1
                else:
                    st.error(f"❌ Sai. Đáp án đúng: {st.session_state.dap_an}")
                st.session_state.index += 1
                if st.session_state.index < st.session_state.so_cau:
                    st.session_state.cauhoi, st.session_state.dap_an = tao_cau_hoi(st.session_state.dokho)

    with c2:
        if st.button("⏭️ Bỏ qua", key=f"btn_{st.session_state.index}_skip"):
            st.info(f"Đáp án là: {st.session_state.dap_an}")
            st.session_state.index += 1
            if st.session_state.index < st.session_state.so_cau:
                st.session_state.cauhoi, st.session_state.dap_an = tao_cau_hoi(st.session_state.dokho)

if st.session_state.started and st.session_state.index >= st.session_state.so_cau:
    total_elapsed = time.time() - st.session_state.start_time
    avg_time = total_elapsed / st.session_state.so_cau
    diem10 = round((st.session_state.so_dung / st.session_state.so_cau) * 10, 2)
    st.success(f"Hết Quiz! Điểm:{diem10}/10 | Đúng:{st.session_state.so_dung}/{st.session_state.so_cau}")
    st.write(f"Tổng TG:{total_elapsed:.2f}s | TG TB:{avg_time:.2f}s")
    save_highscore(diem10, st.session_state.so_cau, total_elapsed, avg_time, st.session_state.dokho, st.session_state.player_name)
    st.markdown("---")
    st.markdown(get_highscore_text(st.session_state.dokho))
    st.markdown(get_player_progress(st.session_state.player_name))
    if st.button("🔄 Chơi lại"):
        st.session_state.update({
            "started": False,
            "index": 0,
            "so_dung": 0,
            "start_time": None,
            "cauhoi": None,
            "dap_an": None,
            "player_name": "",
            "dokho": "Rất Dễ"
        })
