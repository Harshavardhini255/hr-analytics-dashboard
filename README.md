# HR Analytics Dashboard

**People Analytics | Workforce Analytics | HR Data Visualization | Business Intelligence Dashboard**

A comprehensive **HR Analytics** and **People Analytics** solution using **SQL**, **Python**, **Excel**, **Streamlit**, and **Power BI** to analyze workforce data, track HR KPIs, and provide actionable insights for data-driven HR decision-making.

## Features

- **Attrition & Retention Analytics** — Analyze employee turnover rates by department, demographics, tenure, and key drivers. Identify retention risks and support talent management strategies.
- **Compensation & Benefits Analysis** — Salary distribution modeling, pay equity analysis, salary band benchmarking, and hike percentage tracking.
- **Performance Management** — Employee performance ratings, goal achievement tracking, and trends across teams and departments.
- **Diversity & Inclusion Analytics** — Gender ratio, age distribution, educational background, and pay equity assessments.
- **Attendance & Workforce Planning** — Attendance rate tracking, work-from-home trends, absenteeism patterns, and hours worked analysis.
- **Recruitment & Talent Acquisition** — Time-to-hire analysis, recruitment source effectiveness, and hiring funnel metrics.
- **Data Pipeline & ETL** — Automated data generation, data cleaning, data transformation, and standardization using Python.
- **Interactive Dashboards** — Built with Power BI and Streamlit for self-service business intelligence and data storytelling.

## Tech Stack & Skills

| Category | Technologies & Tools |
|----------|---------------------|
| **Languages** | Python, SQL |
| **Data Processing & ETL** | Pandas, NumPy, Data Cleaning, Data Transformation |
| **Visualization** | Power BI, Streamlit, Plotly, Matplotlib, Seaborn |
| **Databases** | SQL Server, MySQL, PostgreSQL |
| **Machine Learning** | scikit-learn (Predictive Analytics, Statistical Modeling) |
| **Excel** | Pivot Tables, Charts, VBA, Data Analysis |
| **Libraries** | openpyxl, Faker, SQLAlchemy, pyodbc |
| **Data Sources** | CSV, Excel, SQL Databases |

## Key Metrics & HR KPIs Tracked

| Category | Metrics |
|----------|---------|
| **Workforce** | Headcount, Active vs Terminated, Tenure Distribution |
| **Attrition** | Attrition Rate, by Department, by Demographics, by Factors |
| **Compensation** | Average Salary, Salary Bands, Hike %, Pay Equity |
| **Performance** | Ratings, Goals Achievement, Performance Trends |
| **Diversity** | Gender Ratio, Age Distribution, Education Levels |
| **Attendance** | Attendance Rate, WFH Trends, Hours Worked, Absenteeism |
| **Recruitment** | Time-to-Hire, Source Effectiveness, Cost-per-Hire |
| **Training** | Training Impact on Performance, Completion Rates |

## Project Structure

```
hr-analytics-dashboard/
├── data/              # CSV and Excel data files
│   ├── employees.csv
│   ├── attendance.csv
│   ├── performance_reviews.csv
│   ├── training.csv
│   ├── recruitment.csv
│   ├── department_budget.csv
│   └── hr_analytics.xlsx
├── sql/               # Database schema and queries
│   ├── schema.sql
│   ├── queries.sql
│   └── views.sql
├── python/            # Data generation and analysis scripts
│   ├── generate_data.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── requirements.txt
├── powerbi/           # Power BI setup guide
│   └── HR_DASHBOARD_GUIDE.md
├── output/            # Generated charts
└── README.md
```

## Quick Start

### 1. Generate Data
```bash
cd python
pip install -r requirements.txt
python generate_data.py
```
This creates CSV files and an Excel workbook in `data/`.

### 2. Clean & Analyze
```bash
python data_cleaning.py   # Cleans and standardizes data
python analysis.py        # Generates insights and charts
```

### 3. Load into SQL
```bash
# Using SQL Server / MySQL / PostgreSQL
# Run: sql/schema.sql to create tables
# Run: sql/queries.sql for analytical queries
# Run: sql/views.sql for reusable views
```

### 4. Open in Power BI
- Open `Power BI Desktop`
- Load CSVs from `data/`
- Follow `powerbi/HR_DASHBOARD_GUIDE.md`

### 5. Explore in Excel
- Open `data/hr_analytics.xlsx`
- Use pivot tables and charts in the sheets

### 6. Launch Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

## Key Insights Generated

- Attrition rate analysis and patterns by department, demographics, and contributing factors
- Salary distribution, compensation benchmarking, and pay equity analysis
- Performance rating trends across departments with training impact assessment
- Attendance patterns, WFH trends, and absenteeism analysis
- Recruitment source effectiveness, time-to-hire, and hiring funnel optimization
- Training ROI and impact on employee performance
- Gender diversity metrics and inclusion analytics
- Workforce planning and headcount forecasting insights

## Use Cases

- **HR Business Partners** — Workforce planning and attrition risk identification
- **Talent Acquisition** — Recruitment metrics and source optimization
- **Compensation & Benefits** — Salary benchmarking and equity analysis
- **Diversity & Inclusion** — Demographic analysis and inclusion tracking
- **HR Leadership** — Strategic workforce analytics and data storytelling
