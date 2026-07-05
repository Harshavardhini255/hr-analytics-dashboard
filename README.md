# HR Analytics Dashboard

A comprehensive HR analytics solution using **SQL**, **Python**, **Excel**, and **Power BI** to analyze workforce data and provide actionable insights.

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

## Key Metrics Tracked

| Category | Metrics |
|----------|---------|
| **Workforce** | Headcount, Active vs Terminated, Tenure |
| **Attrition** | Rate, by Dept, by Demographics, by Factors |
| **Compensation** | Avg Salary, Salary Bands, Hike % |
| **Performance** | Ratings, Goals Achievement, Trends |
| **Diversity** | Gender Ratio, Age Distribution, Education |
| **Attendance** | Rate, WFH Trends, Hours Worked |
| **Recruitment** | Time-to-Hire, Source Effectiveness |

## Key Insights Generated

- Attrition rate and patterns by department/demographics
- Salary distribution and band analysis
- Performance rating trends across departments
- Attendance patterns and absenteeism
- Recruitment source effectiveness and time-to-hire
- Training impact on performance
- Gender diversity and pay equity
