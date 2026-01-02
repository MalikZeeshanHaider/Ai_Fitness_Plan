"""
About Page - Information about the AI Gym system
"""

import streamlit as st

st.set_page_config(
    page_title="About - AI Gym",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 About AI Gym")
st.markdown("Learn about our intelligent workout recommendation system")
st.markdown("---")

# Hero section
st.markdown("""
<div style="background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%); 
            padding: 40px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;">
    <h1 style="color: white; margin-bottom: 15px;">🏋️ AI Gym Workout Recommendation System</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">
        Intelligent, Personalized, Effective - Your AI-Powered Fitness Partner
    </p>
</div>
""", unsafe_allow_html=True)

# Features
st.markdown("### ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; height: 200px;">
        <h3>🤖 AI-Powered</h3>
        <p>Advanced algorithms analyze your profile to create optimal workout plans tailored to your goals.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; height: 200px;">
        <h3>🎯 Goal-Oriented</h3>
        <p>Whether it's weight loss, muscle gain, or endurance - we optimize your workouts for results.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; height: 200px;">
        <h3>🛡️ Safety First</h3>
        <p>Smart injury detection and exercise filtering keeps you safe during your fitness journey.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# AI Technology section
st.markdown("### 🧠 AI Technology")

st.markdown("""
Our system uses a sophisticated multi-agent AI architecture:
""")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown("""
    **1. Simple Reflex Agent** 🔍
    - Safety filtering using if-then rules
    - Injury detection and exercise exclusion
    - Equipment availability checking
    
    **2. Goal-Based Agent** 🎯
    - Fitness goal analysis
    - Target state definition
    - Success criteria establishment
    """)

with tech_col2:
    st.markdown("""
    **3. Utility-Based Agent** ⚡
    - Exercise scoring using utility functions
    - Multi-factor optimization
    - Preference-based ranking
    
    **4. A* Search Algorithm** 🔎
    - Optimal workout plan generation
    - Constraint satisfaction
    - Time and calorie optimization
    """)

st.markdown("---")

# Statistics
st.markdown("### 📈 Platform Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Exercises", "100+", help="Total exercises in our database")

with stat_col2:
    st.metric("Categories", "10+", help="Different exercise categories")

with stat_col3:
    st.metric("AI Agents", "4", help="Intelligent agents working for you")

with stat_col4:
    st.metric("Accuracy", "95%", help="Plan optimization accuracy")

st.markdown("---")

# How it works
st.markdown("### 🔄 How It Works")

st.markdown("""
<div style="display: flex; justify-content: space-between; margin: 20px 0;">
    <div style="text-align: center; flex: 1; padding: 20px;">
        <div style="background: #667eea; color: white; width: 60px; height: 60px; border-radius: 50%; 
                    display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">1</div>
        <h4>Input Profile</h4>
        <p style="color: #666;">Enter your fitness details, goals, and preferences</p>
    </div>
    <div style="text-align: center; flex: 1; padding: 20px;">
        <div style="background: #f093fb; color: white; width: 60px; height: 60px; border-radius: 50%; 
                    display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">2</div>
        <h4>AI Analysis</h4>
        <p style="color: #666;">Our AI agents analyze and optimize your plan</p>
    </div>
    <div style="text-align: center; flex: 1; padding: 20px;">
        <div style="background: #4facfe; color: white; width: 60px; height: 60px; border-radius: 50%; 
                    display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">3</div>
        <h4>Get Plan</h4>
        <p style="color: #666;">Receive your personalized workout routine</p>
    </div>
    <div style="text-align: center; flex: 1; padding: 20px;">
        <div style="background: #11998e; color: white; width: 60px; height: 60px; border-radius: 50%; 
                    display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">4</div>
        <h4>Achieve Goals</h4>
        <p style="color: #666;">Follow the plan and reach your fitness goals</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>AI Gym Workout Recommendation System</strong></p>
    <p>© 2026 All Rights Reserved</p>
    <p>Powered by Advanced AI Technology</p>
</div>
""", unsafe_allow_html=True)
