# 🧠 Kenya Mental Health Monitoring & Evaluation (M&E) Dashboard
## 📊 Dashboard Preview

![Kenya Mental Health Dashboard](sample.png)
> A real-world-style digital health data system tracking mental health service delivery across 41 Kenyan counties — built to simulate the workflows used by health NGOs and county health departments.

---

## 📌 Overview

This project simulates a complete **Monitoring & Evaluation (M&E) system** for mental health programs in Kenya, modelled on the reporting structures used by organisations like the **Ministry of Health Kenya**, **WHO**, and **DHIS2-enabled NGOs**.

It covers the full data pipeline — from raw global health indicators to a structured, operational dataset — and delivers an **interactive Streamlit dashboard** for program managers, health analysts, and decision-makers.

---

## 🎯 Objectives

- Transform raw health datasets into an **analysis-ready M&E system**
- Simulate **DHIS2-style monthly reporting workflows**
- Track **treatment gaps and service delivery performance** at county and facility level
- Build dashboards for **data-driven decision support**

---

## 🗂️ Dataset Description

The final dataset (`kenya_health_m_e_dataset.csv`) is structured at three levels:

| Level | Detail |
|-------|--------|
| Geographic | 41 Kenyan counties |
| Operational | 205 health facilities |
| Temporal | 24 monthly reporting periods (Jan 2022 – Dec 2023) |

**Total records: 4,920 rows**

### Key Variables

| Column | Type | Description |
|--------|------|-------------|
| `county` | string | Kenyan county name |
| `facility_name` | string | Health facility identifier |
| `reporting_month` | date | Monthly reporting period (YYYY-MM-DD) |
| `mental_health_prevalence` | float | Estimated MH prevalence rate (8–22%) |
| `mental_health_burden_daly` | float | Disease burden proxy (DALYs per 100k) |
| `patients_screened` | int | Number of patients screened that month |
| `patients_treated` | int | Number of patients who received treatment |
| `treatment_gap` | float | Proportion of screened patients not treated |
| `treatment_rate` | float | Proportion of screened patients treated |
| `unmet_need` | int | Absolute number of untreated patients |
| `reporting_year` | int | Year of reporting |
| `reporting_quarter` | string | Quarter (Q1–Q4) |

---

## ⚙️ Data Engineering Process

### 1. Data Integration
Combined multiple global health data sources:
- Mental illness prevalence rates (county-level)
- Disease burden estimates (DALYs)
- Treatment gap benchmarks

### 2. Transformation
- Filtered and contextualised data for Kenya
- Standardised variables into **program-aligned M&E indicators**
- Disaggregated annual data into **monthly reporting periods** (DHIS2 style)
- Applied seasonal adjustment factors to simulate real-world patterns

### 3. Data Modelling
Introduced two operational layers:
- **County layer** — geographic analysis and regional comparison
- **Facility layer** — operational accountability and performance monitoring

### 4. Output
```
kenya_health_m_e_dataset.csv   ← Clean, analysis-ready dataset
```

---

## 📊 Streamlit Dashboard

## 📊 Dashboard Preview

![Kenya Mental Health Dashboard](assets/sample.png)

### Features

| Section | What it shows |
|---------|--------------|
| **KPI Cards** | Total screened, treated, treatment gap, treatment rate, unmet need |
| **Monthly Trend** | Screening vs treatment over 24 months |
| **County Comparison** | Top counties by treatment gap (bar chart) |
| **Facility Table** | Ranked facility performance |
| **Scatter Plot** | Screened vs treated by county — size = prevalence, color = gap |
| **Quarterly Summary** | Combined bar + line chart across reporting quarters |

### Sidebar Filters
- County
- Year (2022 / 2023)
- Quarter (Q1–Q4)

### Run locally

```bash
# 1. Clone the repo
git clone https://github.com/evans25575/kenya-mh-dashboard/kenya-mh-dashboard.git
cd kenya-mh-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python generate_dataset.py

# 4. Launch the dashboard
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Pandas** | Data wrangling & transformation |
| **NumPy** | Statistical simulation |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Charts and visualisations |
| **Power BI** | Offline reporting dashboard |

---

## 📁 Project Structure

```
kenya-mh-dashboard/
│
├── generate_dataset.py         # Data pipeline — generates the CSV
├── app.py                      # Streamlit dashboard application
├── kenya_health_m_e_dataset.csv# Final M&E dataset (4,920 rows)
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## 💡 Key Insights (Sample Findings)

- **Treatment gap ranges from 25% to 70%** across counties, indicating major disparities in service delivery
- **Seasonal patterns** visible in monthly screening data, with higher activity in Q1 and Q3
- **Facility-level variation** within the same county suggests operational inefficiencies beyond resource constraints
- **High-burden counties** (high DALYs) do not always correlate with high screening rates — a policy gap

---

## 🌐 Relevance to Digital Health

This project demonstrates practical skills in:

- Health data pipeline design (ETL)
- DHIS2-style M&E system design
- Digital health reporting workflows
- Indicator-based program tracking
- Data-driven decision support tools

---

## 📈 Future Improvements

- [ ] Integrate real DHIS2 Kenya open data
- [ ] Add geospatial county-level choropleth map
- [ ] Deploy Streamlit app to Streamlit Cloud
- [ ] Add forecasting module (treatment demand prediction)
- [ ] Export filtered data to PDF/Excel within dashboard

---

## 👤 Author

**Evans Kiplangat**  
*Data Analyst | Data Engineer | Digital Health Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/YOUR_USERNAME)

---


