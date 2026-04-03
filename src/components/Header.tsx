import React from 'react';

interface HeaderProps {
  health: string;
  budgetAtRisk: number;
  scheduleSlip: number;
}

const Header: React.FC<HeaderProps> = ({ health, budgetAtRisk, scheduleSlip }) => {
  const color = health === 'Red' ? 'bg-red-500' : health === 'Amber' ? 'bg-yellow-500' : 'bg-green-500';
  return (
    <div className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Executive Predictive Risk Dashboard</h1>
      <div className="flex space-x-4">
        <div className="flex items-center">
          <span className={`w-4 h-4 rounded-full ${color} mr-2`}></span>
          <span>Project Health: {health}</span>
        </div>
        <div>Budget at Risk: ${budgetAtRisk.toLocaleString()}</div>
        <div>Schedule Slip: {scheduleSlip} days</div>
      </div>
    </div>
  );
};

export default Header;