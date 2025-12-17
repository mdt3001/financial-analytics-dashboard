"""
KPI Metrics component.
"""

import streamlit as st
import pandas as pd


def render_kpi_metrics(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Hiển thị các KPI metrics chính."""
    col1, col2, col3, col4 = st.columns(4)
    
    # Total Loan Volume
    total_volume = filtered_df['loan_amount'].sum() if 'loan_amount' in filtered_df.columns else 0
    
    with col1:
        st.metric(
            label="📊 Total Loan Volume",
            value=f"${total_volume/1e6:.1f}M",
            delta=f"{len(filtered_df):,} loans"
        )
    
    # Average Interest Rate
    avg_int_rate = filtered_df['int_rate'].mean() * 100 if 'int_rate' in filtered_df.columns else 0
    
    with col2:
        st.metric(
            label="📈 Avg Interest Rate",
            value=f"{avg_int_rate:.2f}%",
            delta=f"DTI: {filtered_df['dti'].mean():.2f}" if 'dti' in filtered_df.columns else "N/A"
        )
    
    # Risk Rate (Charged Off)
    if 'loan_status' in filtered_df.columns:
        risk_count = len(filtered_df[filtered_df['loan_status'] == 'Charged Off'])
        risk_rate = (risk_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    else:
        risk_rate = 0
        risk_count = 0
    
    with col3:
        st.metric(
            label="⚠️ Risk Rate",
            value=f"{risk_rate:.2f}%",
            delta=f"{risk_count:,} charged off" if 'loan_status' in filtered_df.columns else "N/A",
            delta_color="inverse"
        )
    
    # Average Loan Amount
    avg_loan = filtered_df['loan_amount'].mean() if 'loan_amount' in filtered_df.columns else 0
    
    with col4:
        st.metric(
            label="💵 Avg Loan Amount",
            value=f"${avg_loan:,.0f}",
            delta=f"Max: ${filtered_df['loan_amount'].max():,.0f}" if 'loan_amount' in filtered_df.columns else "N/A"
        )