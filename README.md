# 🧠 Mental Health in Tech Analytics

## 📌 Project Overview

This project focuses on analyzing mental health treatment patterns among technology employees using the **2014 Mental Health in Tech Survey** with **1,259 respondents**.

The analysis explores demographic, personal, and workplace factors associated with mental health treatment-seeking behavior.

The project follows an end-to-end **Exploratory Data Analysis (EDA)** workflow, including data cleaning, feature engineering, univariate, bivariate and multivariate analysis, correlation analysis, and statistical hypothesis testing using **Chi-square tests and Cramér's V**.

The findings are translated into actionable workplace insights and presented through an interactive multi-page **Streamlit dashboard** designed for both technical and non-technical stakeholders.

---

## 🎯 Business Objectives

- 🔍 Identify the key factors associated with mental health treatment.
- 👥 Analyze demographic and workplace characteristics of survey respondents.
- 🏢 Examine the relationship between workplace support and treatment behavior.
- 📈 Evaluate how work interference relates to mental health treatment.
- 🛟 Identify gaps in mental health benefits, care options, and workplace support.
- 🧪 Validate important relationships using statistical analysis.
- 💡 Generate data-driven recommendations to support workplace mental health initiatives.

---

## 🛠️ Tools & Technologies

- 🐍 Python
- 📓 Jupyter Notebook
- 🐼 Pandas
- 🔢 NumPy
- 🧪 SciPy
- 📊 Matplotlib
- 📈 Seaborn
- 📉 Plotly
- 🖥️ Streamlit
- 📐 Statistical Analysis
- 🔗 Git & GitHub

---

## 🔄 Project Workflow

### 1. 🧹 Data Preparation

- Inspected the 2014 Mental Health in Tech Survey dataset.
- Cleaned invalid and unrealistic age values.
- Standardized gender responses.
- Handled missing values across key variables.
- Retained missing and uncertain responses as distinct categories where appropriate.
- Excluded the high-missingness `comments` field from quantitative analysis.

### 2. ⚙️ Feature Engineering

- Created age groups.
- Grouped company sizes.
- Classified remote work status.
- Created mental health history indicators.
- Created treatment status categories.
- Converted work interference levels into an ordinal analytical feature.

### 3. 📊 Exploratory Data Analysis

- 👤 Univariate analysis of demographic and mental health variables.
- 🔎 Bivariate analysis of treatment rates across key factors.
- 🧩 Multivariate analysis of treatment patterns.
- 🔗 Correlation analysis using Spearman correlation.
- 🌎 Geographic analysis of respondent distribution.

### 4. 🧪 Statistical Validation

- Chi-square Test of Independence
- Cramér's V effect size
- Statistical significance testing
- Comparison of significant and non-significant relationships

---

## 🔎 Key Analysis

- 🧠 Mental Health Treatment Distribution
- 👥 Age & Gender Analysis
- 👨‍👩‍👧 Family History & Treatment
- 💼 Work Interference & Treatment
- 🛟 Mental Health Benefits & Treatment
- 🏥 Care Options & Treatment
- 🔐 Perceived Anonymity & Treatment
- 🏠 Remote Work & Treatment
- 🏢 Company Size & Treatment
- 🤝 Workplace Mental Health Culture
- 🌎 Geographic Distribution
- 🧩 Multivariate Relationships
- 🧪 Statistical Significance & Effect Size

---

## 📌 Key Findings

| Finding | Detail |
|---|---|
| 🧠 **Overall Treatment Rate** | Approximately **50.6%** of respondents reported receiving mental health treatment. |
| 💼 **Work Interference** | Treatment rates increased substantially with work interference — **85.4%** among respondents reporting interference "Often" compared with **14.1%** among those reporting "Never". |
| 👨‍👩‍👧 **Family History** | Respondents with a family history of mental health conditions had a **74.2%** treatment rate compared with **35.5%** among those without a family history. |
| 🏥 **Care Options** | Awareness of available mental health care options was significantly associated with treatment behavior. |
| 🛟 **Mental Health Benefits** | Respondents reporting access to mental health benefits showed higher treatment rates. |
| 🧪 **Statistical Validation** | Work interference, family history, care options, benefits, and gender showed statistically significant associations with treatment. |
| 📊 **Non-Significant Factors** | Age group, remote work status, company size, and several workplace perception variables did not show statistically significant associations. |

> ⚠️ **Important:** The analysis identifies associations rather than causal relationships. Findings should be interpreted at a population level and should not be used to profile or label individual employees.

---

## 💡 Business Insights

- 🎯 **Work interference** represents the strongest treatment-related signal identified in the analysis.
- 🛟 Organizations can strengthen early support pathways for employees experiencing mental health difficulties that affect their work.
- 🏥 Providing mental health benefits alone may not be sufficient; employees also need clear awareness of available care options.
- 📢 Improving communication around mental health resources can help make support easier to access.
- 👥 Mental health initiatives should focus on employee needs and workplace conditions rather than demographic profiling.
- 🔐 Confidentiality and trust remain important considerations when designing workplace mental health programs.

