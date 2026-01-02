"""
AI Gym Workout Recommendation System - Home Page

This is the main entry point for the web application.
Multi-page navigation is handled via the pages/ folder.

To run:
    streamlit run app.py

Author: AI Gym System
Date: December 2025
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.presentation.ui_components import render_header, render_footer
from src.presentation.ui_state import init_session_state


# Page configuration
st.set_page_config(
    page_title="AI Gym - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css():
    """Load custom CSS styling."""
    from src.presentation.custom_css import load_custom_css as load_css
    load_css()


def main():
    """Main application function - Home Page."""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%); 
                padding: 60px 40px; border-radius: 20px; text-align: center; color: white; margin: 20px 0;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 20px;">🏋️ Welcome to AI Gym</h1>
        <p style="font-size: 1.4rem; opacity: 0.95; margin-bottom: 30px;">
            Your Intelligent Fitness Partner - Personalized Workout Plans Powered by AI
        </p>
        <p style="font-size: 1.1rem; opacity: 0.85;">
            Generate custom workout routines tailored to your goals, experience, and available equipment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Navigation Cards
    st.markdown("### 🚀 Quick Navigation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; color: white; height: 200px;">
            <h2 style="color: white; font-size: 2.5rem;">🏋️</h2>
            <h3 style="color: white;">Workout Generator</h3>
            <p style="opacity: 0.9;">Create your personalized AI workout plan</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Workout", key="nav_workout", use_container_width=True):
            st.switch_page("pages/1_🏋️_Workout_Generator.py")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; color: white; height: 200px;">
            <h2 style="color: white; font-size: 2.5rem;">💳</h2>
            <h3 style="color: white;">Membership</h3>
            <p style="opacity: 0.9;">View plans & register for premium features</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Plans", key="nav_membership", use_container_width=True):
            st.switch_page("pages/2_💳_Membership.py")
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; color: white; height: 200px;">
            <h2 style="color: white; font-size: 2.5rem;">📚</h2>
            <h3 style="color: white;">Tutorials</h3>
            <p style="opacity: 0.9;">Learn proper form for all exercises</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Browse Tutorials", key="nav_tutorials", use_container_width=True):
            st.switch_page("pages/3_📚_Tutorials.py")
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; color: white; height: 200px;">
            <h2 style="color: white; font-size: 2.5rem;">📊</h2>
            <h3 style="color: white;">About</h3>
            <p style="opacity: 0.9;">Learn about our AI technology</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn More", key="nav_about", use_container_width=True):
            st.switch_page("pages/5_📊_About.py")
    
    st.markdown("---")
    
    # Features Section
    st.markdown("### ✨ Why Choose AI Gym?")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; text-align: center;">
            <h2>🤖</h2>
            <h4>AI-Powered Plans</h4>
            <p style="color: #666;">Our intelligent agents analyze your profile to create the perfect workout routine.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; text-align: center;">
            <h2>🎯</h2>
            <h4>Goal-Oriented</h4>
            <p style="color: #666;">Whether weight loss, muscle gain, or endurance - we optimize for your goals.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; text-align: center;">
            <h2>🛡️</h2>
            <h4>Safety First</h4>
            <p style="color: #666;">Smart injury detection keeps you safe during your fitness journey.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it works
    st.markdown("### 🔄 How It Works")
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="background: #667eea; color: white; width: 50px; height: 50px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 20px; font-weight: bold;">1</div>
            <h4>Enter Profile</h4>
            <p style="color: #666; font-size: 0.9rem;">Input your fitness details and goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="background: #f093fb; color: white; width: 50px; height: 50px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 20px; font-weight: bold;">2</div>
            <h4>AI Analyzes</h4>
            <p style="color: #666; font-size: 0.9rem;">Our AI optimizes your plan</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="background: #4facfe; color: white; width: 50px; height: 50px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 20px; font-weight: bold;">3</div>
            <h4>Get Plan</h4>
            <p style="color: #666; font-size: 0.9rem;">Receive your custom workout</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col4:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="background: #11998e; color: white; width: 50px; height: 50px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 20px; font-weight: bold;">4</div>
            <h4>Achieve Goals</h4>
            <p style="color: #666; font-size: 0.9rem;">Follow plan & get results</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 40px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;">
        <h2 style="color: white; margin-bottom: 15px;">Ready to Start Your Fitness Journey?</h2>
        <p style="font-size: 1.1rem; opacity: 0.9; margin-bottom: 20px;">
            Generate your first AI-powered workout plan in seconds!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("🚀 Get Started Now", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🏋️_Workout_Generator.py")
    
    st.markdown("---")
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
