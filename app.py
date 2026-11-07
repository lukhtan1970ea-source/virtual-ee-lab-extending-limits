import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from canvas_bench import interactive_bench

st.set_page_config(page_title="Віртуальна ЛР: Розширення меж приладів", layout="wide")
st.title("🔌 Віртуальна лабораторна робота")

# Блокування клавіатури ВИКЛЮЧНО для полів делінь шкали "n"
st.markdown(
    """
    <style>
    /* Шукаємо блок інпута, який стоїть одразу після заголовка зі словом "мікроамперметра" */
    div[data-testid="stNumberInput"]:has(label:contains("мікроамперметра")) input {
        pointer-events: none !important;
        background-color: #f1f3f6 !important;
        color: #4a4a4a !important;
    }
    /* Залишаємо бічні кнопочки плюс-мінус повністю клікабельними */
    div[data-testid="stNumberInput"]:has(label:contains("мікроамперметра")) button {
        pointer-events: auto !important;
    }
    </style>
    """,
    unsafe_allow_code=True
)

st.subheader("«Розширення меж вимірювання амперметра і вольтметра»")

# Ініціалізація сесії для таблиць експерименту
if "data_stage1" not in st.session_state:
    st.session_state.data_stage1 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
if "data_stage2" not in st.session_state:
    st.session_state.data_stage2 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
if "data_stage3" not in st.session_state:
    st.session_state.data_stage3 = pd.DataFrame(columns=["n (поділки)", "U (мВ)"])

# Створення вкладок для етапів ЛР
tab1, tab2, tab3 = st.tabs([
    "📊 1. Градуювання мікроамперметра", 
    "⚡ 2. Розширення межі амперметра", 
    "🔌 3. Градуювання вольтметра"
])

# ==========================================
# ВКЛАДКА 1: Градуювання мікроамперметра
# ==========================================
with tab1:
    st.markdown("### Складіть схему за Рис. 1.6")
    st.info("🔌 Тягніть дроти мишкою від клеми до клеми. Обертайте круглу чорну ручку потенціометра R1 прямо на стенді для зміни показів!")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Стабільний виклик стенду без скидання дротів
        interactive_bench("stage1", key="bench_s1")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        st.write("Зніміть покази зі стенду та занесіть у протокол:")
        
        # Ручне введення для фіксації результатів студентом
        n_in_s1 = st.number_input("Покази мікроамперметра n (поділки)", min_value=0.0, max_value=50.0, step=1.0, key="n_in_s1")
        i_in_s1 = st.number_input("Покази еталона В7-21А (мкА)", min_value=0.0, step=0.1, key="i_in_s1")
        
        st.markdown("---")
        add_point = st.button("📥 Записати точку в таблицю", key="btn_add_s1", use_container_width=True)
        if add_point:
            new_row = pd.DataFrame([{"n (поділки)": n_in_s1, "I (мкА)": i_in_s1}])
            st.session_state.data_stage1 = pd.concat([st.session_state.data_stage1, new_row], ignore_index=True)
            st.rerun()
            
        if st.button("🧹 Очистити таблицю етапу 1", key="clear_s1"):
            st.session_state.data_stage1 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
            st.rerun()
            
        st.dataframe(st.session_state.data_stage1, use_container_width=True)

# ==========================================
# ВКЛАДКА 2: Розширення межі амперметра
# ==========================================
with tab2:
    st.markdown("### Складіть схему з шунтом за Рис. 1.7")
    st.info("🔌 Підключіть шунт Rш паралельно мікроамперметру, щоб розширити межу вимірювання.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        interactive_bench("stage2", key="bench_s2")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        st.write("Зніміть покази загального струму та поділок:")
        
        n_in_s2 = st.number_input("Покази мікроамперметра n (поділки)", min_value=0.0, max_value=50.0, step=1.0, key="n_in_s2")
        i_in_s2 = st.number_input("Покази еталона В7-21А (Загальний струм, мкА)", min_value=0.0, step=0.1, key="i_in_s2")
        
        st.markdown("---")
        add_point_s2 = st.button("📥 Записати точку в таблицю", key="btn_add_s2", use_container_width=True)
        if add_point_s2:
            new_row = pd.DataFrame([{"n (поділки)": n_in_s2, "I (мкА)": i_in_s2}])
            st.session_state.data_stage2 = pd.concat([st.session_state.data_stage2, new_row], ignore_index=True)
            st.rerun()
            
        if st.button("🧹 Очистити таблицю етапу 2", key="clear_s2"):
            st.session_state.data_stage2 = pd.DataFrame(columns=["n (поділки)", "I (мкА)"])
            st.rerun()
            
        st.dataframe(st.session_state.data_stage2, use_container_width=True)

# ==========================================
# ВКЛАДКА 3: Градуювання вольтметра
# ==========================================
with tab3:
    st.markdown("### Складіть схему для вольтметра за Рис. 1.8")
    st.info("🔌 Зберіть послідовний ланцюг із мікроамперметра та додаткового опору R2.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        interactive_bench("stage3", key="bench_s3")
    
    with col2:
        st.markdown("#### 📟 Контрольна панель вимірювань")
        st.write("Зніміть покази напруги та поділок шкали:")
        
        n_in_s3 = st.number_input("Покази мікроамперметра n (поділки)", min_value=0.0, max_value=50.0, step=1.0, key="n_in_s3")
        u_in_s3 = st.number_input("Покази еталона В7-21А (Напруга, мВ)", min_value=0.0, step=0.1, key="u_in_s3")
        
        st.markdown("---")
        add_point_s3 = st.button("📥 Записати точку в таблицю", key="btn_add_s3", use_container_width=True)
        if add_point_s3:
            new_row = pd.DataFrame([{"n (поділки)": n_in_s3, "U (мВ)": u_in_s3}])
            st.session_state.data_stage3 = pd.concat([st.session_state.data_stage3, new_row], ignore_index=True)
            st.rerun()
            
        if st.button("🧹 Очистити таблицю етапу 3", key="clear_s3"):
            st.session_state.data_stage3 = pd.DataFrame(columns=["n (поділки)", "U (мВ)"])
            st.rerun()
            
        st.dataframe(st.session_state.data_stage3, use_container_width=True)

# ==========================================
# ЗОНА ГРАФІКІВ (АВТОМАТИЧНА ПОБУДОВА ЗНИЗУ)
# ==========================================
