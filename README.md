# 🏥 Cancer Oncology Analytics

## 📌 Project Overview

**Cancer Oncology Analytics** is a data analytics project built using **Snowflake and Streamlit** to analyze oncology-related patient, provider, cancer, and encounter data.

The project implements a complete data pipeline in Snowflake, starting from CSV files stored in a Snowflake stage, loading the data into raw tables, transforming it into a dimensional data warehouse, creating a semantic layer, and finally presenting the analytical results through an interactive Streamlit dashboard.

---

## 🎯 Project Objective

The main objective of this project is to build an analytics solution that provides insights into:

* Patient encounters
* Cancer types
* Treatment types
* Disease stages
* Healthcare providers
* Patient demographics
* Payer information
* Billed amounts
* Encounter trends over time

The Streamlit dashboard allows users to interactively filter the data and analyze the results.

---

## 🛠️ Technologies Used

* **Snowflake** – Cloud data warehouse
* **Snowflake SQL** – Data loading, transformation, and analytics
* **Snowflake Stages** – CSV file storage
* **Snowflake Streams/Tasks concepts** – Data pipeline architecture
* **Python** – Application development
* **Streamlit** – Interactive dashboard
* **VS Code** – Development environment
* **Pandas** – Data processing within Streamlit
* **Git & GitHub** – Version control and project sharing

---

## 🏗️ Project Architecture

```text
                ┌─────────────────────┐
                │      4 CSV Files    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Snowflake Stage   │
                │   ONCOLOGY_STAGE    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     Raw Layer       │
                │   ONCOLOGY_RAW      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Data Warehouse Layer│
                │    ONCOLOGY_DW      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Semantic Layer    │
                │ ONCOLOGY_SEMANTIC   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     Streamlit       │
                │      Dashboard      │
                └─────────────────────┘
```

---

## 📂 Source Data

The project uses four CSV files:

```text
patients.csv
providers.csv
cancer_catalog.csv
encounters.csv
```

These files are manually uploaded into the Snowflake stage.

---

## ❄️ Snowflake Database Structure

### Database

```text
CANCER_ONCOLOGY_DB
```

### Schemas

```text
ONCOLOGY_RAW
ONCOLOGY_DW
ONCOLOGY_SEMANTIC
ONCOLOGY_OPS
ONCOLOGY_STREAMLIT
```

### Warehouse

```text
CANCER_ONCOLOGY_WH
```

---

## 📥 Raw Data Layer

The CSV files are loaded into raw Snowflake tables.

### Raw Tables

```text
RAW_PATIENTS
RAW_PROVIDERS
RAW_CANCER_CATALOG
RAW_ENCOUNTERS
```

The raw layer preserves the source data before it is transformed into the analytical warehouse model.

---

## 🏢 Data Warehouse Layer

The project uses a dimensional data warehouse model.

### Dimension Tables

```text
DIM_PATIENT
DIM_PROVIDER
DIM_CANCER
DIM_DATE
```

### Fact Table

```text
FACT_ENCOUNTER
```

The fact table stores encounter-related measurements such as:

* Encounter ID
* Patient
* Provider
* Cancer
* Disease stage
* Treatment type
* Regimen
* Billed amount
* Payment mode
* Encounter status

The dimension tables provide descriptive information used for analysis.

---

## 📊 Semantic Layer

The semantic layer provides business-friendly analytical views for Streamlit.

Important views include:

```text
VW_EXECUTIVE_SUMMARY
VW_PATIENT_ENCOUNTERS
VW_PROVIDER_PERFORMANCE
VW_CANCER_ANALYSIS
```

These views simplify access to the warehouse data and provide the datasets required by the dashboard.

---

## 🖥️ Streamlit Dashboard

The Streamlit application provides an interactive analytics interface.

### Dashboard Features

#### 📊 Executive Summary

Displays high-level KPIs including:

* Total encounters
* Total patients
* Total providers
* Number of cancer types
* Total billed amount

#### 🎗️ Cancer Analysis

Provides:

* Encounters by cancer type
* Billed amount by cancer type
* Cancer-level analytical details

#### 📅 Service Date Analysis

Provides:

* Encounters over time
* Billed amount over time
* Daily analysis

The date information is connected using the Snowflake `DIM_DATE` table.

#### 💊 Treatment Type Analysis

Provides:

