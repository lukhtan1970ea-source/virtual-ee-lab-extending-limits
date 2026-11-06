import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Стабільний компонент. Автоматично збирає index.html, style.css 
    та script.js в один моноліт перед рендерингом в iFrame, 
    щоб уникнути білого екрану в Streamlit Cloud.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Пути к нашим трем файлам
    html_path = os.path.join(current_dir, "index.html")
    css_path = os.path.join(current_dir, "style.css")
    js_path = os.path.join(current_dir, "script.js")
    
    # Читаем HTML-разметку
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # Читаем стили и вставляем вместо тега подключения CSS
    with open(css_path, "r", encoding="utf-8") as f:
        css_code = f.read()
    html_code = html_code.replace(
        '<link rel="stylesheet" href="style.css">', 
        f'<style>{css_code}</style>'
    )
    
    # Читаем скрипты и вставляем вместо тега подключения JS
    with open(js_path, "r", encoding="utf-8") as f:
        js_code = f.read()
    html_code = html_code.replace(
        '<script src="script.js"></script>', 
        f'<script>{js_code}</script>'
    )
    
    # Передаем стадию (актуально для вкладок)
    html_code = html_code.replace("let currentStage = 'stage1';", f"let currentStage = '{stage_name}';")

    # Рендерим собранный монолит без потери путей
    return components.html(html_code, width=720, height=470, scrolling=False)
