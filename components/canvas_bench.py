import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Абсолютно стабільний кастомний компонент для інтерактивного стенду.
    Зчитує index.html як текст та безпечно рендерить його через нативний iFrame Streamlit Cloud.
    """
    # Знаходимо точний шлях до файлу index.html на сервері
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, "index.html")
    
    # Зчитуємо вміст файлу
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Передаємо назву поточної вкладки всередину JavaScript коду
    html_code = html_code.replace('let currentStage = urlParams.get(\'stage\') || \'stage1\';', f'let currentStage = "{stage_name}";')
    
    # Рендеримо сочний Canvas-стенд
    return components.html(html_code, height=470, key=key)
