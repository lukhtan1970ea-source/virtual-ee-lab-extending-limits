import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Стабільний компонент. Автоматично збирає index.html, style.css 
    та script.js в один моноліт перед рендерингом в iFrame, 
    а також примусово прописує поточний етап всередину JS цепи.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    html_path = os.path.join(current_dir, "index.html")
    css_path = os.path.join(current_dir, "style.css")
    js_path = os.path.join(current_dir, "script.js")
    
    # Читаємо HTML-разметку
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # Інтегруємо стилі
    with open(css_path, "r", encoding="utf-8") as f:
        css_code = f.read()
    html_code = html_code.replace(
        '<link rel="stylesheet" href="style.css">', 
        f'<style>{css_code}</style>'
    )
    
    # Інтегруємо скрипти
    with open(js_path, "r", encoding="utf-8") as f:
        js_code = f.read()
        
    # НАДІЙНЕ ЗАМІЩЕННЯ СТАДІЇ: змушуємо JS прийняти стадію від Стрімліта
    js_code = js_code.replace(
        'let currentStage = window.name.includes("bench_s2") ? "stage2" : (window.name.includes("bench_s3") ? "stage3" : "stage1");',
        f'let currentStage = "{stage_name}";'
    )
    
    html_code = html_code.replace(
        '<script src="script.js"></script>', 
        f'<script>{js_code}</script>'
    )

    # Рендеримо зібраний моноліт з правильним етапом
    return components.html(html_code, width=720, height=470, scrolling=False)
