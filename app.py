import streamlit as st
import warnings

from config.settings import PAGE_CONFIG, CUSTOM_CSS
from utils import load_data, create_loan_status_column
from components import (
    render_header,
    render_footer,
    render_sidebar,
    apply_filters,
    show_filtered_count,
    render_dashboard_tab,
    render_prediction_tab,
    render_data_explorer_tab
)

warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(**PAGE_CONFIG)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Hàm chính chạy ứng dụng Streamlit."""
    
    # Header
    render_header()
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("❌ Không thể load dữ liệu. Vui lòng kiểm tra file financial_loan_clean.csv")
        st.stop()
    
    # Tạo cột loan_status từ one-hot encoding
    df = create_loan_status_column(df)
    
    # Sidebar filters
    filters = render_sidebar(df)
    
    # Check for custom uploaded data
    if 'custom_df' in filters:
        df = filters['custom_df']
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Check if filtered data is empty
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        st.stop()
    
    # Update sidebar with filtered count
    show_filtered_count(len(filtered_df))
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "Dashboard",
        "AI Interest Rate Prediction",
        "Data Explorer"
    ])
    
    with tab1:
        render_dashboard_tab(df, filtered_df)
    
    with tab2:
        render_prediction_tab()
    
    with tab3:
        render_data_explorer_tab(df, filtered_df)
    
    # Footer
    render_footer()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()