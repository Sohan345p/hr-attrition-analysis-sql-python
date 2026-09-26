"""
Step 3: Run the SQL queries from Python, print the results and save charts.

Run:  python src/analysis.py
Output: printed tables + PNG charts in images/ + CSV results in outputs/
"""
import os
import re
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "hr_attrition.db")
QUERIES_PATH = os.path.join(ROOT, "sql", "analysis_queries.sql")
IMG_DIR = os.path.join(ROOT, "images")
OUT_DIR = os.path.join(ROOT, "outputs")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

BLUE, RED, GREY = "#2E6FBA", "#D1495B", "#9AA5B1"
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False})


def load_queries(path):
    """Split the .sql file into {name: query} using the '-- name:' markers."""
    text = open(path).read()
    parts = re.split(r"--\s*name:\s*(\w+)", text)[1:]
    return {parts[i].strip(): parts[i + 1].strip() for i in range(0, len(parts), 2)}


def bar_chart(df, x, y, title, filename, highlight_top=True, xlabel="", ylabel="Attrition rate (%)"):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [BLUE] * len(df)
    if highlight_top:
        colors[int(df[y].values.argmax())] = RED
    bars = ax.bar(df[x].astype(str), df[y], color=colors)
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, filename))
    plt.close()


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit("Database not found. Run: python src/load_to_sqlite.py")

    conn = sqlite3.connect(DB_PATH)
    queries = load_queries(QUERIES_PATH)
    results = {}
    for name, sql in queries.items():
        df = pd.read_sql_query(sql, conn)
        results[name] = df
        df.to_csv(os.path.join(OUT_DIR, f"{name}.csv"), index=False)
        print(f"\n=== {name} ===")
        print(df.to_string(index=False))
    conn.close()

    # ---------- Charts ----------
    bar_chart(results["attrition_by_department"], "department", "attrition_rate_pct",
              "Attrition rate by department", "01_attrition_by_department.png")

    bar_chart(results["attrition_by_overtime"], "overtime", "attrition_rate_pct",
              "Overtime vs attrition", "02_attrition_by_overtime.png", xlabel="Works overtime?")

    bar_chart(results["attrition_by_satisfaction"], "satisfaction_label", "attrition_rate_pct",
              "Attrition by job satisfaction", "03_attrition_by_satisfaction.png",
              xlabel="Job satisfaction")

    bar_chart(results["attrition_by_tenure"], "tenure_band", "attrition_rate_pct",
              "Attrition by years at company", "04_attrition_by_tenure.png", xlabel="Tenure")

    inc = results["attrition_by_income_band"].copy()
    inc["income_band"] = inc["income_band"].str[3:]  # drop the sort prefix
    bar_chart(inc, "income_band", "attrition_rate_pct",
              "Attrition by monthly income (INR)", "05_attrition_by_income.png", xlabel="Income band")

    # Grouped bar: income of leavers vs stayers
    lv = results["income_left_vs_stayed"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    w = 0.38
    xs = range(len(lv))
    b1 = ax.bar([i - w / 2 for i in xs], lv["avg_income_stayed"], w, label="Stayed", color=BLUE)
    b2 = ax.bar([i + w / 2 for i in xs], lv["avg_income_left"], w, label="Left", color=RED)
    ax.bar_label(b1, fmt="%.0f", padding=2, fontsize=8)
    ax.bar_label(b2, fmt="%.0f", padding=2, fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(["Junior", "Mid", "Senior"])
    ax.set_ylabel("Avg monthly income (INR)")
    ax.set_title("Leavers earn less than stayers at every level", fontsize=13, fontweight="bold", loc="left")
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "06_income_left_vs_stayed.png"))
    plt.close()

    print(f"\nCharts saved to {IMG_DIR}")
    print(f"Query results saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
