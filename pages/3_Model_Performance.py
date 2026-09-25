import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Model Performance")

st.write(
    "Evaluate the performance of the lead conversion and segmentation "
    "models using key machine learning metrics."
)

st.markdown("### Classification Model")

st.caption(
    "The classification model predicts whether a sales lead is likely "
    "to convert based on profile, engagement, and buying signals."
)


# --------------------------------------------------------
# Classification Performance Metrics
# --------------------------------------------------------

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

with metric_col1:
    st.metric(
        label="Accuracy",
        value="73.8%"
    )

with metric_col2:
    st.metric(
        label="Precision",
        value="70.6%"
    )

with metric_col3:
    st.metric(
        label="Recall",
        value="57.4%"
    )

with metric_col4:
    st.metric(
        label="F1-Score",
        value="63.3%"
    )

with metric_col5:
    st.metric(
        label="ROC-AUC",
        value="78.9%"
    )


# --------------------------------------------------------
# Model Comparison
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Model Comparison")

st.caption(
    "Comparison of classification models based on validation performance."
)

comparison_data = {
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting",
        "XGBoost"
    ],
    "Accuracy": [
        73.78,
        63.72,
        73.25,
        73.88,
        73.39
    ],
    "Precision": [
        70.84,
        53.69,
        69.44,
        70.56,
        69.35
    ],
    "Recall": [
        56.46,
        54.98,
        56.91,
        57.42,
        57.74
    ],
    "F1-Score": [
        62.83,
        54.32,
        62.55,
        63.31,
        63.01
    ],
    "ROC-AUC": [
        78.98,
        62.18,
        78.38,
        78.91,
        78.31
    ]
}

comparison_df = pd.DataFrame(comparison_data)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------------
# Confusion Matrix
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Confusion Matrix")

st.caption(
    "Validation results for the selected Gradient Boosting classification model."
)

cm_col1, cm_col2 = st.columns([1, 1])

with cm_col1:

    st.markdown("#### Prediction Results")

    confusion_data = pd.DataFrame(
        [
            [1958, 383],
            [652, 861]
        ],
        index=[
            "Actual: Not Converted",
            "Actual: Converted"
        ],
        columns=[
            "Predicted: Not Converted",
            "Predicted: Converted"
        ]
    )

    st.dataframe(
        confusion_data,
        use_container_width=True
    )

with cm_col2:

    st.markdown("#### Interpretation")

    st.markdown(
        """
        **Correct Predictions**
        
        - **1,958** leads were correctly identified as not converted.
        - **861** leads were correctly identified as converted.
        
        **Incorrect Predictions**
        
        - **383** leads were predicted as converted but did not convert.
        - **652** leads were predicted as not converted but actually converted.
        """
    )


# --------------------------------------------------------
# Clustering Performance
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Clustering Performance")

st.caption(
    "Evaluation of K-Means clustering used to identify distinct lead segments."
)

cluster_col1, cluster_col2 = st.columns(2)

with cluster_col1:

    st.metric(
        label="Selected Clusters",
        value="2"
    )

with cluster_col2:

    st.metric(
        label="Silhouette Score",
        value="0.32"
    )

st.markdown("#### K-Means Evaluation")

clustering_data = pd.DataFrame({
    "Number of Clusters": [2, 3, 4, 5, 6],
    "Inertia": [
        95975.02,
        80470.25,
        66749.56,
        56944.13,
        50826.43
    ],
    "Silhouette Score": [
        0.32,
        0.29,
        0.31,
        0.25,
        0.25
    ]
})

st.dataframe(
    clustering_data,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Two clusters were selected because they provided a clear and "
    "interpretable business segmentation while maintaining a comparable "
    "silhouette score to the other tested configurations."
)


# --------------------------------------------------------
# Feature Importance
# --------------------------------------------------------

st.markdown("---")

st.markdown("### Key Conversion Signals")

st.caption(
    "Most influential features in the Gradient Boosting classification model."
)

feature_importance_data = pd.DataFrame({
    "Feature": [
        "Digital Engagement Score",
        "Demo Attended",
        "Sales Rep Interactions",
        "Trial Started",
        "Decision Maker",
        "Contact Requests",
        "Days Since Last Interaction",
        "Total Interactions",
        "Previous Interactions",
        "Employee Count"
    ],
    "Importance": [
        0.50,
        0.14,
        0.04,
        0.04,
        0.04,
        0.03,
        0.03,
        0.02,
        0.01,
        0.01
    ]
})

fig = px.bar(
    feature_importance_data.sort_values(
        "Importance",
        ascending=True
    ),
    x="Importance",
    y="Feature",
    orientation="h",
    text="Importance"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    height=450,
    margin=dict(l=10, r=40, t=10, b=10),
    xaxis_title="Importance",
    yaxis_title="",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.info(
    "Digital Engagement Score was the most influential feature in the "
    "classification model, followed by demo attendance. Other engagement "
    "and buying signals had smaller individual contributions."
)