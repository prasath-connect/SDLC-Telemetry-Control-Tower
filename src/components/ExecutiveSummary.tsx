import React from 'react';

interface ExecutiveSummaryProps {
  summary: string;
}

const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({ summary }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md m-4">
      <h2 className="text-xl font-semibold mb-4">Executive Summary</h2>
      <p>{summary}</p>
    </div>
  );
};

export default ExecutiveSummary;