* Encounters by treatment type
* Billed amount by treatment type
* Treatment-level details

#### 🩺 Disease Stage Analysis

Provides:

* Encounters by disease stage
* Billed amount by disease stage
* Disease-stage details

#### 👥 Patient Demographics

Provides analysis based on:

* Gender
* Patient segment

#### 💳 Payer Analysis

Provides:

* Encounters by payer
* Billed amount by payer
* Payer-level details

#### 👨‍⚕️ Provider Performance

Provides:

* Encounters by provider
* Billed amount by provider
* Provider-level performance information

#### 🔎 Interactive Filters

Users can filter the dashboard using:

* Cancer Type
* Provider
* Treatment Type
* Disease Stage
* Payment Mode
* Date Range

All analytical sections update based on the selected filters.

#### 📥 CSV Export

Users can download the currently filtered patient encounter data as a CSV file.

---

## 📁 Project Structure

```text
cancer_oncology_project/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
│
├── venv/
│
└── README.md
```

### File Description

| File/Folder               | Description                        |
| ------------------------- | ---------------------------------- |
| `app.py`                  | Streamlit dashboard application    |
| `.streamlit/secrets.toml` | Snowflake connection configuration |
| `venv/`                   | Python virtual environment         |
| `README.md`               | Project documentation              |

---

## 🔐 Security

Snowflake credentials are stored in:

```text
.streamlit/secrets.toml
```

The credentials file should **not** be uploaded to GitHub.

Add the following to `.gitignore`:

```text
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
```

This prevents sensitive credentials and local environment files from being committed.

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the Project

```bash
cd cancer_oncology_project
```

### 3. Create/Activate Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

### 4. Install Required Packages

```powershell
pip install streamlit
pip install snowflake-snowpark-python
pip install pandas
```

### 5. Configure Snowflake Credentials

Create:

```text
.streamlit/secrets.toml
```

Example:

```toml
[snowflake]
account = "YOUR_ACCOUNT"
user = "YOUR_USER"
password = "YOUR_PASSWORD"
role = "ACCOUNTADMIN"
warehouse = "CANCER_ONCOLOGY_WH"
database = "CANCER_ONCOLOGY_DB"
schema = "ONCOLOGY_SEMANTIC"
```

**Do not upload this file to GitHub.**

### 6. Run Streamlit

```powershell
streamlit run app.py
```

The application will open in the browser.

---

## 🔄 Data Flow

The complete data flow is:

```text
CSV Files
   ↓
Snowflake Stage
   ↓
Raw Tables
   ↓
Data Warehouse
   ↓
Dimension + Fact Tables
   ↓
Semantic Views
   ↓
Streamlit
   ↓
Interactive Analytics Dashboard
```

---

## 📈 Key Analytical Questions

The project can be used to answer questions such as:

1. How many patient encounters are recorded?
2. How many unique patients are present?
3. How many healthcare providers are involved?
4. What are the most common cancer types?
5. Which cancer types generate the highest billed amounts?
6. Which treatment types have the most encounters?
7. How are encounters distributed across disease stages?
8. Which providers handle the most encounters?
9. Which providers have the highest billed amounts?
10. How do encounters change over time?
11. How does billed amount vary over time?
12. How are patients distributed by gender?
13. How are patients distributed across segments?
14. Which payers have the highest encounter volume?
15. Which payers have the highest billed amounts?

---

## 🚀 Future Enhancements

Possible future improvements include:

* Advanced forecasting
* Automated data ingestion
* Snowflake Tasks and Streams
* Role-based access control
* More advanced visualizations
* Automated data-quality monitoring
* Scheduled dashboard reporting
* Additional oncology KPIs
* Production deployment of the Streamlit application

---

## 👩‍💻 Development Environment

The project was developed using:

```text
Python
Snowflake
Snowpark
Streamlit
Pandas
VS Code
Git
GitHub
```

---

## 📌 Conclusion

The **Cancer Oncology Analytics** project demonstrates how Snowflake can be used as a complete cloud data platform for ingesting, storing, transforming, and analyzing healthcare-related data.

The Streamlit application provides an interactive interface that allows users to explore oncology data, analyze patient encounters, compare providers and cancer types, examine treatment and disease-stage patterns, filter results, and export filtered data.

---

## ⭐ Project

**Cancer Oncology Analytics**

**Snowflake + Python + Streamlit**

```
```
