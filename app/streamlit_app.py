import streamlit as st
from reports.report_generator import generate_compliance_report


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BIS Compliance Advisor",
    page_icon="🏭",
    layout="wide"
)

# Remember whether the analysis has started
if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False
# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏭 BIS Compliance Advisor Agent")

st.write(
    "AI-powered assistant for identifying potentially "
    "applicable Indian Standards and guiding manufacturers "
    "through the next compliance steps."
)

st.divider()


# --------------------------------------------------
# PRODUCT INPUT
# --------------------------------------------------

st.subheader("📦 Describe Your Product")

product_description = st.text_area(
    "Product Description",
    placeholder=(
        "Example: I manufacture battery-powered plastic "
        "toys for children aged 5–10 years."
    ),
    height=150
)

analyze_clicked = st.button(
    "🔍 Analyze Product",
    type="primary"
)
if analyze_clicked:
    if not product_description.strip():
        st.session_state.analysis_started = False
    else:
        st.session_state.analysis_started = True

# --------------------------------------------------
# ANALYSIS FLOW
# --------------------------------------------------

if st.session_state.analysis_started:

    if not product_description.strip():

        st.warning(
            "Please describe your product before starting the analysis."
        )

    else:

        st.success("Product description received.")

        st.divider()

        # --------------------------------------------------
        # PRODUCT PROFILE
        # --------------------------------------------------

        st.subheader("📋 Product Profile")

        st.info(
            "The AI agent will extract the product characteristics "
            "from your description."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Category", "Awaiting analysis")

        with col2:
            st.metric("Material", "Awaiting analysis")

        with col3:
            st.metric("Power Type", "Awaiting analysis")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Age Group", "Awaiting analysis")

        with col5:
            st.metric("Use Case", "Awaiting analysis")

        with col6:
            st.metric("Product Type", "Awaiting analysis")

        st.divider()

        # --------------------------------------------------
        # CLARIFICATION
        # --------------------------------------------------

        st.subheader("🤖 Clarification")

        st.write("Question 1 of 4")

        st.info(
            "The clarification agent will ask the most useful "
            "question to distinguish between applicable standards."
        )

        st.write(
            "**Example question:** Is the product powered by "
            "electricity or batteries?"
        )

        q_col1, q_col2 = st.columns(2)

        with q_col1:
            st.button("🔵 Yes")

        with q_col2:
            st.button("⚪ No")

        st.divider()

        # --------------------------------------------------
        # CANDIDATE STANDARDS
        # --------------------------------------------------

        st.subheader("📊 Candidate Standards")

        st.caption(
            "The retrieval and scoring engine will display "
            "ranked standards here."
        )

        candidate_col1, candidate_col2, candidate_col3 = st.columns(3)

        with candidate_col1:
            st.metric("Top Candidate", "—")

        with candidate_col2:
            st.metric("Match Score", "—")

        with candidate_col3:
            st.metric("Runner-up", "—")

        st.divider()

        # --------------------------------------------------
        # EARLY EXIT
        # --------------------------------------------------

        st.subheader("🛑 Question Budget & Early Exit")

        st.info(
            "The agent can stop asking questions early when "
            "the leading standard has a sufficiently large "
            "score margin over the runner-up."
        )

        st.write("Questions used: **0 / 4**")

        st.progress(0)

        st.caption(
            "Early-exit decision will be provided by the "
            "orchestration layer."
        )

        st.divider()

        # --------------------------------------------------
        # RECOMMENDATION
        # --------------------------------------------------

        st.subheader("🎯 Recommended Standard")

        st.warning(
            "Recommendation will appear after the clarification "
            "and standards-scoring process is completed."
        )

        st.write("### Why this standard matches")

        st.write(
            "The system will explain the match using product type, "
            "category, material, power type, age group, and use case."
        )

        st.divider()

        # --------------------------------------------------
        # COMPLIANCE REPORT
        # --------------------------------------------------

        st.subheader("📄 Compliance Summary")

        st.write(
            "The final compliance report will summarize the "
            "recommended standard and the next certification steps."
        )

        if st.button("📄 Generate Compliance Report"):

         test_profile = {
        "product_type": "Toy",
        "category": "Toys",
        "material": "Plastic",
        "power_type": "Battery",
        "age_group": "5-10 years",
        "use_case": "Children's recreational toy",
    }

         report = generate_compliance_report(
        product_description=product_description,
        product_profile=test_profile,
        recommendation="IS 9873",
        match_score=92,
        next_steps=[
            "Verify the applicable scope of the standard.",
            "Check the applicable BIS certification scheme.",
            "Review testing requirements.",
            "Proceed with the applicable BIS certification process.",
        ],
    )

         st.markdown(report)
         st.warning(
    "⚠️ This is an AI-assisted preliminary compliance recommendation. "
    "It is not an official BIS certification decision. "
    "Verify the applicable standard and certification requirements with BIS "
    "or an authorized certification body before proceeding."
)

         st.download_button(
        label="⬇️ Download Report",
        data=report,
        file_name="bis_compliance_report.md",
        mime="text/markdown",
    )