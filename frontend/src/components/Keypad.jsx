import React from 'react';

export function Keypad({ onDigitClick, onDelete, onVerify, disabled = false }) {
  const digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];

  return (
    <div className="grid grid-cols-3 gap-3 w-full">
      {digits.map((digit) => (
        <button
          key={digit}
          type="button"
          disabled={disabled}
          onClick={() => onDigitClick(digit)}
          className="h-14 rounded-lg border border-slate-200 bg-white text-xl font-semibold text-slate-900 shadow-sm transition-colors hover:bg-slate-100 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {digit}
        </button>
      ))}

      <button
        type="button"
        disabled={disabled}
        onClick={onDelete}
        className="h-14 rounded-lg border border-slate-200 bg-white text-base font-semibold text-slate-700 shadow-sm transition-colors hover:bg-slate-100 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Borrar
      </button>

      <button
        type="button"
        disabled={disabled}
        onClick={() => onDigitClick('0')}
        className="h-14 rounded-lg border border-slate-200 bg-white text-xl font-semibold text-slate-900 shadow-sm transition-colors hover:bg-slate-100 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
      >
        0
      </button>

      <button
        type="button"
        disabled={disabled}
        onClick={onVerify}
        className="h-14 rounded-lg border border-blue-200 bg-blue-50 text-base font-semibold text-blue-700 shadow-sm transition-colors hover:bg-blue-100 active:bg-blue-200 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Consultar
      </button>
    </div>
  );
}
