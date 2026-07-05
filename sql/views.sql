-- ============================================
-- HR Analytics Dashboard - Useful Views
-- ============================================

-- 1. Employee Overview View
CREATE OR REPLACE VIEW v_employee_overview AS
SELECT
    employee_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    department,
    job_role,
    gender,
    age,
    education_field,
    hire_date,
    DATEDIFF(CURRENT_DATE, hire_date) / 365 AS tenure_years,
    salary,
    performance_rating,
    job_satisfaction,
    work_life_balance,
    attrition
FROM employees;

-- 2. Department Summary View
CREATE OR REPLACE VIEW v_department_summary AS
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) AS female_count,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(AVG(performance_rating), 2) AS avg_performance,
    ROUND(AVG(years_at_company), 1) AS avg_tenure,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance
FROM employees
WHERE employment_status = 'Active'
GROUP BY department;

-- 3. Attrition Analysis View
CREATE OR REPLACE VIEW v_attrition_analysis AS
SELECT
    department,
    education_field,
    gender,
    age,
    job_role,
    marital_status,
    business_travel,
    overtime,
    years_at_company,
    years_since_last_promotion,
    job_satisfaction,
    work_life_balance,
    performance_rating,
    salary,
    salary_hike_percent,
    attrition
FROM employees
WHERE attrition = 'Yes';

-- 4. Monthly Attendance View
CREATE OR REPLACE VIEW v_monthly_attendance AS
SELECT
    e.department,
    YEAR(a.date) AS year,
    MONTH(a.date) AS month,
    COUNT(DISTINCT a.employee_id) AS total_employees,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS absent_days,
    SUM(CASE WHEN a.status = 'WFH' THEN 1 ELSE 0 END) AS wfh_days,
    ROUND(AVG(a.hours_worked), 2) AS avg_hours_worked
FROM attendance a
JOIN employees e ON a.employee_id = e.employee_id
GROUP BY e.department, YEAR(a.date), MONTH(a.date);

-- 5. Performance Trend View
CREATE OR REPLACE VIEW v_performance_trend AS
SELECT
    e.department,
    pr.review_period,
    ROUND(AVG(pr.overall_rating), 2) AS avg_rating,
    ROUND(AVG(pr.goals_achieved * 100.0 / NULLIF(pr.goals_target, 0)), 2) AS avg_goal_achievement_pct,
    COUNT(DISTINCT pr.employee_id) AS employees_reviewed
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.employee_id
GROUP BY e.department, pr.review_period
ORDER BY pr.review_period, e.department;

-- 6. Training ROI View
CREATE OR REPLACE VIEW v_training_roi AS
SELECT
    e.department,
    t.training_category,
    COUNT(*) AS training_count,
    SUM(t.cost) AS total_cost,
    ROUND(AVG(t.post_training_score - t.pre_training_score), 2) AS avg_score_improvement,
    ROUND(SUM(t.cost) / NULLIF(COUNT(*), 0), 2) AS cost_per_training
FROM training t
JOIN employees e ON t.employee_id = e.employee_id
WHERE t.completion_status = 'Completed'
GROUP BY e.department, t.training_category;
