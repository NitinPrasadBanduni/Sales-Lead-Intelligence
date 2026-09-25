import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path
import plotly.express as px

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

@st.cache_data
def load_data():

    data_path = PROJECT_ROOT / "Dataset" / "cleaned_leads.csv"

    df = pd.read_csv(data_path)

    return df


# ---------------------------------------------------------
# Load Clustering Model
# ---------------------------------------------------------

@st.cache_resource
def load_clustering_model():

    model_path = PROJECT_ROOT / "Models" / "clustering_pipeline.joblib"

    model = joblib.load(model_path)

    return model


# ---------------------------------------------------------
# Load Segment Mapping
# ---------------------------------------------------------

@st.cache_data
def load_segment_mapping():

    mapping_path = PROJECT_ROOT / "Models" / "segment_mapping.json"

    with open(mapping_path, "r") as file:
        mapping = json.load(file)

    return mapping


# ---------------------------------------------------------
# Load Everything
# ---------------------------------------------------------

df = load_data()

clustering_model = load_clustering_model()

segment_mapping = load_segment_mapping()


# ---------------------------------------------------------
# Generate Lead Segments
# ---------------------------------------------------------

clustering_features = [
    "Digital_Engagement_Score",
    "Total_Interactions",
    "Days_Since_Last_Interaction",
    "Estimated_Budget",
    "Employee_Count",
    "Deal_to_Budget_Ratio"
]

df["Cluster"] = clustering_model.predict(
    df[clustering_features]
)

df["Segment"] = (
    df["Cluster"]
    .astype(str)
    .map(segment_mapping)
)


# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------

st.title("Sales Lead Intelligence")

st.markdown(
    """
    ### Turn lead data into actionable sales insights
    Explore lead quality, conversion performance, engagement,
    and customer segments through an interactive sales dashboard.
    """
)


# ---------------------------------------------------------
# Filters
# ---------------------------------------------------------

st.markdown("### Explore Leads")

