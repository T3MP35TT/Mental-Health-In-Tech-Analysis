# 🧠 Mental Health in Tech Analytics

An end-to-end exploratory data analysis and interactive Streamlit dashboard exploring mental health treatment patterns among technology employees, built on the **2014 Mental Health in Tech Survey** (1,259 respondents).

---

## 📌 Project Overview

Mental health is a critical but often under-addressed workplace issue, particularly in the technology industry, where high-pressure environments and inconsistent organizational support are common. This project analyzes the 2014 Mental Health in Tech Survey to understand **which demographic, personal, and workplace factors are most strongly associated with mental health treatment-seeking behavior**.

The project follows a structured EDA workflow — data cleaning, feature engineering, univariate and multivariate visualization, correlation analysis, and statistical hypothesis testing (Chi-square tests and Cramér's V) — and translates the findings into an interactive multi-page dashboard for non-technical stakeholders.

**Live dashboard:** *[add your deployed Streamlit app link here]*

---

## 🎯 Business Objective

Identify the major factors associated with mental health treatment among technology employees and translate those insights into practical workplace recommendations. Specifically, the analysis aims to help organizations:

- Understand patterns in employee mental health treatment
- Identify groups with substantially different treatment rates
- Evaluate the relationship between workplace support and treatment behavior
- Quantify how work interference relates to treatment
- Identify gaps in mental health benefits, care options, and workplace support
- Use statistically validated relationships (not just visual trends) to prioritize interventions

---

## 🔑 Key Findings

| Finding | Detail |
|---|---|
| **Overall treatment rate** | ~50.6% (637 of 1,259 respondents reported receiving treatment) |
| **Strongest predictor** | Work interference — 85.4% treatment rate among those who report it "often" vs. 14.1% among those who report "never" |
| **Second strongest predictor** | Family history — 74.2% treatment rate with a family history vs. 35.5% without |
| **Workplace support** | Higher treatment rates observed among respondents reporting access to care options and mental health benefits |
| **Geography** | The U.S. accounts for the majority of respondents, with California the most represented state — sample is not globally representative |
| **Statistically significant factors** (Chi-square / Cramér's V) | Work interference, family history, care options, benefits, gender |
| **Not statistically significant** | Age group, remote work status, company size, supervisor attitudes, several physical-health perception variables |

> ⚠️ The survey is observational — all relationships identified are **associations, not causal effects**. Findings should inform population-level workplace policy, not be used to label or profile individual employees.

---

## 🗂️ Dataset

- **Source:** 2014 Mental Health in Tech Survey (OSMI)
- **Size:** 1,259 respondents, 27 original variables
- **Target variable:** `treatment` — whether the respondent reported receiving treatment for a mental health condition
- **Variable categories:** demographics (age, gender, state), employment (company size, remote work, tech company), mental health history and treatment, workplace support (benefits, care options, wellness programs, anonymity, leave), and perceptions (coworker/supervisor attitudes, interview concerns)

### Data Cleaning Highlights
- 8 invalid `Age` values (negative or unrealistic) converted to missing; valid range retained as 18–72
- `Gender` free-text responses standardized into `Male`, `Female`, `Other`
- Missing `state` and `self_employed` values labeled `Unknown` rather than imputed
- Missing `work_interfere` labeled `Not Answered` (kept distinct from `Never`)
- `comments` field excluded from quantitative analysis (~86.97% missing)
- Derived features engineered: `Age Group`, `Company Size Group`, `Remote Work Status`, `Mental Health History`, `Treatment Status`, `Work Interference Level`

Cleaned dataset output: `outputs/cleaned_data/mental_health_tech_cleaned.csv`

---

## 🛠️ Tech Stack

- **Language:** Python
- **Analysis:** pandas, NumPy, SciPy (`chi2_contingency`)
- **Visualization:** Plotly Express / Plotly Graph Objects
- **Dashboard:** Streamlit (multi-page app)
- **Notebook:** Jupyter (`Mental_Health_Tech_EDA.ipynb`)

---

## 📁 Repository Structure

```
mental-health-in-tech-analytics/
│
├── Mental_Health_Tech_EDA.ipynb        # Full EDA notebook: cleaning, viz, stats
├── Overview.py                         # Streamlit app entry point / home page
│
├── pages/
│   ├── 2_Respondent_Profile.py         # Demographics deep-dive
│   ├── 3_Workplace_Support___Culture.py# Benefits, care options, culture
│   ├── 4_Mental_Health___Treatment.py  # Treatment patterns & history
│   ├── 5_Statistical_Analysis.py       # Chi-square tests & Cramér's V
│   └── 6_Executive_Insights.py         # Summary insights & recommendations
│
├── utils/
│   ├── data_loader.py                  # Loads and caches the cleaned dataset
│   ├── analytics.py                    # Treatment-rate & grouping helper functions
│   └── styling.py                      # Shared page styling and layout helpers
│
├── outputs/
│   └── cleaned_data/
│       └── mental_health_tech_cleaned.csv
│
├── requirements.txt
└── README.md
```

> **Note:** File names above reflect the underlying Streamlit page scripts (`2_Respondent_Profile.py`, etc.); place them inside a `pages/` directory for Streamlit's native multi-page navigation to pick them up.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/mental-health-in-tech-analytics.git
cd mental-health-in-tech-analytics

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run Overview.py
```

The app will open at `http://localhost:8501`, with page navigation for Respondent Profile, Workplace Support & Culture, Mental Health & Treatment, Statistical Analysis, and Executive Insights available in the sidebar.

### Run the Notebook

```bash
jupyter notebook Mental_Health_Tech_EDA.ipynb
```

---

## 📊 Dashboard Pages

| Page | Description |
|---|---|
| **Overview** | KPI summary — treatment rate, family history rate, work-interference rate |
| **Respondent Profile** | Age, gender, and geographic distribution of survey respondents |
| **Workplace Support & Culture** | Benefits, care options, wellness programs, anonymity, and leave policy analysis |
| **Mental Health & Treatment** | Treatment status, family history, and work-interference patterns |
| **Statistical Analysis** | Chi-square significance tests and Cramér's V effect sizes across all candidate factors |
| **Executive Insights** | Consolidated, non-technical summary of findings and workplace recommendations |

---

## 💡 Recommendations

1. **Prioritize employees reporting work interference** — the single strongest signal associated with treatment-seeking; early identification and support pathways here have the highest potential impact.
2. **Improve visibility and accessibility of care options and benefits** — awareness gaps, not just availability, appear to matter.
3. **Strengthen confidentiality and anonymity assurances** to reduce stigma-related barriers to seeking help.
4. **Avoid demographic profiling** — factors like age and company size were not statistically significant; interventions should be need-based, not identity-based.
5. **Interpret geographic findings cautiously** — the sample skews heavily U.S./California, limiting global generalizability.

---

## ⚠️ Limitations

- Self-reported, observational survey data — no causal claims can be made
- Data collected in 2014; workplace mental health norms and policies may have shifted since
- Sample skews toward U.S.-based and male respondents, limiting demographic and geographic generalizability
- `comments` free-text field excluded from analysis due to high missingness

---

## 👤 Author

**[Your Name]**
Data Analyst
[LinkedIn](#) · [Portfolio](#) · [GitHub](#)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.