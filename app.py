import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Config
st.set_page_config(layout="wide", page_title="MASTER Project AI Telemetry Control Tower", page_icon="??")

# Enterprise links configuration
st.sidebar.header("Enterprise Configuration")
polarion_url = st.sidebar.text_input("Polarion API URL", "https://polarion.example.com/api")
jira_url = st.sidebar.text_input("Jira/Azure DevOps API URL", "https://jira.example.com/api")
jenkins_url = st.sidebar.text_input("Jenkins/GitLab API URL", "https://jenkins.example.com/api")
ci_cd_url = st.sidebar.text_input("CI/CD API URL", "https://cicd.example.com/api")
st.sidebar.markdown("---")
master_note = st.sidebar.text_area("Notes / Comments for VP", "Enter project-level narrative here")

# Mock data generation

def generate_requirements_data():
    return {
        'traceability': {'Epics': 100, 'User Stories': 85, 'Test Cases': 70, 'Executed': 60},
        'coverage_percent': 78.5,
        'orphaned_reqs': 12,
        'hsi_critical_count': 2,
        'total_reqs': 240,
    }


def generate_development_data():
    sprints = [f"Sprint {i+1}" for i in range(6)]
    data = []
    for sprint in sprints:
        planned = np.random.randint(80, 120)
        actual = np.random.randint(60, 100)
        released = np.random.randint(50, min(actual, 95))
        risk_level = np.random.uniform(50, 95)
        data.append({'Sprint': sprint, 'Planned': planned, 'Actual': actual, 'Released': released, 'Risk_Level': risk_level})
    df = pd.DataFrame(data)
    edges = [('Frontend', 'Backend'), ('Backend', 'Middleware'), ('Middleware', 'Testing'), ('Testing', 'Frontend')]
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
        'nightly_pass_rate': float(np.random.uniform(80, 95).round(1)),
        'smoke_test_status': 'Green' if np.random.rand() > 0.2 else 'Red',
        'build_results': df,
    }


def generate_testing_data():
    return {
        'total_tests_executed': 15420,
        'defect_density': 2.34,
        'critical_hsi_bugs': np.random.randint(1, 6),
        'cosmetic_ui_bugs': np.random.randint(0, 12),
        'security_critical_bugs': np.random.randint(0, 4),
        'coverage_pct': np.random.uniform(70, 94).round(1),
    }


def generate_executive_data():
    sprints = [f"Sprint {i+1}" for i in range(10)]
    data = []
    for sprint in sprints:
        data.append({
            'Sprint': sprint,
            'Budget_Burn': np.random.randint(50000, 100000),
            'Feature_Delivery': np.random.randint(18, 75),
            'Savings_Achieved': np.random.randint(0, 25000),
        })
    df = pd.DataFrame(data)
    schedule_slip_days = np.random.randint(8, 20)
    daily_payroll = 25000
    cost_of_delay = schedule_slip_days * daily_payroll
    return df, cost_of_delay, schedule_slip_days


def run_monte_carlo(sprints_remaining, avg_velocity, velocity_std_dev, num_simulations=1000):
    simulations = []
    for _ in range(num_simulations):
        total_points = 0
        for _ in range(sprints_remaining):
            velocity = np.random.normal(avg_velocity, velocity_std_dev)
            total_points += max(0, velocity)
        simulations.append(total_points)
    return simulations


def calculate_risk_scores(df):
    latest_df = df[df['Sprint'] == df['Sprint'].max()]
    risks = {}
    for _, row in latest_df.iterrows():
        platform = row.get('Platform', f"Platform-{_}")
        req_risk = 10 + (row.get('Unresolved_Dependencies', 0) * 20 if row.get('Req_Age_Days', 0) > 14 else 0)
        design_risk = 15 + (30 if np.random.choice([True, False]) else 0)
        platform_df = df[df['Platform'] == platform] if 'Platform' in df.columns else df
        velocities = platform_df['Sprint_Velocity_Pts'].tail(4).tolist() if 'Sprint_Velocity_Pts' in platform_df.columns else []
        if len(velocities) >= 4:
            avg_3 = np.mean(velocities[:-1])
            current = velocities[-1]
            dev_risk = 85 if current < avg_3 * 0.85 else 20
        else:
            dev_risk = 20
        integration_risk = row.get('CICD_Failure_Rate', 0) + (20 if np.random.choice([True, False]) else 0)
        test_risk = row.get('Defect_Escape_Rate', 0) + (40 if np.random.choice([True, False]) else 0)
        risks[platform] = {
            'Requirements': min(req_risk, 100),
            'Design': min(design_risk, 100),
            'Development': min(dev_risk, 100),
            'Integration': min(integration_risk, 100),
            'Test': min(test_risk, 100),
        }
    return risks


