import streamlit as st
import pandas as pd
import plotly.express as px
import graphviz
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

def main():
    st.set_page_config(page_title="SDLC Telemetry Control Tower", layout="wide", initial_sidebar_state="expanded")

    # Generate mock data
    sprints, requirements, pipeline_runs, financials = generate_mock_telemetry()

    # Executive Summary
    st.title("Enterprise SDLC Telemetry Control Tower")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Health", f"{calculate_overall_health(sprints, requirements, pipeline_runs, financials)}%")
    with col2:
        st.metric("Budget at Risk", calculate_budget_at_risk(financials))
    with col3:
        st.metric("Schedule Slip", calculate_schedule_slip(sprints))

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Requirements (Polarion)", "Development (Jira)", "CI/CD (Jenkins/GitLab)", "Testing", "Financials"])

    with tab1:
        st.header("Requirements (Polarion)")
        with st.expander("API Configuration"):
            st.text_input("Polarion Server URL")
            st.text_input("API Key")
            st.button("Connect")

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

    with tab2:
        st.header("Development (Jira)")
        with st.expander("API Configuration"):
            st.text_input("Jira Server URL")
            st.text_input("API Token")
            st.button("Connect")

        # Dependency Graph
        dot = graphviz.Digraph()
        dot.node('Requirements', 'Requirements\nRisk: 25%')
        dot.node('Design', 'Design\nRisk: 30%')
        dot.node('Development', 'Development\nRisk: 35%')
        dot.node('Integration', 'Integration\nRisk: 40%')
        dot.node('Testing', 'Testing\nRisk: 45%')
        dot.edge('Requirements', 'Design', label='15', color='red' if 15 > 10 else 'black')
        dot.edge('Design', 'Development', label='20', color='red' if 20 > 10 else 'black')
        dot.edge('Development', 'Integration', label='25', color='red' if 25 > 10 else 'black')
        dot.edge('Integration', 'Testing', label='30', color='red' if 30 > 10 else 'black')
        st.graphviz_chart(dot)

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
            st.text_input("CI/CD Server URL")
            st.text_input("Access Token")
            st.button("Connect")

        # Metrics
        last_stable = pipeline_runs[pipeline_runs['status'] == 'Success']['build_number'].iloc[-1] if not pipeline_runs[pipeline_runs['status'] == 'Success'].empty else 'N/A'
        pass_rate = (pipeline_runs['status'] == 'Success').mean() * 100
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Last Stable Build", last_stable)
        with col2:
            st.metric("Pass Rate", f"{pass_rate:.1f}%")

        # Nightly Build Results Bar Chart
        fig = px.bar(pipeline_runs, x='date', y='tests_passed', color='status', title="Nightly Build Results")
        st.plotly_chart(fig)

    with tab4:
        st.header("Testing")
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

    with tab5:
        st.header("Financials")
        # Cost of Delay Metric
        avg_cost_of_delay = financials['cost_of_delay'].mean()
        st.metric("Cost of Delay", f"${avg_cost_of_delay:,.0f}")

        # Budget Burn vs Delivery Area Chart
        fig = px.area(financials, x='date', y=['cumulative_burn', 'features_delivered'], title="Budget Burn vs Delivery")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
