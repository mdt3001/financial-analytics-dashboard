"""
AI Prediction tab component.
"""

import streamlit as st

from utils import load_model, calculate_installment, process_prediction_input, get_rate_category
from charts import create_rate_gauge, create_rate_comparison_chart
from config.settings import PURPOSE_OPTIONS


def render_prediction_tab():
    """Render AI Prediction tab content."""
    st.markdown("### AI-Powered Interest Rate Prediction")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <p style="margin: 0; color: #333;">
            <strong>About this model:</strong> Uses a Stacking Regressor ensemble model 
            trained on historical data to predict the <strong>Interest Rate</strong> 
            that a borrower will receive based on their credit profile.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    model = load_model()
    
    if model is None:
        _render_model_unavailable()
    else:
        st.success("✅ Model loaded successfully!")
        _render_prediction_form(model)


def _render_model_unavailable():
    """Render message when model is unavailable."""
    st.warning("""
    ⚠️ **Model Unavailable**
    
    Unable to load prediction model. Please check:
    1. File `stacking.joblib` exists in the working directory
    2. Required libraries are installed: `pip install joblib xgboost catboost scikit-learn`
    """)


def _render_prediction_form(model):
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
    
    with col2:
        purpose = st.selectbox(
            "Loan Purpose",
            options=PURPOSE_OPTIONS,
            help="Purpose of the loan"
        )
        
        loan_status = st.selectbox(
            "Expected Status",
            options=['Current', 'Fully Paid', 'Charged Off'],
            help="Expected loan status"
        )
        
        verification_status = st.selectbox(
            "Verification Status",
            options=['Not Verified', 'Verified', 'Source Verified'],
            help="Income verification status"
        )
        
        est_total_payment = st.number_input(
            "Estimated Total Payment ($)",
            min_value=loan_amount, max_value=loan_amount * 2,
            value=int(loan_amount * 1.3), step=500,
            help="Estimated total amount to be paid (principal + interest)"
        )
    
    # Calculate installment estimate
    est_int_rate = ((est_total_payment / loan_amount) - 1) / (term_months / 12)
    est_installment = calculate_installment(loan_amount, est_int_rate, term_months)
    
    st.info(f"**Estimated Installment:** ${est_installment:,.2f}/month (based on your total payment input)")
    
    # Predict button
    if st.button("Predict Interest Rate", use_container_width=True, type="primary"):
        _make_prediction(
            model, dti, est_installment, loan_amount, est_total_payment,
            term_months, grade, loan_status, purpose, verification_status
        )


def _make_prediction(model, dti, installment, loan_amount, total_payment,
                     term_months, grade, loan_status, purpose, verification_status):
    """Make prediction and display results."""
    try:
        features = process_prediction_input(
            dti=dti, installment=installment, loan_amount=loan_amount,
            total_payment=total_payment, term_months=term_months,
            grade=grade, loan_status=loan_status,
            purpose=purpose, verification_status=verification_status
        )
        
        predicted_rate = model.predict(features)[0]
        if predicted_rate < 1:
            predicted_rate = predicted_rate * 100
        
        category, color, description = get_rate_category(predicted_rate)
        
        _display_prediction_results(
            predicted_rate, category, color, description,
            loan_amount, term_months, grade, dti, verification_status
        )
        
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")
        st.info("Please check your input parameters.")


def _display_prediction_results(predicted_rate, category, color, description,
                                 loan_amount, term_months, grade, dti, verification_status):
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
    _display_payment_details(predicted_rate, loan_amount, term_months, grade, category)
    
    # Comparison chart
    st.markdown("### Interest Rate Comparison by Grade")
    fig_compare = create_rate_comparison_chart(predicted_rate, grade)
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Tips
    if predicted_rate > 12:
        _display_improvement_tips(dti, grade, verification_status, loan_amount)


def _display_payment_details(predicted_rate, loan_amount, term_months, grade, category):
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
        st.metric(label="Credit Grade", value=grade, delta=category)

def _display_improvement_tips(dti, grade, verification_status, loan_amount):
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
    
    if tips:
        for tip in tips:
            st.markdown(f"- {tip}")
    else:
        st.success("Your profile looks great! Keep maintaining your good credit standing.")