import React from 'react';
import type { Genre } from '../types';
import styles from './SearchBar.module.css';

type FiltersPanelProps = {
  genres: Genre[];
  selectedGenre?: number;
  setSelectedGenre: (id?: number) => void;
  selectedAgeRating?: string;
  setSelectedAgeRating: (r?: string) => void;
  showFeaturedOnly: boolean;
  setShowFeaturedOnly: (v: boolean) => void;
  hasActiveFilters: boolean;
  clearFilters: () => void;
};

const FiltersPanel: React.FC<FiltersPanelProps> = ({
  genres,
  selectedGenre,
  setSelectedGenre,
  selectedAgeRating,
  setSelectedAgeRating,
  showFeaturedOnly,
  setShowFeaturedOnly,
  hasActiveFilters,
  clearFilters
}) => (
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
      <div className={styles.filterGroup}>
        <label className={styles.filterLabel}>Genre</label>
        <select
          value={selectedGenre || ''}
          onChange={e => setSelectedGenre(e.target.value ? Number(e.target.value) : undefined)}
          className={styles.filterSelect}
        >
          <option value="">All Genres</option>
          {genres.map(genre => (
            <option key={genre.id} value={genre.id}>{genre.name}</option>
          ))}
        </select>
      </div>
      <div className={styles.filterGroup}>
        <label className={styles.filterLabel}>Age Rating</label>
        <select
          value={selectedAgeRating || ''}
          onChange={e => setSelectedAgeRating(e.target.value || undefined)}
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
      <div className={styles.filterGroup}>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={showFeaturedOnly}
            onChange={e => setShowFeaturedOnly(e.target.checked)}
            className={styles.filterCheckbox}
          />
          Featured Only
        </label>
      </div>
    </div>
  </div>
);

export default FiltersPanel;
