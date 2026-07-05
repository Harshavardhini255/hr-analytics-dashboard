import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, date, timedelta
import random
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

departments = ['Sales', 'Research & Development', 'Human Resources', 'Finance', 'IT', 'Marketing', 'Operations']
job_roles = {
    'Sales': ['Sales Executive', 'Sales Representative', 'Sales Manager', 'Account Executive'],
    'Research & Development': ['Scientist', 'Research Director', 'Lab Technician', 'R&D Manager'],
    'Human Resources': ['HR Executive', 'HR Manager', 'Recruiter', 'HR Coordinator'],
    'Finance': ['Accountant', 'Financial Analyst', 'Finance Manager', 'Auditor'],
    'IT': ['Software Engineer', 'System Analyst', 'IT Manager', 'Network Administrator'],
    'Marketing': ['Marketing Associate', 'Marketing Manager', 'Content Writer', 'SEO Specialist'],
    'Operations': ['Operations Analyst', 'Operations Manager', 'Supply Chain Coordinator', 'Logistics Executive']
}
education_fields = ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other']
education_levels = ["Bachelor's", "Master's", "PhD", 'High School']
business_travel_options = ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']
marital_statuses = ['Single', 'Married', 'Divorced']

def generate_employees(n=500):
    records = []
    for emp_id in range(1, n + 1):
        department = random.choice(departments)
        role = random.choice(job_roles[department])
        hire_date = fake.date_between(start_date='-10y', end_date='-1y')
        termination = None
        status = 'Active'
        attrition = 'No'
        if random.random() < 0.16:
            termination = fake.date_between(start_date=hire_date, end_date='today')
            status = 'Terminated'
            attrition = 'Yes'

        if isinstance(hire_date, str):
            hire_dt = datetime.strptime(hire_date, '%Y-%m-%d').date()
        elif isinstance(hire_date, date):
            hire_dt = hire_date
        else:
            hire_dt = hire_date.date()
        years_at_company = (date.today() - hire_dt).days / 365

        gender = random.choice(['Male', 'Female'])
        age = random.randint(22, 62)
        salary = round(np.random.normal(60000 + (age * 800), 15000), 2)
        salary = max(25000, min(200000, salary))

        records.append({
            'employee_id': emp_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': f'employee{emp_id}@company.com',
            'gender': gender,
            'age': age,
            'marital_status': random.choice(marital_statuses),
            'department': department,
            'job_role': role,
            'education_field': random.choice(education_fields),
            'education_level': random.choice(education_levels),
            'business_travel': random.choice(business_travel_options),
            'distance_from_home': random.randint(1, 50),
            'hire_date': hire_date,
            'termination_date': termination,
            'employment_status': status,
            'salary': salary,
            'salary_hike_percent': round(random.uniform(2, 25), 2),
            'performance_rating': random.choices([1, 2, 3, 4, 5], weights=[5, 15, 40, 30, 10])[0],
            'previous_employers': random.randint(0, 7),
            'years_at_company': round(years_at_company, 1),
            'years_in_current_role': random.randint(0, 8),
            'years_since_last_promotion': random.randint(0, 6),
            'years_with_current_manager': random.randint(0, 8),
            'stock_option_level': random.randint(0, 3),
            'overtime': random.choice(['Yes', 'No']),
            'training_times_last_year': random.randint(0, 6),
            'work_life_balance': random.randint(1, 4),
            'job_satisfaction': random.randint(1, 4),
            'environment_satisfaction': random.randint(1, 4),
            'relationship_satisfaction': random.randint(1, 4),
            'job_involvement': random.randint(1, 4),
            'attrition': attrition
        })
    return pd.DataFrame(records)

