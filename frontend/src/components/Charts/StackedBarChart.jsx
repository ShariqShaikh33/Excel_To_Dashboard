import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * StackedBarChartCard - Visualizes academic tiers broken down by gender subsets
 * @param {string} title - Header card display title
 * @param {Array<Object>} data - Redux array stream matrix (e.g., education_gender_matrix)
 * @param {string} xKey - The categorical baseline field for X-Axis (e.g., "education")
 */
function StackedBarChartCard({ title, data = [], xKey = "education" }) {
  
  // Custom brand colors matching your application style sheets
  const GENDER_COLORS = {
    male: '#2563eb',   // Vivid Blue
    female: '#db2777', // Deep Pink
    other: '#9333ea'   // Royal Purple
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-xs flex flex-col w-full h-[380px]">
      {/* Title Header Block */}
      <div className="mb-6">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          {title}
        </h3>
      </div>

      {/* Chart Canvas Area */}
      <div className="flex-1 w-full h-full min-h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: -20, bottom: 5 }}
          >
            {/* Horizontal Gridlines for structural scanning balance */}
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            
            {/* X-Axis: Maps educational tiers */}
            <XAxis 
              dataKey={xKey} 
              tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} 
              stroke="#e2e8f0"
              tickFormatter={(str) => str.replace(' degree', '')} // Compacts labels to fit neatly
            />
            
            {/* Y-Axis: Formats scale increments */}
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} stroke="#e2e8f0" />
            
            {/* Interactive Hover Tooltip */}
            <Tooltip 
              cursor={{ fill: '#f8fafc', opacity: 0.6 }}
              contentStyle={{ 
                backgroundColor: '#0f172a', 
                border: 'none', 
                borderRadius: '12px',
                padding: '10px 14px'
              }}
              itemStyle={{ fontSize: '12px', fontWeight: '500', color: '#f8fafc' }}
              labelStyle={{ color: '#94a3b8', fontSize: '11px', fontWeight: '700', marginBottom: '4px', textTransform: 'uppercase' }}
            />
            
            {/* Centered Descriptive Legend Index Indicator */}
            <Legend 
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '12px', fontWeight: '600', paddingTop: '12px' }}
              formatter={(value) => <span className="text-slate-500 capitalize ml-1">{value}</span>}
            />

            {/* Stacked Data Columns - Matching stackId binds them to a single column */}
            <Bar dataKey="male" stackId="educationStack" fill={GENDER_COLORS.male} name="male" radius={[0, 0, 0, 0]} />
            <Bar dataKey="female" stackId="educationStack" fill={GENDER_COLORS.female} name="female" radius={[0, 0, 0, 0]} />
            {/* Only top element of the stack gets rounded top corners for a polished layout */}
            <Bar dataKey="other" stackId="educationStack" fill={GENDER_COLORS.other} name="other" radius={[4, 4, 0, 0]} />
            
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default StackedBarChartCard;