import streamlit as st
from snowflake.snowpark import Session


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Cancer Oncology Analytics",
    page_icon="🏥",
    layout="wide"
)


# ---------------------------------------------------------
# SNOWFLAKE CONNECTION
# ---------------------------------------------------------

@st.cache_resource
def create_snowflake_session():

    connection_parameters = {
        "account": st.secrets["snowflake"]["account"],
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "role": st.secrets["snowflake"]["role"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"]
    }

    return Session.builder.configs(connection_parameters).create()


session = create_snowflake_session()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🏥 Cancer Oncology Analytics")
st.markdown(
    "### Oncology data warehouse and analytics dashboard"
)

st.success("Connected to Snowflake successfully!")

st.divider()


# ---------------------------------------------------------
# LOAD PATIENT ENCOUNTER DATA
# ---------------------------------------------------------

patient_df = session.sql("""
    SELECT
        P.*,
        D.FULL_DATE,
        D.DAY,
        D.MONTH,
        D.MONTH_NAME,
        D.QUARTER,
        D.YEAR,
        D.DAY_OF_WEEK
    FROM CANCER_ONCOLOGY_DB.ONCOLOGY_SEMANTIC.VW_PATIENT_ENCOUNTERS P
    LEFT JOIN CANCER_ONCOLOGY_DB.ONCOLOGY_DW.DIM_DATE D
        ON P.DATE_SK = D.DATE_SK
""").to_pandas()


# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------

st.sidebar.header("🔎 Filters")
# ---------------------------------------------------------
# DATE RANGE FILTER
# ---------------------------------------------------------

st.sidebar.subheader("📅 Date Range")

if not patient_df.empty and "FULL_DATE" in patient_df.columns:

    patient_df["FULL_DATE"] = (
        patient_df["FULL_DATE"]
        .astype("datetime64[ns]")
    )

    min_date = patient_df["FULL_DATE"].min().date()
    max_date = patient_df["FULL_DATE"].max().date()

    selected_start_date = st.sidebar.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

    selected_end_date = st.sidebar.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

else:

    selected_start_date = None
    selected_end_date = None

if not patient_df.empty:

    cancer_options = sorted(
        patient_df["CANCER_NAME"]
        .dropna()
        .unique()
        .tolist()
    )

    provider_options = sorted(
        patient_df["PROVIDER_NAME"]
        .dropna()
        .unique()
        .tolist()
    )

    treatment_options = sorted(
        patient_df["TREATMENT_TYPE"]
        .dropna()
        .unique()
        .tolist()
    )

    stage_options = sorted(
        patient_df["DISEASE_STAGE"]
        .dropna()
        .unique()
        .tolist()
    )

    payment_options = sorted(
        patient_df["PAYMENT_MODE"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_cancer = st.sidebar.multiselect(
        "Cancer Type",
        cancer_options
    )

    selected_provider = st.sidebar.multiselect(
        "Provider",
        provider_options
    )

    selected_treatment = st.sidebar.multiselect(
        "Treatment Type",
        treatment_options
    )

    selected_stage = st.sidebar.multiselect(
        "Disease Stage",
        stage_options
    )

    selected_payment = st.sidebar.multiselect(
        "Payment Mode",
        payment_options
    )

    filtered_df = patient_df.copy()
if (
    selected_start_date is not None
    and selected_end_date is not None
):

    filtered_df = filtered_df[
        (filtered_df["FULL_DATE"].dt.date >= selected_start_date)
        &
        (filtered_df["FULL_DATE"].dt.date <= selected_end_date)
    ]

    if selected_cancer:
        filtered_df = filtered_df[
            filtered_df["CANCER_NAME"].isin(selected_cancer)
        ]

    if selected_provider:
        filtered_df = filtered_df[
            filtered_df["PROVIDER_NAME"].isin(selected_provider)
        ]

    if selected_treatment:
        filtered_df = filtered_df[
            filtered_df["TREATMENT_TYPE"].isin(selected_treatment)
        ]

    if selected_stage:
        filtered_df = filtered_df[
            filtered_df["DISEASE_STAGE"].isin(selected_stage)
        ]

    if selected_payment:
        filtered_df = filtered_df[
            filtered_df["PAYMENT_MODE"].isin(selected_payment)
        ]


# ---------------------------------------------------------
# FILTERED KPIs
# ---------------------------------------------------------

st.subheader("📊 Filtered Summary")

if not patient_df.empty:

    total_encounters = filtered_df["ENCOUNTER_ID"].nunique()

    total_patients = filtered_df["PATIENT_ID"].nunique()

    total_providers = filtered_df["PROVIDER_ID"].nunique()

    total_cancer_types = filtered_df["CANCER_CODE"].nunique()

    total_billed = filtered_df["BILLED_AMOUNT"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Encounters",
        f"{total_encounters:,}"
    )

    col2.metric(
        "Patients",
        f"{total_patients:,}"
    )

    col3.metric(
        "Providers",
        f"{total_providers:,}"
    )

    col4.metric(
        "Cancer Types",
        f"{total_cancer_types:,}"
    )

    col5.metric(
        "Billed Amount",
        f"${total_billed:,.2f}"
    )


st.divider()


# ---------------------------------------------------------
# CANCER ANALYSIS
# ---------------------------------------------------------

st.subheader("🎗️ Cancer Analysis")

if not filtered_df.empty:

    cancer_analysis = (
        filtered_df
        .groupby("CANCER_NAME")
        .agg(
            TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
            TOTAL_PATIENTS=("PATIENT_ID", "nunique"),
            TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
        )
        .sort_values(
            "TOTAL_ENCOUNTERS",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Encounters by Cancer Type")

        st.bar_chart(
            cancer_analysis["TOTAL_ENCOUNTERS"]
        )

    with col2:

        st.write("Billed Amount by Cancer Type")

        st.bar_chart(
            cancer_analysis["TOTAL_BILLED_AMOUNT"]
        )

else:

    st.warning("No data matches the selected filters.")


st.divider()

# ---------------------------------------------------------
# DATE ANALYSIS
# ---------------------------------------------------------

st.subheader("📅 Service Date Analysis")

if not filtered_df.empty:

    if "FULL_DATE" in filtered_df.columns:

        date_analysis = (
            filtered_df
            .groupby("FULL_DATE")
            .agg(
                TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
                TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
            )
            .reset_index()
            .sort_values("FULL_DATE")
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("Encounters Over Time")

            st.line_chart(
                date_analysis.set_index("FULL_DATE")[
                    "TOTAL_ENCOUNTERS"
                ]
            )

        with col2:

            st.write("Billed Amount Over Time")

            st.line_chart(
                date_analysis.set_index("FULL_DATE")[
                    "TOTAL_BILLED_AMOUNT"
                ]
            )

        st.write("Daily Analysis")

        st.dataframe(
            date_analysis,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "FULL_DATE is not available in the patient encounter data."
        )

else:

    st.info("No date data available for the selected filters.")

# ---------------------------------------------------------
# TREATMENT TYPE ANALYSIS
# ---------------------------------------------------------

st.subheader("💊 Treatment Type Analysis")

if not filtered_df.empty:

    treatment_analysis = (
        filtered_df
        .groupby("TREATMENT_TYPE")
        .agg(
            TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
            TOTAL_PATIENTS=("PATIENT_ID", "nunique"),
            TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
        )
        .sort_values(
            "TOTAL_ENCOUNTERS",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Encounters by Treatment Type")

        st.bar_chart(
            treatment_analysis["TOTAL_ENCOUNTERS"]
        )

    with col2:

        st.write("Billed Amount by Treatment Type")

        st.bar_chart(
            treatment_analysis["TOTAL_BILLED_AMOUNT"]
        )

    st.write("Treatment Type Details")

    st.dataframe(
        treatment_analysis,
        use_container_width=True
    )

else:

    st.info("No treatment data available.")

# ---------------------------------------------------------
# DISEASE STAGE ANALYSIS
# ---------------------------------------------------------

st.subheader("🩺 Disease Stage Analysis")

if not filtered_df.empty:

    stage_analysis = (
        filtered_df
        .groupby("DISEASE_STAGE")
        .agg(
            TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
            TOTAL_PATIENTS=("PATIENT_ID", "nunique"),
            TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
        )
        .sort_values(
            "TOTAL_ENCOUNTERS",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Encounters by Disease Stage")

        st.bar_chart(
            stage_analysis["TOTAL_ENCOUNTERS"]
        )

    with col2:

        st.write("Billed Amount by Disease Stage")

        st.bar_chart(
            stage_analysis["TOTAL_BILLED_AMOUNT"]
        )

    st.write("Disease Stage Details")

    st.dataframe(
        stage_analysis,
        use_container_width=True
    )

else:

    st.info("No disease stage data available.")

# ---------------------------------------------------------
# PATIENT DEMOGRAPHICS ANALYSIS
# ---------------------------------------------------------

st.subheader("👥 Patient Demographics Analysis")

if not filtered_df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.write("Patients by Gender")

        gender_analysis = (
            filtered_df
            .groupby("GENDER")
            .agg(
                TOTAL_PATIENTS=("PATIENT_ID", "nunique")
            )
            .sort_values(
                "TOTAL_PATIENTS",
                ascending=False
            )
        )

        st.bar_chart(
            gender_analysis["TOTAL_PATIENTS"]
        )

    with col2:

        st.write("Patients by Segment")

        segment_analysis = (
            filtered_df
            .groupby("SEGMENT")
            .agg(
                TOTAL_PATIENTS=("PATIENT_ID", "nunique")
            )
            .sort_values(
                "TOTAL_PATIENTS",
                ascending=False
            )
        )

        st.bar_chart(
            segment_analysis["TOTAL_PATIENTS"]
        )

else:

    st.info("No patient demographic data available.")

# ---------------------------------------------------------
# PAYER ANALYSIS
# ---------------------------------------------------------

st.subheader("💳 Payer Analysis")

if not filtered_df.empty:

    payer_analysis = (
        filtered_df
        .groupby("PAYER_ID")
        .agg(
            TOTAL_PATIENTS=("PATIENT_ID", "nunique"),
            TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
            TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
        )
        .sort_values(
            "TOTAL_BILLED_AMOUNT",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Encounters by Payer")

        st.bar_chart(
            payer_analysis["TOTAL_ENCOUNTERS"]
        )

    with col2:

        st.write("Billed Amount by Payer")

        st.bar_chart(
            payer_analysis["TOTAL_BILLED_AMOUNT"]
        )

    st.write("Payer Details")

    st.dataframe(
        payer_analysis,
        use_container_width=True
    )

else:

    st.info("No payer data available.")

# ---------------------------------------------------------
# PROVIDER PERFORMANCE
# ---------------------------------------------------------

st.subheader("👨‍⚕️ Provider Performance")

if not filtered_df.empty:

    provider_analysis = (
        filtered_df
        .groupby("PROVIDER_NAME")
        .agg(
            TOTAL_ENCOUNTERS=("ENCOUNTER_ID", "nunique"),
            TOTAL_PATIENTS=("PATIENT_ID", "nunique"),
            TOTAL_BILLED_AMOUNT=("BILLED_AMOUNT", "sum")
        )
        .sort_values(
            "TOTAL_BILLED_AMOUNT",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Encounters by Provider")

        st.bar_chart(
            provider_analysis["TOTAL_ENCOUNTERS"]
        )

    with col2:

        st.write("Billed Amount by Provider")

        st.bar_chart(
            provider_analysis["TOTAL_BILLED_AMOUNT"]
        )


st.divider()


# ---------------------------------------------------------
# PATIENT ENCOUNTER TABLE
# ---------------------------------------------------------

st.subheader("👥 Patient Encounters")

if not filtered_df.empty:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------------
    # DOWNLOAD FILTERED DATA
    # ---------------------------------------------------------

    st.write("### 📥 Download Filtered Data")

    csv_data = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_oncology_encounters.csv",
        mime="text/csv"
    )

else:

    st.info("No patient encounters found.")
# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Cancer Oncology Analytics | Snowflake + Streamlit"
)