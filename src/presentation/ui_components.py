"""
UI Components for Streamlit Application.

This module contains all reusable UI components for the workout
recommendation system.

Components:
- Header and footer
- User input forms
- Workout plan display
- Reasoning explanations display
- PDF download functionality
- Metrics and visualizations
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from src.domain.models.state import State, FitnessGoal, ExperienceLevel
from src.domain.models.exercise import Exercise, ExerciseCategory, IntensityLevel
from src.domain.models.workout_plan import WorkoutPlan
# from src.application.reasoning_explainer import Explanation  # Not used in streamlined workflow


def render_header() -> None:
    """Render the application header."""
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🏋️ AI Gym Workout Recommendation System</div>
        <div class="header-subtitle">
            Intelligent Workout Recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer() -> None:
    """Render the application footer."""
    st.markdown("""
    <div class="footer">
        <p><strong>AI Gym Workout Recommendation System</strong> • Professional Workout Planning System</p>
        <p style="font-size: 0.9rem; color: #64748B; margin-top: 0.5rem;">
            Powered by Advanced AI Technology • © 2025
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_user_input_form() -> Optional[Dict[str, Any]]:
    """
    Render the user input form for profile and preferences.
    
    Returns:
        Optional[Dict[str, Any]]: User input data or None if incomplete
    """
    with st.form("user_input_form"):
        st.markdown("#### 👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input(
                "Age",
                min_value=15,
                max_value=100,
                value=25,
                help="Your current age"
            )
            
            weight = st.number_input(
                "Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=70.0,
                step=0.5,
                help="Your current weight in kilograms"
            )
            
            experience = st.select_slider(
                "Experience Level",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Intermediate",
                help="Your fitness experience level"
            )
        
        with col2:
            height = st.number_input(
                "Height (cm)",
                min_value=120.0,
                max_value=230.0,
                value=170.0,
                step=0.5,
                help="Your height in centimeters"
            )
            
            energy_level = st.slider(
                "Current Energy Level",
                min_value=1,
                max_value=10,
                value=7,
                help="How energetic do you feel? (1=Exhausted, 10=Full of energy)"
            )
        
        st.markdown("---")
        st.markdown("#### 🎯 Fitness Goals")
        
        goal = st.selectbox(
            "Primary Goal",
            options=[
                "Weight Loss",
                "Muscle Gain",
                "Endurance",
                "Flexibility",
                "General Fitness",
                "Strength Building"
            ],
            help="What is your main fitness objective?"
        )
        
        st.markdown("---")
        st.markdown("#### ⚙️ Workout Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            available_time = st.number_input(
                "Available Time (minutes)",
                min_value=15,
                max_value=180,
                value=60,
                step=5,
                help="How much time can you dedicate?"
            )
        
        with col2:
            max_exercises = st.number_input(
                "Maximum Exercises",
                min_value=3,
                max_value=12,
                value=6,
                help="Maximum number of exercises in your plan"
            )
        
        st.markdown("---")
        st.markdown("#### 🏋️ Available Equipment")
        
        equipment_options = [
            "Dumbbells",
            "Barbell",
            "Resistance Bands",
            "Pull-up Bar",
            "Bench",
            "Treadmill",
            "Bike",
            "Rowing Machine",
            "Kettlebell",
            "Medicine Ball"
        ]
        
        equipment = st.multiselect(
            "Select Available Equipment",
            options=equipment_options,
            default=["Dumbbells", "Barbell", "Bench"],
            help="What equipment do you have access to?"
        )
        
        # Add "None" option for bodyweight
        if st.checkbox("Include Bodyweight Exercises", value=True):
            equipment.append("None")
        
        st.markdown("---")
        st.markdown("#### 🏥 Health Considerations")
        
        has_injuries = st.checkbox("I have current injuries or limitations")
        
        injuries = []
        if has_injuries:
            injury_options = st.multiselect(
                "Select Affected Areas",
                options=[
                    "Lower Back",
                    "Knee",
                    "Shoulder",
                    "Elbow",
                    "Wrist",
                    "Ankle",
                    "Hip",
                    "Neck"
                ],
                help="Select any areas with injuries or pain"
            )
            injuries = injury_options
        
        # Submit button
        submitted = st.form_submit_button(
            "Generate Workout Plan 🚀",
            use_container_width=True
        )
        
        if submitted:
            # Map experience to ExperienceLevel enum
            experience_level_map = {
                "Beginner": ExperienceLevel.BEGINNER,
                "Intermediate": ExperienceLevel.INTERMEDIATE,
                "Advanced": ExperienceLevel.ADVANCED
            }
            
            # Map goal to FitnessGoal enum
            goal_map = {
                "Weight Loss": FitnessGoal.WEIGHT_LOSS,
                "Muscle Gain": FitnessGoal.MUSCLE_GAIN,
                "Endurance": FitnessGoal.ENDURANCE,
                "Flexibility": FitnessGoal.FLEXIBILITY,
                "General Fitness": FitnessGoal.GENERAL_FITNESS
            }
            
            # Create State object with proper enum types
            state = State(
                user_id="user_001",
                age=age,
                weight_kg=float(weight),
                height_cm=float(height),
                fitness_goal=goal_map.get(goal, FitnessGoal.GENERAL_FITNESS),
                experience_level=experience_level_map.get(experience, ExperienceLevel.BEGINNER),
                available_equipment=frozenset(equipment) if equipment else frozenset(),
                session_duration_minutes=available_time,
                medical_conditions=frozenset(injuries) if injuries else frozenset()
            )
            
            return {
                'state': state,
                'time': available_time,
                'equipment': equipment,
                'max_exercises': max_exercises,
                'preferences': {
                    'goal': goal,
                    'experience': experience,
                    'difficulty': experience.lower()
                }
            }
    
    return None


