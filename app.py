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
    page_title="SpamGuard — Email Spam Detection",
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

    /* ---------- Google Fonts ---------- */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ---------- Global ---------- */

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    .stApp {
        background-color: #F7F1E5;
        color: #2B2118;
    }

    .block-container {
        max-width: 860px !important;
        padding-top: 2.25rem !important;
        padding-bottom: 5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* ---------- Hide Streamlit chrome ---------- */

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { background: transparent !important; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    [data-testid="stStatusWidget"] { display: none; }

    /* ---------- Remove default stMarkdown margin ---------- */

    .stMarkdown { margin-bottom: 0 !important; }

    /* ---------- Scrollbar ---------- */

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #F7F1E5; }
    ::-webkit-scrollbar-thumb { background: #D8C7B3; border-radius: 3px; }

    /* ============================================================
       HEADER
    ============================================================ */

    .sg-header {
        padding-bottom: 1.75rem;
        border-bottom: 1px solid #D8C7B3;
        margin-bottom: 2rem;
    }

    .sg-header-inner {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
    }

    .sg-brand {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #8F1D14;
        margin-bottom: 0.3rem;
        font-family: 'Inter', sans-serif;
    }

    .sg-page-title {
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #2B2118;
        margin: 0 0 0.3rem 0;
        line-height: 1.2;
        font-family: 'Inter', sans-serif;
    }

    .sg-subtitle {
        font-size: 0.92rem;
        color: #735F4D;
        margin: 0;
        line-height: 1.5;
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Backend status badge ---------- */

    .sg-status-wrap {
        flex-shrink: 0;
        padding-top: 0.1rem;
    }

    .sg-status {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 0.35rem 0.7rem;
        border-radius: 20px;
        border: 1px solid;
        white-space: nowrap;
        font-family: 'Inter', sans-serif;
    }

    .sg-status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .sg-status-ok {
        color: #3B6E3B;
        background-color: #EBF4EB;
        border-color: #A8CFA8;
    }

    .sg-status-ok .sg-status-dot {
        background-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.25);
    }

    .sg-status-err {
        color: #8F1D14;
        background-color: #FCE8E5;
        border-color: #D88A80;
    }

    .sg-status-err .sg-status-dot {
        background-color: #B83226;
    }

    /* ============================================================
       EMAIL CARD
    ============================================================ */

    .sg-card {
        background-color: #FFFDF8;
        border: 1px solid #D8C7B3;
        border-radius: 14px;
        padding: 1.5rem 1.5rem 1.25rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 4px rgba(43, 33, 24, 0.05);
    }

    .sg-card-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8F1D14;
        margin-bottom: 0.75rem;
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Textarea overrides ---------- */

    textarea {
        background-color: #FFFDF8 !important;
        color: #2B2118 !important;
        border: 1.5px solid #D8C7B3 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
        line-height: 1.65 !important;
        padding: 0.85rem 1rem !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        resize: vertical !important;
    }

    textarea:focus {
        border-color: #D65A31 !important;
        box-shadow: 0 0 0 2px rgba(214, 90, 49, 0.15) !important;
        outline: none !important;
    }

    textarea::placeholder {
        color: #A08878 !important;
    }

    /* ---------- char count ---------- */

    .sg-char-count {
        font-size: 0.75rem;
        color: #9E886F;
        text-align: right;
        margin-top: 0.4rem;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       ANALYZE BUTTON
    ============================================================ */

    .stButton > button {
        width: 100%;
        background-color: #8F1D14 !important;
        color: #FFFDF8 !important;
        border: none !important;
        border-radius: 9px !important;
        padding: 0.7rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.93rem !important;
        letter-spacing: 0.01em !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease, box-shadow 0.15s ease !important;
        box-shadow: 0 2px 6px rgba(143, 29, 20, 0.25) !important;
    }

    .stButton > button:hover {
        background-color: #B83226 !important;
        box-shadow: 0 4px 12px rgba(143, 29, 20, 0.3) !important;
        color: #FFFDF8 !important;
        border: none !important;
    }

    .stButton > button:active {
        background-color: #741610 !important;
        box-shadow: 0 1px 4px rgba(143, 29, 20, 0.2) !important;
    }

    /* ============================================================
       RESULT CARD
    ============================================================ */

    .sg-result-card {
        padding: 1.5rem 1.65rem;
        border-radius: 14px;
        border: 1.5px solid;
        margin-top: 0.25rem;
        margin-bottom: 1.5rem;
    }

    .sg-result-spam {
        background-color: #FCECE9;
        border-color: #D08070;
    }

    .sg-result-safe {
        background-color: #FAF0E2;
        border-color: #C8A06A;
    }

    .sg-result-label {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.4rem;
        font-family: 'Inter', sans-serif;
    }

    .sg-result-label-spam { color: #9D2419; }
    .sg-result-label-safe { color: #8A4010; }

    .sg-result-title {
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #2B2118;
        margin-bottom: 0.3rem;
        font-family: 'Inter', sans-serif;
    }

    .sg-result-desc {
        font-size: 0.875rem;
        color: #735F4D;
        line-height: 1.55;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       SECTION TITLE
    ============================================================ */

    .sg-section-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #8F1D14;
        margin-bottom: 0.9rem;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       CONFIDENCE PANEL
    ============================================================ */

    .sg-confidence-panel {
        background-color: #FFFDF8;
        border: 1px solid #D8C7B3;
        border-radius: 14px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(43, 33, 24, 0.04);
    }

    .sg-conf-value {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #2B2118;
        line-height: 1;
        margin: 0.2rem 0 0.8rem;
        font-family: 'Inter', sans-serif;
    }

    .sg-progress-track {
        background-color: #EDE3D6;
        border-radius: 99px;
        height: 7px;
        width: 100%;
        overflow: hidden;
    }

    .sg-progress-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .sg-progress-spam {
        background: linear-gradient(90deg, #B83226 0%, #D65A31 100%);
    }

    .sg-progress-safe {
        background: linear-gradient(90deg, #8A6020 0%, #C8952A 100%);
    }

    /* ============================================================
       PROBABILITY BARS
    ============================================================ */

    .sg-prob-panel {
        background-color: #FFFDF8;
        border: 1px solid #D8C7B3;
        border-radius: 14px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(43, 33, 24, 0.04);
    }

    .sg-prob-row {
        margin-bottom: 1.1rem;
    }

    .sg-prob-row:last-child {
        margin-bottom: 0;
    }

    .sg-prob-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.45rem;
    }

    .sg-prob-name {
        font-size: 0.82rem;
        font-weight: 600;
        color: #2B2118;
        font-family: 'Inter', sans-serif;
    }

    .sg-prob-pct {
        font-size: 0.88rem;
        font-weight: 700;
        color: #2B2118;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       EMAIL SUMMARY
    ============================================================ */

    .sg-summary-panel {
        background-color: #FFFDF8;
        border: 1px solid #D8C7B3;
        border-radius: 14px;
        padding: 1.15rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(43, 33, 24, 0.04);
    }

    .sg-summary-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem 1.5rem;
    }

    .sg-summary-item-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #9E886F;
        margin-bottom: 0.15rem;
        font-family: 'Inter', sans-serif;
    }

    .sg-summary-item-value {
        font-size: 0.92rem;
        font-weight: 600;
        color: #2B2118;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       DIVIDER
    ============================================================ */

    .sg-divider {
        border: none;
        border-top: 1px solid #D8C7B3;
        margin: 1.75rem 0;
    }

    /* ============================================================
       FOOTER
    ============================================================ */

    .sg-footer {
        margin-top: 3.5rem;
        padding-top: 1.1rem;
        border-top: 1px solid #D8C7B3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .sg-footer-left {
        font-size: 0.78rem;
        color: #9E886F;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .sg-footer-right {
        font-size: 0.75rem;
        color: #B9A48C;
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       WARNING / INFO OVERRIDES
    ============================================================ */

    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border: 1px solid !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BACKEND STATUS CHECK
# ============================================================

def check_backend() -> bool:
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=3)
        return r.status_code < 500
    except Exception:
        try:
            # try /predict with empty payload; a 422 means backend is up
            r = requests.post(
                f"{BACKEND_URL}/predict",
                json={"email": ""},
                timeout=3
            )
            return True
        except Exception:
            return False


backend_ok = check_backend()

status_html = (
    '<span class="sg-status sg-status-ok">'
    '<span class="sg-status-dot"></span>Backend connected</span>'
    if backend_ok else
    '<span class="sg-status sg-status-err">'
    '<span class="sg-status-dot"></span>Backend unavailable</span>'
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="sg-header">
        <div class="sg-header-inner">
            <div>
                <div class="sg-brand">SpamGuard</div>
                <div class="sg-page-title">Email Spam Detection</div>
                <p class="sg-subtitle">
                    Analyze suspicious email content using machine learning.
                </p>
            </div>
            <div class="sg-status-wrap">
                {status_html}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EMAIL INPUT CARD
# ============================================================

st.markdown(
    '<div class="sg-card-label">Email content</div>',
    unsafe_allow_html=True
)

email = st.text_area(
    "Email",
    placeholder="Paste the email you want to analyze here...",
    height=300,
    label_visibility="collapsed"
)

# Character / word count
char_count = len(email)
word_count = len(email.split()) if email.strip() else 0

if char_count > 0:
    count_text = f"{char_count:,} character{'s' if char_count != 1 else ''} · {word_count:,} word{'s' if word_count != 1 else ''}"
else:
    count_text = "No content entered"

st.markdown(
    f'<div class="sg-char-count">{count_text}</div>',
    unsafe_allow_html=True
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

analyze = st.button("Analyze Email", use_container_width=True)

if analyze:

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

            confidence_pct = confidence * 100
            spam_pct = spam_probability * 100
            ham_pct = ham_probability * 100

            is_spam = prediction == "SPAM"
            progress_cls = "sg-progress-spam" if is_spam else "sg-progress-safe"


            # ====================================================
            # RESULT CARD
            # ====================================================

            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

            if is_spam:
                st.markdown(
                    """
                    <div class="sg-result-card sg-result-spam">
                        <div class="sg-result-label sg-result-label-spam">Classification</div>
                        <div class="sg-result-title">Spam detected</div>
                        <div class="sg-result-desc">
                            This email contains characteristics commonly associated with spam.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="sg-result-card sg-result-safe">
                        <div class="sg-result-label sg-result-label-safe">Classification</div>
                        <div class="sg-result-title">Not spam</div>
                        <div class="sg-result-desc">
                            No strong spam characteristics were detected in this email.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # CONFIDENCE + PROBABILITIES  (two-column layout)
            # ====================================================

            col_conf, col_prob = st.columns([1, 1], gap="medium")

            with col_conf:

                st.markdown(
                    '<div class="sg-section-title">Model confidence</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="sg-confidence-panel">
                        <div class="sg-conf-value">{confidence_pct:.1f}%</div>
                        <div class="sg-progress-track">
                            <div
                                class="sg-progress-fill {progress_cls}"
                                style="width: {confidence_pct:.1f}%;"
                            ></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_prob:

                st.markdown(
                    '<div class="sg-section-title">Prediction probabilities</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="sg-prob-panel">

                        <div class="sg-prob-row">
                            <div class="sg-prob-header">
                                <span class="sg-prob-name">Spam</span>
                                <span class="sg-prob-pct">{spam_pct:.1f}%</span>
                            </div>
                            <div class="sg-progress-track">
                                <div
                                    class="sg-progress-fill sg-progress-spam"
                                    style="width: {spam_pct:.1f}%;"
                                ></div>
                            </div>
                        </div>

                        <div class="sg-prob-row">
                            <div class="sg-prob-header">
                                <span class="sg-prob-name">Not spam</span>
                                <span class="sg-prob-pct">{ham_pct:.1f}%</span>
                            </div>
                            <div class="sg-progress-track">
                                <div
                                    class="sg-progress-fill sg-progress-safe"
                                    style="width: {ham_pct:.1f}%;"
                                ></div>
                            </div>
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # EMAIL SUMMARY
            # ====================================================

            st.markdown("<hr class='sg-divider'>", unsafe_allow_html=True)
            st.markdown(
                '<div class="sg-section-title">Analysis summary</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="sg-summary-panel">
                    <div class="sg-summary-grid">
                        <div>
                            <div class="sg-summary-item-label">Characters</div>
                            <div class="sg-summary-item-value">{char_count:,}</div>
                        </div>
                        <div>
                            <div class="sg-summary-item-label">Words</div>
                            <div class="sg-summary-item-value">{word_count:,}</div>
                        </div>
                        <div>
                            <div class="sg-summary-item-label">Classification</div>
                            <div class="sg-summary-item-value">
                                {"Spam" if is_spam else "Not spam"}
                            </div>
                        </div>
                        <div>
                            <div class="sg-summary-item-label">Model confidence</div>
                            <div class="sg-summary-item-value">{confidence_pct:.1f}%</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the backend. "
                "Make sure the FastAPI server is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond. "
                "Please try again."
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
    <div class="sg-footer">
        <div class="sg-footer-left">SpamGuard &nbsp;·&nbsp; Random Forest Classification</div>
        <div class="sg-footer-right">Machine Learning · Email Security</div>
    </div>
    """,
    unsafe_allow_html=True
)