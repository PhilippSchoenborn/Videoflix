import { useState, useRef, useCallback } from 'react';

/**
 * Hook zum Laden eines Videos mit Fehler- und Ladezustand.
 */
export function useVideoLoader(videoUrl: string) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const loadVideo = useCallback(async () => {
    if (!videoRef.current) return;
    setIsLoading(true);
    setError('');
    try {
      videoRef.current.src = videoUrl;
      await new Promise((resolve, reject) => {
        if (!videoRef.current) return reject('Video element not found');
        const handleLoad = () => { setIsLoading(false); resolve(true); };
        const handleError = () => { setError('Failed to load video'); setIsLoading(false); reject('Video failed to load'); };
        videoRef.current.addEventListener('loadeddata', handleLoad);
        videoRef.current.addEventListener('error', handleError);
        return () => {
          if (videoRef.current) {
            videoRef.current.removeEventListener('loadeddata', handleLoad);
            videoRef.current.removeEventListener('error', handleError);
          }
        };
      });
    } catch {
      setError('Failed to load video');
      setIsLoading(false);
    }
  }, [videoUrl]);

  return { videoRef, isLoading, error, loadVideo };
}
