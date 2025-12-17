"""
Dashboard tab component.
"""

import streamlit as st
import pandas as pd

from components.kpi_metrics import render_kpi_metrics
from charts import (
    create_grade_distribution_chart,
    create_status_pie_chart,
    create_purpose_chart,
    create_region_map,
    create_interest_rate_histogram,
    create_scatter_plot
)


def render_dashboard_tab(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render Dashboard tab content."""
    # KPI Metrics
    st.markdown("### Key Performance Indicators")
    render_kpi_metrics(df, filtered_df)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        fig_grade = create_grade_distribution_chart(filtered_df)
        st.plotly_chart(fig_grade, use_container_width=True)
    
    with col2:
        fig_status = create_status_pie_chart(filtered_df)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        fig_purpose = create_purpose_chart(filtered_df)
        st.plotly_chart(fig_purpose, use_container_width=True)
    
    with col2:
        fig_region = create_region_map(filtered_df)
        st.plotly_chart(fig_region, use_container_width=True)
    
    # Charts Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        fig_histogram = create_interest_rate_histogram(filtered_df)
        st.plotly_chart(fig_histogram, use_container_width=True)
    
    with col2:
        fig_scatter = create_scatter_plot(filtered_df)
        st.plotly_chart(fig_scatter, use_container_width=True)