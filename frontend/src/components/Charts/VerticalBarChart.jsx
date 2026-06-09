import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

/**
 * VerticalBarChartCard - Visualizes a simple 1D categorical frequency array
 * @param {string} title - Header card display title
 * @param {Array<Object>} data - Redux state array (e.g., attainment_ladder)
 * @param {string} xKey - Object string property key for the horizontal axis (e.g., "level")
 * @param {string} yKey - Object numeric property key for bar height (e.g., "count")
 */
function VerticalBarChartCard({ title, data = [], xKey = "level", yKey = "count" }) {
  
  // Clean monochromatic blue gradient scheme to represent scale progression
  const BASE_COLOR = '#2563eb';

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-xs flex flex-col w-full h-[380px]">
      {/* Title Header Block */}
      <div className="mb-6 flex items-center justify-between">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          {title}
        </h3>
        <span className="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">
          Candidate Volume
        </span>
      </div>

      {/* Chart Canvas Area */}
      <div className="flex-1 w-full h-full min-h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: -20, bottom: 5 }}
          >
            {/* Horizontal reference rules for crisp measurement scanning */}
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            
            {/* X-Axis Setup */}
            <XAxis 
              dataKey={xKey} 
              tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} 
              stroke="#e2e8f0"
              tickFormatter={(str) => str.replace(' school', '').replace(' degree', '')} // Cleans long titles
            />
            
            {/* Y-Axis Setup */}
            <YAxis 
              tick={{ fontSize: 11, fill: '#64748b' }} 
              stroke="#e2e8f0"
              allowDecimals={false}
            />
            
            {/* High-Detail Interactive Tooltip */}
            <Tooltip 
              cursor={{ fill: '#f8fafc', opacity: 0.8 }}
              contentStyle={{ 
                backgroundColor: '#0f172a', 
                border: 'none', 
                borderRadius: '12px',
                padding: '10px 14px'
              }}
              itemStyle={{ fontSize: '12px', fontWeight: '600', color: '#f8fafc' }}
              formatter={(value) => [`${value.toLocaleString()} Candidates`, 'Total']}
              labelStyle={{ color: '#94a3b8', fontSize: '11px', fontWeight: '700', marginBottom: '2px', textTransform: 'uppercase' }}
            />

            {/* Column Render Definition */}
            <Bar 
              dataKey={yKey} 
              fill={BASE_COLOR} 
              radius={[6, 6, 0, 0]} // Applies a smooth curved corner to the top of each bar
              maxBarSize={55}       // Prevents bars from looking awkwardly wide on wide screens
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default VerticalBarChartCard;