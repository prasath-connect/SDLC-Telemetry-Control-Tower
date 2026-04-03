import React, { useState } from 'react';
import Header from '../components/Header';
import ExecutiveSummary from '../components/ExecutiveSummary';
import PhaseGrid from '../components/PhaseGrid';
import RiskChart from '../components/RiskChart';
import DependencyGraph from '../components/DependencyGraph';
import { mockJiraTelemetry } from '../data/mockData';
import { calculateOverallMetrics, generateExecutiveSummary, getLeadingIndicator, getRecommendedAction, getRiskOverTimeData, getPhaseAnalysis, getDependencyGraph } from '../utils/riskCalculator';

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
  const dependencyData = getDependencyGraph(mockJiraTelemetry);
  const [selectedPhase, setSelectedPhase] = useState<string>('requirements');
  const selectedPhaseData = phaseAnalysis.find((p) => p.phase === selectedPhase);

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

        <div className="flex gap-2 mb-4">
          {phaseAnalysis.map(phase => (
            <button
              key={phase.phase}
              onClick={() => setSelectedPhase(phase.phase)}
              className={`px-3 py-2 rounded-md border ${phase.phase === selectedPhase ? 'bg-indigo-600 text-white border-indigo-700' : 'bg-white text-slate-800 border-slate-300'}`}
            >
              {phase.phase}
            </button>
          ))}
        </div>

        {selectedPhaseData ? (
          <article className="border rounded-lg p-4 bg-slate-50">
            <h3 className="text-xl font-bold capitalize mb-2">
              {selectedPhaseData.phase} — Risk {selectedPhaseData.overallRisk}%
            </h3>

            <ul className="grid grid-cols-2 gap-3 text-sm pb-3">
              <li><strong>Debate %</strong>: {selectedPhaseData.weightedMetrics.debatePercent}%</li>
              <li><strong>Block %</strong>: {selectedPhaseData.weightedMetrics.blockPercent}%</li>
              <li><strong>Missing Story %</strong>: {selectedPhaseData.weightedMetrics.missingStoryPercent}%</li>
              <li><strong>Dependency Map Score</strong>: {selectedPhaseData.weightedMetrics.dependencyMapScore}%</li>
            </ul>

            <div className="mb-3">
              <h4 className="font-semibold">SWOT Summary</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div><strong>Strengths</strong><ul className="list-disc pl-5">{selectedPhaseData.swot.strengths.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                <div><strong>Weaknesses</strong><ul className="list-disc pl-5">{selectedPhaseData.swot.weaknesses.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                <div><strong>Opportunities</strong><ul className="list-disc pl-5">{selectedPhaseData.swot.opportunities.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
                <div><strong>Threats</strong><ul className="list-disc pl-5">{selectedPhaseData.swot.threats.map((i, idx) => <li key={idx}>{i}</li>)}</ul></div>
              </div>
            </div>

            <div className="mb-3">
              <h4 className="font-semibold">Top 5 Wake-up Risk Signals</h4>
              <ol className="list-decimal pl-5 text-sm">{selectedPhaseData.topRisks.map((item, idx) => <li key={idx}>{item}</li>)}</ol>
            </div>

            <div>
              <h4 className="font-semibold">VP Action Notes</h4>
              <ul className="list-disc pl-5 text-sm">{selectedPhaseData.vpActions.map((item, idx) => <li key={idx}>{item}</li>)}</ul>
            </div>
          </article>
        ) : (
          <p>No phase analysis found.</p>
        )}
      </section>

      <DependencyGraph data={dependencyData} />
    </div>
  );
};

export default Home;