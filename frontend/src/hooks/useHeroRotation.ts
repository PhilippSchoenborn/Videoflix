import { useEffect, useState } from 'react';

export function useHeroRotation(length: number, intervalMs = 8000) {
  const [index, setIndex] = useState(0);
  useEffect(() => {
    if (length > 1) {
      const interval = setInterval(() => {
        setIndex(i => (i + 1) % length);
      }, intervalMs);
      return () => clearInterval(interval);
    }
  }, [length, intervalMs]);
  return [index, setIndex] as const;
}
