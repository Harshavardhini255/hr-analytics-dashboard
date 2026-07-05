# HR Analytics Dashboard - Power BI Setup Guide

## Step 1: Load Data into Power BI

1. Open **Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Navigate to `hr-analytics-dashboard/data/`
4. Load these files:
   - `employees.csv`
   - `attendance.csv`
   - `performance_reviews.csv`
   - `training.csv`
   - `recruitment.csv`
   - `department_budget.csv`
5. Click **Transform Data** to open Power Query Editor

## Step 2: Create Data Model (Relationships)

In **Model View**, create these relationships:

| From (FK) | To (PK) |
|-----------|---------|
| attendance[employee_id] | employees[employee_id] |
| performance_reviews[employee_id] | employees[employee_id] |
| training[employee_id] | employees[employee_id] |

## Step 3: Create DAX Measures

Create a **Measures Table** and add these measures:

### Workforce KPIs
```dax
Total Employees = COUNTROWS(employees)
Active Employees = CALCULATE(COUNTROWS(employees), employees[employment_status] = "Active")
Attrition Count = CALCULATE(COUNTROWS(employees), employees[attrition] = "Yes")
Attrition Rate = DIVIDE([Attrition Count], [Total Employees], 0) * 100
Avg Salary = AVERAGE(employees[salary])
Avg Tenure = AVERAGE(employees[years_at_company])
Avg Age = AVERAGE(employees[age])
Avg Performance = AVERAGE(employees[performance_rating])
Avg Satisfaction = AVERAGE(employees[job_satisfaction])
```

### Gender Diversity
```dax
Male Count = CALCULATE(COUNTROWS(employees), employees[gender] = "Male")
Female Count = CALCULATE(COUNTROWS(employees), employees[gender] = "Female")
Diversity Score = DIVIDE([Female Count], [Active Employees], 0) * 100
```

### Attendance Metrics
```dax
Attendance Rate = DIVIDE(
    CALCULATE(COUNTROWS(attendance), attendance[status] = "Present"),
    COUNTROWS(attendance), 0) * 100
WFH Rate = DIVIDE(
    CALCULATE(COUNTROWS(attendance), attendance[status] = "WFH"),
    COUNTROWS(attendance), 0) * 100
Absenteeism Rate = DIVIDE(
    CALCULATE(COUNTROWS(attendance), attendance[status] = "Absent"),
    COUNTROWS(attendance), 0) * 100
Avg Hours Worked = AVERAGE(attendance[hours_worked])
```

## Step 4: Build Dashboard Pages

### Page 1: Executive Overview (KPI Dashboard)
| Visual | Configuration |
|--------|--------------|
| **Card visuals** (top row) | Total Employees, Active, Attrition Rate, Avg Salary, Avg Tenure |
| **Donut chart** | Legend: department, Values: Count of employee_id |
| **Line chart** | Axis: hire_date (by year), Values: Active Employees |
| **Gauge** | Value: Attrition Rate, Target: 10% |
| **Table** | Department, Headcount, Avg Salary, Attrition % |

### Page 2: Demographics & Diversity
| Visual | Configuration |
|--------|--------------|
| **Pie chart** | Legend: gender, Values: Count |
| **Clustered bar chart** | Axis: age_band, Values: Count, Legend: gender |
| **Treemap** | Category: education_field, Size: Count |
| **Matrix** | Rows: department, Columns: gender, Values: Count |
| **Bar chart** | Axis: marital_status, Values: Avg Salary |

### Page 3: Attrition Analysis
| Visual | Configuration |
|--------|--------------|
| **Funnel chart** | Category: department, Values: Attrition Count |
| **Stacked bar chart** | Axis: job_role, Values: Attrition Count, Legend: attrition |
| **Scatter chart** | X: job_satisfaction, Y: attrition, Size: salary |
| **Ribbon chart** | Category: years_at_company, Values: Attrition Rate |
| **Key influencers** | Analyze: attrition, Explain by: overtime, business_travel, job_satisfaction |

### Page 4: Compensation Analysis
| Visual | Configuration |
|--------|--------------|
| **Box & whisker** | Category: department, Values: salary |
| **Bar chart** | Axis: salary_band, Values: Count, Legend: gender |
| **Scatter chart** | X: performance_rating, Y: salary_hike_percent, Size: salary |
| **Table** | Department, Min Salary, Avg Salary, Max Salary, StdDev |

### Page 5: Performance & Development
| Visual | Configuration |
|--------|--------------|
| **Stacked column** | Axis: performance_rating, Values: Count |
| **Line chart** | X: review_period, Y: Avg Performance, Legend: department |
| **Bar chart** | Axis: training_category, Values: avg_score_improvement |
| **Gauge** | Value: Avg Performance, Target: 4 |

### Page 6: Attendance & Work Patterns
| Visual | Configuration |
|--------|--------------|
| **Line chart** | Axis: date (by month), Values: Attendance Rate, WFH Rate |
| **Bar chart** | Axis: day_of_week, Values: Avg Hours Worked |
| **Matrix** | Rows: department, Columns: status, Values: Count |
| **Card** | Avg Hours Worked |

## Step 5: Add Slicers & Filters

Add these slicers to all pages:
- **Department** (dropdown)
- **Gender** (dropdown)
- **Age Band** (dropdown)
- **Date Range** (between slider for hire_date)

## Step 6: Formatting Tips

1. **Theme**: Use a professional color palette (e.g., Corporate blue/teal)
2. **Font**: Segoe UI, 10-12pt for visuals
3. **Background**: Light gray (#F5F5F5)
4. **Cards**: Add icons, use conditional formatting for KPI arrows
5. **Tooltips**: Add report page tooltips for drill-through
6. **Bookmarks**: Create bookmarks for different views

## Step 7: Publish & Share

1. Click **Publish** in Power BI Desktop
2. Select your workspace (e.g., "HR Analytics")
3. In Power BI Service:
   - Set up **scheduled refresh** (gateway required)
   - Create **dashboard** from report
   - Share with stakeholders
   - Set up **data alerts** for key metrics
