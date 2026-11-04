import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, r1_value, key=None):
    """
    Стабільний компонент. Передає значення опору R1 всередину JS 
    та адаптує розміри під екран без обрізання.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Внедряем выбранную стадию и текущее значение сопротивления R1
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let currentStage = urlParams.get('stage') || 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let r1_from_streamlit = 2500;", f"let r1_from_streamlit = {r1_value};")

    # Увеличиваем ширину до 720 (ширина canvas 700 + отступы) 
    # и включаем скроллинг на случай узких экранов
    return components.html(html_code, width=720, height=470, scrolling=True)

