"""
Sidebar filters component.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from utils.helpers import create_loan_status_column


def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Render sidebar filters và trả về filter values.
    
    Returns:
        Dictionary chứa các giá trị filter
    """
    filters = {}
    
    with st.sidebar:
        st.markdown("## Filters")
        st.markdown("---")
        
        # Upload custom data
        uploaded_file = st.file_uploader(
            "Upload Custom Data",
            type=['csv'],
            help="Upload your own CSV file with the same structure"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df = create_loan_status_column(df)
                st.success("✅ Custom data loaded successfully!")
                filters['custom_df'] = df
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        st.markdown("---")
        
        # Grade Filter
        if 'grade' in df.columns:
            available_grades = sorted(df['grade'].dropna().unique().tolist())
            filters['grades'] = st.multiselect(
                "Credit Grade",
                options=available_grades,
                default=available_grades,
                help="Filter by credit grade (A=Best, G=Worst)"
            )
        else:
            filters['grades'] = []
        
        # State Filter
        if 'address_state' in df.columns:
            available_states = sorted(df['address_state'].dropna().unique().tolist())
            filters['states'] = st.multiselect(
                "State",
                options=available_states,
                default=[],
                help="Filter by state (leave empty for all)"
            )
        else:
            filters['states'] = []
        
        # Region Filter
        if 'region' in df.columns:
            available_regions = sorted(df['region'].dropna().unique().tolist())
            filters['regions'] = st.multiselect(
                "Region",
                options=available_regions,
                default=available_regions,
                help="Filter by region"
            )
        else:
            filters['regions'] = []
        
        # Loan Amount Range
        if 'loan_amount' in df.columns:
            min_amount = int(df['loan_amount'].min())
            max_amount = int(df['loan_amount'].max())
            filters['amount_range'] = st.slider(
                "Loan Amount Range",
                min_value=min_amount,
                max_value=max_amount,
                value=(min_amount, max_amount),
                format="$%d",
                help="Filter by loan amount range"
            )
        else:
            filters['amount_range'] = (0, float('inf'))
        
        # Interest Rate Range
        if 'int_rate' in df.columns:
            min_rate = float(df['int_rate'].min()) * 100
            max_rate = float(df['int_rate'].max()) * 100
            rate_range = st.slider(
                "Interest Rate Range",
                min_value=min_rate,
                max_value=max_rate,
                value=(min_rate, max_rate),
                format="%.1f%%",
                help="Filter by interest rate range"
            )
            filters['rate_range'] = (rate_range[0] / 100, rate_range[1] / 100)
        else:
            filters['rate_range'] = (0, 1)
        
        st.markdown("---")
        st.markdown("### Data Summary")
        st.info(f"Total Records: **{len(df):,}**")
    
    return filters


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to DataFrame."""
    filtered_df = df.copy()
    
    # Apply Grade filter
    if filters.get('grades') and 'grade' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['grade'].isin(filters['grades'])]
    
    # Apply State filter
    if filters.get('states') and 'address_state' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['address_state'].isin(filters['states'])]
    
    # Apply Region filter
    if filters.get('regions') and 'region' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['region'].isin(filters['regions'])]
    
    # Apply Loan Amount filter
    if 'loan_amount' in filtered_df.columns:
        amount_range = filters.get('amount_range', (0, float('inf')))
        filtered_df = filtered_df[
            (filtered_df['loan_amount'] >= amount_range[0]) &
            (filtered_df['loan_amount'] <= amount_range[1])
        ]
    
    # Apply Interest Rate filter
    if 'int_rate' in filtered_df.columns:
        rate_range = filters.get('rate_range', (0, 1))
        filtered_df = filtered_df[
            (filtered_df['int_rate'] >= rate_range[0]) &
            (filtered_df['int_rate'] <= rate_range[1])
        ]
    
    return filtered_df


def show_filtered_count(count: int):
    """Display filtered record count in sidebar."""
    with st.sidebar:
        st.success(f"Filtered Records: **{count:,}**")