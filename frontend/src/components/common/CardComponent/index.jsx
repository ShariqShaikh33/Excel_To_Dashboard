import React from 'react'

export function CardComponent({ title, value, subtext, icon: Icon, variant = 'blue' }) {
    const themes = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'border-blue-100' },
    pink: { bg: 'bg-pink-50', text: 'text-pink-600', border: 'border-pink-100' },
    green: { bg: 'bg-green-50', text: 'text-green-600', border: 'border-green-100' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600', border: 'border-purple-100' },
    gray: { bg: 'bg-gray-50', text: 'text-gray-600', border: 'border-gray-200' },
  };

  const selectedTheme = themes[variant] || themes.blue;
  return (
    <div className={`bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between transition-all hover:shadow-md`}>
      <div className="space-y-1">
        {/* Header Section */}
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">{title}</p>
        
        {/* Core Value Accent */}
        <p className="text-2xl font-bold text-gray-800 tracking-tight">{value}</p>
        
        {/* Lower Additional Metadata Section */}
        {subtext && (
          <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
            {subtext}
          </p>
        )}
      </div>

      {/* Decorative Icon Container */}
      {Icon && (
        <div className={`p-3 rounded-xl ${selectedTheme.bg} ${selectedTheme.text}`}>
          <Icon size={22} strokeWidth={2.5} />
        </div>
      )}
    </div>
  )
}
