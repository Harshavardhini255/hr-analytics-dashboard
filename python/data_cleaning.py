import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_data():
    employees = pd.read_csv(os.path.join(DATA_DIR, 'employees.csv'))
    attendance = pd.read_csv(os.path.join(DATA_DIR, 'attendance.csv'))
    performance = pd.read_csv(os.path.join(DATA_DIR, 'performance_reviews.csv'))
    training = pd.read_csv(os.path.join(DATA_DIR, 'training.csv'))
    return employees, attendance, performance, training

def clean_employees(df):
    print("=== Cleaning Employees ===")
    print(f"Shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicates: {df.duplicated().sum()}")

    df = df.copy()
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    valid_ages = (df['age'] >= 18) & (df['age'] <= 70)
    df = df[valid_ages]

    valid_salaries = (df['salary'] >= 20000) & (df['salary'] <= 300000)
    df = df[valid_salaries]

    df['years_at_company'] = df['years_at_company'].clip(0, 50)
    df['performance_rating'] = df['performance_rating'].clip(1, 5)
    df['job_satisfaction'] = df['job_satisfaction'].clip(1, 4)
    df['work_life_balance'] = df['work_life_balance'].clip(1, 4)

    df['salary_band'] = pd.cut(df['salary'],
        bins=[0, 40000, 60000, 80000, 100000, 300000],
        labels=['<40K', '40-60K', '60-80K', '80-100K', '100K+'])

    df['age_band'] = pd.cut(df['age'],
        bins=[0, 25, 35, 45, 55, 100],
        labels=['<25', '25-34', '35-44', '45-54', '55+'])

    print(f"After cleaning: {df.shape}")
    return df

def clean_attendance(df):
    print("\n=== Cleaning Attendance ===")
    print(f"Shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.day_name()
    df = df[df['hours_worked'] >= 0]
    df = df[df['hours_worked'] <= 16]
    return df

def clean_performance(df):
    print("\n=== Cleaning Performance ===")
    df = df.copy()
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
    df = df.dropna(subset=['review_date'])
    for col in ['self_rating', 'manager_rating', 'overall_rating']:
        df[col] = df[col].clip(1, 5)
    df['goals_met_pct'] = (df['goals_achieved'] / df['goals_target'].replace(0, 1)) * 100
    return df

def clean_training(df):
    print("\n=== Cleaning Training ===")
    df = df.copy()
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    df = df.dropna(subset=['start_date', 'end_date'])
    df['score_improvement'] = df['post_training_score'] - df['pre_training_score']
    return df

def main():
    employees, attendance, performance, training = load_data()

    employees = clean_employees(employees)
    attendance = clean_attendance(attendance)
    performance = clean_performance(performance)
    training = clean_training(training)

    out = os.path.join(DATA_DIR, 'cleaned')
    os.makedirs(out, exist_ok=True)
    employees.to_csv(os.path.join(out, 'employees_clean.csv'), index=False)
    attendance.to_csv(os.path.join(out, 'attendance_clean.csv'), index=False)
    performance.to_csv(os.path.join(out, 'performance_clean.csv'), index=False)
    training.to_csv(os.path.join(out, 'training_clean.csv'), index=False)
    print(f"\nCleaned data saved to {out}/")

if __name__ == '__main__':
    main()
