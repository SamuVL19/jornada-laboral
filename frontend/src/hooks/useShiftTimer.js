import { useEffect, useState } from 'react';

function calculateElapsedSeconds(startTime) {
  if (!startTime) return 0;
  const start = new Date(startTime).getTime();
  const now = Date.now();
  const diffInSeconds = Math.floor((now - start) / 1000);
  return diffInSeconds > 0 ? diffInSeconds : 0;
}

function formatSeconds(totalSecs) {
  const hours = Math.floor(totalSecs / 3600);
  const minutes = Math.floor((totalSecs % 3600) / 60);
  const seconds = totalSecs % 60;

  const hh = String(hours).padStart(2, '0');
  const mm = String(minutes).padStart(2, '0');
  const ss = String(seconds).padStart(2, '0');

  return `${hh}:${mm}:${ss}`;
}

export function useShiftTimer(startTime, isRunning) {
  const [totalSeconds, setTotalSeconds] = useState(() => {
    if (isRunning && startTime) {
      return calculateElapsedSeconds(startTime);
    }
    return 0;
  });

  useEffect(() => {
    if (!isRunning || !startTime) {
      setTotalSeconds(0);
      return;
    }

    // Calcula inmediatamente para sincronizar en montajes o recargas de página
    setTotalSeconds(calculateElapsedSeconds(startTime));

    const intervalId = setInterval(() => {
      setTotalSeconds(calculateElapsedSeconds(startTime));
    }, 1000);

    return () => clearInterval(intervalId);
  }, [startTime, isRunning]);

  return {
    formattedTime: formatSeconds(totalSeconds),
    totalSeconds,
  };
}
