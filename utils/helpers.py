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


def calculate_grade_encoded(grade: str, sub_grade: str) -> int:
    """
    Tính grade_encoded theo công thức: (chỉ số grade * 5) + (6 - số subgrade)
    Args:
        grade: Credit grade (A-G)
        sub_grade: Sub grade (1-5)
    
    Returns:
        Encoded grade value
    """
    grade_mapping = {'G': 0, 'F': 1, 'E': 2, 'D': 3, 'C': 4, 'B': 5, 'A': 6}
    grade_index = grade_mapping.get(grade.upper(), 0)
    sub_grade_num = int(sub_grade)
    
    return (grade_index * 5) + (6 - sub_grade_num)


def process_prediction_input(
    dti: float,
    loan_amount: float,
    term_months: int,
    grade: str,
    sub_grade: str,
    verification_status: str,
    purpose: str
) -> pd.DataFrame:
    """
    Xử lý input từ form và tạo feature DataFrame cho model XGB.
    
    Model yêu cầu 7 features theo thứ tự:
    - dti
    - loan_amount
    - term_months
    - grade_encoded
    - verification_status_Verified
    - verification_status_Not Verified
    - purpose_debt
    
    Args:
        dti: Debt-to-income ratio
        loan_amount: Loan amount
        term_months: Loan term in months
        grade: Credit grade (A-G)
        sub_grade: Sub grade (1-5)
        verification_status: Verification status
        purpose: Loan purpose
    
    Returns:
        DataFrame with features for prediction
    """
    # Feature names in exact order model expects
    feature_names = [
        'dti', 'loan_amount', 'term_months', 'grade_encoded',
        'verification_status_Verified', 'verification_status_Not Verified', 'purpose_debt'
    ]
    
    # Calculate grade_encoded
    grade_encoded = calculate_grade_encoded(grade, sub_grade)
    
    # Initialize data
    data = {
        'dti': [dti],
        'loan_amount': [loan_amount],
        'term_months': [term_months],
        'grade_encoded': [grade_encoded],
        'verification_status_Verified': [0],
        'verification_status_Not Verified': [0],
        'purpose_debt': [0]
    }
    
    # Set verification status
    if verification_status == 'Verified':
        data['verification_status_Verified'] = [1]
    elif verification_status == 'Not Verified':
        data['verification_status_Not Verified'] = [1]
    # 'Source Verified' = both are 0
    
    # Set purpose_debt (1 if Debt consolidation, 0 otherwise)
    if purpose == 'Debt consolidation':
        data['purpose_debt'] = [1]
    
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