import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

DATA_DIR = "data"

def load_data():
    emp = pd.read_csv(f"{DATA_DIR}/employees.csv")
    perf = pd.read_csv(f"{DATA_DIR}/performance_reviews.csv")
    return emp, perf

emp, perf = load_data()

emp['hire_year'] = pd.to_datetime(emp['hire_date'], errors='coerce').dt.year

salary_bins = [0, 40000, 60000, 80000, 100000, 300000]
salary_labels = ['<40K', '40-60K', '60-80K', '80-100K', '100K+']
emp['salary_band'] = pd.cut(emp['salary'], bins=salary_bins, labels=salary_labels)

age_bins = [0, 25, 35, 45, 55, 100]
age_labels = ['<25', '25-34', '35-44', '45-54', '55+']
emp['age_band'] = pd.cut(emp['age'], bins=age_bins, labels=age_labels)

total = len(emp)
active = int((emp['employment_status'] == 'Active').sum())
attrited = int((emp['attrition'] == 'Yes').sum())
attrition_rate = round(attrited / total * 100, 1)
avg_salary = round(emp['salary'].mean())
avg_tenure = round(emp['years_at_company'].mean(), 1)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bar-chart.png", width=60)
    st.title("HR Analytics")
    st.divider()
    dept_filter = st.multiselect("Department",
        options=sorted(emp['department'].unique()),
        default=sorted(emp['department'].unique()))
    gender_filter = st.multiselect("Gender",
        options=sorted(emp['gender'].unique()),
        default=sorted(emp['gender'].unique()))
    status_filter = st.multiselect("Employment Status",
        options=['Active', 'Terminated'],
        default=['Active'])
    st.divider()
    st.caption("Data last updated: July 2025")

mask = emp['department'].isin(dept_filter) & emp['gender'].isin(gender_filter)
if status_filter:
    mask &= emp['employment_status'].isin(status_filter)
df = emp[mask].copy()

