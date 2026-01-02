"""
Members Page - Admin view of registered members
"""

import streamlit as st
import sys
from pathlib import Path
import json
import os

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.parent))

from src.presentation.ui_components import load_members

st.set_page_config(
    page_title="Members - AI Gym Admin",
    page_icon="👥",
    layout="wide"
)

st.markdown("# 👥 Registered Members")
st.markdown("Admin panel to view and manage gym members")
st.markdown("---")

# Load members
members = load_members()

# Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Members", len(members))

with col2:
    basic_count = len([m for m in members if 'Basic' in m.get('plan', '')])
    st.metric("Basic Plan", basic_count)

with col3:
    pro_count = len([m for m in members if 'Pro' in m.get('plan', '')])
    st.metric("Pro Plan", pro_count)

with col4:
    elite_count = len([m for m in members if 'Elite' in m.get('plan', '')])
    st.metric("Elite Plan", elite_count)

st.markdown("---")

if members:
    # Search
    search = st.text_input("🔍 Search members", placeholder="Search by name or email...")
    
    # Filter
    plan_filter = st.selectbox("Filter by Plan", ["All Plans", "Basic", "Pro", "Elite"])
    
    st.markdown("---")
    
    # Filter members
    filtered_members = members
    if search:
        filtered_members = [m for m in filtered_members if 
                          search.lower() in m.get('first_name', '').lower() or
                          search.lower() in m.get('last_name', '').lower() or
                          search.lower() in m.get('email', '').lower()]
    
    if plan_filter != "All Plans":
        filtered_members = [m for m in filtered_members if plan_filter in m.get('plan', '')]
    
    st.markdown(f"### 📋 Members List ({len(filtered_members)} found)")
    
    # Display as table
    for idx, member in enumerate(filtered_members, 1):
        with st.container():
            col_a, col_b, col_c, col_d, col_e = st.columns([1, 2, 3, 2, 2])
            
            with col_a:
                st.markdown(f"**#{member.get('id', idx)}**")
            
            with col_b:
                st.markdown(f"👤 **{member.get('first_name', '')} {member.get('last_name', '')}**")
            
            with col_c:
                st.markdown(f"📧 {member.get('email', 'N/A')}")
            
            with col_d:
                plan = member.get('plan', 'N/A').split(' -')[0] if member.get('plan') else 'N/A'
                plan_colors = {
                    'Basic': '🥉',
                    'Pro': '🥈',
                    'Elite': '🥇'
                }
                st.markdown(f"{plan_colors.get(plan, '💳')} **{plan}**")
            
            with col_e:
                status = member.get('status', 'active')
                if status == 'active':
                    st.success("✅ Active")
                else:
                    st.error("❌ Inactive")
            
            # Expandable details
            with st.expander("View Details"):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown(f"**Phone:** {member.get('phone', 'Not provided')}")
                    st.markdown(f"**Card:** **** **** **** {member.get('card_last_four', '****')}")
                    st.markdown(f"**Newsletter:** {'✅ Yes' if member.get('newsletter') else '❌ No'}")
                
                with detail_col2:
                    st.markdown(f"**Registered:** {member.get('registered_at', 'N/A')}")
                    st.markdown(f"**Status:** {member.get('status', 'active').title()}")
                    st.markdown(f"**Member ID:** {member.get('id', 'N/A')}")
            
            st.markdown("---")
    
    # Export functionality
    st.markdown("### 📤 Export Data")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # Export as JSON
        members_json = json.dumps(members, indent=2)
        st.download_button(
            label="📥 Export as JSON",
            data=members_json,
            file_name="members_export.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_exp2:
        # Export as CSV
        csv_data = "ID,First Name,Last Name,Email,Phone,Plan,Status,Registered At\n"
        for m in members:
            csv_data += f"{m.get('id', '')},{m.get('first_name', '')},{m.get('last_name', '')},{m.get('email', '')},{m.get('phone', '')},{m.get('plan', '').split(' -')[0] if m.get('plan') else ''},{m.get('status', '')},{m.get('registered_at', '')}\n"
        
        st.download_button(
            label="📥 Export as CSV",
            data=csv_data,
            file_name="members_export.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.info("👋 No members registered yet!")
    st.markdown("""
    <div style="text-align: center; padding: 50px; background: #f8f9fa; border-radius: 15px; margin: 20px 0;">
        <h2>🎯 Get Your First Members!</h2>
        <p style="color: #666; font-size: 1.1rem;">
            Share your gym app and start building your member base.<br/>
            Head to the <strong>Membership</strong> page to register new members.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Go to Membership Page", use_container_width=True):
        st.switch_page("pages/2_💳_Membership.py")
