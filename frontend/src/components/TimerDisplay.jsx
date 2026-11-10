import React from 'react';

export function TimerDisplay({ formattedTime, isActive }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm">
      <span className="text-xs font-bold tracking-widest text-slate-400">
        TIEMPO TRANSCURRIDO
      </span>
      <div className={`mt-2 font-mono text-5xl font-semibold tracking-tight tabular-nums ${
        isActive ? 'text-slate-900' : 'text-slate-300'
      }`}>
        {formattedTime || '00:00:00'}
      </div>
      <p className="mt-2 text-xs text-slate-500">
        {isActive ? 'Cronómetro en ejecución sincronizado con el servidor' : 'Sin turno activo'}
      </p>
    </div>
  );
}
