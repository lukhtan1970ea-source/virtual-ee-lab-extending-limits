import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Кастомний компонент для інтерактивного лабораторного стенда.
    Зчитує чистий HTML/JS з окремого файлу index.html.
    """
    # Знаходимо шлях до файлу index.html у тій самій папці
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Інжектуємо назву поточного етапу (stage1, stage2, stage3) у скрипт
    # замінюючи технічний рядок параметру
    html_code = html_code.replace(
        "let currentStage = urlParams.get('stage') || 'stage1';",
        f"let currentStage = '{stage_name}';"
    )
    
    # Рендеримо чистий, легкий HTML-компонент у Streamlit
    component_value = components.html(html_code, height=460, key=key)
    return component_value

