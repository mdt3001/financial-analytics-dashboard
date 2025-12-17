"""
Model loading functions.
"""

import streamlit as st


@st.cache_resource
def load_model(model_path: str = "stacking.joblib"):
    """
    Load và cache model từ file joblib.
    
    Args:
        model_path: Đường dẫn đến file model
        
    Returns:
        Model đã được train hoặc None nếu lỗi
    """
    try:
        import joblib
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.warning(f"⚠️ Không tìm thấy file model: {model_path}")
        return None
    except ImportError:
        st.warning("⚠️ Cần cài đặt thư viện: pip install joblib xgboost catboost")
        return None
    except Exception as e:
        st.warning(f"⚠️ Lỗi khi load model: {str(e)}")
        return None