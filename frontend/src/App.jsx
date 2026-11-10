import React, { useState } from 'react';
import { shiftsApi } from './api/shiftsApi';
import { AlertBanner } from './components/AlertBanner';
import { Keypad } from './components/Keypad';
import { TimerDisplay } from './components/TimerDisplay';
import { WorkerCard } from './components/WorkerCard';
import { useShiftTimer } from './hooks/useShiftTimer';

export default function App() {
  const [identificationCode, setIdentificationCode] = useState('');
  const [worker, setWorker] = useState(null);
  const [activeShift, setActiveShift] = useState(null);
  const [lastFinishedShift, setLastFinishedShift] = useState(null);
  const [alert, setAlert] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Hook del cronómetro conectado con el start_time del turno activo
  const { formattedTime } = useShiftTimer(
    activeShift?.start_time,
    Boolean(activeShift)
  );

  const handleDigitClick = (digit) => {
    if (identificationCode.length < 10) {
      setIdentificationCode((prev) => prev + digit);
    }
  };

  const handleDelete = () => {
    setIdentificationCode((prev) => prev.slice(0, -1));
  };

  const handleVerify = async (codeToVerify) => {
    const code = codeToVerify || identificationCode;
    if (!code) {
      setAlert({ type: 'error', message: 'Por favor ingresa un número de cédula.' });
      return;
    }

    setIsLoading(true);
    setAlert(null);
    try {
      const data = await shiftsApi.getCurrentStatus(code);
      setWorker({
        worker_id: data.worker_id,
        identification_code: data.identification_code,
        full_name: data.full_name,
        position: data.position,
      });
      setActiveShift(data.active_shift);
      setLastFinishedShift(null);
      setAlert({
        type: 'success',
        message: `Trabajador ${data.full_name} consultado exitosamente.`,
      });
    } catch (err) {
      setWorker(null);
      setActiveShift(null);
      setAlert({
        type: 'error',
        message: err.message || 'Error al consultar la cédula.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartShift = async () => {
    if (!identificationCode) return;
    setIsLoading(true);
    setAlert(null);
    try {
      const shift = await shiftsApi.startShift(identificationCode);
      setActiveShift(shift);
      setLastFinishedShift(null);
      setAlert({
        type: 'success',
        message: 'Jornada iniciada correctamente.',
      });
    } catch (err) {
      setAlert({
        type: 'error',
        message: err.message || 'Error al iniciar la jornada.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndShift = async () => {
    if (!identificationCode) return;
    setIsLoading(true);
    setAlert(null);
    try {
      const shift = await shiftsApi.endShift(identificationCode);
      setActiveShift(null);
      setLastFinishedShift(shift);
      setAlert({
        type: 'success',
        message: `Jornada finalizada exitosamente. Total trabajado: ${shift.total_minutes} minuto(s).`,
      });
    } catch (err) {
      setAlert({
        type: 'error',
        message: err.message || 'Error al finalizar la jornada.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <main className="mx-auto max-w-5xl px-4 py-10">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
            Terminal de Jornada Laboral
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Sistema de registro y control de entrada y salida de personal
          </p>
        </header>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          {/* Columna Izquierda: Entrada de Cédula, Teclado Táctil y Botones de Acción */}
          <section className="flex flex-col gap-5">
            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
              <label
                htmlFor="identification-input"
                className="block text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Cédula del Trabajador
              </label>

              <div className="mt-2 flex gap-2">
                <input
                  id="identification-input"
                  type="text"
                  maxLength={10}
                  value={identificationCode}
                  onChange={(e) => setIdentificationCode(e.target.value.replace(/\D/g, ''))}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleVerify();
                    }
                  }}
                  placeholder="Ej. 100011"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-2xl font-mono tracking-wider text-slate-900 outline-none transition focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              <div className="mt-5">
                <Keypad
                  onDigitClick={handleDigitClick}
                  onDelete={handleDelete}
                  onVerify={() => handleVerify()}
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Botones de Acción */}
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={handleStartShift}
                disabled={Boolean(activeShift) || !identificationCode || isLoading}
                className="w-full rounded-lg bg-blue-700 py-3 text-base font-medium text-white shadow-sm transition hover:bg-blue-800 active:bg-blue-900 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:opacity-60"
              >
                Iniciar Jornada
              </button>

              <button
                type="button"
                onClick={handleEndShift}
                disabled={!activeShift || isLoading}
                className="w-full rounded-lg bg-slate-800 py-3 text-base font-medium text-white shadow-sm transition hover:bg-slate-900 active:bg-black disabled:cursor-not-allowed disabled:bg-slate-300 disabled:opacity-60"
              >
                Terminar Jornada
              </button>
            </div>
          </section>

          {/* Columna Derecha: Alertas, Información del Trabajador, Cronómetro y Resumen */}
          <section className="flex flex-col gap-5">
            <AlertBanner alert={alert} onClose={() => setAlert(null)} />

            <WorkerCard worker={worker} activeShift={activeShift} />

            <TimerDisplay formattedTime={formattedTime} isActive={Boolean(activeShift)} />

            {/* Resumen de última jornada finalizada */}
            {lastFinishedShift && (
              <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Resumen de Turno Finalizado
                </h3>
                <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-500">Estado:</span>
                    <p className="font-semibold text-emerald-700">COMPLETED</p>
                  </div>
                  <div>
                    <span className="text-slate-500">Minutos Laborados:</span>
                    <p className="font-mono text-xl font-bold text-slate-900">
                      {lastFinishedShift.total_minutes} min
                    </p>
                  </div>
                </div>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
