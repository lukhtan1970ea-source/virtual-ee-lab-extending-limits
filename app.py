import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Налаштування сторінки
st.set_page_config(page_title="Віртуальна ЛР: Розширення меж приладів", layout="wide")

st.title("🔌 Віртуальна лабораторна робота")
st.subheader("«Розширення меж вимірювання амперметра і вольтметра»")

# Фізичні константи (номінали приладів)
I_0 = 50.0      # Максимальний струм мікроамперметра (мкА)
R_0 = 1000.0    # Внутрішній опір мікроамперметра (Ом)
R_2 = 4000.0    # Добавочний опір / навантаження (Ом)
R_sh = 111.11   # Опір шунта для розширення межі в 10 разів (k=10)
U_source = 5.0  # Напруга джерела живлення (В)

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

# Спільна функція для малювання гарного SVG-схематичного стенду
def draw_svg_circuit(stage):
    if stage == 1:
        img_url = "https://icons8.com" # Заглушка, або малюємо просту схему текстом
        st.code(" [Джерело +] ----> [Регулятор R1] ----> [μA +] \n                                     | \n [Джерело -] <---- [Еталон ЕП] <---- [R2] <---- [μA -]", language="text")
    elif stage == 2:
        st.code(" [Джерело +] ----> [Регулятор R1] ----> [μA +] <==> [Шунт Rш] \n                                     |             | \n [Джерело -] <---- [Еталон ЕП] <---- [R2] <======== [μA -]", language="text")
    else:
        st.code(" [Джерело +] ----> [Регулятор R1] ----> [μA +] ----> [R2] \n                                                   | \n [Джерело -] <==================================== [R2 вихід] \n               ^                                   | \n               |======== [ Еталон В7-21А ] ========", language="text")

