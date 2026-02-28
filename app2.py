import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="แนะนำคอมเซ็ทตามงบ", layout="wide")

with open("Web-ver01.html", "r", encoding="utf-8") as f:
    html = f.read()

# ปรับ height ได้ตามความยาวหน้าเว็บ
components.html(html, height=1000, scrolling=True)