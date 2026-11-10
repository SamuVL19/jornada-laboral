import React from 'react';

export function WorkerCard({ worker, activeShift }) {
  if (!worker) {
    return (
      <div className="rounded-lg border border-dashed border-slate-200 bg-white p-6 text-center text-slate-500 shadow-sm">
        <p className="text-sm">Digita una cédula y presiona "Consultar" para ver los datos del trabajador.</p>
      </div>
    );
  }

  const formatStartTime = (isoString) => {
    if (!isoString) return '--';
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Cédula: {worker.identification_code}
          </span>
          <h2 className="mt-1 text-xl font-bold text-slate-900">{worker.full_name}</h2>
          <p className="text-sm text-slate-600">{worker.position}</p>
        </div>

        {activeShift ? (
          <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            En Turno
          </div>
        ) : (
          <div className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
            Sin Jornada Activa
          </div>
        )}
      </div>

      {activeShift && (
        <div className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-500">
          <span className="font-medium text-slate-700">Hora de inicio:</span>{' '}
          {formatStartTime(activeShift.start_time)}
        </div>
      )}
    </div>
  );
}
