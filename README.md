# Predictive Risk Dashboard (Python + Streamlit) - Enterprise Edition

A Streamlit application for executive predictive risk assessment in automotive software engineering portfolios, now with CSV ingestion, Monte Carlo simulations, and LLM integration.

## Features

- **CSV Data Ingestion**: Upload Jira extracts or use mock data with simulation mode warning
- **Overall Portfolio Health**: RAG status based on SDLC phase risks
- **Executive Summary**: Dynamic AI-generated insights with optional LLM integration
- **Phase Breakdown**: 5 SDLC phases with risk scores, indicators, and actions
- **Schedule Probability Engine**: Monte Carlo simulations for delivery date predictions
- **Telemetry Chart**: Trend visualization of velocity vs. defect rates

## Installation

1. Ensure Python 3.8+ is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Open `http://localhost:8501` in your browser.

## Project Structure

- `app.py`: Main Streamlit application with enterprise features
- `requirements.txt`: Python dependencies (streamlit, pandas, plotly, numpy)

## New Enterprise Features

- **CSV Upload**: Sidebar file uploader for Jira telemetry data
- **Sample Template**: Download button for CSV schema guidance
- **Monte Carlo Engine**: 1,000 simulations for schedule risk assessment
- **LLM Integration**: Optional API key for AI-powered executive summaries

## Risk Calculation Logic

Predictive Risk Scores (0-100%) calculated for each SDLC phase:
- **Requirements**: Base 10 + 20 per dependency >14 days old
- **Design**: Base 15 + 30 if sign-offs missing
- **Development**: 85 if velocity drops >15% below 3-sprint average
- **Integration**: CI/CD failure rate + 20 for blocked deliveries
- **Test**: Defect escape rate + 40 for critical bugs near release

Critical risk (>75%) triggers Red status and executive actions.