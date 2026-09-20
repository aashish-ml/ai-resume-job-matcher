import json
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Job Matcher",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* ---------- Header ---------- */

    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* ---------- Cards ---------- */

    .info-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        background: rgba(128, 128, 128, 0.04);
        margin-bottom: 1rem;
    }

    .score-card {
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        background: rgba(128, 128, 128, 0.04);
        text-align: center;
        margin-bottom: 1rem;
    }

    .score-number {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .score-label {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 0.4rem;
    }

    /* ---------- Skill Tags ---------- */

    .skill-tag {
        display: inline-block;
        padding: 0.38rem 0.75rem;
        margin: 0.2rem 0.15rem;
        border-radius: 999px;
        font-size: 0.88rem;
        border: 1px solid rgba(128, 128, 128, 0.20);
    }

    .matched-tag {
        background: rgba(34, 197, 94, 0.10);
    }

    .missing-tag {
        background: rgba(239, 68, 68, 0.10);
    }

    .extra-tag {
        background: rgba(59, 130, 246, 0.10);
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ---------- Sidebar ---------- */

    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
    }

    .status-online {
        color: #16a34a;
        font-weight: 600;
    }

    .status-offline {
        color: #dc2626;
        font-weight: 600;
    }

    /* ---------- Footer ---------- */

    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(128, 128, 128, 0.20);
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_API_URL = "http://127.0.0.1:8000"


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

if "job_description" not in st.session_state:
    st.session_state["job_description"] = ""

if "match_result" not in st.session_state:
    st.session_state["match_result"] = None


# ============================================================
# CALLBACK FUNCTIONS
# ============================================================

def load_sample_data():
    """
    Load predefined sample resume and job description.
    This callback runs before the widgets are recreated,
    allowing safe session-state updates.
    """

    st.session_state["resume_text"] = (
        "Python developer with experience in "
        "machine learning, SQL, FastAPI, Docker, "
        "Pandas and NumPy."
    )

    st.session_state["job_description"] = (
        "We are looking for an AI/ML Engineer with "
        "Python, SQL, Machine Learning, Scikit-learn, "
        "FastAPI and Docker skills."
    )

    st.session_state["match_result"] = None


def clear_data():
    """
    Clear all user inputs and previous matching results.
    """

    st.session_state["resume_text"] = ""
    st.session_state["job_description"] = ""
    st.session_state["match_result"] = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙ Configuration</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    api_url = st.text_input(
        "FastAPI URL",
        value=DEFAULT_API_URL,
        help="URL where the FastAPI backend is running.",
    )

    st.divider()

    st.markdown("### 📖 How it works")

    st.markdown(
        """
        **1.** Paste a candidate resume

        **2.** Paste a job description

        **3.** Click **Analyze Match**

        **4.** Review the compatibility score

        **5.** Explore matched, missing and extra skills
        """
    )

    st.divider()

    # --------------------------------------------------------
    # API HEALTH CHECK
    # --------------------------------------------------------

    st.markdown("### 🔌 API Status")

    try:

        health_response = requests.get(
            f"{api_url.rstrip('/')}/health",
            timeout=5,
        )

        if health_response.status_code == 200:

            st.markdown(
                '<div class="status-online">'
                "● API Online"
                "</div>",
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                '<div class="status-offline">'
                "● API Unavailable"
                "</div>",
                unsafe_allow_html=True,
            )

    except requests.RequestException:

        st.markdown(
            '<div class="status-offline">'
            "● API Offline"
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption("AI Resume Job Matcher")
    st.caption("FastAPI + Streamlit")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    "🤖 AI Resume Job Matcher"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
    Analyze how well a candidate's resume matches a job description
    using an AI/ML-oriented skill matching pipeline.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    "📄 Candidate & Job Information"
    "</div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(
    2,
    gap="large",
)


# ============================================================
# RESUME INPUT
# ============================================================

with col1:

    st.markdown("### 👤 Resume")

    resume_text = st.text_area(
        "Paste candidate resume text",
        height=320,
        placeholder=(
            "Example:\n\n"
            "Python developer with experience in machine learning, "
            "SQL, FastAPI, Docker, Pandas and NumPy..."
        ),
        key="resume_text",
    )


# ============================================================
# JOB DESCRIPTION INPUT
# ============================================================

with col2:

    st.markdown("### 💼 Job Description")

    job_description = st.text_area(
        "Paste job description",
        height=320,
        placeholder=(
            "Example:\n\n"
            "We are looking for an AI/ML Engineer with Python, "
            "SQL, Machine Learning, Scikit-learn, FastAPI and Docker skills..."
        ),
        key="job_description",
    )


# ============================================================
# SAMPLE / CLEAR BUTTONS
# ============================================================

sample_col1, sample_col2, sample_col3 = st.columns(
    [1.2, 1.2, 4],
    gap="small",
)


with sample_col1:

    st.button(
        "🧪 Load Sample",
        use_container_width=True,
        on_click=load_sample_data,
        key="load_sample_button",
    )


with sample_col2:

    st.button(
        "🗑️ Clear",
        use_container_width=True,
        on_click=clear_data,
        key="clear_button",
    )


with sample_col3:

    st.caption(
        "Use sample data to quickly test the complete "
        "resume-job matching workflow."
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

analyze = st.button(
    "🚀 Analyze Resume-Job Match",
    type="primary",
    use_container_width=True,
    key="analyze_button",
)


# ============================================================
# API REQUEST
# ============================================================

if analyze:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if not resume_text.strip():

        st.error(
            "Please enter or paste resume text."
        )

    elif not job_description.strip():

        st.error(
            "Please enter or paste a job description."
        )

    else:

        payload = {
            "resume_text": resume_text,
            "job_description": job_description,
        }

        # ----------------------------------------------------
        # API CALL
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Analyzing resume against job description..."
        ):

            try:

                response = requests.post(
                    f"{api_url.rstrip('/')}/match",
                    json=payload,
                    timeout=60,
                )

                # --------------------------------------------
                # SUCCESS
                # --------------------------------------------

                if response.status_code == 200:

                    result = response.json()

                    # IMPORTANT:
                    # Do NOT modify resume_text or
                    # job_description session-state here.
                    #
                    # The text_area widgets already control
                    # these session-state keys.

                    st.session_state["match_result"] = result

                    st.success(
                        "✅ Matching analysis completed successfully."
                    )

                # --------------------------------------------
                # API ERROR
                # --------------------------------------------

                else:

                    try:

                        error_data = response.json()

                    except ValueError:

                        error_data = {
                            "error": response.text
                        }

                    st.error(
                        f"API request failed "
                        f"({response.status_code})"
                    )

                    with st.expander(
                        "🔍 View Error Details"
                    ):

                        st.json(error_data)

            # ------------------------------------------------
            # CONNECTION ERROR
            # ------------------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to FastAPI."
                )

                st.info(
                    "Make sure the FastAPI server is running on "
                    f"{api_url}"
                )

            # ------------------------------------------------
            # TIMEOUT
            # ------------------------------------------------

            except requests.exceptions.Timeout:

                st.error(
                    "⏱ API request timed out."
                )

            # ------------------------------------------------
            # OTHER REQUEST ERROR
            # ------------------------------------------------

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"❌ API request error: {exc}"
                )

            # ------------------------------------------------
            # UNEXPECTED ERROR
            # ------------------------------------------------

            except Exception as exc:

                st.error(
                    f"❌ Unexpected error: {exc}"
                )


