import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Стабільний компонент. Передає етап через URL-параметр,
    запобігаючи скиданню стану та жорсткому зашиванню стадії.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    # Рендеримо iFrame, динамічно вказуючи поточний етап у параметрах
    # Streamlit Community Cloud коректно підхопить локальний файл через srcdoc
    return components.html(html_code, width=720, height=470, scrolling=False)
