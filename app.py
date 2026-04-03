import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

def generate_mock_telemetry():
    # Sprints DataFrame
    sprints = pd.DataFrame({
        'sprint_id': [f'SP{i}' for i in range(1, 11)],
        'start_date': pd.date_range(start='2024-01-01', periods=10, freq='2W'),
        'end_date': pd.date_range(start='2024-01-15', periods=10, freq='2W'),
        'velocity': [random.randint(80, 120) for _ in range(10)],
        'committed_stories': [random.randint(15, 25) for _ in range(10)],
        'completed_stories': [random.randint(12, 22) for _ in range(10)],
        'blockers': [random.randint(0, 3) for _ in range(10)]
    })

    # Requirements DataFrame
    requirements = pd.DataFrame({
        'req_id': [f'REQ{i}' for i in range(1, 51)],
        'phase': random.choices(['Requirements', 'Design', 'Development', 'Integration', 'Testing'], k=50),
        'status': random.choices(['Draft', 'Approved', 'Implemented', 'Verified'], k=50),
        'traceability_links': [random.randint(0, 5) for _ in range(50)],
        'unresolved_dependencies': [random.randint(0, 2) for _ in range(50)],
        'age_days': [random.randint(1, 60) for _ in range(50)]
    })

    # Pipeline Runs DataFrame
    pipeline_runs = pd.DataFrame({
        'run_id': [f'RUN{i}' for i in range(1, 31)],
        'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'status': random.choices(['Success', 'Failure', 'Partial'], weights=[0.7, 0.2, 0.1], k=30),
        'duration_minutes': [random.randint(10, 120) for _ in range(30)],
        'tests_passed': [random.randint(80, 100) for _ in range(30)],
        'tests_failed': [random.randint(0, 10) for _ in range(30)],
        'build_number': [f'v1.0.{i}' for i in range(1, 31)]
    })

    # Financial Burn Rates DataFrame
    financials = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'budget_allocated': [1000000] * 30,
        'budget_burned': [random.randint(20000, 50000) for _ in range(30)],
        'features_delivered': [random.randint(1, 5) for _ in range(30)],
        'cost_of_delay': [random.randint(5000, 15000) for _ in range(30)]
    })
    financials['cumulative_burn'] = financials['budget_burned'].cumsum()
    financials['remaining_budget'] = financials['budget_allocated'] - financials['cumulative_burn']

    return sprints, requirements, pipeline_runs, financials

def calculate_overall_health(sprints, requirements, pipeline_runs, financials):
    # Simple health calculation
    sprint_completion_rate = sprints['completed_stories'].sum() / sprints['committed_stories'].sum()
    req_traceability = requirements['traceability_links'].mean()
    pipeline_success_rate = (pipeline_runs['status'] == 'Success').mean()
    budget_efficiency = financials['remaining_budget'].iloc[-1] / financials['budget_allocated'].iloc[0]

    overall_health = (sprint_completion_rate + req_traceability + pipeline_success_rate + budget_efficiency) / 4 * 100
    return round(overall_health, 1)

def calculate_budget_at_risk(financials):
    remaining = financials['remaining_budget'].iloc[-1]
    total = financials['budget_allocated'].iloc[0]
    risk = (1 - remaining / total) * 100000  # Mock calculation
    return f"${risk:,.0f}"

def calculate_schedule_slip(sprints):
    avg_velocity = sprints['velocity'].mean()
    planned_velocity = 100
    slip_days = (planned_velocity - avg_velocity) / 10 * 30  # Mock calculation
    return f"{max(0, slip_days):.0f} days"


def get_swot_data():
    # Return counts that drive visualization in each tab
    return {
        'Strengths': 3,
        'Weaknesses': 2,
        'Opportunities': 4,
        'Threats': 3
    }


