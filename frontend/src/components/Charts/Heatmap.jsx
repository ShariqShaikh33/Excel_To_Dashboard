import React from 'react';

/**
 * HeatmapMatrix - Renders a 2D grid where cell backgrounds scale by density
 * @param {string} title - Header card title
 * @param {Array<string>} xLabels - Columns labels (e.g., Employment Statuses)
 * @param {Array<string>} yLabels - Row labels (e.g., Top Specializations/Majors)
 * @param {Array<Object>} data - Matrix grid array rows
 * @param {string} dataKey - The field holding the identifier matching yLabels
 */
function Heatmap({ title, xLabels, yLabels, data=[], dataKey = "level" }) {
  
  // Helper to safely find the max value across the entire matrix to calculate proportional opacity scaling
  const maxVal = Math.max(
    ...data.flatMap(row => 
      xLabels?.map(col => Number(row[col.toLowerCase().replace(/[^a-z0-9]/g, '_')]) || 0)
    ), 1
  );
  console.log(data)
  return (
    <div className="w-full bg-white p-6 rounded-2xl border border-slate-100 shadow-xs flex flex-col">
      {/* Title block & Legend indicator */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider">{title}</h3>
          <p className="text-xs text-slate-400 mt-0.5">Color intensity reflects absolute candidate concentrations.</p>
        </div>
        {/* Heatmap Legend Scale Bar */}
        <div className="flex items-center gap-2 self-start">
          <span className="text-[10px] font-bold text-slate-400 uppercase">Less</span>
          <div className="w-24 h-2.5 rounded-sm bg-linear-to-r from-blue-50 to-blue-600 border border-slate-100" />
          <span className="text-[10px] font-bold text-slate-400 uppercase">More</span>
        </div>
      </div>

      {/* Grid Wrapper Canvas */}
      <div className="overflow-x-auto w-full">
        <table className="w-full border-spacing-1 border-separate table-fixed min-w-[640px]">
          <thead>
            <tr>
              {/* Empty corner cell */}
              <th className="w-1/4 p-2 text-left text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                Specialization
              </th>
              {xLabels?.map((colLabel, idx) => (
                
                <th 
                  key={idx} 
                  className="p-2 text-center text-[10px] font-bold text-slate-500 uppercase tracking-wide whitespace-normal break-words"
                >
                  {colLabel}
                </th>
              ))}
            </tr>
          </thead>
          
          <tbody>
            {yLabels?.map((rowLabel, rowIdx) => {
              // Find the corresponding object data row matching our text row identifier
              const dataRow = data.find(item => String(item[dataKey]).toLowerCase() === rowLabel.toLowerCase()) || {};
              console.log(dataRow);
              
              return (
                <tr key={rowIdx} className="hover:bg-slate-50/40">
                  {/* Row Sticky Axis Header Label */}
                  <td className="p-2 text-xs font-bold text-slate-700 capitalize truncate bg-slate-50/50 rounded-lg border border-slate-100/50">
                    {rowLabel}
                  </td>

                  {/* Loop through data intersections to drop shaded cells */}
                  {xLabels.map((colLabel, colIdx) => {
                    // Match object property string styling conventions (e.g., "Unemployed" -> "unemployed")
                    const formattedColKey = colLabel.toLowerCase().replace(/[^a-z0-9]/g, '_');
                    const cellValue = Number(dataRow[formattedColKey]) || 0;
                    
                    // Proportional Alpha Density Calculations
                    const ratio = cellValue / maxVal;
                    
                    return (
                      <td
                        key={colIdx}
                        style={{
                          // Tailwind text handling dynamically mixed with reactive CSS inline variables
                          backgroundColor: cellValue > 0 ? `rgba(37, 99, 235, ${Math.max(ratio, 0.04)})` : '#f8fafc',
                          color: ratio > 0.55 ? '#ffffff' : '#1e293b'
                        }}
                        className={`p-3 text-center rounded-lg font-bold text-xs transition-all duration-150 border relative group cursor-help ${
                          cellValue > 0 ? 'border-blue-200/20' : 'border-slate-100/40'
                        }`}
                      >
                        {cellValue.toLocaleString()}

                        {/* Native Floating Micro-Tooltip overlay */}
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:block z-30 bg-slate-900 text-white text-[10px] px-2 py-1 rounded shadow-md font-medium whitespace-nowrap pointer-events-none">
                          {rowLabel} × {colLabel}: {cellValue.toLocaleString()}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Heatmap;