def generate_attendance(employees_df, days=365):
    records = []
    all_dates = pd.date_range(end=datetime.now().date(), periods=days).tolist()
    active_employees = employees_df[employees_df['employment_status'] == 'Active']
    for _, emp in active_employees.iterrows():
        for date in all_dates:
            if pd.Timestamp(emp['hire_date']) > date:
                continue
            if emp['termination_date'] and pd.Timestamp(emp['termination_date']) < date:
                continue
            rand = random.random()
            if date.weekday() >= 5:
                status = np.random.choice(['Present', 'Absent'], p=[0.1, 0.9])
                if status == 'Present':
                    check_in = f'{random.randint(8,10):02d}:{random.randint(0,59):02d}:00'
                    check_out = f'{random.randint(15,18):02d}:{random.randint(0,59):02d}:00'
                else:
                    check_in, check_out = None, None
            else:
                if rand < 0.75:
                    status = 'Present'
                elif rand < 0.85:
                    status = 'WFH'
                elif rand < 0.97:
                    status = 'Absent'
                else:
                    status = 'Leave'
                if status == 'Present' or status == 'WFH':
                    check_in = f'{random.randint(7,10):02d}:{random.randint(0,59):02d}:00'
                    check_out = f'{random.randint(16,19):02d}:{random.randint(0,59):02d}:00'
                else:
                    check_in, check_out = None, None

            hours = 0
            if check_in and check_out:
                hi = int(check_in.split(':')[0]) + int(check_in.split(':')[1]) / 60
                ho = int(check_out.split(':')[0]) + int(check_out.split(':')[1]) / 60
                hours = round(max(0, ho - hi - 1), 2)

            records.append({
                'employee_id': emp['employee_id'],
                'date': date.date(),
                'day_of_week': date.strftime('%A'),
                'status': status,
                'check_in': check_in,
                'check_out': check_out,
                'hours_worked': hours,
                'is_weekend': date.weekday() >= 5,
                'is_holiday': False
            })
    return pd.DataFrame(records)

def generate_performance_reviews(employees_df):
    records = []
    periods = ['H1-2023', 'H2-2023', 'H1-2024', 'H2-2024', 'H1-2025']
    for _, emp in employees_df.iterrows():
        for period in periods:
            if emp['termination_date'] and pd.Timestamp(emp['termination_date']) < pd.Timestamp(f"20{period[-2:]}-{'06-30' if period[:2]=='H1' else '12-31'}"):
                continue
            base_rating = emp['performance_rating']
            self_r = max(1, min(5, base_rating + random.randint(-1, 1)))
            mgr_r = max(1, min(5, base_rating + random.randint(-1, 1)))
            overall = round((self_r + mgr_r) / 2)
            records.append({
                'employee_id': emp['employee_id'],
                'review_date': f"20{period[-2:]}-{'06-15' if period[:2]=='H1' else '12-15'}",
                'review_period': period,
                'self_rating': self_r,
                'manager_rating': mgr_r,
                'overall_rating': overall,
                'goals_achieved': random.randint(2, 5),
                'goals_target': 5,
                'feedback_summary': fake.sentence()
            })
    return pd.DataFrame(records)

def generate_training(employees_df):
    records = []
    trainings = [
        ('Leadership Workshop', 'Leadership'),
        ('Technical Skills', 'Technical'),
        ('Communication Skills', 'Soft Skills'),
        ('Project Management', 'Management'),
        ('Data Analysis', 'Technical'),
        ('Diversity & Inclusion', 'Soft Skills'),
        ('Safety Training', 'Compliance'),
        ('Sales Techniques', 'Functional'),
    ]
    for _, emp in employees_df.iterrows():
        n_trainings = random.randint(0, 4)
        chosen = random.sample(trainings, min(n_trainings, len(trainings)))
        for name, cat in chosen:
            start = fake.date_between(start_date='-1y', end_date='today')
            end = start + timedelta(days=random.randint(1, 5))
            pre = random.uniform(30, 70)
            post = pre + random.uniform(5, 35)
            records.append({
                'employee_id': emp['employee_id'],
                'training_name': name,
                'training_category': cat,
                'start_date': start,
                'end_date': end,
                'duration_days': (end - start).days,
                'cost': round(random.uniform(200, 2000), 2),
                'completion_status': random.choice(['Completed', 'Completed', 'Completed', 'In Progress', 'Dropped']),
                'pre_training_score': round(pre, 2),
                'post_training_score': round(min(100, post), 2)
            })
    return pd.DataFrame(records)

