import streamlit as st
import streamlit.components.v1 as components
import os

# Получаем путь к папке, где лежит index.html
current_dir = os.path.dirname(os.path.abspath(__file__))

# Регистрируем наш компонент в Streamlit. 
# Он сам автоматически найдет index.html в этой папке!
_interactive_bench_component = components.declare_component(
    "interactive_bench",
    path=current_dir
)

def interactive_bench(stage_name, key=None):
    """
    Вызывает зарегистрированный компонент и безопасно передает
    параметры (например, имя вкладки) напрямую в JavaScript.
    """
    # Вызываем компонент и передаем stage_name как аргумент внутрь JS
    return _interactive_bench_component(stage=stage_name, key=key)
