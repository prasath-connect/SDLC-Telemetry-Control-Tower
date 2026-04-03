import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

# Page Config
st.set_page_config(layout="wide", page_title="SDLC Telemetry Control Tower", page_icon="🚀")

# Mock Data Functions
def generate_requirements_data():
    return {
        'traceability': {'epics': 100, 'user_stories': 85, 'test_cases': 70, 'executed': 60},
        'coverage_percent': 78.5,
        'orphaned_reqs': 12
    }

def generate_development_data():
    sprints = [f"Sprint {i+1}" for i in range(6)]
    data = []
    for sprint in sprints:
        data.append({
            'Sprint': sprint,
            'Planned': np.random.randint(80, 120),
            'Actual': np.random.randint(60, 100),
            'Released': np.random.randint(50, 90)
        })
    df = pd.DataFrame(data)
    # Dependency Map Data
    teams = ['Frontend', 'Backend', 'Middleware', 'Testing']
    edges = [('Frontend', 'Backend'), ('Backend', 'Middleware'), ('Middleware', 'Testing'), ('Testing', 'Frontend')]
    # Risk Tickets
    risk_tickets = pd.DataFrame({
        'Ticket ID': [f'TICK-{i+1}' for i in range(5)],
        'Blocked By': ['API-123', 'DB-456', 'SEC-789', 'INF-101', 'DEP-202'],
        'Age': np.random.randint(5, 30, 5),
        'AI Predicted Risk %': np.random.uniform(60, 95, 5).round(1)
    })
    return df, edges, risk_tickets

def generate_cicd_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=14).strftime('%Y-%m-%d')
    data = []
    for date in dates:
        total = 100
        fail = np.random.randint(0, 20)
        skip = np.random.randint(0, 10)
        pass_count = total - fail - skip
        data.append({'Date': date, 'Pass': pass_count, 'Fail': fail, 'Skip': skip})
    df = pd.DataFrame(data)
    return {
        'last_stable_build': 'BUILD-2026-042',
        'nightly_pass_rate': 87.3,
        'smoke_test_status': 'Green' if np.random.choice([True, False]) else 'Red',
        'build_results': df
    }

def generate_testing_data():
    return {
        'total_tests_executed': 15420,
        'defect_density': 2.34,  # Bugs per KLOC
        'critical_hsi_bugs': 3,
        'cosmetic_ui_bugs': 8
    }

def generate_executive_data():
    sprints = [f"Sprint {i+1}" for i in range(10)]
    data = []
    for sprint in sprints:
        data.append({
            'Sprint': sprint,
            'Budget_Burn': np.random.randint(50000, 100000),
            'Feature_Delivery': np.random.randint(20, 80)
        })
    df = pd.DataFrame(data)
    schedule_slip_days = 15  # Mock
    daily_payroll = 25000  # Mock
    cost_of_delay = schedule_slip_days * daily_payroll
    return df, cost_of_delay

# Main App
st.title("SDLC Telemetry Control Tower")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Requirements (V-Cycle & Traceability)", "Development (Execution & Dependency Risk)", "CI/CD & Integration (Pipeline Health)", "Testing (Quality & Defect Density)", "Executive Financial Metrics"])

with tab1:
    st.header("Requirements: V-Cycle & Traceability")
    
    with st.expander("Polarion API Configuration"):
        polarion_url = st.text_input("Polarion API URL", "https://polarion.example.com/api")
    
    req_data = generate_requirements_data()
    
    # Funnel Chart
    fig_funnel = go.Figure(go.Funnel(
        y=list(req_data['traceability'].keys()),
        x=list(req_data['traceability'].values()),
        textinfo="value+percent initial"
    ))
    fig_funnel.update_layout(template="plotly_white", title="V-Cycle Traceability Funnel")
    st.plotly_chart(fig_funnel)
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Traceability Coverage", f"{req_data['coverage_percent']}%")
    with col2:
        st.metric("Orphaned Requirements", req_data['orphaned_reqs'])

with tab2:
    st.header("Development: Execution & Dependency Risk")
    
    with st.expander("Jira/Azure DevOps API Config"):
        jira_url = st.text_input("Jira API URL", "https://jira.example.com/api")
    
    dev_df, edges, risk_tickets = generate_development_data()
    
    # Feature Burnout Chart
    fig_burnout = go.Figure()
    fig_burnout.add_trace(go.Bar(x=dev_df['Sprint'], y=dev_df['Planned'], name='Planned', marker_color='lightblue'))
    fig_burnout.add_trace(go.Bar(x=dev_df['Sprint'], y=dev_df['Actual'], name='Actual', marker_color='orange'))
    fig_burnout.add_trace(go.Line(x=dev_df['Sprint'], y=dev_df['Released'], name='Released', mode='lines+markers', line=dict(color='green')))
    fig_burnout.update_layout(template="plotly_white", title="Feature Burnout: Planned vs. Actual vs. Released", barmode='group')
    st.plotly_chart(fig_burnout)
    
    # Dependency Map (Simple Network)
    fig_network = go.Figure()
    for edge in edges:
        fig_network.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name=f"{edge[0]} -> {edge[1]}"))
    fig_network.update_layout(template="plotly_white", title="Team Dependency Map", showlegend=False)
    st.plotly_chart(fig_network)
    
    # Risk Tickets Dataframe
    st.subheader("Top 5 Predictive Risk Tickets")
    st.dataframe(risk_tickets)

with tab3:
    st.header("CI/CD & Integration: Pipeline Health")
    
    with st.expander("Jenkins/GitLab API Config"):
        jenkins_url = st.text_input("Jenkins API URL", "https://jenkins.example.com/api")
    
    cicd_data = generate_cicd_data()
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Last Stable Build ID", cicd_data['last_stable_build'])
    with col2:
        st.metric("Nightly Pass Rate", f"{cicd_data['nightly_pass_rate']}%")
    with col3:
        status_color = "🟢" if cicd_data['smoke_test_status'] == 'Green' else "🔴"
        st.metric("Smoke Test Status", f"{status_color} {cicd_data['smoke_test_status']}")
    
    # Build Results Chart
    fig_build = px.bar(cicd_data['build_results'], x='Date', y=['Pass', 'Fail', 'Skip'], 
                       title="Nightly Build Results (Last 14 Days)", template="plotly_white")
    st.plotly_chart(fig_build)

with tab4:
    st.header("Testing: Quality & Defect Density")
    
    test_data = generate_testing_data()
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tests Executed", f"{test_data['total_tests_executed']:,}")
    with col2:
        st.metric("Defect Density (Bugs/KLOC)", f"{test_data['defect_density']}")
    
    # AI Insights
    st.info(f"**What to Worry About:** {test_data['critical_hsi_bugs']} Critical HSI/Middleware bugs detected. Immediate attention required.")
    st.warning(f"**What NOT to Worry About:** {test_data['cosmetic_ui_bugs']} Cosmetic/UI bugs can be deferred to next PI.")

with tab5:
    st.header("Executive Financial Metrics: The Director View")
    
    exec_df, cost_of_delay = generate_executive_data()
    
    st.metric("Cost of Delay", f"${cost_of_delay:,}")
    
    # Budget Burn vs Feature Delivery
    fig_area = px.area(exec_df, x='Sprint', y=['Budget_Burn', 'Feature_Delivery'], 
                       title="Budget Burn vs. Feature Delivery", template="plotly_white")
    st.plotly_chart(fig_area)