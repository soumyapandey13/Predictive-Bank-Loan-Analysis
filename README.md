# 🏦 Predictive Bank Loan Analytics & Machine Learning Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Machine Learning](https://img.shields.io/badge/Machine_Learning-FF6F00?style=for-the-badge&logo=scikitlearn&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

![Dashboard Preview](media/img.png)

## 📌 Executive Summary
This project is an end-to-end Machine Learning and Data Analytics pipeline designed to evaluate a **$436M bank loan portfolio**. Moving beyond traditional historical reporting, this project utilizes Python-based machine learning to predict loan defaults, identify high-risk segments, and visualize portfolio vulnerabilities. 

By engineering a custom predictive model and connecting its outputs to a highly interactive Power BI dashboard, thousands of raw loan records were transformed into forward-looking, actionable intelligence for underwriting teams.

## 🛠️ The Full-Stack Analytics Workflow

### 1. Data Processing & Structuring (SQL)
* **Ingestion & Cleaning:** Extracted raw financial data (`Bank_loan_data`) containing over 38,000 records of borrower demographics, loan attributes, and repayment status.
* **Transformation:** Utilized custom queries (`data_cleaning.sql`) to handle missing values, standardize financial formats (DTI, income, term, interest rates), and derive structured features for model training.

### 🤖 Machine Learning Model Performance
* **Algorithm Chosen:** Random Forest Classifier (Chosen for its robust handling of non-linear financial variables and feature importance outputs).
* **Accuracy:** 88.5%
* **Precision (High-Risk Default):** 84% 
* **Recall (High-Risk Default):** 89%
* **Evaluation Metric Strategy:** Prioritized *Recall* to ensure the model aggressively flags potential defaults, as the cost of a missed default is significantly higher than a false positive.

### 3. Dashboard Engineering & UI/UX (Power BI)
* **Custom Architecture:** Built a completely custom "Dark Mode" aesthetic using transparent glass containers and conditional formatting to intuitively highlight predicted risk areas.
* **Dynamic Filtering:** Engineered interactive slicers (Home Ownership, Loan Term, Employment Length) allowing stakeholders to drill down into specific borrower profiles and watch predicted KPIs recalculate in real-time.
* **Geospatial Analytics:** Integrated a dark-themed map to visualize the ML model's predicted default risk by state, exposing regional vulnerabilities at a glance.

## 🧠 Key Predictive Insights

1. **The Primary Risk Driver:** **Debt Consolidation** is the single largest contributor to predicted default risk, dwarfing all other loan purposes combined. The model recommends stricter Debt-to-Income (DTI) thresholds for this segment.
2. **The "Safe Borrower" Illusion:** Filtering for highly seasoned workers (10+ years of employment) still reveals **1.20K predicted defaults**, proving that employment stability alone does not negate the risk of over-leveraged borrowers.
3. **Mid-Tier Risk Accumulation:** While Grades F and G carry the highest individual risk percentages, the model flags the vast majority of total portfolio vulnerability in **Grades B, C, and D**, where standard underwriting criteria may be too lenient at volume.

4. ## 🚀 How to Run the Project Locally
1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/soumyapandey13/Predictive-Bank-Loan-Analysis.git](https://github.com/soumyapandey13/Predictive-Bank-Loan-Analysis.git)

mail - pandeysoumyaa13@gmail.com
