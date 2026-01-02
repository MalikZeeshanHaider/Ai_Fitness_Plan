"""
Membership Page - View plans and register
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.parent))

from src.presentation.ui_components import render_membership_section

st.set_page_config(
    page_title="Membership - AI Gym",
    page_icon="💳",
    layout="wide"
)

st.markdown("# 💳 Membership Plans")
st.markdown("Choose the perfect plan for your fitness journey!")
st.markdown("---")

render_membership_section()
