import streamlit as st

# ============================================================
# PAGE HEADER
# ============================================================

st.title("Lead Segmentation")

st.write(
    "Identify lead segments based on engagement, company profile, "
    "and buying behavior."
)

# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("### Lead Information")

st.caption(
    "Enter the available lead details to identify the most relevant "
    "sales segment."
)

# ============================================================
# ENGAGEMENT
# ============================================================

st.markdown("#### Engagement")

col1, col2, col3 = st.columns(3)

with col1:
    website_visits = st.slider(
        "Website Visits",
        min_value=0,
        max_value=50,
        value=5
    )

with col2:
    pages_viewed = st.slider(
        "Pages Viewed",
        min_value=0,
        max_value=100,
        value=10
    )

with col3:
    product_page_visits = st.slider(
        "Product Page Visits",
        min_value=0,
        max_value=50,
        value=3
    )

col1, col2, col3 = st.columns(3)

with col1:
    content_downloads = st.slider(
        "Content Downloads",
        min_value=0,
        max_value=20,
        value=2
    )

with col2:
    previous_interactions = st.slider(
        "Previous Interactions",
        min_value=0,
        max_value=20,
        value=2
    )

with col3:
    sales_rep_interactions = st.slider(
        "Sales Rep Interactions",
        min_value=0,
        max_value=15,
        value=1
    )

col1, col2 = st.columns(2)

with col1:
    email_clicks = st.slider(
        "Email Clicks",
        min_value=0,
        max_value=25,
        value=1
    )

with col2:
    days_since_last_interaction = st.slider(
        "Days Since Last Interaction",
        min_value=0,
        max_value=90,
        value=7
    )

# ============================================================
# COMPANY & BUYING
# ============================================================

st.markdown("#### Company & Buying Signals")

col1, col2, col3 = st.columns(3)

with col1:
    employee_count = st.number_input(
        "Employee Count",
        min_value=1,
        max_value=5000,
        value=100,
        step=10
    )

with col2:
    estimated_budget = st.number_input(
        "Estimated Budget (₹)",
        min_value=0.0,
        max_value=16000.0,
        value=2500.0,
        step=100.0
    )

with col3:
    estimated_deal_value = st.number_input(
        "Estimated Deal Value (₹)",
        min_value=0.0,
        max_value=25000.0,
        value=3000.0,
        step=100.0
    )

# ============================================================
# SEGMENTATION ACTION
# ============================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    segment_button = st.button(
        "Identify Lead Segment",
        type="primary",
        use_container_width=True
    )


# ============================================================
# SEGMENTATION
# ============================================================

if segment_button:

    import joblib
    import pandas as pd
    from pathlib import Path

    # --------------------------------------------------------
    # Load clustering pipeline
    # --------------------------------------------------------

    project_root = Path(__file__).resolve().parents[1]

    model_path = (
        project_root
        / "Models"
        / "clustering_pipeline.joblib"
    )

    clustering_model = joblib.load(model_path)

    # --------------------------------------------------------
    # Calculate Total Interactions
    # --------------------------------------------------------

    total_interactions = (
        previous_interactions +
        sales_rep_interactions
    )

    # --------------------------------------------------------
    # Calculate Digital Engagement Score
    # --------------------------------------------------------

    engagement_limits = {
        "Website_Visits": 100,
        "Pages_Viewed": 200,
        "Email_Clicks": 20,
        "Content_Downloads": 20,
        "Product_Page_Visits": 50
    }

    engagement_values = [
        min(
            website_visits /
            engagement_limits["Website_Visits"],
            1
        ),

        min(
            pages_viewed /
            engagement_limits["Pages_Viewed"],
            1
        ),

        min(
            email_clicks /
            engagement_limits["Email_Clicks"],
            1
        ),

        min(
            content_downloads /
            engagement_limits["Content_Downloads"],
            1
        ),

        min(
            product_page_visits /
            engagement_limits["Product_Page_Visits"],
            1
        )
    ]

    digital_engagement_score = (
        sum(engagement_values) /
        len(engagement_values)
    ) * 100

    # --------------------------------------------------------
    # Calculate Deal to Budget Ratio
    # --------------------------------------------------------

    if estimated_budget > 0:

        deal_to_budget_ratio = (
            estimated_deal_value /
            estimated_budget
        )

    else:

        deal_to_budget_ratio = 0

    # --------------------------------------------------------
    # Create model input
    # --------------------------------------------------------

    input_data = pd.DataFrame([{

        "Digital_Engagement_Score":
            digital_engagement_score,

        "Total_Interactions":
            total_interactions,

        "Days_Since_Last_Interaction":
            days_since_last_interaction,

        "Estimated_Budget":
            estimated_budget,

        "Employee_Count":
            employee_count,

        "Deal_to_Budget_Ratio":
            deal_to_budget_ratio

    }])

    # --------------------------------------------------------
    # Predict cluster
    # --------------------------------------------------------

    cluster = clustering_model.predict(
        input_data
    )[0]

    # --------------------------------------------------------
    # Load segment mapping
    # --------------------------------------------------------

    mapping_path = (
        project_root
        / "Models"
        / "segment_mapping.json"
    )

    with open(mapping_path, "r") as file:
        import json
        segment_mapping = json.load(file)

    # --------------------------------------------------------
    # Map cluster to business segment
    # --------------------------------------------------------

    segment = segment_mapping[str(cluster)]

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### Lead Segment")

    result_col1, result_col2 = st.columns([1, 2])

    with result_col1:

        st.metric(
            label="Identified Segment",
            value=segment
        )

    with result_col2:

        if segment == "High-Intent / Highly Engaged":

            st.success(
                "High-Intent / Highly Engaged"
            )

            st.markdown(
                "This lead shows strong engagement and buying signals "
                "and should receive more immediate sales attention."
            )

            st.markdown(
                "**Recommended Approach:** "
                "Prioritize direct sales follow-up and move toward "
                "a conversion-focused conversation."
            )

        else:

            st.info(
                "Low-Engagement / Nurture"
            )

            st.markdown(
                "This lead currently shows weaker engagement and may "
                "require additional nurturing before direct sales follow-up."
            )

            st.markdown(
                "**Recommended Approach:** "
                "Use targeted content and engagement campaigns, "
                "then reassess as activity increases."
            )