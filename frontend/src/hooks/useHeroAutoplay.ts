import { useEffect } from 'react';
import type { Video } from '../types';

export function useHeroAutoplay(
  currentHeroVideo: Video | null,
  heroVideoRef: HTMLVideoElement | null,
  setIsHeroPlaying: (b: boolean) => void
) {
  useEffect(() => {
    if (currentHeroVideo && heroVideoRef) {
      const playHeroVideo = async () => {
        try {
          setIsHeroPlaying(true);
          heroVideoRef.currentTime = 0;
          heroVideoRef.volume = 0.3;
          heroVideoRef.muted = false;
          await heroVideoRef.play();
          setTimeout(() => {
            if (heroVideoRef) {
              heroVideoRef.pause();
              setIsHeroPlaying(false);
            }
          }, 6000);
        } catch {
          setIsHeroPlaying(false);
        }
      };
      const timeout = setTimeout(playHeroVideo, 1000);
      return () => clearTimeout(timeout);
    }
  }, [currentHeroVideo, heroVideoRef, setIsHeroPlaying]);
}
