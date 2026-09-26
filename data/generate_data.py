"""
Generate a synthetic HR dataset (1,500 employees) for the attrition analysis.

The data is fictional and created with a fixed random seed, so anyone who
runs this script gets exactly the same CSV file.

Run:  python data/generate_data.py
Output: data/employees.csv
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1500

departments = ["Sales", "Research & Development", "Human Resources", "IT", "Finance", "Operations"]
dept_weights = [0.28, 0.30, 0.07, 0.15, 0.08, 0.12]
roles = {
    "Sales": ["Sales Executive", "Sales Representative", "Sales Manager"],
    "Research & Development": ["Research Scientist", "Lab Technician", "Research Director"],
    "Human Resources": ["HR Executive", "HR Manager"],
    "IT": ["Software Engineer", "Data Analyst", "IT Manager"],
    "Finance": ["Accountant", "Financial Analyst", "Finance Manager"],
    "Operations": ["Operations Associate", "Supervisor", "Operations Manager"],
}
cities = ["Nagpur", "Pune", "Mumbai", "Bengaluru", "Hyderabad"]
education = ["Diploma", "Bachelor", "Master", "PhD"]

rows = []
for i in range(1, N + 1):
    dept = rng.choice(departments, p=dept_weights)
    role_list = roles[dept]
    level = rng.choice([1, 2, 3], p=[0.55, 0.32, 0.13])  # 1=junior, 2=mid, 3=senior
    role = role_list[min(level, len(role_list)) - 1]

    age = int(np.clip(rng.normal(22 + level * 6, 5), 21, 58))
    years_at_company = int(np.clip(rng.exponential(2.5 + level * 2), 0, age - 21))
    gender = rng.choice(["Male", "Female"], p=[0.6, 0.4])
    marital = rng.choice(["Single", "Married", "Divorced"], p=[0.38, 0.50, 0.12])
    edu = rng.choice(education, p=[0.15, 0.50, 0.30, 0.05])
    city = rng.choice(cities)
    distance_km = int(np.clip(rng.gamma(2, 6), 1, 60))

    base = {1: 30000, 2: 60000, 3: 110000}[level]
    monthly_income = int(base * rng.uniform(0.8, 1.3) * (1 + years_at_company * 0.03))
    overtime = rng.random() < 0.30
    job_satisfaction = int(rng.choice([1, 2, 3, 4], p=[0.18, 0.22, 0.32, 0.28]))
    work_life_balance = int(rng.choice([1, 2, 3, 4], p=[0.08, 0.24, 0.50, 0.18]))
    performance_rating = int(rng.choice([2, 3, 4], p=[0.10, 0.70, 0.20]))
    years_since_promotion = int(min(years_at_company, rng.poisson(2)))
    training_last_year = int(rng.integers(0, 7))

    # Attrition probability built from realistic drivers
    logit = -2.6
    logit += 1.3 if overtime else 0
    logit += {1: 1.0, 2: 0.4, 3: 0.0, 4: -0.4}[job_satisfaction]
    logit += {1: 0.9, 2: 0.3, 3: 0.0, 4: -0.2}[work_life_balance]
    logit += 0.8 if years_at_company <= 1 else (-0.5 if years_at_company >= 7 else 0)
    logit += 0.6 if monthly_income < 30000 else 0
    logit += 0.5 if dept == "Sales" else 0
    logit += 0.4 if marital == "Single" else 0
    logit += 0.4 if distance_km > 20 else 0
    logit += 0.3 if years_since_promotion >= 4 else 0
    p = 1 / (1 + np.exp(-logit))
    attrition = "Yes" if rng.random() < p else "No"

    rows.append({
        "employee_id": 1000 + i,
        "age": age,
        "gender": gender,
        "marital_status": marital,
        "education": edu,
        "department": dept,
        "job_role": role,
        "job_level": level,
        "city": city,
        "distance_from_home_km": distance_km,
        "monthly_income": monthly_income,
        "overtime": "Yes" if overtime else "No",
        "job_satisfaction": job_satisfaction,
        "work_life_balance": work_life_balance,
        "performance_rating": performance_rating,
        "years_at_company": years_at_company,
        "years_since_last_promotion": years_since_promotion,
        "training_times_last_year": training_last_year,
        "attrition": attrition,
    })

df = pd.DataFrame(rows)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.csv")
df.to_csv(out, index=False)
print(f"Saved {len(df)} rows to {out}")
print(f"Overall attrition rate: {(df['attrition'] == 'Yes').mean():.1%}")