---

## 📦 Project Deliverables

This repository contains:

- 📓 **Jupyter Notebook (.ipynb)** – Complete data cleaning, exploratory analysis, visualization, feature engineering, and statistical validation.
- 🖥️ **Streamlit Dashboard** – Interactive multi-page dashboard presenting the analysis and business insights.
- 🗃️ **Cleaned Dataset (.csv)** – Processed datasets used for analysis and dashboard development.
- 🖼️ **Chart Outputs (.png)** – Exported visualizations generated during the analysis.
- 📋 **Requirements File (.txt)** – Python dependencies required to run the project.

---

## 📁 Repository Structure

```text
mental-health-in-tech-analysis/
│
├── 📂 Notebooks/
│   └── 📓 Mental_Health_Tech_EDA.ipynb
│
├── 📂 pages/
│   ├── 👥 2_Respondent_Profile.py
│   ├── 🤝 3_Workplace_Support_&_Culture.py
│   ├── 🧠 4_Mental_Health_&_Treatment.py
│   ├── 🧪 5_Statistical_Analysis.py
│   └── 🎯 6_Executive_Insights.py
│
├── 📂 utils/
│   ├── analytics.py
│   ├── data_loader.py
│   └── styling.py
│
├── 📂 data/
│   └── survey.csv
│
├── 📂 outputs/
│   ├── 📊 charts/
│   └── 📂 cleaned_data/
│       ├── mental_health_tech_cleaned.csv
│       └── mental_health_tech_final.csv
│
├── 🖥️ Overview.py
├── 📋 requirements.txt
├── 📄 README.md
└── 🚫 .gitignore
```

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.9+
- Git

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/T3MP35TT/mental-health-in-tech-analysis.git

# Navigate to the project directory
cd mental-health-in-tech-analysis

# Create a virtual environment
python -m venv venv

# Activate the virtual environment

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 🖥️ Run the Dashboard

```bash
streamlit run Overview.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

### 📓 Run the Notebook

```bash
jupyter notebook Notebooks/Mental_Health_Tech_EDA.ipynb
```

---

## 📊 Dashboard Pages

| Page | Description |
|---|---|
| 🏠 **Overview** | Project overview, KPIs, and high-level findings |
| 👥 **Respondent Profile** | Demographic and geographic analysis |
| 🤝 **Workplace Support & Culture** | Benefits, care options, wellness programs, anonymity, leave, and workplace culture |
| 🧠 **Mental Health & Treatment** | Treatment patterns, family history, and work interference |
| 🧪 **Statistical Analysis** | Chi-square tests, statistical significance, and Cramér's V |
| 🎯 **Executive Insights** | Key findings, business implications, and recommendations |

---

## 🧠 Skills Demonstrated

- 🔍 Exploratory Data Analysis (EDA)
- 🧹 Data Cleaning & Preprocessing
- ⚙️ Feature Engineering
- 🧪 Statistical Analysis
- 📐 Hypothesis Testing
- χ² Chi-square Testing
- 📏 Cramér's V
- 🔗 Spearman Correlation
- 📊 Data Visualization
- 🧩 Multivariate Analysis
- 🐍 Python
- 🐼 Pandas
- 🔢 NumPy
- 🧪 SciPy
- 📈 Seaborn
- 📉 Plotly
- 🖥️ Streamlit
- 💼 Business Analysis
- 📖 Data Storytelling
- 📊 Dashboard Development

---

## 🔮 Future Enhancements

- 🌐 Deploy the Streamlit dashboard for public access.
- 🧪 Add additional statistical tests and analytical techniques.
- 📅 Incorporate more recent mental health datasets for comparison.
- 🔎 Expand the dashboard with additional filtering and segmentation capabilities.
- 📈 Develop longitudinal analysis using newer workplace mental health surveys.

---

## ⚠️ Limitations

- 📅 The dataset was collected in **2014** and may not reflect current workplace conditions.
- 📝 The survey is self-reported and observational.
- 🇺🇸 The sample has a strong representation of respondents from the United States.
- 🌎 The dataset is not globally representative.
- 💬 The `comments` field contains substantial missing data and was excluded from quantitative analysis.
- 🧪 Statistical relationships represent associations and should not be interpreted as causal effects.

---

## 👤 Author

**Kartikey Singh**

**Data Analyst | Power BI | Python | SQL | Excel**

🔗 LinkedIn: *[Kartikey_Singh](https://www.linkedin.com/in/btwitskartiksinghdatanalyst/)*

🐙 GitHub: *[Kartikey_Singh](https://github.com/T3MP35TT)*

🌐 Portfolio: *[Kartikey_Singh](https://sites.google.com/view/kartikeysingh09/home)*

📝 Complete WriteUp: **Coming Soon....**
