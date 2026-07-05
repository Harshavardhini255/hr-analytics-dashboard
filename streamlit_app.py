import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

DATA_DIR = "data"

@st.cache_data
def load_data():
    emp = pd.read_csv(f"{DATA_DIR}/employees.csv")
    perf = pd.read_csv(f"{DATA_DIR}/performance_reviews.csv")
    return emp, perf

emp, perf = load_data()

emp['hire_year'] = pd.to_datetime(emp['hire_date'], errors='coerce').dt.year
emp['salary_band'] = pd.cut(emp['salary'],
    bins=[0, 40000, 60000, 80000, 100000, 300000],
    labels=['<40K', '40-60K', '60-80K', '80-100K', '100K+'])
emp['age_band'] = pd.cut(emp['age'],
    bins=[0, 25, 35, 45, 55, 100],
    labels=['<25', '25-34', '35-44', '45-54', '55+'])

total = len(emp)
active = (emp['employment_status'] == 'Active').sum()
attrited = (emp['attrition'] == 'Yes').sum()
attrition_rate = round(attrited / total * 100, 1)
avg_salary = round(emp['salary'].mean())
avg_tenure = round(emp['years_at_company'].mean(), 1)
avg_age = round(emp['age'].mean(), 1)
avg_perf = round(emp['performance_rating'].mean(), 1)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bar-chart.png", width=60)
    st.title("HR Analytics")
    st.markdown("---")
    dept_filter = st.multiselect("Department", options=emp['department'].unique(),
                                  default=emp['department'].unique())
    gender_filter = st.multiselect("Gender", options=emp['gender'].unique(),
                                    default=emp['gender'].unique())
    status_filter = st.multiselect("Employment Status", options=['Active', 'Terminated'],
                                    default=['Active'])
    st.markdown("---")
    st.caption("Data last updated: July 2025")

mask = emp['department'].isin(dept_filter) & emp['gender'].isin(gender_filter)
if status_filter:
    mask &= emp['employment_status'].isin(status_filter)
df = emp[mask]

st.title("HR Analytics Dashboard")
st.markdown("### Workforce Overview")

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("Total Employees", f"{len(df):,}",
              f"{len(df)-total:+}" if len(df)!=total else "")
with k2:
    st.metric("Active", f"{(df['employment_status']=='Active').sum():,}")
with k3:
    st.metric("Attrition Rate", f"{attrition_rate}%")
with k4:
    st.markdown(f"<h1 style='text-align:center;color:#FF6B6B;font-size:30px'>{attrited}</h1><p style='text-align:center'>Attrited</p>", unsafe_allow_html=True)
with k5:
    st.metric("Avg Salary", f"${avg_salary:,}")
