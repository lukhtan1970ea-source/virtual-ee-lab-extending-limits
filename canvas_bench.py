import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Стабільний ізольований компонент. Рендерить стенд один раз 
    і не скидає дроти при взаємодії.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Впроваджуємо поточний етап
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let currentStage = urlParams.get('stage') || 'stage1';", f"let currentStage = '{stage_name}';")

    return components.html(html_code, width=720, height=470, scrolling=False)
