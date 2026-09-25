import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Lead Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #F5F7FA;
        color: #172B4D;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;

        width: 230px !important;
        min-width: 230px !important;
        max-width: 230px !important;
    }


    /* --------------------------------------------------------
       Collapsed Sidebar
       -------------------------------------------------------- */

    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
    }


    /* --------------------------------------------------------
       Sidebar Content
       -------------------------------------------------------- */

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }


    /* ========================================================
       SIDEBAR DIVIDER
       ======================================================== */

    .sidebar-divider {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 0.8rem 0 1rem 0;
    }


    /* ========================================================
       SIDEBAR DESCRIPTION
       ======================================================== */

    .sidebar-description {
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.55;
        margin-top: 1.3rem;
    }

    /* ========================================================
        SIDEBAR BRAND
       ======================================================== */

    .brand-title {
        font-size: 18px;
        line-height: 1.12;
        font-weight: 700;
        color: #172B4D;
        letter-spacing: -0.2px;
    }

    .brand-tagline {
        margin-top: 7px;
        font-size: 10.5px;
        line-height: 1.45;
        font-weight: 400;
        color: #64748B;
        max-width: 180px;
    }

    /* ========================================================
       MAIN TYPOGRAPHY
       ======================================================== */

    h1, h2, h3 {
        color: #172B4D;
    }

    p {
        color: #475569;
    }


    /* ========================================================
       REMOVE DEFAULT STREAMLIT NAVIGATION SPACING
       ======================================================== */

    [data-testid="stSidebarNav"] {
        display: none;
    }


    /* =======================================================
       Dashboard KPI Cards
       ======================================================= */

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 2px 8px rgba(23, 43, 77, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 14px;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: #172B4D;
        font-size: 30px;
        font-weight: 700;
    }

    /*============================
      Filter panel 
      ============================*/
    .filter-header {
        margin-bottom: 14px;
    }

    .filter-title {
        font-size: 15px;
        font-weight: 600;
        color: #172B4D;
    }

    .filter-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-top: 3px;
    }

    /*======================
      Filter labels 
      ======================*/
    [data-testid="stMultiSelect"] label {
        color: #475569 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /*============================
      KPI Cards
      ============================ */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        min-height: 112px;
        box-shadow: 0 2px 8px rgba(23, 43, 77, 0.05);
    }

    .kpi-label {
        font-size: 13px;
        font-weight: 500;
        color: #475569;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        line-height: 1.15;
        color: #172B4D;
    }

    .kpi-caption {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 7px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE DEFINITIONS
# ============================================================

dashboard = st.Page(
    "pages/0_Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)

conversion = st.Page(
    "pages/1_Lead_Conversion_Prediction.py",
    title="Lead Conversion",
    icon=":material/target:"
)

segmentation = st.Page(
    "pages/2_Lead_Segmentation.py",
    title="Lead Segmentation",
    icon=":material/groups:"
)

performance = st.Page(
    "pages/3_Model_Performance.py",
    title="Model Performance",
    icon=":material/analytics:"
)

insights = st.Page(
    "pages/4_Lead_Insights.py",
    title="Lead Insights",
    icon=":material/lightbulb:"
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    [
        dashboard,
        conversion,
        segmentation,
        performance,
        insights
    ],
    position="hidden"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # Logo
    # --------------------------------------------------------

    brand_icon, brand_text = st.columns(
        [0.75, 1.7],
        vertical_alignment="center"
    )

    with brand_icon:

        st.image(
            "assets/logo_icon.png",
            width=52
        )

    with brand_text:

        st.markdown(
            """
            <div class="brand-title">
                <div>Sales Lead</div>
                <div>Intelligence</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="brand-tagline">
            Smarter Leads. Higher Conversions.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Divider
    # --------------------------------------------------------

    st.markdown(
        '<hr class="sidebar-divider">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    st.page_link(
        dashboard,
        label="Dashboard",
        icon=":material/dashboard:"
    )

    st.page_link(
        conversion,
        label="Lead Conversion",
        icon=":material/target:"
    )

    st.page_link(
        segmentation,
        label="Lead Segmentation",
        icon=":material/groups:"
    )

    st.page_link(
        performance,
        label="Model Performance",
        icon=":material/analytics:"
    )

    st.page_link(
        insights,
        label="Lead Insights",
        icon=":material/lightbulb:"
    )

    # --------------------------------------------------------
    # Divider
    # --------------------------------------------------------

    st.markdown(
        '<hr class="sidebar-divider">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-description">
            Sales intelligence platform for understanding,
            predicting, and segmenting sales leads.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()