def generate_swot():
    return {
        'Requirements': {
            'Strengths': ['Clear V-cycle traceability', 'High coverage in key modules'],
            'Weaknesses': ['Orphaned requirements still exist', 'Partial signoff on HSI flows'],
            'Opportunities': ['Automate artifact linkage', 'Improve requirement review cadence'],
            'Threats': ['Unresolved dependency backlog', 'Regulatory requirement changes']
        },
        'Development': {
            'Strengths': ['Stable velocity for core teams', 'Strong DevOps alignment'],
            'Weaknesses': ['Burnout in Middleware team', 'Blocked by external API delays'],
            'Opportunities': ['Shift-left testing', 'Tech-debt reduction sprint'],
            'Threats': ['Critical dependency chain breaks', 'Resource ramp-down risks']
        },
        'CI/CD': {
            'Strengths': ['High nightly pass rate', 'Good automated test coverage'],
            'Weaknesses': ['Occasional flaky smoke tests', 'Late QA feedback loops'],
            'Opportunities': ['Implement canary release flows', 'Increase pipeline parallelization'],
            'Threats': ['Toolchain version drift', 'Security scanning false negatives']
        },
        'Testing': {
            'Strengths': ['Large test execution throughput', 'Low critical production escapes'],
            'Weaknesses': ['High defect density in core modules', 'Manual regression overhead'],
            'Opportunities': ['AI test case generation', 'Better coverage analytics'],
            'Threats': ['HSI defects hidden in integration', 'Compliance audit readiness']
        },
        'Executive': {
            'Strengths': ['Solid cost tracking', 'Clear delivery pipeline'],
            'Weaknesses': ['Schedule slip variance', 'CapEx burn spikes'],
            'Opportunities': ['Cross-program budget consolidation', 'Vendor renegotiation'],
            'Threats': ['Market timeline pressure', 'Budget reallocation due to risk events']
        }
    }

# Build all baseline data
req_data = generate_requirements_data()
dev_df, dev_edges, risk_tickets_df = generate_development_data()
cicd_data = generate_cicd_data()
test_data = generate_testing_data()
exec_df, cost_of_delay, schedule_slip_days = generate_executive_data()

# Top-level Master Overview
st.subheader("MASTER Project AI Telemetry Command Center")

# Top KPI cards
overall_risks = calculate_risk_scores(pd.DataFrame([{'Platform': 'Global', 'Sprint': 'Sprint 6', 'Unresolved_Dependencies': 4, 'Req_Age_Days': 20, 'CICD_Failure_Rate': 42, 'Defect_Escape_Rate': 35, 'Sprint_Velocity_Pts': 65}]))
max_risk = max([val for phase_dict in overall_risks.values() for val in phase_dict.values()])
health = "Red" if max_risk > 75 else "Amber" if max_risk > 50 else "Green"
productivity_index = np.random.uniform(0.7, 0.92).round(2)
innovation_runway = np.random.randint(3, 10)
compliance_score = np.random.uniform(75, 95).round(1)

mcol1, mcol2, mcol3, mcol4 = st.columns(4)
with mcol1:
    st.metric("Portfolio Health", health)
with mcol2:
    st.metric("Productivity Index", f"{productivity_index}")
with mcol3:
    st.metric("Compliance Score", f"{compliance_score}%")
with mcol4:
    st.metric("Innovation Runway (Q) ", f"{innovation_runway} quarters")

st.markdown("---")

tabs = st.tabs(["Overall Metrics", "Requirements", "Development", "CI/CD", "Testing", "Executive Finance"])

# Master Overall Metrics tab
with tabs[0]:
    st.header("Project Overall Metrics")
    st.markdown("- **Cost of Delay:** ${:,}**".format(cost_of_delay))
    st.markdown("- **Schedule Slip (Days):** {}".format(schedule_slip_days))
    st.markdown("- **Business Impact Risk Level (Synthetic):** {}".format(health))

    # KPI Table
    kpi_df = pd.DataFrame({
        'Metric': ['Energy', 'Velocity Stability', 'Bug Trend', 'Security Posture', 'Customer Escapes'],
        'Value': ['83%', '78%', '12% decrease', '88%', '1.2%']
    })
    st.dataframe(kpi_df)

    swot_master = generate_swot()['Executive']
    st.subheader("Executive SWOT Summary")
    cols_swot = st.columns(4)
    for i, k in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats']):
        with cols_swot[i]:
            st.markdown(f"**{k}**")
            for item in swot_master[k]:
                st.write(f"- {item}")

# Requirements Tab
with tabs[1]:
    st.header("Requirements (V-Cycle & Traceability)")
    with st.expander("Polarion API Configuration"):
        st.text_input("Polarion API URL", polarion_url)
    fig_funnel = go.Figure(go.Funnel(
        y=list(req_data['traceability'].keys()),
        x=list(req_data['traceability'].values()),
        textinfo="value+percent initial"
    ))
    fig_funnel.update_layout(template="plotly_white", title="V-Cycle Traceability Funnel")
    st.plotly_chart(fig_funnel)

    c1, c2 = st.columns(2)
    c1.metric("Traceability Coverage", f"{req_data['coverage_percent']}%")
    c2.metric("Orphaned Requirements", req_data['orphaned_reqs'])

    swot = generate_swot()['Requirements']
    sc1, sc2, sc3, sc4 = st.columns(4)
    for i, key in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats']):
        with [sc1, sc2, sc3, sc4][i]:
            st.markdown(f"### {key}")
            for item in swot[key]:
                st.write(f"- {item}")

