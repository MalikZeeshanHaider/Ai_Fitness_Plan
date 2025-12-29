"""
Session State Management for Streamlit Application.

This module provides utilities for managing session state across
page reruns in the Streamlit application.

Functions:
- init_session_state: Initialize default session state values
- get_session_state: Retrieve current session state
- update_session_state: Update session state with new values
- clear_session_state: Clear all or specific session state values
"""

import streamlit as st
from typing import Any, Dict, Optional, List


def init_session_state() -> None:
    """
    Initialize session state with default values.
    
    This function sets up all necessary session state variables
    when the app first loads.
    """
    # User input state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    # Recommendation response
    if 'response' not in st.session_state:
        st.session_state.response = None
    
    # Explanations
    if 'explanations' not in st.session_state:
        st.session_state.explanations = []
    
    # PDF report
    if 'pdf_report' not in st.session_state:
        st.session_state.pdf_report = None
    
    # PDF generator instance
    if 'pdf_generator' not in st.session_state:
        st.session_state.pdf_generator = None
    
    # Generation history
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Current page/view
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'main'
    
    # Settings
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'theme': 'light',
            'show_technical_details': False,
            'auto_generate_pdf': True
        }
    
    # Error state
    if 'last_error' not in st.session_state:
        st.session_state.last_error = None
    
    # Loading state
    if 'is_loading' not in st.session_state:
        st.session_state.is_loading = False


def get_session_state() -> Dict[str, Any]:
    """
    Get the current session state as a dictionary.
    
    Returns:
        Dict[str, Any]: Dictionary containing all session state variables
    """
    return {
        'user_profile': st.session_state.get('user_profile'),
        'response': st.session_state.get('response'),
        'explanations': st.session_state.get('explanations', []),
        'pdf_report': st.session_state.get('pdf_report'),
        'pdf_generator': st.session_state.get('pdf_generator'),
        'history': st.session_state.get('history', []),
        'current_view': st.session_state.get('current_view', 'main'),
        'settings': st.session_state.get('settings', {}),
        'last_error': st.session_state.get('last_error'),
        'is_loading': st.session_state.get('is_loading', False)
    }


def update_session_state(updates: Dict[str, Any]) -> None:
    """
    Update session state with new values.
    
    Args:
        updates: Dictionary of key-value pairs to update
    """
    for key, value in updates.items():
        st.session_state[key] = value


def clear_session_state(keys: Optional[List[str]] = None) -> None:
    """
    Clear session state variables.
    
    Args:
        keys: Optional list of specific keys to clear.
              If None, clears all recommendation-related state.
    """
    if keys is None:
        # Clear recommendation-related state
        keys = [
            'response',
            'explanations',
            'pdf_report',
            'last_error'
        ]
    
    for key in keys:
        if key in st.session_state:
            st.session_state[key] = None if key != 'explanations' else []


def add_to_history(item: Dict[str, Any]) -> None:
    """
    Add an item to the generation history.
    
    Args:
        item: Dictionary containing history item data
    """
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append(item)


def get_history() -> List[Dict[str, Any]]:
    """
    Get the generation history.
    
    Returns:
        List[Dict[str, Any]]: List of history items
    """
    return st.session_state.get('history', [])


def clear_history() -> None:
    """Clear the generation history."""
    st.session_state.history = []


def set_loading(is_loading: bool) -> None:
    """
    Set the loading state.
    
    Args:
        is_loading: Whether the app is currently loading
    """
    st.session_state.is_loading = is_loading


def is_loading() -> bool:
    """
    Check if the app is currently loading.
    
    Returns:
        bool: True if loading, False otherwise
    """
    return st.session_state.get('is_loading', False)


def set_error(error: Optional[str]) -> None:
    """
    Set the last error message.
    
    Args:
        error: Error message or None to clear
    """
    st.session_state.last_error = error


def get_error() -> Optional[str]:
    """
    Get the last error message.
    
    Returns:
        Optional[str]: Last error message or None
    """
    return st.session_state.get('last_error')


def update_settings(setting: str, value: Any) -> None:
    """
    Update a specific setting.
    
    Args:
        setting: Setting key
        value: New value
    """
    if 'settings' not in st.session_state:
        st.session_state.settings = {}
    
    st.session_state.settings[setting] = value


def get_setting(setting: str, default: Any = None) -> Any:
    """
    Get a specific setting value.
    
    Args:
        setting: Setting key
        default: Default value if setting doesn't exist
    
    Returns:
        Any: Setting value or default
    """
    return st.session_state.get('settings', {}).get(setting, default)
