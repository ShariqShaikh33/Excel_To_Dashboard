import React from 'react';
import * as Icons from 'lucide-react';

/**
 * Reusable KPI Summary Metric Card
 * @param {string} title - The uppercase header label (e.g., "TOTAL CANDIDATES")
 * @param {string|number} value - The main bold display figure (e.g., "50,000")
 * @param {string} iconName - Valid string name of a Lucide React icon (e.g., "Users")
 * @param {string} themeColor - Color palette token: 'blue' | 'emerald' | 'purple' | 'amber'
 * @param {string} subtext - Supporting baseline context string
 * @param {string} badgeText - Optional pill text (e.g., "+12% completed")
 */

export function CardComponent({ 
  title, 
  value, 
  iconName, 
  themeColor = 'blue', 
  subtext, 
  badgeText 
}) {
  // Dynamically extract the component from the Lucide icon dictionary
  const IconComponent = Icons[iconName] || Icons.HelpCircle;

  // Visual style maps matching our global color library tokens
  const themeStyles = {
    blue: {
      bg: 'bg-blue-50/60 text-blue-600 border-blue-100',
      badge: 'bg-blue-50 text-blue-700 border-blue-100'
    },
    emerald: {
      bg: 'bg-emerald-50/60 text-emerald-600 border-emerald-100',
      badge: 'bg-emerald-50 text-emerald-700 border-emerald-100'
    },
    purple: {
      bg: 'bg-purple-50/60 text-purple-600 border-purple-100',
      badge: 'bg-purple-50 text-purple-700 border-purple-100'
    },
    amber: {
      bg: 'bg-amber-50/60 text-amber-600 border-amber-100',
      badge: 'bg-amber-50 text-amber-700 border-amber-100'
    }
  };

  const currentTheme = themeStyles[themeColor] || themeStyles.blue;

  return (
    <div className="bg-white w-36 p-6 rounded-2xl shadow-xs border border-slate-100 flex items-start justify-between hover:shadow-md transition-all duration-200">
      <div className="space-y-2">
        <span className="text-xs font-semibold text-slate-400 tracking-wider uppercase block">
          {title}
        </span>
        
        <h3 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          {value}
        </h3>
        
        <div className="flex items-center gap-2 flex-wrap">
          {badgeText && (
            <span className={`text-[8px] font-medium px-2 py-0.5 rounded-md border ${currentTheme.badge}`}>
              {badgeText}
            </span>
          )}
          {subtext && (
            <span className="text-xs text-slate-400 font-medium">
              {subtext}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
