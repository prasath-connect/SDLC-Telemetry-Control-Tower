import React from 'react';
import Header from '../components/Header';
import ExecutiveSummary from '../components/ExecutiveSummary';
import PhaseGrid from '../components/PhaseGrid';
import RiskChart from '../components/RiskChart';
import { mockJiraTelemetry } from '../data/mockData';
import { calculateOverallMetrics, generateExecutiveSummary, getLeadingIndicator, getRecommendedAction, getRiskOverTimeData } from '../utils/riskCalculator';

const Home: React.FC = () => {
  const { phaseRisks, health, budgetAtRisk, scheduleSlip } = calculateOverallMetrics(mockJiraTelemetry);
  const summary = generateExecutiveSummary(mockJiraTelemetry);
  const indicators = {
    req: getLeadingIndicator('req', mockJiraTelemetry),
    design: getLeadingIndicator('design', mockJiraTelemetry),
    dev: getLeadingIndicator('dev', mockJiraTelemetry),
    integration: getLeadingIndicator('integration', mockJiraTelemetry),
    test: getLeadingIndicator('test', mockJiraTelemetry),
  };
  const actions = {
    req: getRecommendedAction('req', mockJiraTelemetry),
    design: getRecommendedAction('design', mockJiraTelemetry),
    dev: getRecommendedAction('dev', mockJiraTelemetry),
    integration: getRecommendedAction('integration', mockJiraTelemetry),
    test: getRecommendedAction('test', mockJiraTelemetry),
  };
  const chartData = getRiskOverTimeData(mockJiraTelemetry);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header health={health} budgetAtRisk={budgetAtRisk} scheduleSlip={scheduleSlip} />
      <ExecutiveSummary summary={summary} />
      <PhaseGrid phaseRisks={phaseRisks} indicators={indicators} actions={actions} />
      <RiskChart data={chartData} />
    </div>
  );
};

export default Home;