"""
Presentation Layer Package.

This layer contains the user interface components for the
AI Gym Workout Recommendation System.

Components:
- Streamlit application (app.py)
- UI components and widgets
- CSS styling
- Interactive forms and displays

The presentation layer:
- Handles user interactions
- Displays data and visualizations
- Provides intuitive interface
- Remains independent of business logic
"""

from src.presentation.ui_components import (
    render_header,
    render_footer,
    render_user_input_form,
    render_workout_plan,
    render_reasoning_explanations,
    render_pdf_download,
    render_metrics_dashboard,
    render_tips_section
)

from src.presentation.ui_state import (
    init_session_state,
    get_session_state,
    update_session_state,
    clear_session_state,
    add_to_history,
    get_history,
    clear_history,
    set_loading,
    is_loading,
    set_error,
    get_error,
    update_settings,
    get_setting
)

__all__ = [
    # UI Components
    'render_header',
    'render_footer',
    'render_user_input_form',
    'render_workout_plan',
    'render_reasoning_explanations',
    'render_pdf_download',
    'render_metrics_dashboard',
    'render_tips_section',
    
    # State Management
    'init_session_state',
    'get_session_state',
    'update_session_state',
    'clear_session_state',
    'add_to_history',
    'get_history',
    'clear_history',
    'set_loading',
    'is_loading',
    'set_error',
    'get_error',
    'update_settings',
    'get_setting'
]
