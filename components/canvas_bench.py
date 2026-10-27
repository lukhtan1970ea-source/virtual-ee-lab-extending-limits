import streamlit as st
import streamlit.components.v1 as components
import os

def interactive_bench(stage_name, key=None):
    """
    Вызывает интерактивный стенд через безопасный изолированный iFrame,
    который гарантированно запустится на серверах Streamlit Cloud.
    """
    # В облаке Streamlit Cloud статические файлы из папки components 
    # доступны по прямому внутреннему URL-адресу приложения.
    # Мы рендерим index.html напрямую, передавая текущую вкладку как параметр.
    
    # Строим относительный путь к файлу для локального и облачного режимов
    html_url = f"components/index.html?stage={stage_name}"
    
    # Отображаем роскошный Canvas-стенд с фиксированной высотой
    return components.iframe(html_url, height=460, scrolling=False)