# ==========================================
# ВКЛАДКА 1: ГРАДУЮВАННЯ МІКРОАМПЕРМЕТРА
# ==========================================
with tab1:
    st.markdown("### 🛠️ Крок 1: Збирання кола (Рис. 1.6)")
    draw_svg_circuit(1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔌 Віртуальні комутації")
        wire_1 = st.checkbox("З'єднати Джерело(+) з Регулятором R1", key="w1_1")
        wire_2 = st.checkbox("З'єднати Повзунок R1 з мікроамперметром(μA+)", key="w1_2")
        wire_3 = st.checkbox("З'єднати μA(-) з Резистором R2", key="w1_3")
        wire_4 = st.checkbox("З'єднати Резистор R2 з Входом Еталона ЕП", key="w1_4")
        wire_5 = st.checkbox("Замикнути ЕП(Спільний) на Джерело(-)", key="w1_5")
        
        st.markdown("---")
        r1_knob = st.slider("🎛️ Ручка регулятора R1 (Опір)", min_value=0, max_value=5000, value=2500, step=100, key="k1")

    is_correct_1 = wire_1 and wire_2 and wire_3 and wire_4 and wire_5

    with col2:
        st.markdown("#### 📟 Стан приладів")
        if not (wire_1 or wire_2 or wire_3 or wire_4 or wire_5):
            st.warning("🔌 Схема повністю знеструмлена. Почніть з'єднувати контакти.")
        elif is_correct_1:
            total_R = R_0 + R_2 + r1_knob
            current_I = (U_source / total_R) * 1e6
            n_div = (current_I / I_0) * 50.0
            
            st.success("🟢 Схема зібрана ПРАВИЛЬНО! Струм іде.")
            st.metric("📟 Еталон В7-21А (Струм)", f"{current_I:.2f} мкА")
            st.metric("🎯 Мікроамперметр", f"{n_div:.1f} поділок")
        else:
            st.error("🔴 Ланцюг розірвано або підключено невірно. Перевірте всі прапорці з'єднань за Рис. 1.6!")
            current_I, n_div = 0.0, 0.0

        st.markdown("---")
        if st.button("📥 Записати точку в таблицю", key="btn_s1") and is_correct_1:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div, 1), "I (мкА)": round(current_I, 2)}])
            st.session_state.data_stage1 = pd.concat([st.session_state.data_stage1, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage1, use_container_width=True)

# ==========================================
# ВКЛАДКА 2: РОЗШИРЕННЯ МЕЖІ АМПЕРМЕТРА
# ==========================================
with tab2:
    st.markdown("### 🛠️ Крок 2: Підключення шунта (Рис. 1.7)")
    draw_svg_circuit(2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔌 Віртуальні комутації")
        w2_1 = st.checkbox("З'єднати Джерело(+) з Регулятором R1", key="w2_1")
        w2_shunt = st.checkbox("🪛 Підключити Шунт Rш ПАРАЛЕЛЬНО до мікроамперметра", key="w2_sh")
        w2_3 = st.checkbox("З'єднати вихід приладів з Резистором R2", key="w2_3")
        w2_4 = st.checkbox("З'єднати Резистор R2 з Входом Еталона ЕП", key="w2_4")
        w2_5 = st.checkbox("Замикнути ланцюг на Джерело(-)", key="w2_5")
        
        st.markdown("---")
        r1_knob_s2 = st.slider("🎛️ Ручка регулятора R1 (Опір)", min_value=0, max_value=1000, value=500, step=50, key="k2")

    is_correct_2 = w2_1 and w2_shunt and w2_3 and w2_4 and w2_5

    with col2:
        st.markdown("#### 📟 Стан приладів")
        if is_correct_2:
            R_parallel = (R_0 * R_sh) / (R_0 + R_sh)
            total_R = R_parallel + R_2 + r1_knob_s2
            total_I = (U_source / total_R) * 1e6
            I_micro = total_I * (R_sh / (R_0 + R_sh))
            n_div_s2 = (I_micro / I_0) * 50.0
            
            if I_micro > I_0 + 2:
                st.error("🚨 ЗАШКАЛЮВАННЯ! Струм перевищує межу мікроамперметра! Збільшіть опір R1.")
                n_div_s2 = 50.0
            else:
                st.success("🟢 Межу амперметра успішно розширено в 10 разів!")
                
            st.metric("📟 Еталон В7-21А (Загальний струм кола)", f"{total_I:.2f} мкА")
            st.metric("🎯 Показання мікроамперметра", f"{n_div_s2:.1f} поділок")
        else:
            st.error("🔴 Помилка у схемі. Перевірте, чи підключено шунт паралельно приладу за Рис. 1.7.")
            total_I, n_div_s2 = 0.0, 0.0

        st.markdown("---")
        if st.button("📥 Записати точку в таблицю", key="btn_s2") and is_correct_2:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div_s2, 1), "I (мкА)": round(total_I, 2)}])
            st.session_state.data_stage2 = pd.concat([st.session_state.data_stage2, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage2, use_container_width=True)

# ==========================================
# ВКЛАДКА 3: ГРАДУЮВАННЯ ВОЛЬТМЕТРА
# ==========================================
with tab3:
    st.markdown("### 🛠️ Крок 3: Трансформація у Вольтметр (Рис. 1.8)")
    draw_svg_circuit(3)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔌 Віртуальні комутації")
        w3_1 = st.checkbox("З'єднати регулятор R1 з Джерелом", key="w3_1")
        w3_2 = st.checkbox("🪛 Підключити Резистор R2 ПОСЛІДОВНО до μA (Добавочний опір)", key="w3_2")
        w3_ep = st.checkbox("📟 Підключити Еталон ЕП ПАРАЛЕЛЬНО до всієї конструкції (точки a-b)", key="w3_ep")
        
        st.markdown("---")
        r1_knob_s3 = st.slider("🎛️ Ручка регулятора R1 (Опір)", min_value=0, max_value=3000, value=1500, step=100, key="k3")

    is_correct_3 = w3_1 and w3_2 and w3_ep

    with col2:
        st.markdown("#### 📟 Стан приладів")
        if is_correct_3:
            R_voltmeter = R_0 + R_2
            total_R = r1_knob_s3 + R_voltmeter
            I_circuit = U_source / total_R
            U_mv = (I_circuit * R_voltmeter) * 1000.0
            n_div_s3 = ((I_circuit * 1e6) / I_0) * 50.0
            
            st.success("🟢 Схема вольтметра працює стабільно!")
            st.metric("📟 Еталон В7-21А (Напруга)", f"{U_mv:.1f} мВ")
            st.metric("🎯 Мікроамперметр", f"{n_div_s3:.1f} поділок")
        else:
            st.error("🔴 Схема вольтметра не зібрана. Перевірте послідовність R2 та паралельність Еталона.")
            U_mv, n_div_s3 = 0.0, 0.0

        st.markdown("---")
        if st.button("📥 Записати точку в таблицю", key="btn_s3") and is_correct_3:
            new_row = pd.DataFrame([{"n (поділки)": round(n_div_s3, 1), "U (мВ)": round(U_mv, 1)}])
            st.session_state.data_stage3 = pd.concat([st.session_state.data_stage3, new_row], ignore_index=True)
        st.dataframe(st.session_state.data_stage3, use_container_width=True)

# ЗОНА ГРАФІКІВ (ЗНИЗУ)
st.markdown("---")
st.markdown("### 📈 Автоматичні градуювальні графіки")
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
