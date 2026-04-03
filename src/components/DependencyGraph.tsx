import React from 'react';
import { DepGraphData, DepEdge } from '../utils/riskCalculator';

interface DependencyGraphProps {
  data: DepGraphData;
}

const nodeOrder = ['requirements', 'design', 'development', 'integration', 'test'];

const DependencyGraph: React.FC<DependencyGraphProps> = ({ data }) => {
  const width = 720;
  const height = 220;
  const margin = 50;
  const step = (width - 2 * margin) / (nodeOrder.length - 1);
  const centerY = height / 2;

  const coords = nodeOrder.reduce((acc, phase, i) => {
    acc[phase] = { x: margin + i * step, y: centerY };
    return acc;
  }, {} as { [phase: string]: { x: number; y: number } });

  const getStrokeWidth = (weight: number) => Math.min(14, Math.max(2, weight / 5));

  return (
    <div className="p-4 bg-white rounded-lg shadow-md m-4">
      <h2 className="text-xl font-semibold mb-2">Dependency Graph Positioning</h2>
      <p className="text-sm text-gray-600 mb-4">Fast dependency flow snapshot (higher weight = higher risk/criticality).</p>
      <svg width={width} height={height}>
        {data.edges.map((edge: DepEdge, idx: number) => {
          const src = coords[edge.source];
          const tgt = coords[edge.target];
          if (!src || !tgt) return null;
          const midX = (src.x + tgt.x) / 2;
          return (
            <g key={idx}>
              <line
                x1={src.x}
                y1={src.y}
                x2={tgt.x}
                y2={tgt.y}
                stroke="#c026d3"
                strokeWidth={getStrokeWidth(edge.weight)}
                markerEnd="url(#arrowhead)"
                opacity={0.7}
              />
              <text x={midX} y={src.y - 15} textAnchor="middle" className="text-xs fill-purple-700">
                {edge.label} ({edge.weight.toFixed(0)})
              </text>
            </g>
          );
        })}
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#c026d3" />
          </marker>
        </defs>

        {nodeOrder.map((phase) => {
          const c = coords[phase];
          return (
            <g key={phase}>
              <circle cx={c.x} cy={c.y} r={20} fill="#2563eb" />
              <text x={c.x} y={c.y + 5} textAnchor="middle" className="text-sm font-semibold fill-white capitalize">
                {phase}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default DependencyGraph;
