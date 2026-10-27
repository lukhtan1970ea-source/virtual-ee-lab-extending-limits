import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.canvas_bench import interactive_bench
import physics as phys

st.set_page_config(page_title="Віртуальна ЛР: Розширення меж приладів", layout="wide")
st.title("🔌 Віртуальна лабораторна робота")
st.subheader("«Розширення меж вимірювання амперметра і вольтметра»")

# Ініціалізація сесії для таблиць досліджень
if "data_stage1" not in st.session_state:
    st.session_state.data_stage1 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
if "data_stage2" not in st.session_state:
    st.session_state.data_stage2 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
if "data_stage3" not in st.session_state:
    st.session_state.data_stage3 = pd.DataFrame(columns=["n (поділки)", "U (мВ)"])

tab1, tab2, tab3 = st.tabs([
    "📊 1. Градуювання мікроамперметра", 
    "⚡ 2. Розширення межі амперметра", 
    "🔌 3. Градуювання вольтметра"
])

# ВКЛАДКА 1
with tab1:
    st.markdown("### Складіть схему за Рис. 1.6")
    col1, col2 = st.columns(2)
    with col1:
        bench_data = interactive_bench("stage1", key="bench_s1")
    wires = bench_data.get("wires", []) if bench_data else []
    angle = bench_data.get("knobAngle", 0.0) if bench_data else 0.0
    res = phys.calculate_stage1(wires, angle)
    
    with col2:
        st.markdown("#### 📟 Стан приладів")
        if len(wires) == 0:
            st.warning("🔌 Схема знеструмлена. Натягніть дроти мишкою.")
        elif res["status"] == "ok":
            st.success("🟢 Схема зібрана ПРАВИЛЬНО!")
            st.metric("Еталон В7-21А (Струм)", f"{res['I']:.2f} мкА")
            st.metric("Мікроамперметр", f"{res['n']:.1f} поділок")
        elif res["status"] == "short":
            st.error("🚨 КОРОТКЕ ЗАМИКАННЯ! Спрацював захист джерела.")
        else:
            st.error("🔴 Помилка у схемі! Перевірте з'єднання за Рис. 1.6.")
            
        add_point = st.button("📥 Записати точку в таблицю", key="btn_add_s1")
        if add_point and res["status"] == "ok":
            new_row = pd.DataFrame([{"n (поділки)": round(res["n"], 1), "I (мкА)": round(res["I"], 2)}])
            st.session_state.data_stage1 = pd.concat([st.session_state.data_stage1, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage1, use_container_width=True)

# ВКЛАДКА 2
with tab2:
    st.markdown("### Складіть схему з шунтом за Рис. 1.7")
    col1, col2 = st.columns(2)
    with col1:
        bench_data_s2 = interactive_bench("stage2", key="bench_s2")
    wires_s2 = bench_data_s2.get("wires", []) if bench_data_s2 else []
    angle_s2 = bench_data_s2.get("knobAngle", 0.0) if bench_data_s2 else 0.0
    res_s2 = phys.calculate_stage2(wires_s2, angle_s2)
    
    with col2:
        st.markdown("#### 📟 Стан приладів")
        if len(wires_s2) == 0:
            st.warning("🔌 Схема знеструмлена.")
        elif res_s2["status"] in ["ok", "overload"]:
            if res_s2["status"] == "overload":
                st.error("🚨 ЗАШКАЛЮВАННЯ! Зменшіть струм ручкою R1.")
            else:
                st.success("🟢 Схема розширення меж зібрана вірно!")
            st.metric("Еталон В7-21А (Загальний струм)", f"{res_s2['I']:.2f} мкА")
            st.metric("Мікроамперметр", f"{res_s2['n']:.1f} поділок")
        else:
            st.error("🔴 Помилка. Перевірте паралельність шунта за Рис. 1.7.")
            
        add_point_s2 = st.button("📥 Записати точку в таблицю", key="btn_add_s2")
        if add_point_s2 and res_s2["status"] in ["ok", "overload"]:
            new_row = pd.DataFrame([{"n (поділки)": round(res_s2["n"], 1), "I (мкА)": round(res_s2["I"], 2)}])
            st.session_state.data_stage2 = pd.concat([st.session_state.data_stage2, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage2, use_container_width=True)

# ВКЛАДКА 3
with tab3:
    st.markdown("### Складіть схему для вольтметра за Рис. 1.8")
    col1, col2 = st.columns(2)
    with col1:
        bench_data_s3 = interactive_bench("stage3", key="bench_s3")
    wires_s3 = bench_data_s3.get("wires", []) if bench_data_s3 else []
    angle_s3 = bench_data_s3.get("knobAngle", 0.0) if bench_data_s3 else 0.0
    res_s3 = phys.calculate_stage3(wires_s3, angle_s3)
    
    with col2:
        st.markdown("#### 📟 Стан приладів")
        if len(wires_s3) == 0:
            st.warning("🔌 Схема знеструмлена.")
        elif res_s3["status"] == "ok":
            st.success("🟢 Схема вольтметра зібрана ПРАВИЛЬНО!")
            st.metric("Еталон В7-21А (Напруга)", f"{res_s3['U']:.1f} мВ")
            st.metric("Мікроамперметр", f"{res_s3['n']:.1f} поділок")
        else:
            st.error("🔴 Помилка. Перевірте добавочний опір R2 та Еталон за Рис. 1.8.")
            
        add_point_s3 = st.button("📥 Записати точку в таблицю", key="btn_add_s3")
        if add_point_s3 and res_s3["status"] == "ok":
            new_row = pd.DataFrame([{"n (поділки)": round(res_s3["n"], 1), "U (мВ)": round(res_s3["U"], 1)}])
            st.session_state.data_stage3 = pd.concat([st.session_state.data_stage3, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage3, use_container_width=True)

# ЗОНА ГРАФІКІВ (ЗНИЗУ)
st.markdown("---")
st.markdown("### 📈 Градуювальні графіки")
g_col1, g_col2 = st.columns(2)
with g_col1:
    if not st.session_state.data_stage1.empty:
        fig1 = go.Figure(go.Scatter(x=st.session_state.data_stage1["I (мкА)"], y=st.session_state.data_stage1["n (поділки)"], mode='markers+lines', line=dict(color='red')))
        fig1.update_layout(title="Градуювальний графік мікроамперметра", xaxis_title="I, мкА", yaxis_title="n, поділки")
        st.plotly_chart(fig1, use_container_width=True)
with g_col2:
    if not st.session_state.data_stage3.empty:
        fig3 = go.Figure(go.Scatter(x=st.session_state.data_stage3["U (мВ)"], y=st.session_state.data_stage3["n (поділки)"], mode='markers+lines', line=dict(color='blue')))
        fig3.update_layout(title="Градуювальний графік вольтметра", xaxis_title="U, мв", yaxis_title="n, поділки")
        st.plotly_chart(fig3, use_container_width=True)

