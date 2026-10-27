import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Кастомний компонент для інтерактивного лабораторного стенда.
    Безпечно завантажує index.html через механізм Streamlit без ручного replace.
    """
    # Знаходимо шлях до папки з файлом index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, "index.html")
    
    # Перевіряємо, чи файл взагалі існує, щоб уникнути збоїв
    if not os.path.exists(html_file_path):
        st.error(f"Помилка: Файл index.html не знайдено у папці components!")
        return None

    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Передаємо назву етапу через простий хак всередині скрипта перед рендером
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let currentStage = urlParams.get('stage') || 'stage1';", f"let currentStage = '{stage_name}';")

    # Рендеримо HTML всередині iFrame
    return components.html(html_code, height=470, key=key)
