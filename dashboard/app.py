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
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }

        .result-card {
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 1rem;
        }

        .skill-tag {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            margin: 0.2rem;
            border-radius: 20px;
            background-color: rgba(0, 128, 255, 0.10);
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Configuration")

    api_url = st.text_input(
        "FastAPI URL",
        value=API_URL,
    )

    st.divider()

    st.markdown("### 📌 How it works")

    st.markdown(
        """
        1. Paste a resume
        2. Paste a job description
        3. Click **Analyze Match**
        4. Review the compatibility score
        5. Explore matched and missing skills
        """
    )

    st.divider()

    st.caption("AI Resume Job Matcher")
    st.caption("FastAPI + Streamlit")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Resume Job Matcher</div>',
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

st.subheader("📄 Candidate & Job Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Resume")

    resume_text = st.text_area(
    "Paste candidate resume text",
    value=st.session_state.get("resume_text", ""),
    height=320,
    placeholder=(
        "Example:\n\n"
        "Python developer with experience in machine learning, "
        "SQL, FastAPI, Docker, Pandas and NumPy..."
    ),
)


with col2:
    st.markdown("### 💼 Job Description")

    job_description = st.text_area(
    "Paste job description",
    value=st.session_state.get("job_description", ""),
    height=320,
    placeholder=(
        "Example:\n\n"
        "We are looking for an AI/ML Engineer with Python, "
        "SQL, Machine Learning, FastAPI and Docker skills..."
    ),
)


# ============================================================
# SAMPLE DATA
# ============================================================

sample_col1, sample_col2 = st.columns([1, 5])

with sample_col1:
    load_sample = st.button(
        "🧪 Load Sample",
        use_container_width=True,
    )

with sample_col2:
    st.caption(
        "Use sample data to quickly test the complete matching workflow."
    )


if load_sample:
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

    st.rerun()


# ============================================================
# MATCH BUTTON
# ============================================================

st.divider()

analyze = st.button(
    "🚀 Analyze Resume–Job Match",
    type="primary",
    use_container_width=True,
)


# ============================================================
# API REQUEST
# ============================================================

if analyze:

    if not resume_text.strip():
        st.error("Please enter or paste resume text.")

    elif not job_description.strip():
        st.error("Please enter or paste a job description.")

    else:

        payload = {
            "resume_text": resume_text,
            "job_description": job_description,
        }

        with st.spinner("🔍 Analyzing resume against job description..."):

            try:

                response = requests.post(
                    f"{api_url.rstrip('/')}/match",
                    json=payload,
                    timeout=60,
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("✅ Matching analysis completed successfully.")

                    # Save result
                    st.session_state["match_result"] = result

                else:

                    try:
                        error_data = response.json()
                    except Exception:
                        error_data = response.text

                    st.error(
                        f"API request failed ({response.status_code})"
                    )

                    st.json(error_data)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to FastAPI."
                )

                st.info(
                    "Make sure the FastAPI server is running on "
                    f"{api_url}"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ API request timed out."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ============================================================
# RESULTS
# ============================================================

if "match_result" in st.session_state:

    result = st.session_state["match_result"]

    st.divider()

    st.subheader("📊 Matching Results")


    # --------------------------------------------------------
    # MAIN METRICS
    # --------------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Match Score",
            f"{result.get('match_percentage', 0)}%",
        )

    with metric2:
        st.metric(
            "Matched Skills",
            result.get("matched_count", 0),
        )

    with metric3:
        st.metric(
            "Missing Skills",
            result.get("missing_count", 0),
        )

    with metric4:
        st.metric(
            "Extra Skills",
            result.get("extra_count", 0),
        )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.markdown("### 🎯 Compatibility Score")

    score = result.get("match_percentage", 0)

    st.progress(
        max(0, min(score, 100)) / 100
    )

    st.caption(
        f"Overall resume–job compatibility: {score}%"
    )


    # --------------------------------------------------------
    # SKILL ANALYSIS
    # --------------------------------------------------------

    st.markdown("### 🧠 Skill Analysis")

    skill_col1, skill_col2, skill_col3 = st.columns(3)


    with skill_col1:

        st.markdown("#### ✅ Matched Skills")

        matched_skills = result.get(
            "matched_skills",
            [],
        )

        if matched_skills:

            for skill in matched_skills:
                st.markdown(
                    f'<span class="skill-tag">✓ {skill}</span>',
                    unsafe_allow_html=True,
                )

        else:
            st.info("No matched skills found.")


    with skill_col2:

        st.markdown("#### ❌ Missing Skills")

        missing_skills = result.get(
            "missing_skills",
            [],
        )

        if missing_skills:

            for skill in missing_skills:
                st.markdown(
                    f'<span class="skill-tag">⚠ {skill}</span>',
                    unsafe_allow_html=True,
                )

        else:
            st.info("No missing skills found.")


    with skill_col3:

        st.markdown("#### ➕ Extra Skills")

        extra_skills = result.get(
            "extra_skills",
            [],
        )

        if extra_skills:

            for skill in extra_skills:
                st.markdown(
                    f'<span class="skill-tag">+ {skill}</span>',
                    unsafe_allow_html=True,
                )

        else:
            st.info("No extra skills found.")


    # --------------------------------------------------------
    # PIPELINE STATUS
    # --------------------------------------------------------

    st.divider()

    st.markdown("### 🔧 Pipeline Information")

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.write(
            "**Pipeline Status:**",
            result.get(
                "pipeline_status",
                "unknown",
            ),
        )

    with info_col2:
        st.write(
            "**Skill Score:**",
            result.get(
                "skill_score",
                0,
            ),
        )

    with info_col3:
        st.write(
            "**Maximum Skill Score:**",
            result.get(
                "skill_score_max",
                0,
            ),
        )


    # --------------------------------------------------------
    # RAW API RESPONSE
    # --------------------------------------------------------

    with st.expander("🔍 View API Response"):

        st.json(result)