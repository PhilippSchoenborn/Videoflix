import { useState, useCallback } from 'react';
import type { Video, SearchFilters } from '../types';

export function useVideoFilters(allVideos: Video[]) {
  const [filteredVideos, setFilteredVideos] = useState<Video[]>(allVideos);

  const handleFiltersChange = useCallback((filters: SearchFilters) => {
    let filtered = [...allVideos];
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(video =>
        video.title.toLowerCase().includes(searchTerm) ||
        video.description.toLowerCase().includes(searchTerm) ||
        video.genre?.name.toLowerCase().includes(searchTerm)
      );
    }
    if (filters.genre) {
      filtered = filtered.filter(video => video.genre?.id === filters.genre);
    }
    if (filters.age_rating) {
      filtered = filtered.filter(video => video.age_rating === filters.age_rating);
    }
    if (filters.featured) {
      filtered = filtered.filter(video => video.is_featured);
    }
    setFilteredVideos(filtered);
  }, [allVideos]);

  return { filteredVideos, handleFiltersChange };
}
