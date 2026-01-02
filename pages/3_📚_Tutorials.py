"""
Exercise Tutorials Page - Learn proper form for all exercises
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.parent))

from src.presentation.ui_components import get_exercise_tutorial

st.set_page_config(
    page_title="Exercise Tutorials - AI Gym",
    page_icon="📚",
    layout="wide"
)


def render_tutorial(exercise_name: str, tutorial: dict):
    """Render a single exercise tutorial."""
    
    # YouTube Video Section at the top
    st.markdown("**🎬 Video Tutorial:**")
    if 'youtube_video' in tutorial and tutorial['youtube_video']:
        # Display embedded YouTube video
        video_url = tutorial['youtube_video']
        # Extract video ID for embed
        if 'watch?v=' in video_url:
            video_id = video_url.split('watch?v=')[1].split('&')[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            st.markdown(f'''
            <iframe width="100%" height="400" src="{embed_url}" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
            encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            ''', unsafe_allow_html=True)
        st.markdown(f"🔗 [Open in YouTube]({video_url})")
    else:
        # Fallback to search link
        youtube_search = exercise_name.replace(" ", "+") + "+exercise+tutorial+how+to"
        youtube_url = f"https://www.youtube.com/results?search_query={youtube_search}"
        st.markdown(f"🔗 [Search Video Tutorials on YouTube]({youtube_url})")
    
    st.markdown("")
    
    # Steps
    st.markdown("**📝 Step-by-Step Instructions:**")
    for step_num, step in enumerate(tutorial['steps'], 1):
        st.markdown(f"{step_num}. {step}")
    
    st.markdown("")
    
    # Tips
    st.markdown("**💡 Pro Tips:**")
    for tip in tutorial['tips']:
        st.markdown(f"• {tip}")
    
    # Common mistakes
    with st.expander("⚠️ Common Mistakes to Avoid"):
        for mistake in tutorial['mistakes']:
            st.markdown(f"❌ {mistake}")
    
    # Sets and reps
    st.markdown("**🔢 Recommended Sets & Reps:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🟢 **Beginner**\n{tutorial['reps']['beginner']}")
    with col2:
        st.warning(f"🟡 **Intermediate**\n{tutorial['reps']['intermediate']}")
    with col3:
        st.error(f"🔴 **Advanced**\n{tutorial['reps']['advanced']}")


st.markdown("# 📚 Exercise Tutorials")
st.markdown("Learn proper form and technique for all exercises!")
st.markdown("---")

# Exercise categories
exercises_by_category = {
    "💪 Strength - Upper Body": [
        "Barbell Bench Press",
        "Pull-ups",
        "Push-ups",
        "Dumbbell Shoulder Press",
        "Bicep Curls",
        "Tricep Dips"
    ],
    "🦵 Strength - Lower Body": [
        "Barbell Squat",
        "Deadlift",
        "Lunges",
        "Leg Press",
        "Calf Raises",
        "Romanian Deadlift"
    ],
    "❤️ Cardio": [
        "Mountain Climbers",
        "High Knees",
        "Burpees",
        "Jumping Jacks",
        "Jump Rope",
        "Running"
    ],
    "🧘 Core & Flexibility": [
        "Plank",
        "Crunches",
        "Russian Twists",
        "Leg Raises",
        "Bird Dog",
        "Dead Bug"
    ]
}

# Search functionality
search_term = st.text_input("🔍 Search for an exercise", placeholder="e.g., squat, bench press...")

# Category selection
selected_category = st.selectbox(
    "Filter by Category",
    options=["All Categories"] + list(exercises_by_category.keys())
)

st.markdown("---")

# Display exercises
if search_term:
    # Search mode
    st.markdown(f"### 🔍 Search Results for '{search_term}'")
    found = False
    for category, exercises in exercises_by_category.items():
        for exercise in exercises:
            if search_term.lower() in exercise.lower():
                found = True
                tutorial = get_exercise_tutorial(exercise)
                with st.expander(f"**{exercise}** ({category.split(' - ')[-1] if ' - ' in category else category})", expanded=True):
                    render_tutorial(exercise, tutorial)
    if not found:
        st.warning(f"No exercises found matching '{search_term}'. Try a different search term.")
else:
    # Category view
    categories_to_show = exercises_by_category.items() if selected_category == "All Categories" else [(selected_category, exercises_by_category[selected_category])]
    
    for category, exercises in categories_to_show:
        st.markdown(f"### {category}")
        
        cols = st.columns(2)
        for idx, exercise in enumerate(exercises):
            with cols[idx % 2]:
                tutorial = get_exercise_tutorial(exercise)
                with st.expander(f"**{exercise}**"):
                    render_tutorial(exercise, tutorial)
        
        st.markdown("---")
