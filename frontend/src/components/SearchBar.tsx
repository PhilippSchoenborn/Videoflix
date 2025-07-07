import React, { useState, useEffect } from 'react';
import { Search, Filter, X } from 'lucide-react';
import type { Genre, SearchFilters } from '../types';
import styles from './SearchBar.module.css';

interface SearchBarProps {
  genres: Genre[];
  onFiltersChange: (filters: SearchFilters) => void;
  placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  genres, 
  onFiltersChange, 
  placeholder = "Search movies and shows..." 
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGenre, setSelectedGenre] = useState<number | undefined>();
  const [selectedAgeRating, setSelectedAgeRating] = useState<string | undefined>();
  const [showFeaturedOnly, setShowFeaturedOnly] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      onFiltersChange({
        search: searchTerm || undefined,
        genre: selectedGenre,
        age_rating: selectedAgeRating,
        featured: showFeaturedOnly || undefined,
      });
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, selectedGenre, selectedAgeRating, showFeaturedOnly, onFiltersChange]);

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedGenre(undefined);
    setSelectedAgeRating(undefined);
    setShowFeaturedOnly(false);
  };

  const hasActiveFilters = selectedGenre || selectedAgeRating || showFeaturedOnly;

  return (
    <div className={styles.searchContainer}>
      {/* Search Input */}
      <div className={styles.searchInputContainer}>
        <Search className={styles.searchIcon} />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder={placeholder}
          className={styles.searchInput}
        />
        {searchTerm && (
          <button
            onClick={() => setSearchTerm('')}
            className={styles.clearButton}
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Filter Toggle */}
      <button
        onClick={() => setShowFilters(!showFilters)}
        className={`${styles.filterButton} ${hasActiveFilters ? styles.filterActive : ''}`}
      >
        <Filter className="w-4 h-4" />
        Filters
        {hasActiveFilters && (
          <span className={styles.filterBadge}>
            {[selectedGenre, selectedAgeRating, showFeaturedOnly].filter(Boolean).length}
          </span>
        )}
      </button>

      {/* Filters Panel */}
      {showFilters && (
        <div className={styles.filtersPanel}>
          <div className={styles.filtersHeader}>
            <h3>Filters</h3>
            {hasActiveFilters && (
              <button onClick={clearFilters} className={styles.clearFiltersButton}>
                Clear All
              </button>
            )}
          </div>

          <div className={styles.filtersGrid}>
            {/* Genre Filter */}
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>Genre</label>
              <select
                value={selectedGenre || ''}
                onChange={(e) => setSelectedGenre(e.target.value ? Number(e.target.value) : undefined)}
                className={styles.filterSelect}
              >
                <option value="">All Genres</option>
                {genres.map((genre) => (
                  <option key={genre.id} value={genre.id}>
                    {genre.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Age Rating Filter */}
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>Age Rating</label>
              <select
                value={selectedAgeRating || ''}
                onChange={(e) => setSelectedAgeRating(e.target.value || undefined)}
                className={styles.filterSelect}
              >
                <option value="">All Ratings</option>
                <option value="FSK 0">FSK 0</option>
                <option value="FSK 6">FSK 6</option>
                <option value="FSK 12">FSK 12</option>
                <option value="FSK 16">FSK 16</option>
                <option value="FSK 18">FSK 18</option>
              </select>
            </div>

            {/* Featured Only Filter */}
            <div className={styles.filterGroup}>
              <label className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={showFeaturedOnly}
                  onChange={(e) => setShowFeaturedOnly(e.target.checked)}
                  className={styles.filterCheckbox}
                />
                Featured Only
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
