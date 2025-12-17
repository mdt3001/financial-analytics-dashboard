"""
Data loading functions.
"""

import streamlit as st
import pandas as pd


@st.cache_data(ttl=3600)
def load_data(file_path: str = "financial_loan_clean.csv") -> pd.DataFrame:
    """
    Load và cache dữ liệu từ file CSV.
    
    Args:
        file_path: Đường dẫn đến file CSV
        
    Returns:
        DataFrame chứa dữ liệu khoản vay
    """
    try:
        df = pd.read_csv(file_path)
        
        # Chuyển đổi các cột date nếu có
        date_columns = ['issue_date', 'last_credit_pull_date', 'last_payment_date', 'next_payment_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy file: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {str(e)}")
        return pd.DataFrame()