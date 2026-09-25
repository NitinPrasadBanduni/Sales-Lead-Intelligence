import streamlit as st

st.title("Lead Insights")

st.write(
    "Key findings from the lead analysis, classification model, "
    "and customer segmentation."
)

st.markdown("### Business Insights")

st.caption(
    "Use these findings to understand lead quality, engagement behavior, "
    "and opportunities for improving sales conversion."
)


# --------------------------------------------------------
# Lead Conversion Insights
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Lead Conversion Insights")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.markdown("#### Engagement Drives Conversion")

    st.write(
        "Digital engagement is the strongest signal in the conversion "
        "model. Website visits, pages viewed, content downloads, and "
        "product page visits all contribute to the overall engagement "
        "level of a lead."
    )

with insight_col2:

    st.markdown("#### Buying Signals Matter")

    st.write(
        "Demo attendance, trial activity, and decision-maker involvement "
        "are important signals for identifying leads with stronger "
        "conversion potential."
    )


# --------------------------------------------------------
# Lead Segment Insights
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Lead Segment Insights")

segment_col1, segment_col2 = st.columns(2)

with segment_col1:

    st.markdown("#### High-Intent / Highly Engaged")

    st.write(
        "This segment contains 5,119 leads, representing 26.57% of "
        "the lead base. These leads show higher digital engagement, "
        "more interactions, and larger estimated budgets."
    )

    st.success(
        "Observed conversion rate: 68.12%"
    )

with segment_col2:

    st.markdown("#### Low-Engagement / Nurture")

    st.write(
        "This segment contains 14,150 leads, representing 73.43% of "
        "the lead base. These leads show lower engagement and fewer "
        "interactions and may require additional nurturing."
    )

    st.info(
        "Observed conversion rate: 28.81%"
    )


# --------------------------------------------------------
# Recommended Sales Actions
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Recommended Sales Actions")

action_col1, action_col2 = st.columns(2)

with action_col1:

    st.markdown("#### Prioritize High-Intent Leads")

    st.write(
        "Focus sales follow-up on leads with strong digital engagement, "
        "demo participation, trial activity, and decision-maker involvement."
    )

    st.markdown(
        "**Action:** Move high-intent leads toward direct sales "
        "conversations and timely follow-up."
    )

with action_col2:

    st.markdown("#### Nurture Lower-Engagement Leads")

    st.write(
        "Leads with weaker engagement can remain in targeted nurture "
        "workflows while their activity and buying signals are monitored."
    )

    st.markdown(
        "**Action:** Use relevant content and engagement campaigns "
        "before increasing direct sales effort."
    )