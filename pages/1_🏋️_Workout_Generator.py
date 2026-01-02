"""
Workout Generator Page - Generate personalized workout plans
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.parent))

from src.presentation.ui_components import render_user_input_form
from src.presentation.ui_state import init_session_state, get_session_state, update_session_state
from src.infrastructure.data.data_loader import DataLoader
from src.application.streamlined_workout_usecase import (
    StreamlinedWorkoutUseCase,
    StreamlinedRequest,
    StreamlinedResponse
)
from src.application.pdf_generator import PDFGenerator, PDFStyle


st.set_page_config(
    page_title="Workout Generator - AI Gym",
    page_icon="🏋️",
    layout="wide"
)

st.markdown("# 🏋️ Workout Generator")
st.markdown("Generate your personalized AI-powered workout plan!")
st.markdown("---")

# Initialize session state
init_session_state()

# Main content area
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### 📋 Profile & Preferences")
    
    # Render user input form
    user_input = render_user_input_form()
    
    if user_input:
        with st.spinner("🔄 Generating your personalized workout plan..."):
            try:
                data_loader = DataLoader()
                use_case = StreamlinedWorkoutUseCase(data_loader)
                
                request = StreamlinedRequest(
                    current_state=user_input['state'],
                    available_time=user_input['time'],
                    available_equipment=user_input['equipment'],
                    user_preferences=user_input.get('preferences', {})
                )
                
                response = use_case.execute(request)
                
                update_session_state({'response': response})
                
                st.success("✅ Workout plan generated successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating workout plan: {str(e)}")

with col2:
    st.markdown("### 🎯 Your Workout Plan")
    
    session_state = get_session_state()
    
    if session_state.get('response'):
        response: StreamlinedResponse = session_state['response']
        
        st.success("✅ Your workout plan is ready!")
        
        # Summary metrics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Exercises", len(response.exercises))
        with col_b:
            total_time = sum(ex.duration_minutes for ex in response.exercises)
            st.metric("Duration", f"{total_time} min")
        with col_c:
            total_cal = sum(ex.calories_per_minute * ex.duration_minutes for ex in response.exercises)
            st.metric("Calories", f"{total_cal:.0f}")
        
        st.markdown("---")
        
        # Exercise list
        for i, exercise in enumerate(response.exercises, 1):
            with st.expander(f"**Exercise {i}: {exercise.name}** • {exercise.duration_minutes} min", expanded=(i <= 2)):
                col_x, col_y = st.columns([2, 1])
                with col_x:
                    st.markdown(f"**Category:** {exercise.category.value if exercise.category else 'N/A'}")
                    st.markdown(f"**Difficulty:** {exercise.difficulty or 'N/A'}")
                    if exercise.primary_muscles:
                        st.markdown(f"**Target Muscles:** {', '.join(exercise.primary_muscles[:3])}")
                with col_y:
                    calories = exercise.calories_per_minute * exercise.duration_minutes
                    st.metric("🔥 Calories", f"{calories:.0f}")
                
                # YouTube link
                youtube_search = exercise.name.replace(" ", "+") + "+exercise+tutorial"
                youtube_url = f"https://www.youtube.com/results?search_query={youtube_search}"
                st.markdown(f"🎬 [Watch Tutorial on YouTube]({youtube_url})")
        
        # Download section
        st.markdown("---")
        st.markdown("### 💾 Export Your Plan")
        
        workout_text = "🏋️ MY WORKOUT PLAN\n" + "="*50 + "\n\n"
        for i, exercise in enumerate(response.exercises, 1):
            workout_text += f"{i}. {exercise.name}\n"
            workout_text += f"   Duration: {exercise.duration_minutes} minutes\n"
            workout_text += f"   Calories: ~{exercise.calories_per_minute * exercise.duration_minutes:.0f} kcal\n\n"
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download as Text",
                data=workout_text,
                file_name="my_workout_plan.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_dl2:
            try:
                pdf_gen = PDFGenerator()
                report = pdf_gen.create_workout_report(
                    workout_plan=response.workout_plan,
                    user_state=response.workout_plan.initial_state,
                    style=PDFStyle.PROFESSIONAL
                )
                pdf_bytes = pdf_gen.generate_pdf(report)
                
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_bytes,
                    file_name="my_workout_plan.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF error: {str(e)}")
    else:
        st.info("👈 Fill in your profile and click 'Generate Workout Plan' to get started!")
