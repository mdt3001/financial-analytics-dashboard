"""
Header component.
"""

import streamlit as st


def render_header():
    """Render dashboard header."""
    st.markdown("""
    <div class="dashboard-header">
        <h1>Financial Analytics Dashboard</h1>
        <p>Self-Service Analytics Platform for Loan Portfolio Management</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render dashboard footer."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><strong>Financial Analytics Dashboard</strong></p>
    </div>
    """, unsafe_allow_html=True)