with st.container(border=True):

    st.markdown(
        """
        <div class="filter-header">
            <div class="filter-title">Dashboard Filters</div>
            <div class="filter-subtitle">
                Refine the dashboard by lead characteristics
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        selected_industry = st.multiselect(
            "Industry",
            sorted(df["Industry"].dropna().unique()),
            placeholder="All industries"
        )

    with filter_col2:
        selected_state = st.multiselect(
            "State",
            sorted(df["State"].dropna().unique()),
            placeholder="All states"
        )

    with filter_col3:
        selected_source = st.multiselect(
            "Lead Source",
            sorted(df["Lead_Source"].dropna().unique()),
            placeholder="All lead sources"
        )

    with filter_col4:
        selected_campaign = st.multiselect(
            "Campaign Type",
            sorted(df["Campaign_Type"].dropna().unique()),
            placeholder="All campaigns"
        )


# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------

filtered_df = df.copy()


if selected_industry:

    filtered_df = filtered_df[
        filtered_df["Industry"].isin(selected_industry)
    ]


if selected_state:

    filtered_df = filtered_df[
        filtered_df["State"].isin(selected_state)
    ]


if selected_source:

    filtered_df = filtered_df[
        filtered_df["Lead_Source"].isin(selected_source)
    ]


if selected_campaign:

    filtered_df = filtered_df[
        filtered_df["Campaign_Type"].isin(selected_campaign)
    ]


# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

total_leads = len(filtered_df)


if total_leads > 0:

    conversion_rate = (
        filtered_df["Converted"].mean() * 100
    )

    high_intent_leads = (
        filtered_df["Segment"]
        .eq("High-Intent / Highly Engaged")
        .sum()
    )

    avg_deal_value = (
        filtered_df["Estimated_Deal_Value"]
        .mean()
    )

else:

    conversion_rate = 0

    high_intent_leads = 0

    avg_deal_value = 0


# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------

st.markdown("### Lead Performance")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Leads</div>
            <div class="kpi-value">{total_leads:,}</div>
            <div class="kpi-caption">Leads in current selection</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Conversion Rate</div>
            <div class="kpi-value">{conversion_rate:.1f}%</div>
            <div class="kpi-caption">Overall lead conversion</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">High-Intent Leads</div>
            <div class="kpi-value">{high_intent_leads:,}</div>
            <div class="kpi-caption">Highly engaged segment</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg. Deal Value</div>
            <div class="kpi-value">₹{avg_deal_value:,.0f}</div>
            <div class="kpi-caption">Average estimated value</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Lead Source × Campaign Type Conversion Heatmap
# ---------------------------------------------------------

st.markdown("---")

st.markdown("### Conversion by Lead Source & Campaign")

if len(filtered_df) > 0:

    heatmap_data = (
        filtered_df
        .pivot_table(
            index="Lead_Source",
            columns="Campaign_Type",
            values="Converted",
            aggfunc="mean"
        )
        * 100
    )

    fig = px.imshow(
        heatmap_data,
        text_auto=".1f",
        aspect="auto",
        labels={
            "x": "Campaign Type",
            "y": "Lead Source",
            "color": "Conversion Rate (%)"
        }
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172B4D"
        ),
        coloraxis_colorbar=dict(
            title="Conversion %",
            thickness=12,
            len=0.75
        )
    )

    fig.update_xaxes(
        title=None,
        showgrid=False
    )

    fig.update_yaxes(
        title=None,
        showgrid=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

else:

    st.info("No leads match the selected filters.")


# ---------------------------------------------------------
# Lead Segment Performance
# ---------------------------------------------------------

st.markdown("---")


st.markdown("### Lead Segment Performance")

segment_data = (
    filtered_df
    .groupby("Segment")
    .agg(
        Lead_Count=("Lead_ID", "count"),
        Conversion_Rate=("Converted", "mean")
    )
    .reset_index()
)

segment_data["Conversion_Rate"] = (
    segment_data["Conversion_Rate"] * 100
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# Segment Distribution
# ---------------------------------------------------------

with col1:

    fig_segment = px.pie(
        segment_data,
        names="Segment",
        values="Lead_Count",
        hole=0.58
    )

    fig_segment.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        textfont=dict(
            size=14,
            color="white"
        ),
        marker=dict(
            line=dict(
                color="white",
                width=2
            )
        )
    )

    fig_segment.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172B4D"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ---------------------------------------------------------
# Segment Conversion
# ---------------------------------------------------------

with col2:

    fig_conversion = px.bar(
        segment_data,
        x="Segment",
        y="Conversion_Rate",
        text="Conversion_Rate",
        labels={
            "Conversion_Rate": "Conversion Rate (%)",
            "Segment": "Lead Segment"
        }
    )

    fig_conversion.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont=dict(
            size=13,
            color="#172B4D"
        )
    )

    fig_conversion.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172B4D"
        ),
        yaxis=dict(
            title=None,
            range=[0, 100],
            showgrid=True,
            gridcolor="#E2E8F0",
            zeroline=False
        ),
        xaxis=dict(
            title=None,
            showgrid=False
        )
    )

    st.plotly_chart(
        fig_conversion,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ---------------------------------------------------------
# Lead Quality Map
# ---------------------------------------------------------

st.markdown("---")

st.markdown("### Lead Quality Map")

st.caption(
    "Engagement and recency help identify leads that may need immediate sales attention."
)

plot_df = filtered_df.copy()

plot_df = plot_df.dropna(
    subset=[
        "Digital_Engagement_Score",
        "Days_Since_Last_Interaction",
        "Estimated_Budget",
        "Segment"
    ]
)

if len(plot_df) > 3000:
    plot_df = plot_df.sample(
        3000,
        random_state=42
    )

segment_colors = {
    "High-Intent / Highly Engaged": "#0F766E",
    "Low-Engagement / Nurture": "#2563EB"
}

fig_quality = px.scatter(
    plot_df,
    x="Digital_Engagement_Score",
    y="Days_Since_Last_Interaction",
    size="Estimated_Budget",
    color="Segment",
    color_discrete_map=segment_colors,
    hover_data=[
        "Lead_ID",
        "Industry",
        "Lead_Source",
        "Campaign_Type",
        "Estimated_Deal_Value",
        "Converted"
    ],
    labels={
        "Digital_Engagement_Score": "Digital Engagement Score",
        "Days_Since_Last_Interaction": "Days Since Last Interaction",
        "Estimated_Budget": "Estimated Budget",
        "Segment": "Lead Segment"
    },
    size_max=35
)

fig_quality.update_traces(
    marker=dict(
        opacity=0.72,
        line=dict(
            width=0.5,
            color="white"
        )
    )
)

fig_quality.update_xaxes(
    title_text="Digital Engagement Score",
    title_font=dict(
        size=13,
        color="#475569"
    ),
    showgrid=True,
    gridcolor="#E2E8F0",
    zeroline=False
)

fig_quality.update_yaxes(
    title_text="Days Since Last Interaction",
    title_font=dict(
        size=13,
        color="#475569"
    ),
    range=[0, 100],
    showgrid=True,
    gridcolor="#E2E8F0",
    zeroline=False
)

fig_quality.update_layout(
    height=520,
    margin=dict(
        l=55,
        r=20,
        t=20,
        b=70
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        color="#172B4D"
    ),
    legend_title_text="Lead Segment",
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255,255,255,0)",
        borderwidth=0
    )
)

st.plotly_chart(
    fig_quality,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ---------------------------------------------------------
# Key Conversion Signals
# ---------------------------------------------------------

st.markdown("---")

st.markdown("### Key Conversion Signals")

st.caption(
    "Conversion rates across key lead behaviors and buying signals."
)

signal_data = []

# Demo Attended
demo_rate = (
    filtered_df
    .groupby("Demo_Attended")["Converted"]
    .mean()
    .reset_index()
)

for _, row in demo_rate.iterrows():
    signal_data.append({
        "Signal": "Demo Attended",
        "Status": row["Demo_Attended"],
        "Conversion Rate": row["Converted"] * 100
    })


# Trial Started
trial_rate = (
    filtered_df
    .groupby("Trial_Started")["Converted"]
    .mean()
    .reset_index()
)

for _, row in trial_rate.iterrows():
    signal_data.append({
        "Signal": "Trial Started",
        "Status": row["Trial_Started"],
        "Conversion Rate": row["Converted"] * 100
    })


# Decision Maker
decision_rate = (
    filtered_df
    .groupby("Decision_Maker")["Converted"]
    .mean()
    .reset_index()
)

for _, row in decision_rate.iterrows():
    signal_data.append({
        "Signal": "Decision Maker",
        "Status": row["Decision_Maker"],
        "Conversion Rate": row["Converted"] * 100
    })


signal_df = pd.DataFrame(signal_data)


fig_signals = px.bar(
    signal_df,
    x="Signal",
    y="Conversion Rate",
    color="Status",
    barmode="group",
    text="Conversion Rate",
    labels={
        "Signal": "Conversion Signal",
        "Conversion Rate": "Conversion Rate (%)",
        "Status": "Status"
    },
    color_discrete_map={
    "Yes": "#0068C9",
    "No": "#60B4FF"
    }
)


fig_signals.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside",
    textfont=dict(
        size=12,
        color="#172B4D"
    )
)


fig_signals.update_xaxes(
    title=None,
    showgrid=False,
    zeroline=False
)


fig_signals.update_yaxes(
    title="Conversion Rate (%)",
    range=[0, 100],
    showgrid=True,
    gridcolor="#E2E8F0",
    zeroline=False
)


fig_signals.update_layout(
    height=450,
    margin=dict(
        l=55,
        r=20,
        t=20,
        b=55
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        color="#172B4D"
    ),
    legend_title_text="Status",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)


st.plotly_chart(
    fig_signals,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ---------------------------------------------------------
# Dataset Summary
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    f"Showing **{len(filtered_df):,}** "
    f"of **{len(df):,}** leads"
)