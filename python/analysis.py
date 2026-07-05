import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_cleaned():
    path = os.path.join(DATA_DIR, 'cleaned')
    employees = pd.read_csv(os.path.join(path, 'employees_clean.csv'))
    attendance = pd.read_csv(os.path.join(path, 'attendance_clean.csv'))
    performance = pd.read_csv(os.path.join(path, 'performance_clean.csv'))
    training = pd.read_csv(os.path.join(path, 'training_clean.csv'))
    return employees, attendance, performance, training

def analyze_workforce(emp):
    print("=" * 50)
    print("WORKFORCE OVERVIEW")
    print("=" * 50)
    total = len(emp)
    active = (emp['employment_status'] == 'Active').sum()
    attrited = (emp['attrition'] == 'Yes').sum()
    print(f"Total Employees: {total}")
    print(f"Active: {active} ({active/total*100:.1f}%)")
    print(f"Attrited: {attrited} ({attrited/total*100:.1f}%)")
    print(f"Attrition Rate: {attrited/total*100:.1f}%")
    print(f"Avg Salary: ${emp['salary'].mean():.2f}")
    print(f"Avg Age: {emp['age'].mean():.1f}")
    print(f"Avg Tenure: {emp['years_at_company'].mean():.1f} yrs")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    dept_count = emp['department'].value_counts()
    axes[0, 0].barh(dept_count.index, dept_count.values, color='steelblue')
    axes[0, 0].set_title('Headcount by Department')
    axes[0, 0].set_xlabel('Count')

    attrition_dept = emp.groupby('department')['attrition'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values()
    axes[0, 1].barh(attrition_dept.index, attrition_dept.values, color='coral')
    axes[0, 1].set_title('Attrition Rate by Department (%)')
    axes[0, 1].set_xlabel('Attrition %')

    gender_count = emp['gender'].value_counts()
    axes[1, 0].pie(gender_count.values, labels=gender_count.index, autopct='%1.1f%%', colors=['lightblue', 'pink'])
    axes[1, 0].set_title('Gender Distribution')

    age_bands = emp.groupby('age_band', observed=False).size()
    axes[1, 1].bar(age_bands.index.astype(str), age_bands.values, color='seagreen')
    axes[1, 1].set_title('Age Distribution')
    axes[1, 1].set_xlabel('Age Band')
    axes[1, 1].set_ylabel('Count')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'workforce_overview.png'), dpi=150)
    plt.close()
    print(f"Saved: workforce_overview.png")

def analyze_salary(emp):
    print("\n" + "=" * 50)
    print("SALARY ANALYSIS")
    print("=" * 50)
    dept_salary = emp.groupby('department')['salary'].agg(['mean', 'min', 'max', 'std']).round(2)
    print(dept_salary)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.boxplot(data=emp, x='department', y='salary', ax=axes[0])
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title('Salary Distribution by Department')

    dept_avg = emp.groupby('department')['salary'].mean().sort_values()
    axes[1].barh(dept_avg.index, dept_avg.values, color='teal')
    axes[1].set_title('Average Salary by Department')
    axes[1].set_xlabel('Avg Salary ($)')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'salary_analysis.png'), dpi=150)
    plt.close()
    print(f"Saved: salary_analysis.png")

def analyze_attrition(emp):
    print("\n" + "=" * 50)
    print("ATTRITION ANALYSIS")
    print("=" * 50)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for ax, col, title in zip(
        axes.flatten(),
        ['overtime', 'business_travel', 'marital_status', 'education_field', 'job_satisfaction', 'work_life_balance'],
        ['By Overtime', 'By Business Travel', 'By Marital Status', 'By Education Field', 'By Job Satisfaction', 'By Work-Life Balance']
    ):
        ctab = pd.crosstab(emp[col], emp['attrition'], normalize='index') * 100
        ctab[['Yes']].plot(kind='bar', ax=ax, legend=False, color='salmon')
        ax.set_title(f'Attrition {title}')
        ax.set_ylabel('Attrition %')
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'attrition_factors.png'), dpi=150)
    plt.close()
    print(f"Saved: attrition_factors.png")

    key_factors = emp.groupby('department').agg(
        Attrition_Rate=('attrition', lambda x: (x == 'Yes').mean() * 100),
        Avg_Salary=('salary', 'mean'),
        Avg_Satisfaction=('job_satisfaction', 'mean'),
        Avg_Tenure=('years_at_company', 'mean')
    ).round(2)
    print("\nAttrition Factors by Department:")
    print(key_factors)

