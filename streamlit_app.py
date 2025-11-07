import csv
import io
import random
import time
import streamlit as st


def roll_dice(count: int, sides: int) -> list:
    """주사위를 굴려 결과 리스트를 반환합니다."""
    return [random.randint(1, sides) for _ in range(count)]


st.set_page_config(page_title="주사위 굴리기", page_icon="🎲")
st.title("주사위 굴리기 �")
st.write("원하는 설정으로 주사위를 굴려볼 수 있는 간단한 앱입니다.")

# 사이드바: 설정
with st.sidebar:
    st.header("설정")
    count = st.number_input("굴릴 주사위 개수", min_value=1, max_value=10, value=2, step=1)
    sides = st.selectbox("주사위 면 수", options=[4, 6, 8, 10, 12, 20], index=1)
    animate = st.checkbox("굴릴 때 간단한 애니메이션", value=True)
    keep_history = st.checkbox("세션에 기록 남기기", value=True)

# 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("굴리기"):
        if animate:
            placeholder = st.empty()
            for i in range(6):
                placeholder.markdown(f"**굴리는 중{'.' * (i % 4)}**")
                time.sleep(0.08)
            placeholder.empty()

        rolls = roll_dice(count, sides)
        total = sum(rolls)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = {"time": timestamp, "sides": sides, "rolls": rolls, "sum": total}
        if keep_history:
            st.session_state.history.insert(0, entry)

        st.metric("합계", total)
        cols = st.columns(len(rolls))
        for i, r in enumerate(rolls):
            cols[i].markdown(f"### 🎲 {r}")

with col2:
    if st.button("기록 초기화"):
        st.session_state.history = []
        st.experimental_rerun()

st.markdown("---")
st.subheader("세션 기록")
if not st.session_state.history:
    st.info("기록이 없습니다. '굴리기' 버튼을 눌러 기록을 만들어보세요.")
else:
    for e in st.session_state.history[:50]:
        st.write(f"{e['time']} — {e['sides']}면 x{len(e['rolls'])} → {e['rolls']} (합: {e['sum']})")

    # CSV로 내보내기
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(["time", "sides", "count", "rolls", "sum"])
    for e in st.session_state.history:
        writer.writerow([e["time"], e["sides"], len(e["rolls"]), " ".join(map(str, e["rolls"])), e["sum"]])
    st.download_button("CSV로 내보내기", data=csv_buf.getvalue().encode("utf-8"), file_name="dice_history.csv", mime="text/csv")

    # 간단한 통계
    sums = [e["sum"] for e in st.session_state.history]
    st.write(f"기록 수: {len(sums)} — 평균 합: {sum(sums)/len(sums):.2f}")

