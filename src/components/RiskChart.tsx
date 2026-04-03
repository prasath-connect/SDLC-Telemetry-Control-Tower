import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface RiskChartProps {
  data: { date: string; req: number; design: number; dev: number; integration: number; test: number }[];
}

const RiskChart: React.FC<RiskChartProps> = ({ data }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md m-4">
      <h2 className="text-xl font-semibold mb-4">Risk Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="req" stroke="#8884d8" name="Requirements" />
          <Line type="monotone" dataKey="design" stroke="#82ca9d" name="Design" />
          <Line type="monotone" dataKey="dev" stroke="#ffc658" name="Development" />
          <Line type="monotone" dataKey="integration" stroke="#ff7300" name="Integration" />
          <Line type="monotone" dataKey="test" stroke="#00ff00" name="Test" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskChart;