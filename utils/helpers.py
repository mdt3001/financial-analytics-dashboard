"""
Helper functions cho ứng dụng.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def get_loan_status_from_columns(row: pd.Series) -> str:
    """
    Xác định loan status từ các cột one-hot encoding.
    """
    if 'loan_status_Charged Off' in row.index and row.get('loan_status_Charged Off', 0) == 1:
        return 'Charged Off'
    elif 'loan_status_Current' in row.index and row.get('loan_status_Current', 0) == 1:
        return 'Current'
    elif 'loan_status_Fully Paid' in row.index and row.get('loan_status_Fully Paid', 0) == 1:
        return 'Fully Paid'
    return 'Unknown'


def create_loan_status_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo cột loan_status từ các cột one-hot encoding.
    """
    df = df.copy()
    
    status_cols = ['loan_status_Charged Off', 'loan_status_Current', 'loan_status_Fully Paid']
    existing_cols = [col for col in status_cols if col in df.columns]
    
    if existing_cols:
        df['loan_status'] = df.apply(get_loan_status_from_columns, axis=1)
    elif 'loan_status' not in df.columns:
        df['loan_status'] = 'Unknown'
    
    return df


def calculate_installment(loan_amount: float, int_rate: float, term_months: int) -> float:
    """
    Tính installment (khoản trả hàng tháng) dựa trên công thức PMT.
    """
    monthly_rate = int_rate / 12
    if monthly_rate > 0:
        installment = loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / \
                     ((1 + monthly_rate) ** term_months - 1)
    else:
        installment = loan_amount / term_months
    return installment


def process_prediction_input(
    dti: float,
    installment: float,
    loan_amount: float,
    total_payment: float,
    term_months: int,
    grade: str,
    loan_status: str,
    purpose: str,
    verification_status: str
) -> pd.DataFrame:
    """
    Xử lý input từ form và tạo feature DataFrame cho model dự đoán Interest Rate.
    
    Model yêu cầu 19 features với tên chính xác (CatBoost cần tên có space):
    - dti, installment, loan_amount, total_payment, term_months, grade_num
    - loan_status_Charged Off, loan_status_Current, loan_status_Fully Paid
    - purpose_Debt consolidation
    - verification_status_Not Verified, verification_status_Verified
    - grade_A, grade_B, grade_C, grade_D, grade_E, grade_F, grade_G
    """
    # Feature names in exact order model expects (with SPACES for CatBoost)
    feature_names = [
        'dti', 'installment', 'loan_amount', 'total_payment', 'term_months', 'grade_num',
        'loan_status_Charged Off', 'loan_status_Current', 'loan_status_Fully Paid',
        'purpose_Debt consolidation',
        'verification_status_Not Verified', 'verification_status_Verified',
        'grade_A', 'grade_B', 'grade_C', 'grade_D', 'grade_E', 'grade_F', 'grade_G'
    ]
    
    # Initialize all features to 0
    data = {name: [0] for name in feature_names}
    
    # Numerical features
    data['dti'] = [dti]
    data['installment'] = [installment]
    data['loan_amount'] = [loan_amount]
    data['total_payment'] = [total_payment]
    data['term_months'] = [term_months]
    
    # grade_num: A=1, B=2, ..., G=7
    grade_num_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    data['grade_num'] = [grade_num_mapping.get(grade, 3)]
    
    # loan_status one-hot (WITH SPACES!)
    if loan_status == 'Charged Off':
        data['loan_status_Charged Off'] = [1]
    elif loan_status == 'Current':
        data['loan_status_Current'] = [1]
    elif loan_status == 'Fully Paid':
        data['loan_status_Fully Paid'] = [1]
    
    # purpose - only Debt consolidation (WITH SPACE!)
    if purpose == 'Debt consolidation':
        data['purpose_Debt consolidation'] = [1]
    
    # verification_status (WITH SPACES!)
    if verification_status == 'Not Verified':
        data['verification_status_Not Verified'] = [1]
    elif verification_status == 'Verified':
        data['verification_status_Verified'] = [1]
    # Note: 'Source Verified' = both are 0
    
    # grade one-hot
    if grade in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        data[f'grade_{grade}'] = [1]
    
    # Create DataFrame with correct column order
    df = pd.DataFrame(data)
    
    return df[feature_names]


def get_rate_category(rate: float) -> Tuple[str, str, str]:
    """
    Categorize interest rate and return category info.
    
    Returns:
        Tuple of (category_name, color, description)
    """
    if rate < 8:
        return ("Excellent", "#38ef7d", "Very competitive rate! You have an excellent credit profile.")
    elif rate < 12:
        return ("Good", "#667eea", "Good rate. Your credit profile is solid.")
    elif rate < 16:
        return ("Average", "#feca57", "Average rate. There's room for improvement.")
    elif rate < 20:
        return ("Below Average", "#ff9f43", "Higher than average. Consider improving your credit profile.")
    else:
        return ("High Risk", "#f5576c", "High rate due to elevated risk factors. Review improvement tips below.")

def format_currency(value: float) -> str:
    """Format số tiền theo định dạng USD."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format phần trăm."""
    return f"{value:.2f}%"