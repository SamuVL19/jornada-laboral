import React from 'react';

export function AlertBanner({ alert, onClose }) {
  if (!alert) return null;

  const isError = alert.type === 'error';

  return (
    <div
      className={`relative flex items-center justify-between rounded-lg border p-4 text-sm shadow-sm transition-all ${
        isError
          ? 'border-red-200 bg-red-50 text-red-700'
          : 'border-emerald-200 bg-emerald-50 text-emerald-800'
      }`}
    >
      <div className="flex items-center gap-2 pr-6">
        <span className="font-semibold">{isError ? 'Error:' : 'Éxito:'}</span>
        <span>{alert.message}</span>
      </div>

      {onClose && (
        <button
          type="button"
          onClick={onClose}
          className={`rounded p-1 font-bold leading-none hover:opacity-75 ${
            isError ? 'text-red-700' : 'text-emerald-800'
          }`}
          aria-label="Cerrar alerta"
        >
          ×
        </button>
      )}
    </div>
  );
}
