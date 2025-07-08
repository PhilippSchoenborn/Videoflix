import React from 'react';
import { Filter } from 'lucide-react';
import styles from './SearchBar.module.css';

type FilterToggleButtonProps = {
  active: boolean;
  count: number;
  onClick: () => void;
};

const FilterToggleButton: React.FC<FilterToggleButtonProps> = ({ active, count, onClick }) => (
  <button
    onClick={onClick}
    className={`${styles.filterButton} ${active ? styles.filterActive : ''}`}
  >
    <Filter className="w-4 h-4" />
    Filters
    {active && <span className={styles.filterBadge}>{count}</span>}
  </button>
);

export default FilterToggleButton;
