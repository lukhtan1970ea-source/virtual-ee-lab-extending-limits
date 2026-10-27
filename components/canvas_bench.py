import streamlit as st
import streamlit.components.v1 as components
import os

# Автоматичне визначення папки компонента
current_dir = os.path.dirname(os.path.abspath(__file__))

# Реєстрація єдиного компонента
_bench_comp = components.declare_component("interactive_bench", path=current_dir)

def interactive_bench(stage_name, key=None):
    """Офіційний виклик інтерактивного стенду з передачею вкладки"""
    return _bench_comp(stage=stage_name, key=key)
