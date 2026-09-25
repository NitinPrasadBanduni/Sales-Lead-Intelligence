import streamlit as st


# ============================================================
# PAGE HEADER
# ============================================================

st.title("Lead Conversion Prediction")

st.write(
    "Estimate the likelihood of lead conversion using profile, "
    "engagement, and buying signals."
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("### Lead Information")

st.caption(
    "Enter the available lead details to generate a conversion prediction."
)

# ============================================================
# COMPANY INFORMATION
# ============================================================

st.markdown("#### Company Information")

col1, col2, col3 = st.columns(3)

with col1:
    industry = st.selectbox(
        "Industry",
        [
            "IT Services",
            "Telecommunications",
            "Financial Services",
            "Healthcare",
            "Manufacturing",
            "Professional Services",
            "Retail",
            "Logistics",
            "Real Estate",
            "Education",
            "Unknown"
        ]
    )

with col2:
    state = st.selectbox(
        "State",
        [
            "Andhra Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Delhi",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Tamil Nadu",
            "Telangana",
            "Uttar Pradesh",
            "Uttarakhand",
            "West Bengal"
        ]
    )

with col3:
    employee_count = st.number_input(
        "Employee Count",
        min_value=1,
        max_value=5000,
        value=100,
        step=10
    )

# ============================================================
# LEAD ACQUISITION
# ============================================================

st.markdown("#### Lead Acquisition")

col1, col2 = st.columns(2)

with col1:
    lead_source = st.selectbox(
        "Lead Source",
        [
            "Website",
            "Referral",
            "Social Media",
            "Email",
            "Paid Search",
            "Organic Search",
            "Direct",
            "Partner"
        ]
    )

with col2:
    campaign_type = st.selectbox(
        "Campaign Type",
        [
            "Product Demo",
            "Webinar",
            "Enterprise Outreach",
            "Free Trial",
            "Content Marketing",
            "Unknown"
        ]
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
    contact_requests = st.slider(
        "Contact Requests",
        min_value=0,
        max_value=10,
        value=1
    )


col1, col2, col3 = st.columns(3)

with col1:
    sales_rep_interactions = st.slider(
        "Sales Rep Interactions",
        min_value=0,
        max_value=15,
        value=1
    )

with col2:
    email_opens = st.slider(
        "Email Opens",
        min_value=0,
        max_value=50,
        value=5
    )

with col3:
    email_clicks = st.slider(
        "Email Clicks",
        min_value=0,
        max_value=25,
        value=1
    )


days_since_last_interaction = st.slider(
    "Days Since Last Interaction",
    min_value=0,
    max_value=90,
    value=7
)


# ============================================================
# BUYING SIGNALS
# ============================================================

st.markdown("#### Buying Signals")

col1, col2 = st.columns(2)

with col1:
    estimated_budget = st.number_input(
        "Estimated Budget (₹)",
        min_value=0.0,
        max_value=16000.0,
        value=2500.0,
        step=100.0
    )

with col2:
    estimated_deal_value = st.number_input(
        "Estimated Deal Value (₹)",
        min_value=0.0,
        max_value=25000.0,
        value=3000.0,
        step=100.0
    )


col1, col2, col3 = st.columns(3)

with col1:
    demo_attended = st.selectbox(
        "Demo Attended",
        ["Yes", "No"]
    )

with col2:
    trial_started = st.selectbox(
        "Trial Started",
        ["Yes", "No"]
    )

with col3:
    decision_maker = st.selectbox(
        "Decision Maker",
        ["Yes", "No"]
    )


# ============================================================
# PREDICTION ACTION
# ============================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    predict_button = st.button(
        "Predict Conversion",
        type="primary",
        use_container_width=True
    )

# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    import joblib
    import pandas as pd
    from pathlib import Path

    # --------------------------------------------------------
    # Load classification pipeline
    # --------------------------------------------------------

    project_root = Path(__file__).resolve().parents[1]

    model_path = (
        project_root
        / "Models"
        / "classification_pipeline.joblib"
    )

    classification_model = joblib.load(model_path)

    # --------------------------------------------------------
    # Calculate Company Size
    # --------------------------------------------------------

    company_bins = [0, 50, 250, 1000, 5000]
    company_labels = [
        "Small",
        "Medium",
        "Large",
        "Enterprise"
    ]

    company_size = pd.cut(
        [employee_count],
        bins=company_bins,
        labels=company_labels,
        include_lowest=True
    )[0]

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

    engagement_values = []

    for col, limit in engagement_limits.items():

        if col == "Website_Visits":
            value = website_visits

        elif col == "Pages_Viewed":
            value = pages_viewed

        elif col == "Email_Clicks":
            value = email_clicks

        elif col == "Content_Downloads":
            value = content_downloads

        elif col == "Product_Page_Visits":
            value = product_page_visits

        normalized_value = min(value / limit, 1)

        engagement_values.append(normalized_value)

    digital_engagement_score = (
        sum(engagement_values) /
        len(engagement_values)
    ) * 100

    # --------------------------------------------------------
    # Calculate Budget per Employee
    # --------------------------------------------------------

    budget_per_employee = (
        estimated_budget / employee_count
    )

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

        "Industry": industry,

        "State": state,

        "Lead_Source": lead_source,

        "Campaign_Type": campaign_type,

        "Employee_Count": employee_count,

        "Company_Size": company_size,

        "Previous_Interactions": previous_interactions,

        "Sales_Rep_Interactions": sales_rep_interactions,

        "Total_Interactions": total_interactions,

        "Digital_Engagement_Score": digital_engagement_score,

        "Website_Visits": website_visits,

        "Pages_Viewed": pages_viewed,

        "Content_Downloads": content_downloads,

        "Product_Page_Visits": product_page_visits,

        "Email_Opens": email_opens,

        "Email_Clicks": email_clicks,

        "Contact_Requests": contact_requests,

        "Days_Since_Last_Interaction":
            days_since_last_interaction,

        "Estimated_Budget": estimated_budget,

        "Estimated_Deal_Value": estimated_deal_value,

        "Budget_per_Employee":
            budget_per_employee,

        "Deal_to_Budget_Ratio":
            deal_to_budget_ratio,

        "Demo_Attended": demo_attended,

        "Trial_Started": trial_started,

        "Decision_Maker": decision_maker

    }])

    # --------------------------------------------------------
    # Make prediction
    # --------------------------------------------------------

    prediction = classification_model.predict(
        input_data
    )[0]

    probability = classification_model.predict_proba(
        input_data
    )[0][1]

    probability_percent = probability * 100

    # --------------------------------------------------------
    # Prediction Result
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### Prediction Result")

    result_col1, result_col2 = st.columns([1, 2])

    with result_col1:

        st.metric(
            label="Conversion Probability",
            value=f"{probability_percent:.1f}%"
        )

    with result_col2:

        if prediction == 1:

            st.success(
                "High likelihood of conversion"
            )

            st.markdown(
                "**Recommended Action:** "
                "Prioritize this lead for sales follow-up."
            )

        else:

            st.info(
                "Lower likelihood of conversion"
            )

            st.markdown(
                "**Recommended Action:** "
                "Place this lead into a nurture workflow "
                "and monitor engagement."
            )