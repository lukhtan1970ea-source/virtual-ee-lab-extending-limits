import streamlit as st
import streamlit.components.v1 as components
import os

# Офіційний та найнадійніший шлях реєстрації компонентів у Streamlit
current_dir = os.path.dirname(os.path.abspath(__file__))

_interactive_bench_component = components.declare_component(
    "interactive_bench",
    path=current_dir
)

def interactive_bench(stage_name, key=None):
    """
    Викликає зареєстрований компонент та безпечно передає 
    параметри безпосередньо в JavaScript.
    """
    return _interactive_bench_component(stage=stage_name, key=key)
