import React from 'react';

/**
 * DataMatrixTable Component
 * @param {Array<string>} headers - Header array labels, e.g., ["Status", "Male", "Female", "Other", "Total"]
 * @param {Array<Object>} rows - Array of row items directly from your Redux store payload
 * @param {Array<string>} keys - Array of object property keys to read in order, e.g., ["status", "male", "female", "other", "total"]
 */
function TableComponent({ headers, rows = [], keys = [] }) {
  
  // Safe fallback if data hasn't loaded or is structured incorrectly
  if (!rows || rows.length === 0) {
    return (
      <div className="w-full bg-white p-8 text-center rounded-2xl border border-slate-100 text-slate-400 font-medium text-sm">
        No matrix data available to display.
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-2xl border border-slate-100 shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-sm">
          
          {/* Table Sticky Header */}
          <thead className="bg-slate-50/80 border-b border-slate-100 backdrop-blur-xs">
            <tr>
              {headers.map((header, idx) => {
                // Style rule: First column aligns left (text labels), all numeric columns align center
                const isFirstColumn = idx === 0;
                const isLastColumn = idx === headers.length - 1;
                
                return (
                  <th
                    key={idx}
                    className={`px-6 py-4 font-bold text-slate-500 uppercase tracking-wider text-[11px] ${
                      isFirstColumn ? 'text-left' : 'text-center'
                    } ${
                      isLastColumn ? 'bg-slate-100/50 text-slate-700 font-extrabold' : ''
                    }`}
                  >
                    {header}
                  </th>
                );
              })}
            </tr>
          </thead>

          {/* Table Body */}
          <tbody className="divide-y divide-slate-100/70">
            {rows.map((row, rowIdx) => (
              <tr
                key={rowIdx}
                className="hover:bg-slate-50/60 transition-colors duration-150 group"
              >
                {keys.map((key, keyIdx) => {
                  const cellValue = row[key];
                  const isFirstColumn = keyIdx === 0;
                  const isLastColumn = keyIdx === keys.length - 1;

                  return (
                    <td
                      key={keyIdx}
                      className={`px-6 py-3.5 whitespace-nowrap text-xs font-semibold ${
                        isFirstColumn
                          ? 'text-slate-700 font-bold capitalize text-left' // Format text label rows
                          : 'text-slate-600 text-center'                     // Format metric count columns
                      } ${
                        // Visually highlight the aggregate column values on the far right
                        isLastColumn ? 'bg-slate-50/40 text-slate-900 font-black border-l border-slate-50' : ''
                      }`}
                    >
                      {/* Formats native raw numbers with commas (e.g. 24050 -> 24,050) while preserving string categories */}
                      {typeof cellValue === 'number' ? cellValue.toLocaleString() : cellValue}
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

export default TableComponent;