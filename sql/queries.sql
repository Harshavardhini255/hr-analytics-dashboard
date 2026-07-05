-- ============================================
-- HR Analytics Dashboard - Key SQL Queries
-- ============================================

-- 1. Workforce Overview
-- 1.1 Total Employee Count
SELECT COUNT(*) AS total_employees FROM employees WHERE employment_status = 'Active';

-- 1.2 Active vs Terminated
SELECT employment_status, COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM employees GROUP BY employment_status;

-- 1.3 Attrition Rate
SELECT 
  COUNT(CASE WHEN attrition = 'Yes' THEN 1 END) * 100.0 / COUNT(*) AS attrition_rate,
  COUNT(CASE WHEN attrition = 'Yes' THEN 1 END) AS attrited_count,
  COUNT(*) AS total_employees
FROM employees;

-- 2. Department Analysis
-- 2.1 Headcount by Department
SELECT department, COUNT(*) AS headcount,
       ROUND(AVG(salary), 2) AS avg_salary,
       ROUND(AVG(age), 1) AS avg_age,
       ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM employees WHERE employment_status = 'Active'
GROUP BY department ORDER BY headcount DESC;

-- 2.2 Attrition by Department
SELECT department,
       COUNT(*) AS total,
       SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
       ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100, 2) AS attrition_pct
FROM employees GROUP BY department ORDER BY attrition_pct DESC;

-- 3. Demographics
-- 3.1 Gender Distribution
SELECT gender, COUNT(*) AS count,
       ROUND(AVG(salary), 2) AS avg_salary,
       ROUND(AVG(performance_rating), 2) AS avg_performance
FROM employees WHERE employment_status = 'Active'
GROUP BY gender;

-- 3.2 Age Band Analysis
SELECT
  CASE
    WHEN age < 25 THEN '<25'
    WHEN age BETWEEN 25 AND 34 THEN '25-34'
    WHEN age BETWEEN 35 AND 44 THEN '35-44'
    WHEN age BETWEEN 45 AND 54 THEN '45-54'
    ELSE '55+'
  END AS age_band,
  COUNT(*) AS count,
  ROUND(AVG(salary), 2) AS avg_salary
FROM employees WHERE employment_status = 'Active'
GROUP BY age_band ORDER BY age_band;

-- 3.3 Education Field Breakdown
SELECT education_field, COUNT(*) AS count,
       ROUND(AVG(salary), 2) AS avg_salary,
       SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited
FROM employees GROUP BY education_field ORDER BY count DESC;

-- 4. Salary Analysis
-- 4.1 Salary Range by Department
SELECT department,
       MIN(salary) AS min_salary,
       ROUND(AVG(salary), 2) AS avg_salary,
       MAX(salary) AS max_salary,
       ROUND(STDDEV(salary), 2) AS salary_stddev
FROM employees WHERE employment_status = 'Active'
GROUP BY department;

-- 4.2 Salary Hike vs Performance
SELECT performance_rating,
       ROUND(AVG(salary_hike_percent), 2) AS avg_hike_pct,
       COUNT(*) AS employee_count
FROM employees GROUP BY performance_rating ORDER BY performance_rating;

-- 5. Performance Analysis
-- 5.1 Performance Rating Distribution
SELECT performance_rating, COUNT(*) AS count
FROM employees GROUP BY performance_rating ORDER BY performance_rating;

-- 5.2 Department Performance Averages
SELECT department,
       ROUND(AVG(performance_rating), 2) AS avg_rating,
       ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
       ROUND(AVG(work_life_balance), 2) AS avg_wlb
FROM employees WHERE employment_status = 'Active'
GROUP BY department ORDER BY avg_rating DESC;

-- 6. Tenure Analysis
-- 6.1 Tenure Distribution
SELECT years_at_company,
       COUNT(*) AS employee_count,
       SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited
FROM employees GROUP BY years_at_company ORDER BY years_at_company;

-- 6.2 Promotion Gap
SELECT years_since_last_promotion,
       COUNT(*) AS employee_count
FROM employees WHERE employment_status = 'Active'
GROUP BY years_since_last_promotion ORDER BY years_since_last_promotion;

-- 7. Attendance Analysis
-- 7.1 Overall Attendance Rate
SELECT
  COUNT(*) AS total_days,
  SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_days,
  SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent_days,
  ROUND(SUM(CASE WHEN status = 'Present' THEN 1.0 ELSE 0 END) * 100 / COUNT(*), 2) AS attendance_rate
FROM attendance;

-- 7.2 Attendance by Department (via employee join)
SELECT e.department,
       ROUND(SUM(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0 END) * 100 / COUNT(*), 2) AS attendance_rate,
       ROUND(AVG(a.hours_worked), 2) AS avg_hours
FROM attendance a
JOIN employees e ON a.employee_id = e.employee_id
GROUP BY e.department ORDER BY attendance_rate DESC;

-- 7.3 Work From Home Trends
SELECT
  FORMAT(date, 'yyyy-MM') AS month,
  COUNT(CASE WHEN status = 'WFH' THEN 1 END) AS wfh_count,
  COUNT(CASE WHEN status = 'Present' THEN 1 END) AS present_count
FROM attendance
GROUP BY FORMAT(date, 'yyyy-MM')
ORDER BY month;

-- 8. Recruitment Metrics
-- 8.1 Time to Hire
SELECT department,
       ROUND(AVG(days_to_offer), 1) AS avg_days_to_offer,
       ROUND(AVG(interview_score), 2) AS avg_interview_score,
       COUNT(*) AS candidates
FROM recruitment
GROUP BY department ORDER BY avg_days_to_offer;

-- 8.2 Source Effectiveness
SELECT source,
       COUNT(*) AS total_applications,
       SUM(CASE WHEN offer_accepted = 1 THEN 1 ELSE 0 END) AS accepted,
       ROUND(AVG(interview_score), 2) AS avg_score,
       ROUND(SUM(CASE WHEN offer_accepted = 1 THEN 1.0 ELSE 0 END) * 100 / COUNT(*), 2) AS conversion_rate
FROM recruitment
GROUP BY source ORDER BY conversion_rate DESC;

-- 9. Training Impact
-- 9.1 Training Completion
SELECT training_category,
       COUNT(*) AS total,
       SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) AS completed,
       ROUND(AVG(post_training_score - pre_training_score), 2) AS avg_improvement
FROM training GROUP BY training_category;

-- 10. Composite Insights (Window Functions)
-- 10.1 Employees with Highest Tenure per Department
SELECT department, employee_id, first_name, last_name, years_at_company
FROM (
  SELECT *,
         DENSE_RANK() OVER (PARTITION BY department ORDER BY years_at_company DESC) AS rnk
  FROM employees WHERE employment_status = 'Active'
) ranked WHERE rnk <= 5;

-- 10.2 Salary Percentiles by Department
SELECT department,
       ROUND(AVG(salary), 2) AS avg_salary,
       ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY department), 2) AS p25_salary,
       ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY department), 2) AS median_salary,
       ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY department), 2) AS p75_salary
FROM employees WHERE employment_status = 'Active'
QUALIFY ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) = 1;
