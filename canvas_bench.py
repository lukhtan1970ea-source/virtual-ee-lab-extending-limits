import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, r1_value, key=None):
    """
    Стабільний компонент. Передає значення опору R1 з повзунка Streamlit всередину JS.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Внедряем выбранную стадию и текущее значение сопротивления R1
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let currentStage = urlParams.get('stage') || 'stage1';", f"let currentStage = '{stage_name}';")
    
    # Динамически передаем реальное значение R1 из слайдера в JS-переменную
    html_code = html_code.replace("let r1_from_streamlit = 2500;", f"let r1_from_streamlit = {r1_value};")

    return components.html(html_code, height=470)
