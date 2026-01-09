# Aadhaar as a Living System

**Data Analysis & Visualization of UIDAI Aadhaar Enrolment, Biometric, and Demographic Data**

---

## 📌 Overview

This project analyses Aadhaar enrolment, biometric, and demographic datasets to uncover **system-level patterns, trends, anomalies, and predictive indicators**.
Instead of treating Aadhaar as a one-time registration system, the dashboard models it as a **living digital infrastructure** with continuous usage and evolving demand.

All insights are derived **strictly from the provided UIDAI datasets**, with no external data or assumptions.

---

## 🎯 Objective

To support **informed decision-making and system improvements** by:

* Identifying long-term usage patterns
* Detecting regional concentration and service hubs
* Highlighting early warning signals for infrastructure stress
* Translating raw data into actionable policy insights

---

## 📂 Datasets Used

* **Enrolment Data**
  Age groups: `0–5`, `5–17`, `18+`
  Represents Aadhaar inflow (new registrations)

* **Biometric Data**
  Age groups: `5–17`, `17+`
  Represents recurring Aadhaar usage (authentication & updates)

* **Demographic Data**
  Age groups: `5–17`, `17+`
  Represents resident Aadhaar population (stock)

⚠️ Age-group mismatches are handled analytically (stocks vs flows) and **not force-aligned**.

---

## 📊 Key Insights

1. **Aadhaar has evolved into a continuously used system**
   Biometric activity remains high even when enrolments stabilize.

2. **Adult population (17+) drives biometric demand**
   Most system load originates from working-age users.

3. **Enrolment is a leading indicator of biometric usage**
   Growth in adult enrolment predicts future biometric demand.

4. **Biometric usage is regionally concentrated**
   Certain districts act as Aadhaar service hubs due to migration or administrative load.

5. **Growth-rate analysis reveals future pressure points**
   Rapidly growing districts can be identified before absolute volumes peak.

6. **No system-wide anomaly spikes detected**
   Usage patterns are stable, supporting reliance on long-term trends.

---

## 🧱 Project Structure

```
aadhar-hackathon/
│
├── app.py
├── requirements.txt
│
└── data/
    ├── enrolment.csv
    ├── biometric.csv
    └── demographic.csv
```

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
