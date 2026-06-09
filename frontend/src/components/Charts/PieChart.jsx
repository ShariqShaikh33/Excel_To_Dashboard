import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

/**
 * Solid Full-Circle Pie Chart with High-Detail Numeric Grid
 * @param {string} title - Header title label
 * @param {Array} data - Your Redux state array (e.g., representation_ratio)
 * @param {string} dataKey - Numerical mapping property (defaults to "count")
 * @param {string} nameKey - Text category mapping label (defaults to "gender")
 */
function PieChartComponent({ title, data = [], dataKey = "count", nameKey = "gender" }) {
  
  // High-contrast professional palette configuration
  const COLORS = ['#2563eb', '#db2777', '#9333ea', '#f59e0b'];

  // Calculate total cumulative volume to safely generate percentage ratios for the bottom cards
  const totalVolume = data.reduce((sum, item) => sum + (Number(item[dataKey]) || 0), 0);

  // Custom inline label renderer for the inside of the pie slices
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const RADIAN = Math.PI / 180;
    // For a solid pie, setting the multiplier to 0.6 places text perfectly inside the slice bounds
    const radius = outerRadius * 0.6;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (percent < 0.03) return null; // Skips rendering for tiny segments to keep text clean

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor="middle" 
        dominantBaseline="central"
        className="text-[12px] font-bold tracking-wider"
      >
        {`${(percent * 100).toFixed(1)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-xs flex flex-col w-full min-h-[460px]">
      {/* Chart Header Title */}
      <div className="mb-2">
        <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider">{title}</h3>
      </div>

      {/* 1. Chart Canvas Area */}
      <div className="h-56 w-full min-h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              dataKey={dataKey}
              nameKey={nameKey}
              innerRadius={0}             // CRITICAL: Changing this to 0 transforms the donut into a full circle
              outerRadius={85}            // Radius boundary size perimeter
              labelLine={false}
              label={renderCustomizedLabel}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]} 
                  className="focus:outline-none transition-all duration-200 hover:opacity-85 cursor-pointer"
                />
              ))}
            </Pie>

            <Tooltip 
              formatter={(value) => [`${value.toLocaleString()} Candidates`, 'Volume']}
              contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '12px' }}
              itemStyle={{ color: '#f8fafc', fontSize: '12px', fontWeight: '500' }}
              labelStyle={{ display: 'none' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* 2. Enhanced Native Grid Layout (Renders names and numbers below the chart) */}
      <div className="mt-6 border-t border-slate-50 pt-6 space-y-3">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">
          Detailed Metrics Breakdowns
        </span>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {data.map((item, index) => {
            const countValue = Number(item[dataKey]) || 0;
            const percentage = totalVolume > 0 ? ((countValue / totalVolume) * 100).toFixed(1) : '0.0';
            
            return (
              <div 
                key={index} 
                className="flex items-center justify-between p-3 rounded-xl border border-slate-50 bg-slate-50/40"
                >
                {/* Colored Legend Dot and Name */}
                <div className="flex items-center gap-2.5 min-w-0">
                  <span 
                    className="w-2.5 h-2.5 rounded-full shrink-0" 
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  />
                  <span className="text-xs font-bold text-slate-600 capitalize truncate">
                    {item[nameKey]}
                  </span>
                </div>
                
                {/* Numeric Summary Values */}
                <div className="text-right pl-2 shrink-0">
                  <span className="text-xs font-black text-slate-800 block">
                    {countValue.toLocaleString()}
                  </span>
                  <span className="text-[10px] font-medium text-slate-400 block">
                    {percentage}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default PieChartComponent;