def generate_recruitment():
    records = []
    sources = ['LinkedIn', 'Indeed', 'Referral', 'Company Website', 'Campus Recruitment', 'Job Fair']
    for i in range(1, 201):
        dept = random.choice(departments)
        position = random.choice(job_roles[dept])
        app_date = fake.date_between(start_date='-6m', end_date='today')
        status = random.choice(['Selected', 'Rejected', 'On Hold', 'In Process'])
        accepted = status == 'Selected' and random.random() < 0.7
        joining = fake.date_between(start_date=app_date + timedelta(days=15),
                                     end_date=app_date + timedelta(days=60)) if accepted else None
        records.append({
            'candidate_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'applied_position': position,
            'application_date': app_date,
            'status': status,
            'source': random.choice(sources),
            'interview_score': round(random.uniform(40, 100), 2),
            'offer_amount': round(random.uniform(35000, 120000), 2) if status == 'Selected' else None,
            'joining_date': joining,
            'offer_accepted': accepted,
            'days_to_offer': random.randint(7, 45),
            'department': dept
        })
    return pd.DataFrame(records)

def generate_department_budget():
    records = []
    for dept in departments:
        for year in [2023, 2024, 2025]:
            base = random.randint(500000, 3000000)
            records.append({
                'department': dept,
                'fiscal_year': year,
                'total_budget': base,
                'salary_budget': round(base * 0.6),
                'training_budget': round(base * 0.05),
                'recruitment_budget': round(base * 0.03),
                'actual_spend': round(base * random.uniform(0.85, 1.05)),
                'budget_variance': 0
            })
    df = pd.DataFrame(records)
    df['budget_variance'] = df['total_budget'] - df['actual_spend']
    return df

def create_excel_report(employees, attendance, performance, training, recruitment, budgets):
    filepath = os.path.join(OUTPUT_DIR, 'hr_analytics.xlsx')
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        employees.to_excel(writer, sheet_name='Employees', index=False)
        attendance.head(5000).to_excel(writer, sheet_name='Attendance_Sample', index=False)
        performance.to_excel(writer, sheet_name='Performance_Reviews', index=False)
        training.to_excel(writer, sheet_name='Training', index=False)
        recruitment.to_excel(writer, sheet_name='Recruitment', index=False)
        budgets.to_excel(writer, sheet_name='Department_Budget', index=False)

        dept_summary = employees.groupby('department').agg(
            Employee_Count=('employee_id', 'count'),
            Avg_Salary=('salary', 'mean'),
            Avg_Performance=('performance_rating', 'mean'),
            Avg_Tenure=('years_at_company', 'mean'),
            Attrition_Count=('attrition', lambda x: (x == 'Yes').sum())
        ).round(2)
        dept_summary.to_excel(writer, sheet_name='Dept_Summary')

        demo_summary = employees.groupby(['department', 'gender']).agg(
            Count=('employee_id', 'count'),
            Avg_Salary=('salary', 'mean')
        ).round(2)
        demo_summary.to_excel(writer, sheet_name='Gender_Dept_Analysis')

        rating_dist = employees.groupby(['department', 'performance_rating']).size().unstack(fill_value=0)
        rating_dist.to_excel(writer, sheet_name='Performance_Distribution')

    print(f"Excel report saved: {filepath}")
    return filepath

def main():
    print("Generating HR Analytics Data...")
    employees = generate_employees(500)
    print(f"Employees: {len(employees)}")

    attendance = generate_attendance(employees, 180)
    print(f"Attendance: {len(attendance)}")

    performance = generate_performance_reviews(employees)
    print(f"Reviews: {len(performance)}")

    training = generate_training(employees)
    print(f"Training: {len(training)}")

    recruitment = generate_recruitment()
    print(f"Recruitment: {len(recruitment)}")

    budgets = generate_department_budget()
    print(f"Budget: {len(budgets)}")

    employees.to_csv(os.path.join(OUTPUT_DIR, 'employees.csv'), index=False)
    attendance.to_csv(os.path.join(OUTPUT_DIR, 'attendance.csv'), index=False)
    performance.to_csv(os.path.join(OUTPUT_DIR, 'performance_reviews.csv'), index=False)
    training.to_csv(os.path.join(OUTPUT_DIR, 'training.csv'), index=False)
    recruitment.to_csv(os.path.join(OUTPUT_DIR, 'recruitment.csv'), index=False)
    budgets.to_csv(os.path.join(OUTPUT_DIR, 'department_budget.csv'), index=False)
    print("CSV files saved in data/")

    create_excel_report(employees, attendance, performance, training, recruitment, budgets)
    print("Done! All files generated.")

if __name__ == '__main__':
    main()
