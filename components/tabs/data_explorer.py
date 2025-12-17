"""
Data Explorer tab component.
"""

import streamlit as st
import pandas as pd
import numpy as np


def render_data_explorer_tab(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render Data Explorer tab content."""
    st.markdown("### Data Explorer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Showing {len(filtered_df):,} records** (filtered from {len(df):,} total)")
    
    with col2:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="filtered_loan_data.csv",
            mime="text/csv"
        )
    
    # Column selection
    all_columns = filtered_df.columns.tolist()
    default_columns = ['id', 'loan_amount', 'grade', 'int_rate', 'annual_income', 
                      'dti', 'loan_status', 'term_months', 'total_payment']
    default_columns = [col for col in default_columns if col in all_columns]
    
    selected_columns = st.multiselect(
        "Select columns to display",
        options=all_columns,
        default=default_columns if default_columns else all_columns[:10]
    )
    
    if selected_columns:
        st.dataframe(
            filtered_df[selected_columns].head(100),
            use_container_width=True,
            height=400
        )
    
    # Statistical Summary
    _render_statistical_summary(filtered_df)


def _render_statistical_summary(filtered_df: pd.DataFrame):
    """Render statistical summary section."""
    st.markdown("### Statistical Summary")
    
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        default_summary = ['loan_amount', 'int_rate', 'annual_income', 'dti']
        default_summary = [col for col in default_summary if col in numeric_cols][:4]
        
        summary_cols = st.multiselect(
            "Select columns for summary",
            options=numeric_cols,
            default=default_summary
        )
        
        if summary_cols:
            summary_df = filtered_df[summary_cols].describe().T.round(2)
            st.dataframe(summary_df, use_container_width=True)