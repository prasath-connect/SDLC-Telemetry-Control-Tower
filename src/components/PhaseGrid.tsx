import React from 'react';

interface PhaseCardProps {
  phase: string;
  risk: number;
  indicator: string;
  action: string;
}

const PhaseCard: React.FC<PhaseCardProps> = ({ phase, risk, indicator, action }) => {
  const color = risk > 75 ? 'bg-red-100 border-red-500' : risk > 50 ? 'bg-yellow-100 border-yellow-500' : 'bg-green-100 border-green-500';
  return (
    <div className={`p-4 rounded-lg border-2 ${color} m-2`}>
      <h3 className="text-lg font-bold capitalize">{phase}</h3>
      <p className="text-2xl font-semibold">{Math.round(risk)}%</p>
      <p className="text-sm">Leading Indicator: {indicator}</p>
      <p className="text-sm">Action: {action}</p>
    </div>
  );
};

interface PhaseGridProps {
  phaseRisks: { req: number; design: number; dev: number; integration: number; test: number };
  indicators: { [key: string]: string };
  actions: { [key: string]: string };
}

const PhaseGrid: React.FC<PhaseGridProps> = ({ phaseRisks, indicators, actions }) => {
  return (
    <div className="grid grid-cols-5 gap-4 p-4">
      <PhaseCard phase="Requirements" risk={phaseRisks.req} indicator={indicators.req} action={actions.req} />
      <PhaseCard phase="Design" risk={phaseRisks.design} indicator={indicators.design} action={actions.design} />
      <PhaseCard phase="Development" risk={phaseRisks.dev} indicator={indicators.dev} action={actions.dev} />
      <PhaseCard phase="Integration" risk={phaseRisks.integration} indicator={indicators.integration} action={actions.integration} />
      <PhaseCard phase="Test" risk={phaseRisks.test} indicator={indicators.test} action={actions.test} />
    </div>
  );
};

export default PhaseGrid;