# ============================================================
# RESULTS
# ============================================================

if st.session_state["match_result"] is not None:

    result = st.session_state["match_result"]

    st.divider()

    st.markdown(
        '<div class="section-title">'
        "📊 Matching Results"
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # SCORE OVERVIEW
    # ========================================================

    try:

        score = float(
            result.get(
                "match_percentage",
                0,
            )
        )

    except (TypeError, ValueError):

        score = 0.0


    metric1, metric2, metric3, metric4 = st.columns(4)


    with metric1:

        st.metric(
            "Match Score",
            f"{score:.2f}%",
        )


    with metric2:

        st.metric(
            "Matched Skills",
            result.get(
                "matched_count",
                0,
            ),
        )


    with metric3:

        st.metric(
            "Missing Skills",
            result.get(
                "missing_count",
                0,
            ),
        )


    with metric4:

        st.metric(
            "Extra Skills",
            result.get(
                "extra_count",
                0,
            ),
        )


    # ========================================================
    # COMPATIBILITY SCORE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        "🎯 Compatibility Score"
        "</div>",
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-number">{score:.2f}%</div>
            <div class="score-label">
                Overall resume-job compatibility
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.progress(
        max(
            0.0,
            min(
                score,
                100.0,
            ),
        ) / 100.0
    )


    # ========================================================
    # SKILL ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        "🧠 Skill Analysis"
        "</div>",
        unsafe_allow_html=True,
    )


    matched_skills = result.get(
        "matched_skills",
        [],
    )

    missing_skills = result.get(
        "missing_skills",
        [],
    )

    extra_skills = result.get(
        "extra_skills",
        [],
    )


    skill_col1, skill_col2, skill_col3 = st.columns(
        3,
        gap="large",
    )


    # --------------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------------

    with skill_col1:

        st.markdown(
            "#### ✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f'<span class="skill-tag matched-tag">'
                    f"✓ {skill}"
                    "</span>",
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No matched skills found."
            )


    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    with skill_col2:

        st.markdown(
            "#### ❌ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f'<span class="skill-tag missing-tag">'
                    f"⚠ {skill}"
                    "</span>",
                    unsafe_allow_html=True,
                )

        else:

            st.success(
                "No missing skills found."
            )


    # --------------------------------------------------------
    # EXTRA SKILLS
    # --------------------------------------------------------

    with skill_col3:

        st.markdown(
            "#### ➕ Extra Skills"
        )

        if extra_skills:

            for skill in extra_skills:

                st.markdown(
                    f'<span class="skill-tag extra-tag">'
                    f"+ {skill}"
                    "</span>",
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No extra skills found."
            )


    # ========================================================
    # CANDIDATE / JOB SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        "📝 Analysis Summary"
        "</div>",
        unsafe_allow_html=True,
    )


    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.markdown(
            "### 👤 Candidate"
        )

        resume_preview = result.get(
            "resume_name",
            "Candidate resume",
        )

        st.markdown(
            f'<div class="info-card">'
            f"{resume_preview}"
            "</div>",
            unsafe_allow_html=True,
        )


    with summary_col2:

        st.markdown(
            "### 💼 Job"
        )

        job_preview = result.get(
            "job_title",
            "Job description",
        )

        st.markdown(
            f'<div class="info-card">'
            f"{job_preview}"
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # PIPELINE INFORMATION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        "🔧 Pipeline Information"
        "</div>",
        unsafe_allow_html=True,
    )


    info_col1, info_col2, info_col3 = st.columns(3)


    with info_col1:

        st.metric(
            "Pipeline Status",
            result.get(
                "pipeline_status",
                "unknown",
            ),
        )


    with info_col2:

        st.metric(
            "Skill Score",
            result.get(
                "skill_score",
                0,
            ),
        )


    with info_col3:

        st.metric(
            "Maximum Skill Score",
            result.get(
                "skill_score_max",
                0,
            ),
        )


    # ========================================================
    # DOWNLOAD RESULT
    # ========================================================

    st.divider()

    result_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )


    st.download_button(
        label="📥 Download Match Result",
        data=result_json,
        file_name="resume_job_match_result.json",
        mime="application/json",
        use_container_width=True,
        key="download_result_button",
    )


    # ========================================================
    # RAW API RESPONSE
    # ========================================================

    with st.expander(
        "🔍 View Raw API Response"
    ):

        st.json(result)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Resume Job Matcher &nbsp;|&nbsp;
        FastAPI + Streamlit &nbsp;|&nbsp;
        AI/ML Portfolio Project
    </div>
    """,
    unsafe_allow_html=True,
)