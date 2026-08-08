import os

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="SpamGuard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background-color: #F7F1E5;
        color: #2B2118;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* ---------- Hide Streamlit branding ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- Typography ---------- */

    h1, h2, h3 {
        color: #2B2118 !important;
        font-family: Arial, sans-serif;
    }

    p, label, span {
        color: #4A392D;
    }

    /* ---------- Header ---------- */

    .brand {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #8F1D14;
        margin-bottom: 0.25rem;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #2B2118;
        margin-bottom: 0.35rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #735F4D;
        margin-bottom: 2rem;
    }

    /* ---------- Input ---------- */

    textarea {
        background-color: #FFFDF8 !important;
        color: #2B2118 !important;
        border: 1px solid #D8C7B3 !important;
        border-radius: 10px !important;
    }

    textarea:focus {
        border-color: #D65A31 !important;
        box-shadow: 0 0 0 1px #D65A31 !important;
    }

    /* ---------- Button ---------- */

    .stButton > button {
        width: 100%;
        background-color: #B83226;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1rem;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .stButton > button:hover {
        background-color: #8F1D14;
        color: white;
        border: none;
    }

    /* ---------- Result Cards ---------- */

    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        border: 1px solid;
    }

    .spam-card {
        background-color: #FCE8E5;
        border-color: #D88A80;
    }

    .safe-card {
        background-color: #F9EBDD;
        border-color: #D9A06E;
    }

    .result-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .spam-label {
        color: #9D2419;
    }

    .safe-label {
        color: #A34D16;
    }

    .result-title {
        font-size: 1.65rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: #2B2118;
    }

    .result-description {
        color: #735F4D;
        font-size: 0.9rem;
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        background-color: #FFFDF8;
        border: 1px solid #D8C7B3;
        border-radius: 10px;
        padding: 1.15rem;
        margin-top: 1rem;
    }

    .metric-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #806B58;
    }

    .metric-value {
        font-size: 1.45rem;
        font-weight: 700;
        color: #2B2118;
        margin-top: 0.25rem;
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2B2118;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        margin-top: 4rem;
        padding-top: 1.25rem;
        border-top: 1px solid #D8C7B3;
        color: #8B7764;
        font-size: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="brand">SPAMGUARD</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-title">Email Spam Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze email content using a trained machine learning model.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# EMAIL INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Email content</div>',
    unsafe_allow_html=True
)

email = st.text_area(
    "Email",
    placeholder=(
        "Paste the email you want to analyze here..."
    ),
    height=280,
    label_visibility="collapsed"
)


# ============================================================
# ANALYZE
# ============================================================

if st.button("Analyze Email", use_container_width=True):

    if not email.strip():

        st.warning("Enter some email content before analyzing.")

    else:

        try:

            with st.spinner("Analyzing email..."):

                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    json={
                        "email": email
                    },
                    timeout=30
                )

                response.raise_for_status()

                result = response.json()


            prediction = result["prediction"]
            confidence = result["confidence"]
            spam_probability = result["spam_probability"]
            ham_probability = result["ham_probability"]


            # ====================================================
            # RESULT
            # ====================================================

            if prediction == "SPAM":

                st.markdown(
                    f"""
                    <div class="result-card spam-card">

                        <div class="result-label spam-label">
                            Classification
                        </div>

                        <div class="result-title">
                            Spam detected
                        </div>

                        <div class="result-description">
                            The model identified characteristics
                            commonly associated with spam.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="result-card safe-card">

                        <div class="result-label safe-label">
                            Classification
                        </div>

                        <div class="result-title">
                            Not spam
                        </div>

                        <div class="result-description">
                            The model did not identify strong
                            spam characteristics in this email.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # METRICS
            # ====================================================

            st.markdown(
                '<div class="section-title">Model results</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-title">
                            Confidence
                        </div>

                        <div class="metric-value">
                            {confidence * 100:.1f}%
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-title">
                            Spam probability
                        </div>

                        <div class="metric-value">
                            {spam_probability * 100:.1f}%
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-title">
                            Not spam probability
                        </div>

                        <div class="metric-value">
                            {ham_probability * 100:.1f}%
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # PROBABILITY CHART
            # ====================================================

            st.markdown(
                '<div class="section-title">'
                'Prediction probabilities'
                '</div>',
                unsafe_allow_html=True
            )

            chart_data = {
                "Probability": {
                    "Spam": spam_probability,
                    "Not Spam": ham_probability
                }
            }

            st.bar_chart(chart_data)


        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the backend. "
                "Make sure FastAPI is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond."
            )


        except requests.exceptions.HTTPError as error:

            st.error(
                f"Backend request failed: {error}"
            )


        except Exception as error:

            st.error(
                f"An unexpected error occurred: {error}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SpamGuard · Random Forest Spam Classification
    </div>
    """,
    unsafe_allow_html=True
)