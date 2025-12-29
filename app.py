"""
AI Gym Workout Recommendation System - Streamlined Streamlit Application

This is the main entry point for the web application.
It provides an interactive UI for generating personalized workout recommendations
using a simplified, easy-to-explain AI architecture:

AI Workflow:
1. Simple Reflex Agent → Safety filtering (if-then rules)
2. Goal-Based Agent → Fitness goal definition  
3. Utility-Based Agent → Exercise scoring (utility function)
4. A* Search Algorithm → Optimal workout plan generation

This simplified architecture is designed for clear academic explanation.

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

from src.presentation.ui_components import (
    render_header,
    render_user_input_form,
    render_workout_plan,
    render_footer
)
from src.presentation.ui_state import init_session_state, get_session_state, update_session_state
from src.infrastructure.data.data_loader import DataLoader
from src.application.streamlined_workout_usecase import (
    StreamlinedWorkoutUseCase,
    StreamlinedRequest,
    StreamlinedResponse
)
from src.application.pdf_generator import PDFGenerator, PDFStyle
from src.domain.models.state import ExperienceLevel


# Page configuration
st.set_page_config(
    page_title="AI Gym Workout Recommendation System",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css():
    """Load custom CSS styling."""
    from src.presentation.custom_css import load_custom_css as load_css
    load_css()


def main():
    """Main application function."""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Main content area
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### � Profile & Preferences")
        
        # Render user input form (returns data when form is submitted)
        user_input = render_user_input_form()
        
        # Process when form is submitted
        if user_input:
            with st.spinner("🔄 Generating your personalized workout plan..."):
                try:
                    # Initialize services
                    data_loader = DataLoader()
                    use_case = StreamlinedWorkoutUseCase(data_loader)
                    
                    # Create streamlined request
                    request = StreamlinedRequest(
                        current_state=user_input['state'],
                        available_time=user_input['time'],
                        available_equipment=user_input['equipment'],
                        user_preferences=user_input.get('preferences', {})
                    )
                    
                    # Execute streamlined workflow
                    response = use_case.execute(request)
                    
                    # Store in session state
                    update_session_state({
                        'response': response
                    })
                    
                    st.success("✅ Workout plan generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating workout plan: {str(e)}")
                    st.exception(e)
    
    with col2:
        st.markdown("### 🏋️ Your Workout Plan")
        
        # Display results if available
        session_state = get_session_state()
        
        if session_state.get('response'):
            response: StreamlinedResponse = session_state['response']
            
            # Success message
            st.success("✅ Your workout plan is ready!")
            
            # Display workout plan with improved styling
            st.markdown("---")
            for i, exercise in enumerate(response.exercises, 1):
                # Create a professional card-like expander
                with st.expander(f"**Exercise {i}: {exercise.name}** • {exercise.duration_minutes} min", expanded=(i <= 2)):
                    # Exercise metrics in clean layout
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("⏱️ Duration", f"{exercise.duration_minutes} min")
                    with col_b:
                        calories = exercise.calories_per_minute * exercise.duration_minutes
                        st.metric("🔥 Calories", f"{calories:.0f}")
                    with col_c:
                        st.metric("📊 Intensity", exercise.intensity.value if exercise.intensity else 'Moderate')
                    
                    # Additional details
                    st.markdown("---")
                    detail_col1, detail_col2 = st.columns(2)
                    with detail_col1:
                        st.markdown(f"**Category:** {exercise.category.value if exercise.category else 'N/A'}")
                        st.markdown(f"**Difficulty:** {exercise.difficulty or 'N/A'}")
                    with detail_col2:
                        if exercise.primary_muscles:
                            muscles_display = ', '.join(exercise.primary_muscles[:3])
                            if len(exercise.primary_muscles) > 3:
                                muscles_display += f" (+{len(exercise.primary_muscles) - 3} more)"
                            st.markdown(f"**Target Muscles:** {muscles_display}")
                        if exercise.equipment:
                            st.markdown(f"**Equipment:** {', '.join(exercise.equipment[:2])}")
            
            # Display plan summary with professional styling
            st.markdown("---")
            st.markdown("### 📈 Plan Summary")
            
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                st.metric("Exercises", len(response.exercises), help="Total exercises in plan")
            with col_y:
                total_time = sum(ex.duration_minutes for ex in response.exercises)
                st.metric("Duration", f"{total_time} min", help="Total workout time")
            with col_z:
                total_cal = sum(ex.calories_per_minute * ex.duration_minutes for ex in response.exercises)
                st.metric("Calories", f"{total_cal:.0f}", help="Estimated burn")
            
            # Download buttons with professional styling
            st.markdown("---")
            st.markdown("### 💾 Export Options")
            col_dl1, col_dl2 = st.columns(2)
            
            # Text download
            workout_text = "🏋️ MY WORKOUT PLAN\n" + "="*50 + "\n\n"
            for i, exercise in enumerate(response.exercises, 1):
                workout_text += f"{i}. {exercise.name}\n"
                workout_text += f"   Duration: {exercise.duration_minutes} minutes\n"
                workout_text += f"   Category: {exercise.category.value if exercise.category else 'N/A'}\n"
                workout_text += f"   Difficulty: {exercise.difficulty or 'N/A'}\n"
                workout_text += f"   Calories: ~{exercise.calories_per_minute * exercise.duration_minutes:.0f} kcal\n"
                if exercise.primary_muscles:
                    workout_text += f"   Muscles: {', '.join(exercise.primary_muscles)}\n"
                workout_text += "\n"
            
            workout_text += f"\n{'='*50}\n"
            workout_text += f"Total Exercises: {len(response.exercises)}\n"
            workout_text += f"Total Time: {total_time} minutes\n"
            workout_text += f"Total Calories: ~{total_cal:.0f} kcal\n"
            
            with col_dl1:
                st.download_button(
                    label="📥 Download as Text",
                    data=workout_text,
                    file_name="my_workout_plan.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # PDF download
            with col_dl2:
                try:
                    # Generate PDF
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
                    st.error(f"PDF generation failed: {str(e)}")
            
        else:
            # Empty state with professional design
            st.markdown("""
            <div style="text-align: center; padding: 80px 20px;">
                <div style="background: white; 
                            padding: 50px 40px; 
                            border-radius: 16px; 
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07); 
                            margin: 20px auto; 
                            max-width: 700px;
                            border: 1px solid rgba(226, 232, 240, 0.8);">
                    <h1 style="font-size: 3em; margin-bottom: 15px; color: #1E3A8A;">🏋️</h1>
                    <h2 style="color: #1E3A8A; margin-bottom: 15px; font-weight: 600;">Welcome to AI Gym Workout Recommendation System</h2>
                    <p style="font-size: 1.15em; color: #64748B; margin-bottom: 35px; line-height: 1.6;">
                        Create personalized workout plans tailored to your fitness goals, <br/>
                        experience level, and available time.
                    </p>
                    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%); 
                                padding: 35px 40px; 
                                border-radius: 12px; 
                                color: white; 
                                margin: 25px 0;">
                        <h3 style="margin-bottom: 18px; font-weight: 600; font-size: 1.3em;">Getting Started</h3>
                        <p style="font-size: 1.05em; line-height: 1.8; margin-bottom: 12px;">
                            1. Complete your profile in the left sidebar<br/>
                            2. Select your fitness goal and preferences<br/>
                            3. Click <strong>"Generate Workout Plan"</strong>
                        </p>
                        <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                            <p style="font-size: 0.95em; opacity: 0.9;">
                                💡 Our AI will analyze your profile and create an optimized workout routine just for you.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
