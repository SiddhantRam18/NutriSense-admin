import streamlit as st


st.set_page_config(
    page_title="Nutrisense - Diet Recommendation",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)


custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Manrope', sans-serif;
        letter-spacing: 0;
    }

    .stApp {
        background:
            radial-gradient(circle at 78% 12%, rgba(20, 184, 166, 0.18), transparent 30%),
            radial-gradient(circle at 18% 18%, rgba(37, 99, 235, 0.22), transparent 34%),
            linear-gradient(135deg, #09070d 0%, #0b1020 48%, #061520 100%);
        color: #f8fafc;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.13;
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
        background-size: 42px 42px;
    }

    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Equal-height columns */
    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }

    [data-testid="stColumn"] {
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="stColumn"] > div,
    [data-testid="stColumn"] > div > div,
    [data-testid="stColumn"] > div > div > div,
    [data-testid="stColumn"] [data-testid="stVerticalBlock"] {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="stColumn"] [data-testid="stMarkdownContainer"] {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }

    .glass-panel {
        flex: 1 !important;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    section[data-testid="stSidebar"] {
        background: rgba(11, 10, 17, 0.84);
        border-right: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(24px) saturate(130%);
        -webkit-backdrop-filter: blur(24px) saturate(130%);
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        background: transparent;
    }

    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 800;
        letter-spacing: 0;
    }

    h1 {
        font-size: clamp(2.7rem, 4.4vw, 4.15rem);
        line-height: 1;
        margin: 0;
        text-shadow: 0 18px 48px rgba(0, 0, 0, 0.42);
    }

    h2 {
        font-size: clamp(2rem, 3.3vw, 3.25rem);
        line-height: 1.14;
        margin-bottom: 1.2rem;
    }

    p, .stMarkdown {
        color: #d1d5db;
        font-size: 1.04rem;
        line-height: 1.75;
    }

    .glass-panel,
    .feature-card,
    .sidebar-glass {
        position: relative;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid rgba(255, 255, 255, 0.28);
        background:
            linear-gradient(145deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.055)),
            rgba(31, 33, 33, 0.48);
        backdrop-filter: blur(28px) saturate(135%);
        -webkit-backdrop-filter: blur(28px) saturate(135%);
        box-shadow:
            0 34px 90px rgba(0, 0, 0, 0.46),
            inset 0 1px 0 rgba(255, 255, 255, 0.34),
            inset 0 -82px 92px rgba(255, 255, 255, 0.025);
    }

    .glass-panel {
        min-height: 360px;
        border-radius: 28px;
        padding: clamp(1.4rem, 2.5vw, 2.65rem);
        display: flex;
        align-items: stretch;
    }

    .feature-card {
        overflow: visible;
        height: auto;
        min-height: 260px;
        border-radius: 22px;
        padding: 2.4rem;
        margin: 1rem 0;
        display: flex;
        align-items: stretch;
        transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.46);
        box-shadow:
            0 40px 100px rgba(0, 0, 0, 0.54),
            inset 0 1px 0 rgba(255, 255, 255, 0.38);
    }

    .glass-panel::before,
    .feature-card::before,
    .sidebar-glass::before {
        content: '';
        position: absolute;
        inset: 0;
        pointer-events: none;
        opacity: 0.28;
        background-image:
            radial-gradient(circle at 25% 20%, rgba(255, 255, 255, 0.18), transparent 1px),
            radial-gradient(circle at 72% 68%, rgba(255, 255, 255, 0.12), transparent 1px);
        background-size: 4px 4px;
    }

    .glass-panel::after,
    .feature-card::after {
        content: '';
        position: absolute;
        left: 2rem;
        right: 2rem;
        top: 5.75rem;
        height: 1px;
        pointer-events: none;
        background: rgba(255, 255, 255, 0.24);
    }

    .glass-content,
    .feature-card-content,
    .sidebar-glass-content {
        position: relative;
        z-index: 1;
        width: 100%;
    }

    .glass-content {
        display: flex;
        min-height: 100%;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }

    .hero-main {
        margin-top: 2rem;
        width: 100%;
    }

    .feature-card-content {
        display: flex;
        min-height: 100%;
        flex-direction: column;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        align-self: flex-start;
        margin-bottom: 0;
        padding: 0.45rem 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 8px;
        color: #f8fafc;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .eyebrow-mark {
        width: 0.65rem;
        height: 0.65rem;
        display: inline-block;
        border: 2px solid #f8fafc;
        border-radius: 3px;
    }

    .section-title {
        margin: 4rem 0 1.8rem;
        text-align: center;
    }

    .feature-index {
        color: rgba(248, 250, 252, 0.72);
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 4.2rem;
        text-transform: uppercase;
    }

    .feature-card h3 {
        color: #f8fafc;
        font-size: clamp(1.1rem, 1.5vw, 1.55rem);
        line-height: 1.25;
        min-height: unset;
        margin: 0 0 1rem;
        word-break: break-word;
    }

    .feature-card p {
        color: #d1d5db;
        font-size: 1rem;
        margin: 0;
        max-width: 100%;
    }

    .nav-link,
    .stButton > button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        color: #f8fafc;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 10px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(16px);
        font-weight: 700;
        min-height: 3.3rem;
        text-decoration: none;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .nav-link:hover,
    .stButton > button:hover {
        color: #ffffff;
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 20px 48px rgba(0, 0, 0, 0.34);
    }

    .nav-link:focus,
    .stButton > button:focus {
        outline: none;
        border-color: rgba(255, 255, 255, 0.56);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.08), 0 20px 48px rgba(0, 0, 0, 0.34);
    }

    .sidebar-glass {
        margin-top: 1.2rem;
        padding: 1.2rem;
        border-radius: 12px;
    }

    .sidebar-glass p {
        color: #f8fafc;
        font-size: 0.95rem;
        margin: 0;
    }

    .rotating-line {
        display: inline-flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 1.35rem;
        color: #e5e7eb;
        font-size: clamp(1.05rem, 1.6vw, 1.3rem);
        font-weight: 700;
    }

    .rotating-window {
        position: relative;
        display: inline-flex;
        min-width: 13.5rem;
        height: 2.75rem;
        overflow: hidden;
        align-items: center;
        justify-content: center;
        padding: 0 1.1rem;
        color: #f8fafc;
        border: 1px solid rgba(255, 255, 255, 0.26);
        border-radius: 12px;
        background:
            linear-gradient(145deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.055)),
            rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(18px) saturate(145%);
        -webkit-backdrop-filter: blur(18px) saturate(145%);
        box-shadow:
            0 14px 34px rgba(0, 0, 0, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.34);
    }

    .rotating-window span {
        position: absolute;
        opacity: 0;
        transform: translateY(120%);
        animation: rotateWords 8s cubic-bezier(0.22, 1, 0.36, 1) infinite;
        white-space: nowrap;
        font-weight: 750;
    }

    .rotating-window span:nth-child(2) {
        animation-delay: 2s;
    }

    .rotating-window span:nth-child(3) {
        animation-delay: 4s;
    }

    .rotating-window span:nth-child(4) {
        animation-delay: 6s;
    }

    @keyframes rotateWords {
        0% {
            opacity: 0;
            transform: translateY(120%);
        }
        8%, 22% {
            opacity: 1;
            transform: translateY(0);
        }
        30%, 100% {
            opacity: 0;
            transform: translateY(-120%);
        }
    }

    @media (max-width: 900px) {
        .glass-panel {
            min-height: unset;
            padding: 1.5rem;
        }

        .feature-card {
            min-height: unset;
            padding: 1.5rem;
        }

        .feature-card h3 {
            font-size: 1.1rem;
        }

        .eyebrow {
            margin-bottom: 0;
        }

        .hero-main {
            margin-top: 3.5rem;
        }
    }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

