"""
AI Prediction tab component.
"""

import streamlit as st

from utils import load_model, load_scaler, calculate_installment, process_prediction_input, get_rate_category
from charts import create_rate_gauge, create_rate_comparison_chart
from config.settings import PURPOSE_OPTIONS


def render_prediction_tab():
    """Render AI Prediction tab content."""
    st.markdown("### AI-Powered Interest Rate Prediction")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <p style="margin: 0; color: #333;">
            <strong>About this model:</strong> Uses an XGBoost model 
            trained on historical data to predict the <strong>Interest Rate</strong> 
            that a borrower will receive based on their credit profile.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    model = load_model()
    scaler = load_scaler()
    
    if model is None:
        _render_model_unavailable()
    elif scaler is None:
        _render_scaler_unavailable()
    else:
        st.success("✅ Model and Scaler loaded successfully!")
        _render_prediction_form(model, scaler)


def _render_model_unavailable():
    """Render message when model is unavailable."""
    st.warning("""
    ⚠️ **Model Unavailable**
    
    Unable to load prediction model. Please check:
    1. File `xgb.joblib` exists in the working directory
    2. Required libraries are installed: `pip install joblib xgboost`
    """)


def _render_scaler_unavailable():
    """Render message when scaler is unavailable."""
    st.warning("""
    ⚠️ **Scaler Unavailable**
    
    Unable to load scaler. Please check:
    1. File `scaler.pkl` exists in the working directory
    2. Required libraries are installed: `pip install joblib scikit-learn`
    """)


def _render_prediction_form(model, scaler):
    """Render the prediction form and results."""
    st.markdown("#### Enter Loan Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=1000, max_value=50000, value=15000, step=1000,
            help="Amount you want to borrow"
        )
        
        term_months = st.selectbox(
            "Loan Term",
            options=[36, 60],
            format_func=lambda x: f"{x} months ({x//12} years)",
            help="Repayment period"
        )
        
        dti = st.slider(
            "DTI - Debt-to-Income Ratio (%)",
            min_value=0.0, max_value=50.0, value=15.0, step=0.5,
            help="Monthly debt payments / Monthly income"
        )
        
        grade = st.selectbox(
            "Credit Grade",
            options=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            index=2,
            help="Credit grade assessment (A=Best, G=Highest Risk)"
        )
        
        sub_grade = st.selectbox(
            "Sub Grade",
            options=['1', '2', '3', '4', '5'],
            index=2,
            help="Sub grade within the credit grade (1=Best, 5=Worst)"
        )
    
    with col2:
        purpose = st.selectbox(
            "Loan Purpose",
            options=PURPOSE_OPTIONS,
            help="Purpose of the loan (Debt consolidation affects rate)"
        )
        
        verification_status = st.selectbox(
            "Verification Status",
            options=['Not Verified', 'Verified', 'Source Verified'],
            help="Income verification status"
        )
        
        # Show grade_encoded calculation
        from utils.helpers import calculate_grade_encoded
        grade_encoded = calculate_grade_encoded(grade, sub_grade)
        st.info(f"**Grade Encoded:** {grade_encoded} (calculated from {grade}{sub_grade})")
        
        # Show purpose_debt info
        purpose_debt = 1 if purpose == 'Debt consolidation' else 0
        st.info(f"**Purpose Debt:** {purpose_debt} ({'Debt consolidation' if purpose_debt else 'Other purpose'})")
    
    # Predict button
    if st.button("Predict Interest Rate", use_container_width=True, type="primary"):
        _make_prediction(
            model, scaler, dti, loan_amount, term_months,
            grade, sub_grade, verification_status, purpose
        )


def _make_prediction(model, scaler, dti, loan_amount, term_months,
                     grade, sub_grade, verification_status, purpose):
    """Make prediction and display results."""
    try:
        # Process input features
        features = process_prediction_input(
            dti=dti,
            loan_amount=loan_amount,
            term_months=term_months,
            grade=grade,
            sub_grade=sub_grade,
            verification_status=verification_status,
            purpose=purpose
        )
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        predicted_rate = model.predict(features_scaled)[0]
        
        # Convert to percentage if needed
        if predicted_rate < 1:
            predicted_rate = predicted_rate * 100
        
        category, color, description = get_rate_category(predicted_rate)
        
        _display_prediction_results(
            predicted_rate, category, color, description,
            loan_amount, term_months, grade, sub_grade, dti, verification_status
        )
        
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")
        st.info("Please check your input parameters.")


def _display_prediction_results(predicted_rate, category, color, description,
                                 loan_amount, term_months, grade, sub_grade, dti, verification_status):
    """Display prediction results."""
    st.markdown("---")
    st.markdown("### Prediction Results")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="rate-card" style="background: linear-gradient(135deg, {color} 0%, {color}99 100%);">
            <p>Predicted Interest Rate</p>
            <h2>{predicted_rate:.2f}%</h2>
            <p><strong>{category}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 10px;">
            <p style="margin: 0; color: #333;">💡 <strong>Assessment:</strong> {description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        fig_gauge = create_rate_gauge(predicted_rate, color)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Payment details
    _display_payment_details(predicted_rate, loan_amount, term_months, grade, sub_grade, category)
    
    # Comparison chart
    st.markdown("### Interest Rate Comparison by Grade")
    fig_compare = create_rate_comparison_chart(predicted_rate, grade)
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Tips
    if predicted_rate > 12:
        _display_improvement_tips(dti, grade, sub_grade, verification_status, loan_amount)


def _display_payment_details(predicted_rate, loan_amount, term_months, grade, sub_grade, category):
    """Display payment details based on predicted rate."""
    st.markdown("### Loan Details with Predicted Rate")
    
    actual_installment = calculate_installment(loan_amount, predicted_rate/100, term_months)
    actual_total_payment = actual_installment * term_months
    actual_total_interest = actual_total_payment - loan_amount
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Monthly Payment", value=f"${actual_installment:,.2f}", delta="per month")
    
    with col2:
        st.metric(label="Total Payment", value=f"${actual_total_payment:,.2f}",
                  delta=f"+${actual_total_interest:,.0f} interest")
    
    with col3:
        st.metric(label="Total Interest", value=f"${actual_total_interest:,.2f}",
                  delta=f"{(actual_total_interest/loan_amount)*100:.1f}% of principal")
    
    with col4:
        st.metric(label="Credit Grade", value=f"{grade}{sub_grade}", delta=category)


def _display_improvement_tips(dti, grade, sub_grade, verification_status, loan_amount):
    """Display tips to improve interest rate."""
    st.markdown("### 💡 Tips to Improve Your Interest Rate")
    tips = []
    
    if dti > 20:
        tips.append("Lower DTI: Pay off existing debts to reduce your debt-to-income ratio")
    if grade in ['D', 'E', 'F', 'G']:
        tips.append("Improve Credit Score: Make on-time payments and reduce credit utilization")
    if verification_status == 'Not Verified':
        tips.append("Verify Income: Provide income verification documents to increase credibility")
    if loan_amount > 25000:
        tips.append("Reduce Loan Amount: Borrowing less may help lower your interest rate")
    if sub_grade in ['4', '5']:
        tips.append("Improve Sub Grade: Work on improving your credit to get a better sub grade")
    
    if tips:
        for tip in tips:
            st.markdown(f"- {tip}")
    else:
        st.success("Your profile looks great! Keep maintaining your good credit standing.")