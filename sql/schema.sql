-- HR Analytics Dashboard - Database Schema
-- Database: hr_analytics

CREATE DATABASE IF NOT EXISTS hr_analytics;
USE hr_analytics;

-- 1. Employees Table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    marital_status VARCHAR(20),
    department VARCHAR(50),
    job_role VARCHAR(50),
    education_field VARCHAR(50),
    education_level VARCHAR(30),
    business_travel VARCHAR(30),
    distance_from_home INT,
    hire_date DATE,
    termination_date DATE NULL,
    employment_status VARCHAR(20) DEFAULT 'Active',
    salary DECIMAL(10,2),
    salary_hike_percent DECIMAL(5,2),
    performance_rating INT,
    previous_employers INT,
    years_at_company INT,
    years_in_current_role INT,
    years_since_last_promotion INT,
    years_with_current_manager INT,
    stock_option_level INT,
    overtime VARCHAR(5),
    training_times_last_year INT,
    work_life_balance INT,
    job_satisfaction INT,
    environment_satisfaction INT,
    relationship_satisfaction INT,
    job_involvement INT,
    attrition VARCHAR(5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Attendance Table
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    date DATE,
    day_of_week VARCHAR(15),
    status VARCHAR(20),
    check_in TIME,
    check_out TIME,
    hours_worked DECIMAL(4,2),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- 3. Performance Reviews
CREATE TABLE performance_reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    review_date DATE,
    review_period VARCHAR(20),
    self_rating INT,
    manager_rating INT,
    overall_rating INT,
    goals_achieved INT,
    goals_target INT,
    feedback_summary TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- 4. Training & Development
CREATE TABLE training (
    training_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    training_name VARCHAR(100),
    training_category VARCHAR(50),
    start_date DATE,
    end_date DATE,
    duration_days INT,
    cost DECIMAL(10,2),
    completion_status VARCHAR(20),
    pre_training_score DECIMAL(5,2),
    post_training_score DECIMAL(5,2),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- 5. Recruitment
CREATE TABLE recruitment (
    candidate_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    applied_position VARCHAR(50),
    application_date DATE,
    status VARCHAR(30),
    source VARCHAR(50),
    interview_score DECIMAL(5,2),
    offer_amount DECIMAL(10,2),
    joining_date DATE NULL,
    offer_accepted BOOLEAN,
    days_to_offer INT,
    department VARCHAR(50)
);

-- 6. Department Budget
CREATE TABLE department_budget (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    department VARCHAR(50),
    fiscal_year INT,
    total_budget DECIMAL(15,2),
    salary_budget DECIMAL(15,2),
    training_budget DECIMAL(15,2),
    recruitment_budget DECIMAL(15,2),
    actual_spend DECIMAL(15,2),
    budget_variance DECIMAL(15,2)
);