hero_left, hero_right = st.columns(2, gap="large")

with hero_left:
    st.markdown(
        """
        <div class="glass-panel">
            <div class="glass-content">
                <div class="eyebrow"><span class="eyebrow-mark"></span>Nutrisense</div>
                <div class="hero-main">
                    <h1>NUTRISENSE</h1>
                    <h3 style="color:#e5e7eb; margin-top:0.8rem;">Intelligent Diet Recommendation System</h3>
                    <div class="rotating-line">
                        Built for
                        <span class="rotating-window">
                            <span>balanced meals</span>
                            <span>calorie goals</span>
                            <span>recipe discovery</span>
                            <span>nutrition clarity</span>
                        </span>
                    </div>
                    <p style="max-width: 640px; margin-top: 1.5rem;">
                        Transform your nutrition journey with personalized diet recommendations powered by machine learning and nutritional science.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div class="glass-panel">
            <div class="glass-content">
                <div class="eyebrow"><span class="eyebrow-mark"></span>Nutrition AI</div>
                <div class="hero-main">
                    <h2 style="max-width: 560px;">Plan meals with clearer nutritional context.</h2>
                    <p>Choose a goal, set your meal structure, and explore recipe recommendations in a focused workspace.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<h2 class="section-title">Key Features</h2>', unsafe_allow_html=True)

feature_col1, feature_col2, feature_col3 = st.columns(3, gap="large")

with feature_col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-content">
                <div class="feature-index">Feature 01</div>
                <h3>Smart Recommendations</h3>
                <p>Get personalized diet plans based on nutritional goals and preferences using machine learning algorithms.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-content">
                <div class="feature-index">Feature 02</div>
                <h3>Advanced Analytics</h3>
                <p>Track nutritional content and understand eating patterns with detailed insights and visualizations.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-content">
                <div class="feature-index">Feature 03</div>
                <h3>Food Discovery</h3>
                <p>Explore recipes and custom food recommendations tailored to specific dietary needs and preferences.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<h2 class="section-title">Getting Started</h2>', unsafe_allow_html=True)

start_col1, start_col2 = st.columns(2, gap="large")

with start_col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-content">
                <div class="feature-index">Path 01</div>
                <h3>Diet Recommendation</h3>
                <p>Provide personal details and receive a customized daily diet plan with calorie breakdowns and nutritional guidance.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a class="nav-link" href="/Diet_Recommendation" target="_self">Go to Diet Recommendation</a>',
        unsafe_allow_html=True,
    )

with start_col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-content">
                <div class="feature-index">Path 02</div>
                <h3>Custom Food Search</h3>
                <p>Search for foods, get recipes, and discover detailed nutritional information in one place.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a class="nav-link" href="/Custom_Food_Recommendation" target="_self">Go to Custom Food Search</a>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="text-align:center; color:#9ca3af; font-size:0.95rem; margin:3rem 0 1rem;">
        <p>Powered by <strong>Scikit-Learn</strong> | <strong>FastAPI</strong> | <strong>Streamlit</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-glass">
        <div class="sidebar-glass-content">
            <p>Select a recommendation app from the menu above.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
