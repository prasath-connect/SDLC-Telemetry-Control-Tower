import React from 'react';
import Header from '../components/Header';
import ExecutiveSummary from '../components/ExecutiveSummary';
import PhaseGrid from '../components/PhaseGrid';
import RiskChart from '../components/RiskChart';
import { mockJiraTelemetry } from '../data/mockData';
import { calculateOverallMetrics, generateExecutiveSummary, getLeadingIndicator, getRecommendedAction, getRiskOverTimeData, getPhaseAnalysis } from '../utils/riskCalculator';

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
  const phaseAnalysis = getPhaseAnalysis(mockJiraTelemetry);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Header health={health} budgetAtRisk={budgetAtRisk} scheduleSlip={scheduleSlip} />
      <ExecutiveSummary summary={summary} />
      <PhaseGrid phaseRisks={phaseRisks} indicators={indicators} actions={actions} />
      <RiskChart data={chartData} />

      <section className="bg-white p-6 rounded-lg shadow-lg m-4">
        <h2 className="text-2xl font-semibold mb-4">Integrated Phase Intelligence & VP Snapshot</h2>
        <p className="text-sm text-gray-600 mb-4">
          Consolidated metrics based on Jira-style telemetry, weighted ticket intelligence, dependency map clarity, and predictive risk factors.
          (Debate %, Block %, Missing Stories %, Dependency Map Score)
        </p>
        <div className="space-y-4">
          {phaseAnalysis.map(phase => (
            <article key={phase.phase} className="border rounded-lg p-4 bg-slate-50">
              <h3 className="text-xl font-bold capitalize mb-2">
                {phase.phase} — Risk {phase.overallRisk}%
              </h3>
              <ul className="grid grid-cols-2 gap-3 text-sm pb-3">
                <li><strong>Debate %</strong>: {phase.weightedMetrics.debatePercent}%</li>
                <li><strong>Block %</strong>: {phase.weightedMetrics.blockPercent}%</li>
                <li><strong>Missing Story %</strong>: {phase.weightedMetrics.missingStoryPercent}%</li>
                <li><strong>Dependency Map Score</strong>: {phase.weightedMetrics.dependencyMapScore}%</li>
              </ul>

              <div className="mb-3">
                <h4 className="font-semibold">SWOT Summary</h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div><strong>Strengths</strong><ul className="list-disc pl-5">{phase.swot.strengths.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                  <div><strong>Weaknesses</strong><ul className="list-disc pl-5">{phase.swot.weaknesses.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                  <div><strong>Opportunities</strong><ul className="list-disc pl-5">{phase.swot.opportunities.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                  <div><strong>Threats</strong><ul className="list-disc pl-5">{phase.swot.threats.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                </div>
              </div>

              <div className="mb-3">
                <h4 className="font-semibold">Top 5 Wake-up Risk Signals</h4>
                <ol className="list-decimal pl-5 text-sm">{phase.topRisks.map((item, idx) => <li key={idx}>{item}</li>)}</ol>
              </div>

              <div>
                <h4 className="font-semibold">VP Action Notes</h4>
                <ul className="list-disc pl-5 text-sm">{phase.vpActions.map((item, idx) => <li key={idx}>{item}</li>)}</ul>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;