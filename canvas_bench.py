import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Абсолютно стабільний компонент. Лежить у корені, тому немає конфліктів.
    """
    # Знаходимо index.html прямо у корені поруч
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Передаємо назву вкладки всередину JS коду за допомогою простої заміни тексту
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")
    html_code = html_code.replace("let currentStage = urlParams.get('stage') || 'stage1';", f"let currentStage = '{stage_name}';")

    # Рендеримо HTML всередині безпечного iFrame
    return components.html(html_code, height=470)

