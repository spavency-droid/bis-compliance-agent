import html
import uuid

import streamlit as st
from langgraph.types import Command

from graph.workflow import build_workflow
from data.standards import DEFAULT_STANDARDS
from reports.report_generator import generate_compliance_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BIS Compliance Advisor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HTML HELPER
# ============================================================

def safe(value):
    """Escape dynamic values before placing them in HTML."""
    if value is None:
        return ""

    return html.escape(str(value))


def render_html(content):
    """
    Render real HTML using Streamlit's HTML renderer.

    IMPORTANT:
    Do NOT replace this with st.markdown().
    """
    st.html(content)


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    * {
        box-sizing: border-box;
    }

    html,
    body {
        margin: 0;
        padding: 0;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(83, 70, 255, 0.28),
                transparent 30%
            ),
            radial-gradient(
                circle at 95% 20%,
                rgba(0, 220, 190, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 70% 100%,
                rgba(255, 170, 80, 0.08),
                transparent 30%
            ),
            #070a20;
        color: #f7f7ff;
        min-height: 100vh;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       ANIMATED BACKGROUND
       ====================================================== */

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        width: 450px;
        height: 450px;
        border-radius: 50%;
        background: rgba(83, 70, 255, 0.13);
        filter: blur(100px);
        top: -120px;
        left: -120px;
        pointer-events: none;
        z-index: 0;
        animation: floatPurple 11s ease-in-out infinite alternate;
    }

    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        width: 420px;
        height: 420px;
        border-radius: 50%;
        background: rgba(0, 220, 190, 0.10);
        filter: blur(100px);
        right: -130px;
        bottom: -100px;
        pointer-events: none;
        z-index: 0;
        animation: floatTeal 13s ease-in-out infinite alternate;
    }

    @keyframes floatPurple {
        from {
            transform: translate(0, 0);
        }

        to {
            transform: translate(90px, 80px);
        }
    }

    @keyframes floatTeal {
        from {
            transform: translate(0, 0);
        }

        to {
            transform: translate(-90px, -70px);
        }
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .top-header {
        position: relative;
        z-index: 2;

        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 25px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        width: 46px;
        height: 46px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                #8175ff,
                #43d9c1
            );

        color: white;
        font-size: 24px;
        font-weight: 800;

        box-shadow:
            0 0 30px
            rgba(67, 217, 193, 0.25);

        animation: iconPulse 3s ease-in-out infinite;
    }

    .brand-name {
        color: white;
        font-size: 1.22rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .brand-subtitle {
        color: #8e94b6;
        font-size: 0.76rem;
        margin-top: 2px;
    }

    .status-pill {
        display: flex;
        align-items: center;

        padding: 9px 15px;

        border-radius: 999px;

        background:
            rgba(20, 29, 59, 0.80);

        border:
            1px solid
            rgba(85, 225, 198, 0.28);

        color: #b7f4e7;
        font-size: 0.78rem;

        backdrop-filter: blur(18px);
    }

    .status-dot {
        width: 7px;
        height: 7px;

        margin-right: 8px;

        border-radius: 50%;

        background: #48e2bf;

        box-shadow:
            0 0 12px
            rgba(72, 226, 191, 0.95);

        animation: dotPulse 1.7s ease-in-out infinite;
    }

    @keyframes iconPulse {
        0%,
        100% {
            box-shadow:
                0 0 20px
                rgba(67, 217, 193, 0.15);
        }

        50% {
            box-shadow:
                0 0 42px
                rgba(67, 217, 193, 0.35);
        }
    }

    @keyframes dotPulse {
        0%,
        100% {
            transform: scale(1);
            opacity: 1;
        }

        50% {
            transform: scale(0.65);
            opacity: 0.5;
        }
    }


    /* ======================================================
       GLASS PANELS
       ====================================================== */

    .glass-panel {
        position: relative;
        z-index: 1;

        background:
            linear-gradient(
                145deg,
                rgba(27, 31, 76, 0.90),
                rgba(11, 15, 43, 0.88)
            );

        border:
            1px solid
            rgba(131, 141, 210, 0.22);

        border-radius: 24px;

        box-shadow:
            0 24px 70px
            rgba(0, 0, 0, 0.30),

            inset 0 1px 0
            rgba(255, 255, 255, 0.045);

        backdrop-filter: blur(22px);
    }

    .conversation-panel {
        padding: 32px;
        min-height: 560px;
    }

    .side-panel {
        padding: 24px;
        margin-bottom: 18px;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero-title {
        margin: 0 0 15px 0;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: clamp(
            2.4rem,
            4vw,
            3.7rem
        );

        line-height: 1.02;

        letter-spacing: -0.045em;

        background:
            linear-gradient(
                100deg,
                #ffffff 0%,
                #b8b9ff 50%,
                #75ead3 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-copy {
        max-width: 720px;

        color: #aeb4d1;

        font-size: 1rem;

        line-height: 1.65;
    }


    /* ======================================================
       AI CARD
       ====================================================== */

    .ai-card {
        margin-top: 28px;

        padding: 25px;

        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                rgba(80, 78, 166, 0.27),
                rgba(42, 162, 148, 0.08)
            );

        border:
            1px solid
            rgba(137, 144, 224, 0.23);

        animation:
            cardIn
            0.55s
            ease-out;
    }

    .ai-label {
        color: #91e6d4;

        font-size: 0.70rem;

        font-weight: 800;

        letter-spacing: 0.12em;

        text-transform: uppercase;

        margin-bottom: 10px;
    }

    .question {
        color: white;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 1.55rem;

        line-height: 1.3;
    }

    @keyframes cardIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    /* ======================================================
       PROFILE
       ====================================================== */

    .profile-card {
        position: relative;
        z-index: 2;

        margin-top: 20px;

        padding: 18px;

        border-radius: 18px;

        background:
            rgba(255, 255, 255, 0.035);

        border:
            1px solid
            rgba(255, 255, 255, 0.075);

        animation:
            fadeIn
            0.45s
            ease-out;
    }

    .profile-title {
        color: white;

        font-weight: 750;

        margin-bottom: 14px;
    }

    .profile-item {
        margin-bottom: 8px;

        padding: 12px 14px;

        border-radius: 12px;

        background:
            rgba(255, 255, 255, 0.035);
    }

    .profile-key {
        color: #8188ac;

        font-size: 0.66rem;

        text-transform: uppercase;

        letter-spacing: 0.09em;
    }

    .profile-value {
        color: #eceeff;

        font-size: 0.88rem;

        margin-top: 4px;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }


    /* ======================================================
       RESULT
       ====================================================== */

    .result-card {
        position: relative;
        z-index: 2;

        margin-top: 22px;

        padding: 25px;

        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                rgba(73, 78, 166, 0.35),
                rgba(31, 158, 143, 0.13)
            );

        border:
            1px solid
            rgba(91, 226, 201, 0.30);

        animation:
            resultIn
            0.65s
            cubic-bezier(
                0.2,
                0.8,
                0.2,
                1
            );
    }

    .result-label {
        color: #76e2ce;

        font-size: 0.69rem;

        text-transform: uppercase;

        letter-spacing: 0.12em;

        font-weight: 800;
    }

    .result-id {
        color: #9299bc;

        font-size: 0.82rem;

        margin-top: 11px;
    }

    .result-title {
        color: white;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 1.65rem;

        line-height: 1.2;

        margin-top: 4px;
    }

    .score-number {
        font-size: 2rem;

        font-weight: 850;

        background:
            linear-gradient(
                90deg,
                #8d83ff,
                #49e2c2
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    @keyframes resultIn {
        from {
            opacity: 0;
            transform:
                translateY(18px)
                scale(0.97);
        }

        to {
            opacity: 1;
            transform:
                translateY(0)
                scale(1);
        }
    }


    /* ======================================================
       RIGHT PANEL
       ====================================================== */

    .panel-title {
        color: white;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 1.45rem;
    }

    .panel-subtitle {
        color: #8e94b6;

        font-size: 0.83rem;

        line-height: 1.5;

        margin-top: 5px;

        margin-bottom: 20px;
    }


    /* ======================================================
       WAITING ORB
       ====================================================== */

    .waiting {
        text-align: center;

        padding:
            45px
            10px;

        color: #7f86aa;
    }

    .waiting-orb {
        width: 56px;
        height: 56px;

        margin:
            0
            auto
            17px;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                #8175ff,
                #43d9c1
            );

        box-shadow:
            0 0 40px
            rgba(67, 217, 193, 0.28);

        animation:
            orbPulse
            2.1s
            ease-in-out
            infinite;
    }

    @keyframes orbPulse {
        0%,
        100% {
            transform: scale(0.92);
            opacity: 0.72;
        }

        50% {
            transform: scale(1.08);
            opacity: 1;
        }
    }


    /* ======================================================
       SHORTLIST
       ====================================================== */

    .standard-row {
        margin: 18px 0;
    }

    .standard-top {
        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 12px;

        color: #eceeff;

        font-size: 0.85rem;

        margin-bottom: 7px;
    }

    .standard-name {
        color: #858caf;

        font-size: 0.75rem;

        line-height: 1.35;

        margin-bottom: 8px;
    }

    .score-bar {
        width: 100%;

        height: 8px;

        border-radius: 99px;

        background:
            rgba(255, 255, 255, 0.08);

        overflow: hidden;
    }

    .score-fill {
        height: 100%;

        border-radius: 99px;

        background:
            linear-gradient(
                90deg,
                #45dfbf,
                #c9e95c,
                #ffba4d
            );

        animation:
            barGrow
            1s
            ease-out;
    }

    @keyframes barGrow {
        from {
            width: 0;
        }
    }


    /* ======================================================
       DISCLAIMER
       ====================================================== */

    .disclaimer {
        position: relative;
        z-index: 2;

        margin-top: 18px;

        padding: 14px 16px;

        border-radius: 13px;

        background:
            rgba(245, 158, 11, 0.07);

        border:
            1px solid
            rgba(245, 158, 11, 0.18);

        color: #d6c8aa;

        font-size: 0.76rem;

        line-height: 1.5;
    }


    /* ======================================================
       STREAMLIT INPUT STYLING
       ====================================================== */

    div[data-testid="stTextArea"] textarea {
        background:
            rgba(11, 15, 43, 0.82) !important;

        color: white !important;

        border:
            1px solid
            rgba(130, 139, 205, 0.30) !important;

        border-radius: 15px !important;
    }

    div[data-testid="stTextInput"] input {
        background:
            rgba(11, 15, 43, 0.82) !important;

        color: white !important;

        border:
            1px solid
            rgba(130, 139, 205, 0.30) !important;

        border-radius: 15px !important;
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color:
            #7770ff !important;

        box-shadow:
            0 0 0 2px
            rgba(119, 112, 255, 0.14) !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border: none !important;

        border-radius: 14px !important;

        background:
            linear-gradient(
                100deg,
                #8175ff,
                #43d9c1
            ) !important;

        color: white !important;

        font-weight: 800 !important;

        min-height: 46px !important;

        box-shadow:
            0 8px 25px
            rgba(67, 217, 193, 0.12);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    .stButton > button:hover {
        transform:
            translateY(-2px);

        box-shadow:
            0 13px 35px
            rgba(67, 217, 193, 0.22);
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-title {
            font-size: 2.3rem;
        }

        .conversation-panel {
            min-height: auto;
        }

        .status-pill {
            display: none;
        }
    }

    </style>
    """
)


# ============================================================
# WORKFLOW
# ============================================================

@st.cache_resource
def get_workflow():
    return build_workflow()


workflow = get_workflow()


# ============================================================
# SESSION STATE
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = uuid.uuid4().hex

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "result" not in st.session_state:
    st.session_state.result = None

if "question" not in st.session_state:
    st.session_state.question = None

if "product_description" not in st.session_state:
    st.session_state.product_description = ""


config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


# ============================================================
# WORKFLOW HELPERS
# ============================================================

def get_question(result):
    """
    Safely extract the clarification question from
    a LangGraph interrupted result.
    """

    if result is None:
        return None

    interrupts = result.get("__interrupt__", []) or []

    if not interrupts:
        return None

    value = interrupts[0].value

    if isinstance(value, dict):
        return value.get("question")

    if value is None:
        return None

    return str(value)


def get_ranked_results(result):
    """
    Safely extract ranked retrieval results.
    """

    if result is None:
        return []

    return result.get("ranked_results", []) or []


def unpack_result(item):
    """
    Supports Person 1's RetrievalResult object.

    Also supports dictionaries if serialization
    converts the result.
    """

    if item is None:
        return {}, 0.0

    if hasattr(item, "standard"):
        standard = item.standard or {}
        score = item.combined_score or 0.0

        return (
            standard,
            float(score),
        )

    standard = item.get(
        "standard",
        {},
    ) or {}

    score = item.get(
        "combined_score",
        0.0,
    ) or 0.0

    return (
        standard,
        float(score),
    )


# ============================================================
# PROFILE UI
# ============================================================

def show_profile(profile):

    if not profile:
        return

    if not isinstance(profile, dict):
        return

    materials = profile.get(
        "materials",
        [],
    ) or []

    features = profile.get(
        "features",
        [],
    ) or []

    material_text = (
        ", ".join(map(str, materials))
        if materials
        else "Not specified"
    )

    feature_text = (
        ", ".join(map(str, features))
        if features
        else "Not specified"
    )

    render_html(
        f"""
        <div class="profile-card">

            <div class="profile-title">
                ✦ Extracted product profile
            </div>

            <div
                style="
                    display:grid;
                    grid-template-columns:
                        repeat(2, minmax(0, 1fr));
                    gap:8px;
                "
            >

                <div class="profile-item">

                    <div class="profile-key">
                        Product type
                    </div>

                    <div class="profile-value">
                        {safe(
                            profile.get(
                                "product_type"
                            )
                            or "Not specified"
                        )}
                    </div>

                </div>


                <div class="profile-item">

                    <div class="profile-key">
                        Material
                    </div>

                    <div class="profile-value">
                        {safe(material_text)}
                    </div>

                </div>


                <div class="profile-item">

                    <div class="profile-key">
                        Age group
                    </div>

                    <div class="profile-value">
                        {safe(
                            profile.get(
                                "age_group"
                            )
                            or "Not specified"
                        )}
                    </div>

                </div>


                <div class="profile-item">

                    <div class="profile-key">
                        Power type
                    </div>

                    <div class="profile-value">
                        {safe(
                            profile.get(
                                "power_type"
                            )
                            or "Not specified"
                        )}
                    </div>

                </div>


                <div class="profile-item">

                    <div class="profile-key">
                        Intended use
                    </div>

                    <div class="profile-value">
                        {safe(
                            profile.get(
                                "intended_use"
                            )
                            or "Not specified"
                        )}
                    </div>

                </div>


                <div class="profile-item">

                    <div class="profile-key">
                        Features
                    </div>

                    <div class="profile-value">
                        {safe(feature_text)}
                    </div>

                </div>

            </div>

        </div>
        """
    )


# ============================================================
# LIVE SHORTLIST
# ============================================================

def show_shortlist(result):

    ranked = get_ranked_results(result)

    render_html(
        """
        <div class="glass-panel side-panel">

            <div class="panel-title">
                Live shortlist
            </div>

            <div class="panel-subtitle">
                Standards ranked from the current
                product information.
            </div>
        """
    )

    if not ranked:

        render_html(
            """
            <div class="waiting">

                <div class="waiting-orb"></div>

                <div>
                    Waiting for enough product
                    information...
                </div>

            </div>
            """
        )

    else:

        visible = ranked[:5]

        safe_items = []

        for item in visible:
            try:
                standard, score = unpack_result(item)
                safe_items.append(
                    (
                        standard or {},
                        score,
                    )
                )
            except Exception:
                continue

        scores = [
            score
            for _, score in safe_items
        ]

        maximum = (
            max(scores)
            if scores
            else 1
        )

        for standard, score in safe_items:

            if maximum > 0:
                width = (
                    score
                    / maximum
                    * 100
                )
            else:
                width = 5

            width = max(
                5,
                min(100, width)
            )

            render_html(
                f"""
                <div class="standard-row">

                    <div class="standard-top">

                        <span>
                            {safe(
                                standard.get(
                                    "standard_id",
                                    "Unknown"
                                )
                            )}
                        </span>

                        <span>
                            {score:.3f}
                        </span>

                    </div>


                    <div class="standard-name">
                        {safe(
                            standard.get(
                                "title",
                                "Unknown standard"
                            )
                        )}
                    </div>


                    <div class="score-bar">

                        <div
                            class="score-fill"
                            style="
                                width:{width:.1f}%;
                            "
                        ></div>

                    </div>

                </div>
                """
            )

    render_html(
        """
        </div>
        """
    )


# ============================================================
# FINAL RESULT
# ============================================================

def show_final_result(result):

    ranked = get_ranked_results(result)

    if not ranked:

        render_html(
            """
            <div class="result-card">

                <div class="result-label">
                    Analysis complete
                </div>

                <div class="result-title">
                    No viable standard candidate
                    was found.
                </div>

            </div>
            """
        )

        return None

    try:
        standard, score = unpack_result(
            ranked[0]
        )
    except Exception:
        standard = {}
        score = 0.0

    if not standard:

        render_html(
            """
            <div class="result-card">

                <div class="result-label">
                    Analysis complete
                </div>

                <div class="result-title">
                    No usable standard result
                    was returned.
                </div>

            </div>
            """
        )

        return None

    render_html(
        f"""
        <div class="result-card">

            <div class="result-label">
                Potentially applicable BIS standard
            </div>

            <div class="result-id">
                {safe(
                    standard.get(
                        "standard_id",
                        "Unknown"
                    )
                )}
            </div>

            <div class="result-title">
                {safe(
                    standard.get(
                        "title",
                        "Unknown standard"
                    )
                )}
            </div>

            <div
                style="
                    margin-top:18px;
                "
            >

                <span class="score-number">
                    {score:.3f}
                </span>

                <span
                    style="
                        color:#9298b9;
                        font-size:0.8rem;
                    "
                >
                    &nbsp; combined retrieval score
                </span>

            </div>

        </div>
        """
    )


    if standard.get("category"):

        st.caption(
            f"Category · {standard['category']}"
        )


    if standard.get("scope"):

        st.markdown("#### Scope")

        st.write(
            standard["scope"]
        )


    if standard.get(
        "certification_scheme"
    ):

        st.markdown(
            "#### Certification information"
        )

        st.write(
            standard[
                "certification_scheme"
            ]
        )


    render_html(
        """
        <div class="disclaimer">
            This is an AI-assisted preliminary
            compliance assessment. Verify the current
            applicable BIS requirements before
            certification or commercial decisions.
        </div>
        """
    )

    return standard, score


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="top-header">

        <div class="brand">

            <div class="brand-icon">
                ✦
            </div>

            <div>

                <div class="brand-name">
                    BIS Compliance Advisor
                </div>

                <div class="brand-subtitle">
                    AI-assisted standards discovery
                </div>

            </div>

        </div>


        <div class="status-pill">

            <span class="status-dot"></span>

            Agent online

        </div>

    </div>
    """
)


# ============================================================
# LANDING PAGE
# ============================================================

if not st.session_state.started:

    left, right = st.columns(
        [1.65, 0.85],
        gap="large"
    )


    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------

    with left:

        render_html(
            """
            <div class="glass-panel conversation-panel">

                <div class="hero-title">
                    Which Indian Standard<br>
                    applies to your product?
                </div>


                <div class="hero-copy">
                    Tell us what you make. The AI agent
                    extracts important product details,
                    asks targeted clarification questions,
                    and searches the BIS standards dataset.
                </div>


                <div class="ai-card">

                    <div class="ai-label">
                        AI compliance agent
                    </div>

                    <div class="question">
                        Start with a simple product
                        description.
                    </div>

                </div>

            </div>
            """
        )


        st.markdown(
            "### Product description"
        )


        product_description = st.text_area(
            "Product description",
            placeholder=(
                "Example: A battery-powered plastic "
                "toy car for children aged 5 to 10 years."
            ),
            height=130,
            label_visibility="collapsed",
        )


        if st.button(
            "✦ Find applicable standards",
            type="primary",
            use_container_width=True,
        ):

            if not product_description.strip():

                st.warning(
                    "Please describe your product first."
                )

                st.stop()


            # ----------------------------------------------
            # Reset analysis-specific state
            # ----------------------------------------------

            st.session_state.product_description = (
                product_description
            )

            st.session_state.started = True

            st.session_state.finished = False
            st.session_state.result = None
            st.session_state.question = None


            # ----------------------------------------------
            # Initial LangGraph state
            # ----------------------------------------------

            initial_state = {

                "product_description":
                    product_description,

                "product_profile":
                    {},

                "standards":
                    [
                        standard.model_dump()
                        for standard in DEFAULT_STANDARDS
                    ],

                "question":
                    "",

                "user_answer":
                    "",

                "question_count":
                    0,

                "ranked_results":
                    [],

                "stop_reason":
                    "",
            }


            # ----------------------------------------------
            # Start workflow
            # ----------------------------------------------

            try:

                result = workflow.invoke(
                    initial_state,
                    config=config,
                )

            except Exception as exc:

                st.session_state.started = False
                st.session_state.result = None
                st.session_state.question = None

                st.error(
                    "The compliance workflow could not be started."
                )

                st.exception(exc)

                st.stop()


            # ----------------------------------------------
            # Store workflow state safely
            # ----------------------------------------------

            if result is not None:

                st.session_state.result = result

                st.session_state.question = (
                    get_question(result)
                )

            else:

                st.session_state.result = None
                st.session_state.question = None


            st.rerun()


    # --------------------------------------------------------
    # RIGHT
    # --------------------------------------------------------

    with right:

        render_html(
            """
            <div class="glass-panel side-panel">

                <div class="panel-title">
                    Live shortlist
                </div>

                <div class="panel-subtitle">
                    Standards will appear here as
                    the agent understands your product.
                </div>


                <div class="waiting">

                    <div class="waiting-orb"></div>

                    <div>
                        Waiting for your product
                        description...
                    </div>

                </div>

            </div>
            """
        )


        render_html(
            """
            <div class="glass-panel side-panel">

                <div class="panel-title">
                    How it works
                </div>

                <div class="panel-subtitle">
                    A simple three-step compliance
                    workflow.
                </div>


                <div class="standard-row">

                    <b>
                        01 · Understand
                    </b>

                    <div
                        style="
                            color:#8e94b6;
                            font-size:0.8rem;
                            margin-top:5px;
                        "
                    >
                        Extract product
                        characteristics.
                    </div>

                </div>


                <div class="standard-row">

                    <b>
                        02 · Clarify
                    </b>

                    <div
                        style="
                            color:#8e94b6;
                            font-size:0.8rem;
                            margin-top:5px;
                        "
                    >
                        Ask targeted questions.
                    </div>

                </div>


                <div class="standard-row">

                    <b>
                        03 · Match
                    </b>

                    <div
                        style="
                            color:#8e94b6;
                            font-size:0.8rem;
                            margin-top:5px;
                        "
                    >
                        Retrieve potentially
                        applicable standards.
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# ACTIVE ANALYSIS
# ============================================================

else:

    result = st.session_state.result


    # --------------------------------------------------------
    # IMPORTANT STATE GUARD
    # --------------------------------------------------------

    if result is None:

        st.warning(
            "The analysis state was not available. "
            "Please restart the analysis."
        )

        if st.button(
            "↻ Restart analysis",
            use_container_width=True,
        ):

            st.session_state.clear()
            st.rerun()

        st.stop()


    left, right = st.columns(
        [1.65, 0.85],
        gap="large"
    )


    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------

    with left:

        render_html(
            """
            <div class="glass-panel conversation-panel">

                <div
                    class="hero-title"
                    style="font-size:2.35rem;"
                >
                    Let's identify your standard.
                </div>
            """
        )


        # ----------------------------------------------------
        # User message
        # ----------------------------------------------------

        st.chat_message(
            "user"
        ).write(
            st.session_state.product_description
        )


        # ----------------------------------------------------
        # Extracted profile
        # ----------------------------------------------------

        profile = result.get(
            "product_profile",
            {}
        ) or {}

        show_profile(profile)


        # ----------------------------------------------------
        # Current question
        # ----------------------------------------------------

        question = (
            st.session_state.question
        )


        if (
            question
            and not st.session_state.finished
        ):

            render_html(
                f"""
                <div class="ai-card">

                    <div class="ai-label">
                        ✦ Compliance agent
                    </div>

                    <div class="question">
                        {safe(question)}
                    </div>

                </div>
                """
            )


            st.markdown(
                "<div style='height:10px'></div>",
                unsafe_allow_html=True,
            )


            with st.form(
                "answer_form",
                clear_on_submit=True
            ):

                answer = st.text_input(
                    "Your answer",
                    placeholder=(
                        "Type your answer..."
                    ),
                    label_visibility="collapsed",
                )


                submitted = (
                    st.form_submit_button(
                        "Send answer  →",
                        use_container_width=True,
                    )
                )


            if submitted:

                if not answer.strip():

                    st.warning(
                        "Please enter an answer."
                    )

                    st.stop()


                # ------------------------------------------
                # Resume interrupted LangGraph workflow
                # ------------------------------------------

                try:

                    next_result = workflow.invoke(
                        Command(
                            resume=answer
                        ),
                        config=config,
                    )

                except Exception as exc:

                    st.error(
                        "The workflow could not process "
                        "that answer."
                    )

                    st.exception(exc)

                    st.stop()


                # ------------------------------------------
                # Store next state
                # ------------------------------------------

                if next_result is not None:

                    st.session_state.result = (
                        next_result
                    )

                    next_question = (
                        get_question(
                            next_result
                        )
                    )

                else:

                    st.session_state.result = result
                    next_question = None


                # ------------------------------------------
                # Determine whether workflow continues
                # ------------------------------------------

                if next_question:

                    st.session_state.question = (
                        next_question
                    )

                    st.session_state.finished = False

                else:

                    st.session_state.question = None

                    st.session_state.finished = True


                st.rerun()


        elif st.session_state.finished:

            final = show_final_result(
                result
            )


            if final:

                standard, score = final


                profile = result.get(
                    "product_profile",
                    {}
                ) or {}


                materials = profile.get(
                    "materials",
                    []
                ) or []


                report_profile = {

                    "product_type":
                        profile.get(
                            "product_type",
                            ""
                        ),

                    "category":
                        standard.get(
                            "category",
                            ""
                        ),

                    "material":
                        ", ".join(
                            map(str, materials)
                        ),

                    "power_type":
                        profile.get(
                            "power_type",
                            ""
                        ),

                    "age_group":
                        profile.get(
                            "age_group",
                            ""
                        ),

                    "use_case":
                        profile.get(
                            "intended_use",
                            ""
                        ),
                }


                next_steps = [

                    (
                        "Review the scope and "
                        "requirements of the "
                        "identified standard."
                    ),

                    (
                        "Verify the current BIS "
                        "certification scheme and "
                        "mandatory status."
                    ),

                    (
                        "Confirm testing and "
                        "certification requirements "
                        "with BIS or an authorized "
                        "certification body."
                    ),

                ]


                report = (
                    generate_compliance_report(

                        product_description=(
                            st.session_state
                            .product_description
                        ),

                        product_profile=(
                            report_profile
                        ),

                        recommendation=(
                            standard.get(
                                "standard_id",
                                ""
                            )
                        ),

                        match_score=round(
                            score,
                            3
                        ),

                        next_steps=(
                            next_steps
                        ),
                    )
                )


                st.download_button(
                    "↓ Download compliance report",

                    data=report,

                    file_name=(
                        "bis_compliance_report.md"
                    ),

                    mime="text/markdown",

                    use_container_width=True,
                )


        render_html(
            """
            </div>
            """
        )


    # --------------------------------------------------------
    # RIGHT
    # --------------------------------------------------------

    with right:

        show_shortlist(result)


        if st.session_state.finished:

            render_html(
                """
                <div class="glass-panel side-panel">

                    <div class="panel-title">
                        Analysis complete
                    </div>

                    <div class="panel-subtitle">
                        The agent has finished the
                        clarification cycle.
                    </div>

                    <div
                        style="
                            color:#70e6ce;
                            font-size:0.88rem;
                        "
                    >
                        ✓ Standard identified
                    </div>

                </div>
                """
            )

        else:

            render_html(
                """
                <div class="glass-panel side-panel">

                    <div class="panel-title">
                        Agent status
                    </div>

                    <div class="panel-subtitle">
                        The agent is refining the
                        product profile before making
                        a retrieval decision.
                    </div>

                    <div
                        style="
                            color:#70e6ce;
                            font-size:0.88rem;
                        "
                    >
                        ● Listening for product details
                    </div>

                </div>
                """
            )


# ============================================================
# RESET
# ============================================================

if st.session_state.finished:

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True,
    )


    if st.button(
        "↻ Analyze another product",
        use_container_width=True,
    ):

        st.session_state.clear()

        st.rerun()