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
import requests
from io import BytesIO
import json
import os
import hashlib

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


# Members storage file path
MEMBERS_FILE = "data/members.json"


def load_members() -> List[Dict]:
    """Load members from JSON file."""
    if os.path.exists(MEMBERS_FILE):
        try:
            with open(MEMBERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_member(member_data: Dict) -> bool:
    """Save a new member to JSON file."""
    try:
        members = load_members()
        
        # Check if email already exists
        for m in members:
            if m.get('email') == member_data.get('email'):
                return False  # Email already registered
        
        # Add member with ID and timestamp
        member_data['id'] = len(members) + 1
        member_data['registered_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        member_data['status'] = 'active'
        
        # Hash the password for security
        if 'password' in member_data:
            member_data['password'] = hashlib.sha256(member_data['password'].encode()).hexdigest()
        
        # Remove sensitive card info (in real app, use payment gateway)
        member_data['card_last_four'] = member_data.get('card_number', '')[-4:] if member_data.get('card_number') else '****'
        member_data.pop('card_number', None)
        member_data.pop('cvv', None)
        
        members.append(member_data)
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(MEMBERS_FILE), exist_ok=True)
        
        with open(MEMBERS_FILE, 'w') as f:
            json.dump(members, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving member: {e}")
        return False


def get_member_count() -> int:
    """Get total number of registered members."""
    return len(load_members())


def get_exercise_tutorial(exercise_name: str) -> Dict[str, Any]:
    """
    Get tutorial information for a specific exercise.
    
    Args:
        exercise_name: Name of the exercise
        
    Returns:
        Dictionary with steps, tips, mistakes, and reps
    """
    # Comprehensive exercise tutorials database
    tutorials = {
        "barbell bench press": {
            "steps": [
                "Lie flat on the bench with your eyes under the bar",
                "Grip the bar slightly wider than shoulder-width apart",
                "Unrack the bar and hold it above your chest with arms extended",
                "Lower the bar slowly to your mid-chest while keeping elbows at 45°",
                "Push the bar back up explosively to the starting position",
                "Keep your feet flat on the floor and maintain a slight arch in your back"
            ],
            "tips": [
                "Keep your shoulder blades pinched together throughout",
                "Don't bounce the bar off your chest",
                "Breathe in as you lower, exhale as you push",
                "Use a spotter for heavy weights"
            ],
            "mistakes": [
                "Flaring elbows too wide (can cause shoulder injury)",
                "Lifting hips off the bench",
                "Not using a full range of motion",
                "Gripping the bar too narrow or too wide"
            ],
            "reps": {
                "beginner": "3 sets x 8-10 reps (light weight)",
                "intermediate": "4 sets x 6-8 reps (moderate weight)",
                "advanced": "5 sets x 4-6 reps (heavy weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=rT7DgCr-3pg"
        },
        "barbell squat": {
            "steps": [
                "Position the bar on your upper back (not on your neck)",
                "Stand with feet shoulder-width apart, toes slightly pointed out",
                "Unrack the bar and take 2-3 steps back",
                "Brace your core and keep your chest up",
                "Lower down by bending knees and hips simultaneously",
                "Go down until thighs are parallel to the floor (or lower)",
                "Drive through your heels to stand back up"
            ],
            "tips": [
                "Keep your knees tracking over your toes",
                "Maintain a neutral spine throughout",
                "Look slightly down to keep neck neutral",
                "Warm up thoroughly before heavy squats"
            ],
            "mistakes": [
                "Letting knees cave inward",
                "Rounding the lower back",
                "Rising on toes instead of pushing through heels",
                "Not hitting proper depth"
            ],
            "reps": {
                "beginner": "3 sets x 10-12 reps (bodyweight or light bar)",
                "intermediate": "4 sets x 6-8 reps (moderate weight)",
                "advanced": "5 sets x 3-5 reps (heavy weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=ultWZbUMPL8"
        },
        "deadlift": {
            "steps": [
                "Stand with feet hip-width apart, bar over mid-foot",
                "Bend at hips and knees to grip the bar (shoulder-width)",
                "Keep your back flat and chest up",
                "Take a deep breath and brace your core",
                "Drive through your feet and extend hips and knees together",
                "Stand tall at the top, squeezing glutes",
                "Lower the bar by hinging at hips first, then bending knees"
            ],
            "tips": [
                "Keep the bar close to your body throughout",
                "Think about pushing the floor away",
                "Lock out by squeezing glutes, not hyperextending back",
                "Use mixed grip or straps for heavy weights"
            ],
            "mistakes": [
                "Rounding the lower back",
                "Starting with hips too high or too low",
                "Letting the bar drift away from body",
                "Jerking the weight off the floor"
            ],
            "reps": {
                "beginner": "3 sets x 8-10 reps (light weight, focus on form)",
                "intermediate": "4 sets x 5-6 reps (moderate weight)",
                "advanced": "5 sets x 1-3 reps (heavy weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=op9kVnSso6Q"
        },
        "pull-ups": {
            "steps": [
                "Grab the bar with hands slightly wider than shoulder-width",
                "Hang with arms fully extended, engage your lats",
                "Pull yourself up by driving elbows down and back",
                "Continue until your chin is over the bar",
                "Lower yourself with control to full arm extension",
                "Repeat without swinging or kipping"
            ],
            "tips": [
                "Squeeze your shoulder blades together as you pull",
                "Keep your core tight to prevent swinging",
                "Focus on pulling with your back, not just arms",
                "Use assisted machine or bands if needed"
            ],
            "mistakes": [
                "Using momentum/kipping instead of strict form",
                "Not going through full range of motion",
                "Shrugging shoulders up to ears",
                "Gripping too wide or too narrow"
            ],
            "reps": {
                "beginner": "3 sets x 3-5 reps (assisted if needed)",
                "intermediate": "4 sets x 6-10 reps (bodyweight)",
                "advanced": "5 sets x 10-15 reps (add weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=eGo4IYlbE5g"
        },
        "push-ups": {
            "steps": [
                "Start in a plank position with hands slightly wider than shoulders",
                "Keep your body in a straight line from head to heels",
                "Lower your chest toward the floor by bending elbows",
                "Keep elbows at about 45° angle to your body",
                "Go down until chest nearly touches the floor",
                "Push back up to the starting position"
            ],
            "tips": [
                "Engage your core throughout the movement",
                "Don't let your hips sag or pike up",
                "Keep your head in neutral position",
                "Modify on knees if needed"
            ],
            "mistakes": [
                "Flaring elbows out to 90°",
                "Letting hips drop or rise",
                "Not using full range of motion",
                "Holding breath"
            ],
            "reps": {
                "beginner": "3 sets x 5-10 reps (on knees if needed)",
                "intermediate": "4 sets x 15-20 reps",
                "advanced": "5 sets x 25-30 reps (or add weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=IODxDxX7oi4"
        },
        "mountain climbers": {
            "steps": [
                "Start in a high plank position with hands under shoulders",
                "Keep your core tight and body in a straight line",
                "Drive one knee toward your chest",
                "Quickly switch legs, driving the other knee forward",
                "Continue alternating legs at a running pace",
                "Keep hips level throughout the movement"
            ],
            "tips": [
                "Move as fast as possible while maintaining form",
                "Keep your shoulders over your wrists",
                "Breathe rhythmically throughout",
                "Land softly on the balls of your feet"
            ],
            "mistakes": [
                "Letting hips bounce up and down",
                "Not bringing knees far enough forward",
                "Holding breath",
                "Shifting weight too far back"
            ],
            "reps": {
                "beginner": "3 sets x 20 seconds",
                "intermediate": "4 sets x 30 seconds",
                "advanced": "5 sets x 45-60 seconds"
            },
            "youtube_video": "https://www.youtube.com/watch?v=nmwgirgXLYM"
        },
        "high knees": {
            "steps": [
                "Stand tall with feet hip-width apart",
                "Drive one knee up toward chest height",
                "Quickly switch and drive the other knee up",
                "Pump your arms in opposition to your legs",
                "Stay on the balls of your feet",
                "Maintain an upright posture throughout"
            ],
            "tips": [
                "Aim to get knees to hip height",
                "Land softly to reduce impact",
                "Keep your core engaged",
                "Maintain a quick, steady rhythm"
            ],
            "mistakes": [
                "Leaning back while running",
                "Not lifting knees high enough",
                "Landing flat-footed",
                "Letting arms hang at sides"
            ],
            "reps": {
                "beginner": "3 sets x 20 seconds",
                "intermediate": "4 sets x 30 seconds",
                "advanced": "5 sets x 45 seconds"
            },
            "youtube_video": "https://www.youtube.com/watch?v=ZZZoCNMU48U"
        },
        "plank": {
            "steps": [
                "Start face down with forearms on the floor",
                "Position elbows directly under shoulders",
                "Lift your body off the ground onto forearms and toes",
                "Keep your body in a straight line from head to heels",
                "Engage your core by pulling belly button to spine",
                "Hold the position while breathing normally"
            ],
            "tips": [
                "Don't hold your breath - breathe steadily",
                "Squeeze your glutes for extra stability",
                "Look at the floor to keep neck neutral",
                "Start with shorter holds and build up"
            ],
            "mistakes": [
                "Letting hips sag toward the floor",
                "Piking hips up too high",
                "Looking up (strains neck)",
                "Holding breath"
            ],
            "reps": {
                "beginner": "3 sets x 20-30 seconds",
                "intermediate": "4 sets x 45-60 seconds",
                "advanced": "5 sets x 90+ seconds"
            },
            "youtube_video": "https://www.youtube.com/watch?v=ASdvN_XEl_c"
        },
        "lunges": {
            "steps": [
                "Stand tall with feet hip-width apart",
                "Step forward with one leg about 2-3 feet",
                "Lower your hips until both knees are at 90°",
                "Keep front knee over ankle (not past toes)",
                "Push through front heel to return to standing",
                "Repeat on the other leg"
            ],
            "tips": [
                "Keep your torso upright throughout",
                "Take a big enough step to achieve proper depth",
                "Control the movement - don't bounce at the bottom",
                "Keep your core engaged for balance"
            ],
            "mistakes": [
                "Front knee going past toes",
                "Leaning forward too much",
                "Taking too short of a step",
                "Letting back knee slam into ground"
            ],
            "reps": {
                "beginner": "3 sets x 8 reps each leg",
                "intermediate": "4 sets x 12 reps each leg",
                "advanced": "5 sets x 15 reps each leg (add weight)"
            },
            "youtube_video": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"
        },
        "burpees": {
            "steps": [
                "Stand with feet shoulder-width apart",
                "Squat down and place hands on the floor",
                "Jump or step feet back into a plank position",
                "Perform a push-up (optional for beginners)",
                "Jump or step feet back toward hands",
                "Explode up into a jump with arms overhead"
            ],
            "tips": [
                "Land softly when jumping",
                "Keep core tight in plank position",
                "Move fluidly between positions",
                "Scale by removing jump or push-up"
            ],
            "mistakes": [
                "Letting hips sag in plank",
                "Not fully extending at the top",
                "Landing with locked knees",
                "Rushing through with poor form"
            ],
            "reps": {
                "beginner": "3 sets x 5 reps (no push-up)",
                "intermediate": "4 sets x 10 reps",
                "advanced": "5 sets x 15-20 reps"
            },
            "youtube_video": "https://www.youtube.com/watch?v=TU8QYVW0gDU"
        }
    }
    
    # Default tutorial for exercises not in database
    default_tutorial = {
        "steps": [
            "Start in the proper starting position",
            "Engage your core and maintain good posture",
            "Perform the movement with controlled tempo",
            "Focus on the target muscles",
            "Return to starting position with control",
            "Repeat for the desired number of repetitions"
        ],
        "tips": [
            "Focus on form over speed or weight",
            "Breathe steadily throughout the movement",
            "Start with lighter weight to master technique",
            "Rest adequately between sets"
        ],
        "mistakes": [
            "Using momentum instead of muscle control",
            "Holding your breath",
            "Rushing through repetitions",
            "Ignoring pain or discomfort"
        ],
        "reps": {
            "beginner": "3 sets x 10-12 reps",
            "intermediate": "4 sets x 8-10 reps",
            "advanced": "5 sets x 6-8 reps"
        }
    }
    
    # Return specific tutorial or default
    return tutorials.get(exercise_name.lower(), default_tutorial)


def render_membership_section() -> None:
    """Render the membership plans section."""
    st.markdown("### 💳 Membership Plans")
    st.markdown("Choose the perfect plan for your fitness journey!")
    
    # Initialize session state for registration
    if 'selected_plan' not in st.session_state:
        st.session_state.selected_plan = None
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; color: white; height: 400px;">
            <h3 style="color: white; margin-bottom: 10px;">🥉 Basic</h3>
            <h2 style="color: white; font-size: 2.5rem; margin: 15px 0;">$9.99</h2>
            <p style="color: #e0e0e0; margin-bottom: 5px;">/month</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <p>✓ 5 Workout Plans/month</p>
            <p>✓ Basic Exercise Library</p>
            <p>✓ Email Support</p>
            <p style="color: #aaa;">✗ Video Tutorials</p>
            <p style="color: #aaa;">✗ Personal Trainer</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Basic", key="basic_plan", use_container_width=True):
            st.session_state.selected_plan = "Basic - $9.99/month"
            st.session_state.registration_complete = False
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; color: white; 
                    height: 400px; box-shadow: 0 10px 40px rgba(240,147,251,0.4); transform: scale(1.05);">
            <div style="background: #FFD700; color: #333; padding: 5px 15px; border-radius: 20px; 
                        display: inline-block; margin-bottom: 10px; font-weight: bold;">⭐ POPULAR</div>
            <h3 style="color: white; margin-bottom: 10px;">🥈 Pro</h3>
            <h2 style="color: white; font-size: 2.5rem; margin: 15px 0;">$19.99</h2>
            <p style="color: #e0e0e0; margin-bottom: 5px;">/month</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <p>✓ Unlimited Workout Plans</p>
            <p>✓ Full Exercise Library</p>
            <p>✓ Video Tutorials</p>
            <p>✓ Priority Support</p>
            <p style="color: #aaa;">✗ Personal Trainer</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Pro", key="pro_plan", use_container_width=True, type="primary"):
            st.session_state.selected_plan = "Pro - $19.99/month"
            st.session_state.registration_complete = False
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; color: white; height: 400px;">
            <h3 style="color: white; margin-bottom: 10px;">🥇 Elite</h3>
            <h2 style="color: white; font-size: 2.5rem; margin: 15px 0;">$39.99</h2>
            <p style="color: #e0e0e0; margin-bottom: 5px;">/month</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <p>✓ Unlimited Everything</p>
            <p>✓ Personal AI Trainer</p>
            <p>✓ Custom Meal Plans</p>
            <p>✓ 24/7 Live Support</p>
            <p>✓ Progress Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Elite", key="elite_plan", use_container_width=True):
            st.session_state.selected_plan = "Elite - $39.99/month"
            st.session_state.registration_complete = False
            st.rerun()
    
    # Registration Form
    if st.session_state.selected_plan and not st.session_state.registration_complete:
        st.markdown("---")
        st.markdown(f"### 📝 Register for {st.session_state.selected_plan.split(' -')[0]} Plan")
        
        with st.form("membership_registration_form"):
            st.info(f"**Selected Plan:** {st.session_state.selected_plan}")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                first_name = st.text_input("First Name *")
                email = st.text_input("Email Address *")
                phone = st.text_input("Phone Number")
            
            with col_b:
                last_name = st.text_input("Last Name *")
                password = st.text_input("Create Password *", type="password")
                confirm_password = st.text_input("Confirm Password *", type="password")
            
            st.markdown("---")
            st.markdown("#### 💳 Payment Information")
            
            pay_col1, pay_col2 = st.columns(2)
            
            with pay_col1:
                card_number = st.text_input("Card Number *")
                card_name = st.text_input("Name on Card *")
            
            with pay_col2:
                exp_col, cvv_col = st.columns(2)
                with exp_col:
                    expiry = st.text_input("Expiry Date *")
                with cvv_col:
                    cvv = st.text_input("CVV *", type="password")
            
            st.markdown("---")
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            newsletter = st.checkbox("Send me workout tips and special offers")
            
            col_submit, col_cancel = st.columns(2)
            
            with col_submit:
                submitted = st.form_submit_button("Complete Registration 🚀", use_container_width=True, type="primary")
            
            with col_cancel:
                cancelled = st.form_submit_button("Cancel", use_container_width=True)
            
            if submitted:
                # Validation
                errors = []
                if not first_name:
                    errors.append("First name is required")
                if not last_name:
                    errors.append("Last name is required")
                if not email or "@" not in email:
                    errors.append("Valid email is required")
                if not password or len(password) < 8:
                    errors.append("Password must be at least 8 characters")
                if password != confirm_password:
                    errors.append("Passwords do not match")
                if not card_number or len(card_number.replace(" ", "")) < 16:
                    errors.append("Valid card number is required")
                if not terms:
                    errors.append("You must agree to the Terms of Service")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Save member to file
                    member_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'password': password,
                        'plan': st.session_state.selected_plan,
                        'card_number': card_number,
                        'card_name': card_name,
                        'card_expiry': expiry,
                        'cvv': cvv,
                        'newsletter': newsletter
                    }
                    
                    if save_member(member_data):
                        st.session_state.registration_complete = True
                        st.session_state.member_name = f"{first_name} {last_name}"
                        st.session_state.member_email = email
                        st.session_state.member_id = get_member_count()
                        st.rerun()
                    else:
                        st.error("❌ Email already registered! Please use a different email or login.")
            
            if cancelled:
                st.session_state.selected_plan = None
                st.rerun()
    
    # Success message after registration
    if st.session_state.registration_complete:
        st.markdown("---")
        st.balloons()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 40px; border-radius: 15px; text-align: center; color: white;">
            <h2 style="color: white;">🎉 Welcome to AI Gym!</h2>
            <p style="font-size: 1.2rem;">Thank you, <strong>{st.session_state.get('member_name', 'Member')}</strong>!</p>
            <p>Your <strong>{st.session_state.selected_plan}</strong> membership is now active.</p>
            <p style="margin-top: 20px;">A confirmation email has been sent to <strong>{st.session_state.get('member_email', '')}</strong></p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <p>🏋️ Start your fitness journey today!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start New Registration", use_container_width=True):
            st.session_state.selected_plan = None
            st.session_state.registration_complete = False
            st.rerun()
    
    st.markdown("---")
    
    # Membership benefits
    st.markdown("### 🎁 All Members Get")
    benefit_cols = st.columns(4)
    
    benefits = [
        ("🏋️", "AI-Powered Plans", "Smart workouts tailored to you"),
        ("📊", "Progress Tracking", "Monitor your fitness journey"),
        ("🎯", "Goal Setting", "Set and achieve your targets"),
        ("📱", "Mobile Access", "Train anywhere, anytime")
    ]
    
    for col, (icon, title, desc) in zip(benefit_cols, benefits):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 2.5rem;">{icon}</div>
                <h4 style="margin: 10px 0;">{title}</h4>
                <p style="color: #666; font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Admin: View registered members (expandable)
    st.markdown("---")
    with st.expander("👥 View Registered Members (Admin)"):
        members = load_members()
        if members:
            st.success(f"**Total Registered Members: {len(members)}**")
            
            # Display members in a table
            for idx, member in enumerate(members, 1):
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                    with col1:
                        st.write(f"**#{member.get('id', idx)}**")
                    with col2:
                        st.write(f"👤 {member.get('first_name', '')} {member.get('last_name', '')}")
                    with col3:
                        st.write(f"📧 {member.get('email', '')}")
                    with col4:
                        plan_name = member.get('plan', '').split(' -')[0] if member.get('plan') else 'N/A'
                        st.write(f"💳 {plan_name}")
                    st.markdown(f"<small style='color:#666'>Registered: {member.get('registered_at', 'N/A')}</small>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No members registered yet. Be the first to join! 🎉")


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
        
        # Create columns for image and exercise card
        img_col, content_col = st.columns([1, 3])
        
        with img_col:
            # Display exercise image using Pexels-style fitness images
            try:
                # Use a hash of exercise name to get consistent but varied images
                exercise_hash = abs(hash(exercise.name)) % 1000
                # Use Lorem Picsum with specific ID for fitness-related images
                image_url = f"https://picsum.photos/id/{(exercise_hash % 200) + 100}/200/150"
                
                # Fetch image using requests
                response = requests.get(image_url, timeout=5)
                if response.status_code == 200:
                    st.image(BytesIO(response.content), use_container_width=True)
                else:
                    # Fallback to placeholder
                    st.image("https://via.placeholder.com/200x150/4F46E5/FFFFFF?text=Exercise", use_container_width=True)
            except Exception as e:
                # Show a colored placeholder box with exercise initial
                st.markdown(f"""
                <div style="width:100%;height:150px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;
                font-size:48px;font-weight:bold;">{exercise.name[0].upper()}</div>
                """, unsafe_allow_html=True)
        
        with content_col:
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
                
                # Tutorial Section
                st.markdown("---")
                st.markdown("#### 📚 Exercise Tutorial")
                
                # Get tutorial data for this exercise
                tutorial = get_exercise_tutorial(exercise.name)
                
                # Step by step instructions
                st.markdown("**📝 Step-by-Step Instructions:**")
                for step_num, step in enumerate(tutorial['steps'], 1):
                    st.markdown(f"{step_num}. {step}")
                
                # Tips
                st.markdown("**💡 Pro Tips:**")
                for tip in tutorial['tips']:
                    st.markdown(f"• {tip}")
                
                # Common mistakes
                with st.expander("⚠️ Common Mistakes to Avoid"):
                    for mistake in tutorial['mistakes']:
                        st.markdown(f"❌ {mistake}")
                
                # Sets and Reps recommendation
                st.markdown("**🔢 Recommended Sets & Reps:**")
                st.markdown(f"• Beginners: {tutorial['reps']['beginner']}")
                st.markdown(f"• Intermediate: {tutorial['reps']['intermediate']}")
                st.markdown(f"• Advanced: {tutorial['reps']['advanced']}")
                
                # Video tutorials
                st.markdown("---")
                st.markdown("**🎬 Video Tutorials:**")
                youtube_search = exercise.name.replace(" ", "+") + "+exercise+tutorial+how+to"
                youtube_url = f"https://www.youtube.com/results?search_query={youtube_search}"
                st.markdown(f"🔗 [Watch on YouTube]({youtube_url})")
                
                # Safety notes
                if hasattr(exercise, 'contraindications') and exercise.contraindications:
                    st.warning(f"⚠️ **Safety Warning:** Not recommended if you have: {', '.join(exercise.contraindications)}")
    
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
