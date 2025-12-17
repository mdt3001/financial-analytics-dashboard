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
) -> np.ndarray:
    """
    Xử lý input từ form và tạo feature vector cho model dự đoán Interest Rate.
    """
    features = np.zeros(19)
    
    # Numerical features
    features[0] = dti
    features[1] = installment
    features[2] = loan_amount
    features[3] = total_payment
    features[4] = term_months
    
    # grade_num: A=1, B=2, ..., G=7
    grade_num_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    features[5] = grade_num_mapping.get(grade, 3)
    
    # loan_status one-hot (indices 6-8)
    if loan_status == 'Charged Off':
        features[6] = 1
    elif loan_status == 'Current':
        features[7] = 1
    elif loan_status == 'Fully Paid':
        features[8] = 1
    
    # purpose_Debt_consolidation (index 9)
    features[9] = 1 if purpose == 'Debt consolidation' else 0
    
    # verification_status (indices 10-11)
    if verification_status == 'Not Verified':
        features[10] = 1
    elif verification_status == 'Verified':
        features[11] = 1
    
    # grade one-hot (indices 12-18: A, B, C, D, E, F, G)
    grade_onehot_mapping = {'A': 12, 'B': 13, 'C': 14, 'D': 15, 'E': 16, 'F': 17, 'G': 18}
    if grade in grade_onehot_mapping:
        features[grade_onehot_mapping[grade]] = 1
    
    return features.reshape(1, -1)


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