def analyze_performance(emp, perf):
    print("\n" + "=" * 50)
    print("PERFORMANCE ANALYSIS")
    print("=" * 50)
    print(emp.groupby('performance_rating').size().to_frame('Count'))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    perf_dept = emp.groupby('department')['performance_rating'].mean().sort_values()
    axes[0].barh(perf_dept.index, perf_dept.values, color='mediumpurple')
    axes[0].set_title('Avg Performance Rating by Department')
    axes[0].set_xlabel('Avg Rating')
    axes[0].set_xlim(0, 5)

    salary_vs_perf = emp.groupby('performance_rating')['salary'].mean()
    axes[1].plot(salary_vs_perf.index, salary_vs_perf.values, marker='o', color='darkorange', linewidth=2)
    axes[1].set_title('Avg Salary vs Performance Rating')
    axes[1].set_xlabel('Performance Rating')
    axes[1].set_ylabel('Avg Salary ($)')
    axes[1].set_xticks(range(1, 6))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'performance_analysis.png'), dpi=150)
    plt.close()
    print(f"Saved: performance_analysis.png")

def analyze_attendance(att):
    print("\n" + "=" * 50)
    print("ATTENDANCE ANALYSIS")
    print("=" * 50)
    status_counts = att['status'].value_counts()
    print(status_counts)
    print(f"Attendance Rate: {status_counts.get('Present', 0)/len(att)*100:.1f}%")
    print(f"Avg Hours Worked: {att['hours_worked'].mean():.2f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    att['date'] = pd.to_datetime(att['date'])
    att['month'] = att['date'].dt.month
    monthly = att.groupby('month')['status'].apply(lambda x: (x == 'Present').mean() * 100)
    axes[0].plot(monthly.index, monthly.values, marker='s', color='forestgreen')
    axes[0].set_title('Monthly Attendance Rate')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Attendance %')
    axes[0].set_xticks(range(1, 13))

    daily_hours = att.groupby('day_of_week')['hours_worked'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    axes[1].bar(daily_hours.index, daily_hours.values, color='cornflowerblue')
    axes[1].set_title('Avg Hours Worked by Day')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'attendance_analysis.png'), dpi=150)
    plt.close()
    print(f"Saved: attendance_analysis.png")

def main():
    employees, attendance, performance, training = load_cleaned()

    analyze_workforce(employees)
    analyze_salary(employees)
    analyze_attrition(employees)
    analyze_performance(employees, performance)
    analyze_attendance(attendance)

    print("\n" + "=" * 50)
    print("KEY INSIGHTS")
    print("=" * 50)
    print(f"1. Overall attrition rate: {(employees['attrition'] == 'Yes').mean()*100:.1f}%")
    print(f"2. Department with highest attrition: {employees.groupby('department')['attrition'].apply(lambda x: (x=='Yes').mean()).idxmax()}")
    print(f"3. Department with highest salary: {employees.groupby('department')['salary'].mean().idxmax()}")
    print(f"4. Most common performance rating: {employees['performance_rating'].mode()[0]}")
    print(f"5. Average work-life balance score: {employees['work_life_balance'].mean():.2f}/4")
    print(f"6. Overtime employees attrition: {employees[employees['overtime']=='Yes']['attrition'].value_counts(normalize=True).get('Yes', 0)*100:.1f}%")
    print(f"\nCharts saved to: {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
