-- ============================================================
-- HR Employee Attrition Analysis - SQL queries
-- Each query answers one business question.
-- The "-- name:" line is used by src/analysis.py to run them.
-- ============================================================

-- name: overall_kpis
-- Q1. How many employees do we have, how many left, and what is the attrition rate?
SELECT
    COUNT(*)                                                    AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)          AS employees_left,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 0)                               AS avg_monthly_income,
    ROUND(AVG(years_at_company), 1)                             AS avg_tenure_years
FROM employees;

-- name: attrition_by_department
-- Q2. Which departments lose the most people?
SELECT
    department,
    COUNT(*)                                                    AS headcount,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)          AS employees_left,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- name: attrition_by_overtime
-- Q3. Does working overtime increase attrition?
SELECT
    overtime,
    COUNT(*)                                                    AS headcount,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY overtime;

-- name: attrition_by_satisfaction
-- Q4. How does job satisfaction relate to attrition?
SELECT
    job_satisfaction,
    CASE job_satisfaction
        WHEN 1 THEN 'Low' WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High' ELSE 'Very High' END                 AS satisfaction_label,
    COUNT(*)                                                    AS headcount,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction;

-- name: attrition_by_tenure
-- Q5. Are new joiners more likely to leave? (CASE to create tenure bands)
SELECT
    CASE
        WHEN years_at_company <= 1 THEN '0-1 yrs'
        WHEN years_at_company <= 3 THEN '2-3 yrs'
        WHEN years_at_company <= 6 THEN '4-6 yrs'
        ELSE '7+ yrs'
    END                                                         AS tenure_band,
    COUNT(*)                                                    AS headcount,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY tenure_band
ORDER BY MIN(years_at_company);

-- name: attrition_by_income_band
-- Q6. Does salary affect attrition?
SELECT
    CASE
        WHEN monthly_income < 30000  THEN '1. < 30K'
        WHEN monthly_income < 60000  THEN '2. 30K-60K'
        WHEN monthly_income < 100000 THEN '3. 60K-1L'
        ELSE '4. 1L+'
    END                                                         AS income_band,
    COUNT(*)                                                    AS headcount,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY income_band
ORDER BY income_band;

-- name: income_left_vs_stayed
-- Q7. Average salary of employees who left vs stayed, per job level
SELECT
    job_level,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN monthly_income END), 0) AS avg_income_left,
    ROUND(AVG(CASE WHEN attrition = 'No'  THEN monthly_income END), 0) AS avg_income_stayed
FROM employees
GROUP BY job_level
ORDER BY job_level;

-- name: top_risk_roles
-- Q8. Top 5 job roles by attrition rate (only roles with 30+ employees)
SELECT
    job_role,
    department,
    COUNT(*)                                                    AS headcount,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM employees
GROUP BY job_role, department
HAVING COUNT(*) >= 30
ORDER BY attrition_rate_pct DESC
LIMIT 5;

-- name: dept_vs_company_avg
-- Q9. Which departments are above the company average? (subquery)
SELECT
    department,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS dept_rate_pct,
    (SELECT ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1)
       FROM employees)                                          AS company_rate_pct
FROM employees
GROUP BY department
HAVING dept_rate_pct > (SELECT 100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) FROM employees)
ORDER BY dept_rate_pct DESC;

-- name: high_risk_current_employees
-- Q10. Current employees who match the high-risk profile (CTE)
-- Profile: overtime + low satisfaction (1-2) + poor work-life balance (1-2)
WITH current_staff AS (
    SELECT * FROM employees WHERE attrition = 'No'
)
SELECT
    department,
    COUNT(*) AS high_risk_employees
FROM current_staff
WHERE overtime = 'Yes'
  AND job_satisfaction <= 2
  AND work_life_balance <= 2
GROUP BY department
ORDER BY high_risk_employees DESC;