with k6:
    st.metric("Avg Tenure", f"{avg_tenure}yrs")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Department Overview", "Attrition Analysis", "Salary & Compensation",
     "Demographics", "Performance"]
)

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        dept_count = df.groupby('department').agg(
            Headcount=('employee_id', 'count'),
            Avg_Salary=('salary', 'mean'),
            Avg_Tenure=('years_at_company', 'mean')
        ).round(1).reset_index()
        fig = px.bar(dept_count, x='department', y='Headcount',
                     color='Avg_Salary', color_continuous_scale='Blues',
                     text='Headcount', title='Headcount by Department')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        dept_stats = df.groupby('department').agg(
            Headcount=('employee_id', 'count'),
            Attrition_Rate=('attrition', lambda x: round((x=='Yes').mean()*100, 1))
        ).reset_index()
        fig = px.bar(dept_stats, x='department', y='Attrition_Rate',
                     color='Attrition_Rate', color_continuous_scale='Reds',
                     text='Attrition_Rate', title='Attrition Rate by Department (%)')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(dept_count.style.format({'Avg_Salary': '${:,.0f}', 'Avg_Tenure': '{:.1f}'}),
                 use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        factors = ['overtime', 'business_travel', 'marital_status']
        factor_labels = ['Overtime', 'Business Travel', 'Marital Status']
        for col, label in zip(factors, factor_labels):
            ctab = pd.crosstab(df[col], df['attrition'], normalize='index') * 100
            ctab = ctab.reset_index()
            fig = px.bar(ctab, x=col, y='Yes' if 'Yes' in ctab.columns else 'No',
                         title=f'Attrition by {label}',
                         labels={'Yes': 'Attrition %', col: ''},
                         color_discrete_sequence=['#FF6B6B'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        att_by_dept = df.groupby('department').agg(
            Total=('employee_id', 'count'),
            Attrited=('attrition', lambda x: (x=='Yes').sum())
        ).reset_index()
        att_by_dept['Retained'] = att_by_dept['Total'] - att_by_dept['Attrited']
        fig = px.bar(att_by_dept, x='department', y=['Retained', 'Attrited'],
                     title='Attrition Breakdown by Department',
                     barmode='stack', color_discrete_map={'Retained': '#4ECDC4', 'Attrited': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

        sat_vs_att = df.groupby('job_satisfaction').agg(
            Attrition_Rate=('attrition', lambda x: (x=='Yes').mean()*100),
            Count=('employee_id', 'count')
        ).reset_index()
        fig = px.line(sat_vs_att, x='job_satisfaction', y='Attrition_Rate',
                      markers=True, title='Attrition Rate by Job Satisfaction',
                      labels={'job_satisfaction': 'Satisfaction (1-4)', 'Attrition_Rate': 'Attrition %'})
        st.plotly_chart(fig, use_container_width=True)

        wlb = df.groupby('work_life_balance').agg(
            Attrition_Rate=('attrition', lambda x: (x=='Yes').mean()*100)
        ).reset_index()
        fig = px.line(wlb, x='work_life_balance', y='Attrition_Rate',
                      markers=True, title='Attrition Rate by Work-Life Balance',
                      labels={'work_life_balance': 'WLB Score (1-4)'})
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.box(df, x='department', y='salary', color='department',
                     title='Salary Distribution by Department',
                     labels={'salary': 'Salary ($)'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        salary_by_gender = df.groupby(['department', 'gender'])['salary'].mean().reset_index()
        fig = px.bar(salary_by_gender, x='department', y='salary', color='gender',
                     barmode='group', title='Avg Salary: Gender by Department',
                     labels={'salary': 'Avg Salary ($)'},
                     color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        band_count = df.groupby('salary_band', observed=False).size().reset_index(name='Count')
        fig = px.pie(band_count, names='salary_band', values='Count',
                     title='Salary Band Distribution', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        perf_vs_salary = df.groupby('performance_rating')['salary'].mean().reset_index()
        fig = px.line(perf_vs_salary, x='performance_rating', y='salary',
                      markers=True, title='Avg Salary vs Performance Rating',
                      labels={'performance_rating': 'Rating', 'salary': 'Avg Salary ($)'})
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        gender_dist = df['gender'].value_counts().reset_index()
        fig = px.pie(gender_dist, names='gender', values='count',
                     title='Gender Distribution',
                     color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        age_dist = df.groupby('age_band', observed=False).size().reset_index(name='Count')
        fig = px.bar(age_dist, x='age_band', y='Count',
                     title='Age Distribution', color='Count',
                     color_continuous_scale='Viridis',
                     labels={'age_band': 'Age Band'})
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        edu = df['education_field'].value_counts().reset_index()
        fig = px.bar(edu, x='education_field', y='count',
                     title='Education Background',
                     color='count', color_continuous_scale='Tealgrn')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        mar = df['marital_status'].value_counts().reset_index()
        fig = px.pie(mar, names='marital_status', values='count',
                     title='Marital Status', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Gender Diversity by Department")
    div = df.groupby(['department', 'gender']).size().reset_index(name='Count')
    fig = px.bar(div, x='department', y='Count', color='gender',
                 barmode='stack', text='Count',
                 color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    c1, c2 = st.columns(2)
    with c1:
        perf_dist = df['performance_rating'].value_counts().sort_index().reset_index()
        fig = px.bar(perf_dist, x='performance_rating', y='count',
                     title='Performance Rating Distribution',
                     labels={'performance_rating': 'Rating', 'count': 'Count'},
                     color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        dept_perf = df.groupby('department')['performance_rating'].mean().reset_index()
        fig = px.bar(dept_perf, x='department', y='performance_rating',
                     title='Avg Performance Rating by Department',
                     color='performance_rating', color_continuous_scale='RdYlGn',
                     labels={'performance_rating': 'Avg Rating'},
                     text_auto='.2f')
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        satisfaction = df[['job_satisfaction', 'work_life_balance',
                           'environment_satisfaction', 'relationship_satisfaction',
                           'job_involvement']].mean().round(2).reset_index()
        satisfaction.columns = ['Metric', 'Avg Score']
        fig = px.bar(satisfaction, x='Metric', y='Avg Score',
                     title='Employee Satisfaction Scores (Avg)',
                     color='Avg Score', color_continuous_scale='Tealgrn',
                     text_auto='.2f')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        tenure_vs_perf = df.groupby('years_at_company').agg(
            Avg_Performance=('performance_rating', 'mean'),
            Count=('employee_id', 'count')
        ).reset_index()
        fig = px.scatter(tenure_vs_perf, x='years_at_company', y='Avg_Performance',
                         size='Count', color='Avg_Performance',
                         title='Performance vs Tenure',
                         labels={'years_at_company': 'Years at Company',
                                 'Avg_Performance': 'Avg Performance'},
                         color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### Employee Directory")
search = st.text_input("Search by name, role, or department")
cols = ['employee_id', 'first_name', 'last_name', 'department', 'job_role',
        'gender', 'age', 'salary', 'years_at_company', 'performance_rating',
        'job_satisfaction', 'attrition']
display = df[cols].copy()
if search:
    display = display[display.apply(lambda r: search.lower() in r.astype(str).str.lower().str.cat(sep=' '), axis=1)]
st.dataframe(display.style.format({'salary': '${:,.0f}'}),
             use_container_width=True, hide_index=True,
             column_config={'employee_id': 'ID', 'salary': st.column_config.NumberColumn(format="$%.0f")})

st.markdown("---")
st.caption(f"HR Analytics Dashboard | {active} Active Employees | Data refreshed from CSV")