def main():
    st.set_page_config(page_title="SDLC Telemetry Control Tower", layout="wide", initial_sidebar_state="expanded")

    # Generate mock data
    sprints, requirements, pipeline_runs, financials = generate_mock_telemetry()

    # Executive Summary
    st.title("Enterprise SDLC Telemetry Control Tower")
    swot_data = get_swot_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Health", f"{calculate_overall_health(sprints, requirements, pipeline_runs, financials)}%")
    with col2:
        st.metric("Budget at Risk", calculate_budget_at_risk(financials))
    with col3:
        st.metric("Schedule Slip", calculate_schedule_slip(sprints))
    with col4:
        st.metric("Executive Confidence", "High" if swot_data['Strengths'] > swot_data['Threats'] else "Medium")

    # Extended VP KPIs
    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Project Velocity", f"{sprints['velocity'].mean():.1f}")
    kpi_cols[1].metric("Blocker Count", f"{sprints['blockers'].sum()}")
    kpi_cols[2].metric("Traceability %,", f"{(requirements['traceability_links'] > 0).mean() * 100:.1f}%")
    kpi_cols[3].metric("Cost Burn %", f"{financials['cumulative_burn'].iloc[-1] / financials['budget_allocated'].iloc[-1] * 100:.1f}%")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Requirements (Polarion)", "Development (Jira)", "CI/CD (Jenkins/GitLab)", "Testing", "Financials"])

    with tab1:
        st.header("Requirements (Polarion)")
        with st.expander("API Configuration"):
            st.text_input("Polarion Server URL", key="polarion_url")
            st.text_input("API Key", key="polarion_api_key")
            st.button("Connect", key="polarion_connect")
            st.markdown("[Open Polarion Requirements Dashboard](https://polarion.example.com)")

        # V-Cycle Traceability Funnel
        phases = ['Requirements', 'Design', 'Development', 'Integration', 'Testing']
        values = [requirements[requirements['phase'] == phase].shape[0] for phase in phases]
        fig = px.funnel(y=phases, x=values, title="V-Cycle Traceability Funnel")
        st.plotly_chart(fig)

        # Traceability Coverage Metric
        total_reqs = len(requirements)
        traced_reqs = requirements['traceability_links'].gt(0).sum()
        coverage = (traced_reqs / total_reqs) * 100
        st.metric("% Traceability Coverage", f"{coverage:.1f}%")

        swot_df = pd.DataFrame({'SWOT': list(get_swot_data().keys()), 'Value': list(get_swot_data().values())})
        swot_chart = px.pie(swot_df, names='SWOT', values='Value', title='Requirements SWOT Distribution')
        st.plotly_chart(swot_chart)

        # 4-quadrant insights
        a1, a2 = st.columns(2)
        with a1:
            st.write("#### Requirements Trends")
            st.bar_chart(requirements['phase'].value_counts())
        with a2:
            st.write("#### Risk by Age")
            age_cut = pd.cut(requirements['age_days'], bins=[0, 15, 30, 45, 60], labels=['0-15', '16-30', '31-45', '46-60'])
            st.bar_chart(age_cut.value_counts())

        b1, b2 = st.columns(2)
        with b1:
            st.write("#### Dependency vs Traceability")
            dep = requirements.groupby('unresolved_dependencies').size().reset_index(name='count')
            st.bar_chart(dep.set_index('unresolved_dependencies'))
        with b2:
            st.write("#### Phase Status Pivot")
            pivot = requirements.groupby(['phase', 'status']).size().unstack(fill_value=0)
            st.dataframe(pivot)


    with tab2:
        st.header("Development (Jira)")
        with st.expander("API Configuration"):
            st.text_input("Jira Server URL", key="jira_url")
            st.text_input("API Token", key="jira_api_token")
            st.button("Connect", key="jira_connect")
            st.markdown("[Open JIRA Dashboard](https://jira.example.com)")

        swot_df = pd.DataFrame({'SWOT': list(get_swot_data().keys()), 'Value': list(get_swot_data().values())})
        swot_chart = px.bar(swot_df, x='SWOT', y='Value', title='Development SWOT - Executive View')
        st.plotly_chart(swot_chart)

        # 4-quadrant leader view: Development
        c1, c2 = st.columns(2)
        with c1:
            sprint_effort = px.bar(sprints, x='sprint_id', y='committed_stories', title='Sprint Committed Stories')
            st.plotly_chart(sprint_effort)
        with c2:
            blocker_pie = px.pie(sprints, names='sprint_id', values='blockers', title='Blocker Distribution by Sprint')
            st.plotly_chart(blocker_pie)

        c3, c4 = st.columns(2)
        with c3:
            dev_velocity = px.line(sprints, x='sprint_id', y='velocity', title='Velocity Trend')
            st.plotly_chart(dev_velocity)
        with c4:
            dev_risk = pd.DataFrame({'Status': ['Low', 'Medium', 'High'], 'Count': [random.randint(1,4), random.randint(2,6), random.randint(3,7)]})
            st.write('### Dev Risk Heatmap')
            st.bar_chart(dev_risk.set_index('Status'))

        # Feature Burnout Bar Chart
        fig = px.bar(sprints, x='sprint_id', y='completed_stories', title="Feature Burnout")
        st.plotly_chart(fig)

        # Top 5 Predictive Risk Tickets
        risk_tickets = pd.DataFrame({
            'Ticket ID': [f'TICKET-{i}' for i in range(1, 6)],
            'Risk Score': [95, 88, 82, 76, 71],
            'Description': ['Critical dependency', 'Security issue', 'Performance bottleneck', 'Integration failure', 'Test coverage gap']
        })
        st.dataframe(risk_tickets)

    with tab3:
        st.header("CI/CD (Jenkins/GitLab)")
        with st.expander("API Configuration"):
            st.text_input("CI/CD Server URL", key="cicd_url")
            st.text_input("Access Token", key="cicd_api_token")
            st.button("Connect", key="cicd_connect")
            st.markdown("[Open CI/CD Dashboard](https://cicd.example.com)")

        swot_df = pd.DataFrame({'SWOT': list(get_swot_data().keys()), 'Value': list(get_swot_data().values())})
        swot_chart = px.bar(swot_df, x='SWOT', y='Value', title='CI/CD SWOT - Executive View')
        st.plotly_chart(swot_chart)

        # Metrics
        last_stable = pipeline_runs[pipeline_runs['status'] == 'Success']['build_number'].iloc[-1] if not pipeline_runs[pipeline_runs['status'] == 'Success'].empty else 'N/A'
        pass_rate = (pipeline_runs['status'] == 'Success').mean() * 100
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Last Stable Build", last_stable)
        with col2:
            st.metric("Pass Rate", f"{pass_rate:.1f}%")

        q1, q2 = st.columns(2)
        with q1:
            st.write("#### Build Duration Trends")
            st.line_chart(pipeline_runs.set_index('date')['duration_minutes'])
        with q2:
            st.write("#### Status Share")
            status_pie = px.pie(names=pipeline_runs['status'].value_counts().index, values=pipeline_runs['status'].value_counts().values, title='Build Status Distribution')
            st.plotly_chart(status_pie)

        q3, q4 = st.columns(2)
        with q3:
            st.write("#### Failed Tests Trend")
            st.line_chart(pipeline_runs.set_index('date')['tests_failed'])
        with q4:
            st.write("#### Builds by Week")
            by_week = pipeline_runs.copy(); by_week['week'] = pd.to_datetime(by_week['date']).dt.isocalendar().week
            st.bar_chart(by_week.groupby('week').size())

    with tab4:
        st.header("Testing")
        with st.expander("API Configuration"):
            st.text_input("Testing Tool URL", key="testing_url")
            st.text_input("API Token", key="testing_api_token")
            st.button("Connect", key="testing_connect")
            st.markdown("[Open Testing Dashboard](https://testing.example.com)")

        swot_df = pd.DataFrame({'SWOT': list(get_swot_data().keys()), 'Value': list(get_swot_data().values())})
        swot_chart = px.bar(swot_df, x='SWOT', y='Value', title='Testing SWOT - Executive View')
        st.plotly_chart(swot_chart)

        # Defect Density Metric
        total_tests = pipeline_runs['tests_passed'].sum() + pipeline_runs['tests_failed'].sum()
        total_defects = pipeline_runs['tests_failed'].sum()
        defect_density = (total_defects / total_tests) * 100 if total_tests > 0 else 0
        st.metric("Defect Density", f"{defect_density:.2f}%")

        # AI Insights
        critical_bugs = random.randint(1, 5)
        deferred_bugs = random.randint(5, 15)
        st.warning(f"🚨 {critical_bugs} Critical Bugs Detected - Immediate Attention Required")
        st.success(f"✅ {deferred_bugs} Deferred Bugs Identified - Can be addressed in next sprint")

        # 4-quadrant testing insights
        q1, q2 = st.columns(2)
        with q1:
            st.write("#### Test Pass/Fail Rate")
            st.bar_chart(pipeline_runs.set_index('date')[['tests_passed', 'tests_failed']])
        with q2:
            st.write("#### Failure Count Distribution")
            fail_pie = px.pie(names=pipeline_runs['tests_failed'].value_counts().index, values=pipeline_runs['tests_failed'].value_counts().values, title='Failure Magnitude')
            st.plotly_chart(fail_pie)

        q3, q4 = st.columns(2)
        with q3:
            st.write("#### Average Duration by Status")
            st.bar_chart(pipeline_runs.groupby('status')['duration_minutes'].mean())
        with q4:
            st.write("#### Regression vs Smoke\n(Estimated)")
            st.line_chart(pd.DataFrame({'Regression': pipeline_runs['tests_failed'] * 1.1, 'Smoke': pipeline_runs['tests_passed'] * 0.6}, index=pipeline_runs['date']))

    with tab5:
        st.header("Financials")
        with st.expander("API Configuration"):
            st.text_input("Financial API URL", key="finance_url")
            st.text_input("API Token", key="finance_api_token")
            st.button("Connect", key="finance_connect")
            st.markdown("[Open Finance Dashboard](https://finance.example.com)")

        swot_df = pd.DataFrame({'SWOT': list(get_swot_data().keys()), 'Value': list(get_swot_data().values())})
        swot_chart = px.pie(swot_df, names='SWOT', values='Value', title='Financial SWOT - Executive View')
        st.plotly_chart(swot_chart)

        # Cost of Delay Metric
        avg_cost_of_delay = financials['cost_of_delay'].mean()
        st.metric("Cost of Delay", f"${avg_cost_of_delay:,.0f}")

        # Budget Burn vs Delivery Area Chart
        fig = px.area(financials, x='date', y=['cumulative_burn', 'features_delivered'], title="Budget Burn vs Delivery")
        st.plotly_chart(fig)

        # 4-quadrant financial cuts
        f1, f2 = st.columns(2)
        with f1:
            burn = px.line(financials, x='date', y='cumulative_burn', title='Cumulative Budget Burn')
            st.plotly_chart(burn)
        with f2:
            st.write('#### Delivery vs Burn Ratio')
            ratio = financials['features_delivered'] / (financials['budget_burned'] + 1)
            st.area_chart(ratio)

        f3, f4 = st.columns(2)
        with f3:
            st.bar_chart(financials.set_index('date')['cost_of_delay'])
        with f4:
            st.write('#### Remaining Budget Status')
            st.metric('Remaining Budget', f"${financials['remaining_budget'].iloc[-1]:,.0f}")
            st.metric('Burn %', f"{financials['cumulative_burn'].iloc[-1]/financials['budget_allocated'].iloc[-1]*100:.1f}%")

if __name__ == "__main__":
    main()