def render_workout_plan(response) -> None:
    """
    Render the workout plan with metrics and exercise details.
    
    Args:
        response: RecommendationResponse object
    """
    workout_plan = response.workout_plan
    
    # Success probability
    success_prob = response.success_probability * 100
    
    st.markdown(f"""
    <div class="success-bar">
        <div class="success-fill" style="width: {success_prob}%;">
            {success_prob:.1f}% Success Probability
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(workout_plan.exercises)}</div>
            <div class="metric-label">Exercises</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_duration = workout_plan.total_duration_minutes
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_duration}</div>
            <div class="metric-label">Minutes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_calories = workout_plan.total_calories
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_calories:.0f}</div>
            <div class="metric-label">Calories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate variety as percentage of unique exercise types
        if workout_plan.exercises:
            unique_types = len(set(ex.exercise.category for ex in workout_plan.exercises))
            variety_score = min(100, int((unique_types / max(len(workout_plan.exercises), 1)) * 100))
        else:
            variety_score = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{variety_score}%</div>
            <div class="metric-label">Variety</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Safety warnings
    if response.safety_warnings:
        st.markdown("### ⚠️ Safety Warnings")
        for warning in response.safety_warnings:
            st.warning(warning)
    
    # Exercise list
    st.markdown("### 📋 Exercise Details")
    
    for idx, ex_in_plan in enumerate(workout_plan.exercises, 1):
        exercise = ex_in_plan.exercise
        with st.expander(f"**{idx}. {exercise.name}** ({exercise.category.value.title()}):"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {exercise.description}")
                st.markdown(f"**Target Muscles:** {', '.join(exercise.primary_muscles) if exercise.primary_muscles else 'Full body'}")
                equipment_str = ', '.join(exercise.equipment) if exercise.equipment else 'Bodyweight'
                st.markdown(f"**Equipment:** {equipment_str}")
            
            with col2:
                st.metric("Duration", f"{exercise.duration_minutes} min")
                st.metric("Calories", f"{int(exercise.calories_per_minute * exercise.duration_minutes)}")
                
                # Difficulty badge
                difficulty_colors = {
                    "easy": "🟢",
                    "beginner": "🟢",
                    "medium": "🟡",
                    "intermediate": "🟡",
                    "hard": "🔴",
                    "advanced": "🔴"
                }
                diff_value = exercise.difficulty.value if hasattr(exercise.difficulty, 'value') else str(exercise.difficulty)
                st.markdown(
                    f"{difficulty_colors.get(diff_value.lower(), '⚪')} "
                    f"**{diff_value.title()}**"
                )
            
            # Safety notes
            if hasattr(exercise, 'contraindications') and exercise.contraindications:
                st.info(f"💡 **Safety Tips:** {', '.join(exercise.contraindications)}")
    
    # Alternative plans
    if response.alternative_plans:
        st.markdown("---")
        st.markdown("### 🔄 Alternative Plans")
        st.info(f"Found {len(response.alternative_plans)} alternative workout plans. Consider trying different strategies!")


def render_reasoning_explanations(explanations: List) -> None:
    """
    Render AI reasoning explanations.
    
    Args:
        explanations: List of Explanation objects
    """
    st.markdown("### 🧠 AI Reasoning Explained")
    
    if not explanations:
        st.info("No explanations available.")
        return
    
    # Create tabs for different explanation types
    if len(explanations) > 1:
        tab_names = [exp.title for exp in explanations]
        tabs = st.tabs(tab_names)
        
        for tab, explanation in zip(tabs, explanations):
            with tab:
                _render_single_explanation(explanation)
    else:
        _render_single_explanation(explanations[0])


def _render_single_explanation(explanation) -> None:
    """
    Render a single explanation.
    
    Args:
        explanation: Explanation object
    """
    st.markdown(f"**{explanation.title}**")
    
    if explanation.content:
        st.markdown(explanation.content)
    
    if explanation.reasoning_steps:
        st.markdown("**Reasoning Steps:**")
        for idx, step in enumerate(explanation.reasoning_steps, 1):
            st.markdown(f"{idx}. {step}")
    
    if explanation.details:
        with st.expander("📊 Technical Details"):
            for detail in explanation.details:
                st.markdown(f"• {detail}")
    
    if explanation.confidence is not None:
        confidence_pct = explanation.confidence * 100
        st.progress(explanation.confidence)
        st.caption(f"Confidence: {confidence_pct:.1f}%")


def render_pdf_download(pdf_report, pdf_generator) -> None:
    """
    Render PDF download functionality.
    
    Args:
        pdf_report: PDFReport object
        pdf_generator: PDFGenerator instance
    """
    st.markdown("### 📄 Download Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate PDF
        try:
            pdf_bytes = pdf_generator.generate_pdf(pdf_report)
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Download your workout plan as a professional PDF document"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        # Generate Markdown
        try:
            markdown_content = pdf_generator.generate_markdown(pdf_report)
            
            st.download_button(
                label="📝 Download Markdown",
                data=markdown_content,
                file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                help="Download your workout plan in Markdown format"
            )
        except Exception as e:
            st.error(f"Error generating Markdown: {str(e)}")


def render_metrics_dashboard(workout_plan: WorkoutPlan) -> None:
    """
    Render a metrics dashboard for the workout plan.
    
    Args:
        workout_plan: WorkoutPlan object
    """
    st.markdown("### 📊 Workout Metrics")
    
    # Exercise type distribution
    type_counts = {}
    for ex_in_plan in workout_plan.exercises:
        exercise = ex_in_plan.exercise
        exercise_type = exercise.category.value
        type_counts[exercise_type] = type_counts.get(exercise_type, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Exercise Type Distribution**")
        for ex_type, count in sorted(type_counts.items()):
            percentage = (count / len(workout_plan.exercises)) * 100
            st.progress(percentage / 100)
            st.caption(f"{ex_type.title()}: {count} exercises ({percentage:.0f}%)")
    
    with col2:
        st.markdown("**Difficulty Distribution**")
        difficulty_counts = {}
        for ex_in_plan in workout_plan.exercises:
            exercise = ex_in_plan.exercise
            diff = exercise.difficulty if isinstance(exercise.difficulty, str) else exercise.difficulty.value
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        for diff, count in sorted(difficulty_counts.items()):
            percentage = (count / len(workout_plan.exercises)) * 100
            st.progress(percentage / 100)
            st.caption(f"{diff.title()}: {count} exercises ({percentage:.0f}%)")


def render_tips_section(goal: str) -> None:
    """
    Render workout tips based on the user's goal.
    
    Args:
        goal: User's fitness goal
    """
    st.markdown("### 💡 Workout Tips")
    
    tips = {
        "weight_loss": [
            "Stay hydrated throughout your workout",
            "Focus on maintaining proper form over speed",
            "Combine with a balanced, calorie-controlled diet",
            "Track your progress weekly"
        ],
        "muscle_gain": [
            "Ensure adequate protein intake (1.6-2.2g per kg bodyweight)",
            "Progressive overload is key - gradually increase weights",
            "Get 7-9 hours of sleep for optimal recovery",
            "Focus on compound movements"
        ],
        "endurance": [
            "Start slow and build up gradually",
            "Monitor your heart rate during workouts",
            "Include rest days for recovery",
            "Stay consistent with your training schedule"
        ],
        "flexibility": [
            "Never bounce while stretching",
            "Hold each stretch for 15-30 seconds",
            "Breathe deeply and relax into stretches",
            "Warm up before stretching"
        ],
        "general_fitness": [
            "Aim for variety in your workouts",
            "Listen to your body and rest when needed",
            "Stay consistent - frequency matters more than intensity",
            "Celebrate small wins and progress"
        ]
    }
    
    goal_key = goal.lower().replace(" ", "_")
    relevant_tips = tips.get(goal_key, tips["general_fitness"])
    
    for tip in relevant_tips:
        st.markdown(f"✓ {tip}")