st.title("HR Analytics Dashboard")
st.markdown("### Workforce Overview")

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1: st.metric("Total Employees", f"{len(df):,}")
with k2: st.metric("Active", f"{active:,}")
with k3: st.metric("Attrition Rate", f"{attrition_rate}%")
with k4: st.metric("Attrited", f"{attrited}")
with k5: st.metric("Avg Salary", f"${avg_salary:,}")
with k6: st.metric("Avg Tenure", f"{avg_tenure}yrs")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Department Overview", "Attrition Analysis", "Salary & Compensation",
     "Demographics", "Performance"]
)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        gb = df.groupby('department', as_index=False)['employee_id'].count()
        gb.columns = ['department', 'Headcount']
        fig = px.bar(gb, x='department', y='Headcount',
                     color='Headcount', color_continuous_scale='Blues',
                     text='Headcount', title='Headcount by Department')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        gb2 = df.groupby('department')['attrition'].apply(
            lambda x: round((x == 'Yes').mean() * 100, 1)).reset_index()
        gb2.columns = ['department', 'Attrition_Rate']
        fig = px.bar(gb2, x='department', y='Attrition_Rate',
                     color='Attrition_Rate', color_continuous_scale='Reds',
                     text='Attrition_Rate', title='Attrition Rate by Department (%)')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    summary = df.groupby('department', as_index=False).agg(
        Headcount=('employee_id', 'count'),
        Avg_Salary=('salary', 'mean'),
        Avg_Tenure=('years_at_company', 'mean')
    )
    summary['Avg_Salary'] = summary['Avg_Salary'].round(0).astype(int)
    summary['Avg_Tenure'] = summary['Avg_Tenure'].round(1)
    st.dataframe(summary, use_container_width=True, hide_index=True,
                 column_config={"Avg_Salary": st.column_config.NumberColumn(format="$%d")})

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        for col_name in ['overtime', 'business_travel', 'marital_status']:
            ct = pd.crosstab(df[col_name], df['attrition'], normalize='index') * 100
            ct = ct.reset_index()
            y_col = 'Yes' if 'Yes' in ct.columns else ct.columns[-1]
            fig = px.bar(ct, x=col_name, y=y_col,
                         title=f'Attrition by {col_name.replace("_", " ").title()}',
                         labels={y_col: 'Attrition %'}, color_discrete_sequence=['#FF6B6B'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        att = df.groupby('department', as_index=False).agg(
            Total=('employee_id', 'count'),
            Attrited=('attrition', lambda x: int((x == 'Yes').sum()))
        )
        att['Retained'] = att['Total'] - att['Attrited']
        fig = px.bar(att, x='department', y=['Retained', 'Attrited'],
                     title='Attrition Breakdown', barmode='stack',
                     color_discrete_map={'Retained': '#4ECDC4', 'Attrited': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

        sat = df.groupby('job_satisfaction', as_index=False)['attrition'].apply(
            lambda x: round((x == 'Yes').mean() * 100, 1))
        sat.columns = ['job_satisfaction', 'Attrition_Rate']
        fig = px.line(sat, x='job_satisfaction', y='Attrition_Rate',
                      markers=True, title='Attrition by Job Satisfaction',
                      labels={'job_satisfaction': 'Satisfaction (1-4)'})
        st.plotly_chart(fig, use_container_width=True)

        wlb = df.groupby('work_life_balance', as_index=False)['attrition'].apply(
            lambda x: round((x == 'Yes').mean() * 100, 1))
        wlb.columns = ['work_life_balance', 'Attrition_Rate']
        fig = px.line(wlb, x='work_life_balance', y='Attrition_Rate',
                      markers=True, title='Attrition by Work-Life Balance',
                      labels={'work_life_balance': 'WLB (1-4)'})
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(df, x='department', y='salary', color='department', title='Salary Distribution')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sg = df.groupby(['department', 'gender'], as_index=False)['salary'].mean()
        fig = px.bar(sg, x='department', y='salary', color='gender', barmode='group',
                     title='Avg Salary by Gender',
                     color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        bc = df['salary_band'].value_counts().reset_index()
        bc.columns = ['salary_band', 'Count']
        fig = px.pie(bc, names='salary_band', values='Count',
                     title='Salary Band Distribution', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        pv = df.groupby('performance_rating', as_index=False)['salary'].mean()
        fig = px.line(pv, x='performance_rating', y='salary',
                      markers=True, title='Avg Salary vs Performance',
                      labels={'performance_rating': 'Rating'})
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        gd = df['gender'].value_counts().reset_index()
        gd.columns = ['gender', 'count']
        fig = px.pie(gd, names='gender', values='count', title='Gender',
                     color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ad = df['age_band'].value_counts().reset_index()
        ad.columns = ['age_band', 'Count']
        fig = px.bar(ad, x='age_band', y='Count', title='Age Distribution',
                     color='Count', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        ed = df['education_field'].value_counts().reset_index()
        ed.columns = ['education_field', 'count']
        fig = px.bar(ed, x='education_field', y='count', title='Education',
                     color='count', color_continuous_scale='Tealgrn')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ms = df['marital_status'].value_counts().reset_index()
        ms.columns = ['marital_status', 'count']
        fig = px.pie(ms, names='marital_status', values='count', title='Marital Status', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Gender Diversity by Department")
    dv = df.groupby(['department', 'gender'], as_index=False).size()
    dv.columns = ['department', 'gender', 'Count']
    fig = px.bar(dv, x='department', y='Count', color='gender', barmode='stack',
                 color_discrete_map={'Male': '#4A90D9', 'Female': '#FF6B6B'})
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    col1, col2 = st.columns(2)
    with col1:
        pd_dist = df['performance_rating'].value_counts().sort_index().reset_index()
        pd_dist.columns = ['performance_rating', 'count']
        fig = px.bar(pd_dist, x='performance_rating', y='count',
                     title='Performance Rating Distribution', color='count',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dp = df.groupby('department', as_index=False)['performance_rating'].mean()
        fig = px.bar(dp, x='department', y='performance_rating',
                     title='Avg Performance by Department',
                     color='performance_rating', color_continuous_scale='RdYlGn',
                     text_auto='.2f')
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sat_cols = ['job_satisfaction', 'work_life_balance',
                    'environment_satisfaction', 'relationship_satisfaction', 'job_involvement']
        sat_df = df[sat_cols].mean().round(2).reset_index()
        sat_df.columns = ['Metric', 'Avg Score']
        fig = px.bar(sat_df, x='Metric', y='Avg Score', title='Satisfaction Scores',
                     color='Avg Score', color_continuous_scale='Tealgrn', text_auto='.2f')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        tv = df.groupby('years_at_company', as_index=False).agg(
            Avg_Performance=('performance_rating', 'mean'),
            Count=('employee_id', 'count')
        )
        fig = px.scatter(tv, x='years_at_company', y='Avg_Performance',
                         size='Count', color='Avg_Performance',
                         title='Performance vs Tenure',
                         color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### Employee Directory")
search = st.text_input("Search by name, role, or department")
cols = ['employee_id', 'first_name', 'last_name', 'department', 'job_role',
        'gender', 'age', 'salary', 'years_at_company', 'performance_rating',
        'job_satisfaction', 'attrition']
display = df[cols].copy()
if search:
    mask_search = display.astype(str).apply(
        lambda r: r.str.lower().str.contains(search.lower())).any(axis=1)
    display = display[mask_search]
st.dataframe(display, use_container_width=True, hide_index=True,
             column_config={
                 "employee_id": "ID",
                 "salary": st.column_config.NumberColumn(format="$%.0f")
             })

st.divider()
st.caption(f"HR Analytics Dashboard | {active} Active Employees | Data refreshed from CSV")
