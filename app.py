import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from canvas_bench import interactive_bench
import physics as phys

st.set_page_config(page_title="Віртуальна ЛР: Розширення меж приладів", layout="wide")
st.title("🔌 Віртуальна лабораторна робота")
st.subheader("«Розширення меж вимірювання амперметра і вольтметра»")

# Ініціалізація сесії для таблиць
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
    st.info("🔌 Тягніть дроти мишкою від клеми до клеми на інтерактивному стенді нижче. Видалення дроту — Клік правою кнопкою миші.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Наш роскошный интерактивный стенд без желтых окон!
        interactive_bench("stage1", key="bench_s1")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        # Чтобы обойти блокировки обмена данными, даем студенту возможность регулировать R1 на панели
        r1_val = st.slider("🎛️ Ручка потенціометра R1 (Ом)", 0, 5000, 2500, key="r1_s1")
        is_wire_correct = st.checkbox("⚙️ Я з'єднав ланцюг послідовно (Повзунок R1 -> μA -> R2 -> ЕП)", value=False)
        
        st.markdown("---")
        if is_wire_correct:
            # Математический расчет из физического движка
            total_R = 1000.0 + 4000.0 + r1_val
            current_I = (5.0 / total_R) * 1e6
            n_div = (current_I / 50.0) * 50.0
            
            st.success("🟢 Ланцюг замкнено! Струм подано.")
            st.metric("Еталон В7-21А (Струм)", f"{current_I:.2f} мкА")
            st.metric("Мікроамперметр", f"{n_div:.1f} поділок")
        else:
            st.warning("🔌 Схема знеструмлена. Зберіть дроти на стенді та підтвердіть з'єднання.")
            current_I, n_div = 0.0, 0.0

        add_point = st.button("📥 Записати точку в таблицю", key="btn_add_s1")
        if add_point and is_wire_correct:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div, 1), "I (мкА)": round(current_I, 2)}])
            st.session_state.data_stage1 = pd.concat([st.session_state.data_stage1, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage1, use_container_width=True)

# ВКЛАДКА 2
with tab2:
    st.markdown("### Складіть схему з шунтом за Рис. 1.7")
    col1, col2 = st.columns([2, 1])
    with col1:
        interactive_bench("stage2", key="bench_s2")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        r1_val_s2 = st.slider("🎛️ Ручка потенціометра R1 (Ом)", 0, 1000, 500, key="r1_s2")
        is_wire_correct_s2 = st.checkbox("⚙️ Шунт підключено паралельно мікроамперметру", value=False)
        
        st.markdown("---")
        if is_wire_correct_s2:
            R_parallel = (1000.0 * 111.11) / (1000.0 + 111.11)
            total_R = R_parallel + 4000.0 + r1_val_s2
            total_I = (5.0 / total_R) * 1e6
            I_micro = total_I * (111.11 / (1000.0 + 111.11))
            n_div_s2 = (I_micro / 50.0) * 50.0
            
            if I_micro > 55.0:
                st.error("🚨 ЗАШКАЛЮВАННЯ! Збільшіть опір R1.")
                n_div_s2 = 50.0
            else:
                st.success("🟢 Схема розширення меж активована!")
            st.metric("Еталон В7-21А (Загальний струм)", f"{total_I:.2f} мкА")
            st.metric("Мікроамперметр", f"{n_div_s2:.1f} поділок")
        else:
            st.warning("🔌 Перевірте паралельність шунта на стенді.")
            total_I, n_div_s2 = 0.0, 0.0
            
        add_point_s2 = st.button("📥 Записати точку в таблицю", key="btn_add_s2")
        if add_point_s2 and is_wire_correct_s2:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div_s2, 1), "I (мкА)": round(total_I, 2)}])
            st.session_state.data_stage2 = pd.concat([st.session_state.data_stage2, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage2, use_container_width=True)

# ВКЛАДКА 3
with tab3:
    st.markdown("### Складіть схему для вольтметра за Рис. 1.8")
    col1, col2 = st.columns([2, 1])
    with col1:
        interactive_bench("stage3", key="bench_s3")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        r1_val_s3 = st.slider("🎛️ Ручка потенціометра R1 (Ом)", 0, 3000, 1500, key="r1_s3")
        is_wire_correct_s3 = st.checkbox("⚙️ Добавочний R2 підключено послідовно, ЕП — паралельно", value=False)
        
        st.markdown("---")
        if is_wire_correct_s3:
            R_voltmeter = 1000.0 + 4000.0
            total_R = r1_val_s3 + R_voltmeter
            I_circuit = 5.0 / total_R
            U_mv = (I_circuit * R_voltmeter) * 1000.0
            n_div_s3 = ((I_circuit * 1e6) / 50.0) * 50.0
            
            st.success("🟢 Схема вольтметра працює стабільно!")
            st.metric("Еталон В7-21А (Напруга)", f"{U_mv:.1f} мВ")
            st.metric("Мікроамперметр", f"{n_div_s3:.1f} поділок")
        else:
            st.warning("🔌 Зберіть послідовний ланцюг вольтметра.")
            U_mv, n_div_s3 = 0.0, 0.0
            
        add_point_s3 = st.button("📥 Записати точку в таблицю", key="btn_add_s3")
        if add_point_s3 and is_wire_correct_s3:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div_s3, 1), "U (мВ)": round(U_mv, 1)}])
            st.session_state.data_stage3 = pd.concat([st.session_state.data_stage3, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage3, use_container_width=True)

# ГРАФІКІВ (ЗНИЗУ)
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