# Development Tab
with tabs[2]:
    st.header("Development (Execution & Dependency Risk)")
    with st.expander("Jira/Azure DevOps API Config"):
        st.text_input("DevOps API URL", jira_url)

    fig_burnout = go.Figure()
    fig_burnout.add_trace(go.Bar(x=dev_df['Sprint'], y=dev_df['Planned'], name='Planned', marker_color='lightblue'))
    fig_burnout.add_trace(go.Bar(x=dev_df['Sprint'], y=dev_df['Actual'], name='Actual', marker_color='orange'))
    fig_burnout.add_trace(go.Line(x=dev_df['Sprint'], y=dev_df['Released'], name='Released', mode='lines+markers', line=dict(color='green')))
    fig_burnout.update_layout(template='plotly_white', title='Feature Burnout: Planned vs. Actual vs. Released', barmode='group')
    st.plotly_chart(fig_burnout)

    st.subheader('Dependency Map')
    fig_network = go.Figure()
    for edge in dev_edges:
        fig_network.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name=f"{edge[0]} ? {edge[1]}"))
    fig_network.update_layout(template='plotly_white', title='Team Blocker Dependency Map', showlegend=False)
    st.plotly_chart(fig_network)

    st.subheader('Top 5 Predictive Risk Tickets')
    st.table(risk_tickets_df)

    swot = generate_swot()['Development']
    d1, d2, d3, d4 = st.columns(4)
    for i, key in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats']):
        with [d1, d2, d3, d4][i]:
            st.markdown(f"### {key}")
            for item in swot[key]:
                st.write(f"- {item}")

# CI/CD Tab
with tabs[3]:
    st.header("CI/CD & Integration (Pipeline Health)")
    with st.expander("Jenkins/GitLab API Config"):
        st.text_input("CI/CD API URL", jenkins_url)

    m1, m2, m3 = st.columns(3)
    m1.metric("Last Stable Build ID", cicd_data['last_stable_build'])
    m2.metric("Nightly Pass Rate", f"{cicd_data['nightly_pass_rate']}%")
    m3.metric("Smoke Test Status", cicd_data['smoke_test_status'])

    fig_build = px.bar(cicd_data['build_results'], x='Date', y=['Pass', 'Fail', 'Skip'], template='plotly_white', title='Nightly Build Results (Last 14 Days)')
    st.plotly_chart(fig_build)

    swot = generate_swot()['CI/CD']
    c1, c2, c3, c4 = st.columns(4)
    for i, key in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats']):
        with [c1, c2, c3, c4][i]:
            st.markdown(f"### {key}")
            for item in swot[key]:
                st.write(f"- {item}")

# Testing Tab
with tabs[4]:
    st.header("Testing (Quality & Defect Density)")
    m1, m2 = st.columns(2)
    m1.metric("Total Test Executed", f"{test_data['total_tests_executed']:,}")
    m2.metric("Defect Density (Bugs/KLOC)", f"{test_data['defect_density']}")

    status = "Critical HSI/Middleware issue detected" if test_data['critical_hsi_bugs'] >= 3 else "HSI/Middleware looks manageable"
    st.info(f"What to Worry About: {status} (Critical defects = {test_data['critical_hsi_bugs']})")
    st.warning(f"What NOT to Worry About: UI/cosmetic bugs can be deferred ({test_data['cosmetic_ui_bugs']} currently)")

    swot = generate_swot()['Testing']
    t1, t2, t3, t4 = st.columns(4)
    for i, key in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats']):
        with [t1, t2, t3, t4][i]:
            st.markdown(f"### {key}")
            for item in swot[key]:
                st.write(f"- {item}")

# Executive Finance Tab
with tabs[5]:
    st.header("Executive Financial Metrics")
    st.metric("Cost of Delay", f"${cost_of_delay:,}")
    st.metric("Schedule Slip", f"{schedule_slip_days} days")

    fig_area = px.area(exec_df, x='Sprint', y=['Budget_Burn', 'Feature_Delivery'], template='plotly_white', title='Budget Burn vs. Feature Delivery')
    st.plotly_chart(fig_area)

    st.markdown("---")
    st.markdown("### AI-Driven VP Metrics")
    vp_metrics = pd.DataFrame({
        'Metric': ['Spend Efficiency', 'Delivery Predictability', 'Risk Velocity', 'Audit Readiness'],
        'Value': ['82%', '78%', '60 pts/week', 'High']
    })
    st.table(vp_metrics)

# External enterprise config display (for reference)
st.markdown("---")
st.markdown("#### Configured Enterprise Links")
link_df = pd.DataFrame({
    'Service': ['Polarion', 'Jira/Azure DevOps', 'Jenkins/GitLab', 'CI/CD'],
    'URL': [polarion_url, jira_url, jenkins_url, ci_cd_url]
})
st.table(link_df)

# Final status
st.success('MASTER Project AI Telemetry Control Tower is fully operational.')
