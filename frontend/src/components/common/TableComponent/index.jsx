// src/components/Table.jsx
import React from 'react';

export default function TableComponent({ title, columns, data }) {
  // Gracefully handle empty array buffers or load delays
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-100 p-6 text-center text-gray-400 font-medium">
        No records available to display.
      </div>
    );
  }

  // Extract key strings from the custom props object structure
  const columnKeys = Object.keys(columns);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      {title && (
        <div className="px-6 py-4 border-b border-gray-50">
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
        </div>
      )}
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          {/* 1. DYNAMIC HEADER GENERATION */}
          <thead className="bg-gray-50/70 border-b border-gray-100">
            <tr>
              {columnKeys.map((key) => (
                <th 
                  key={key} 
                  className="px-6 py-3 text-xs font-bold uppercase tracking-wider text-gray-500 whitespace-nowrap"
                >
                  {columns[key]}
                </th>
              ))}
            </tr>
          </thead>

          {/* 2. DYNAMIC ROW ITERATION */}
          <tbody className="divide-y divide-gray-50">
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50/40 transition-colors">
                {columnKeys.map((key) => {
                  const rawValue = row[key];
                  
                  // Clean cell formatter for numbers, arrays, or text strings
                  const renderedValue = typeof rawValue === 'number' 
                    ? rawValue.toLocaleString() 
                    : rawValue;

                  return (
                    <td 
                      key={key} 
                      className="px-6 py-3.5 text-sm font-semibold text-gray-600 whitespace-nowrap"
                    >
                      {renderedValue !== undefined && renderedValue !== null ? renderedValue : '—'}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}