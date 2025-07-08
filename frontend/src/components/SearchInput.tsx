import React from 'react';
import { Search, X } from 'lucide-react';
import styles from './SearchBar.module.css';

type SearchInputProps = {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
};

const SearchInput: React.FC<SearchInputProps> = ({ value, onChange, placeholder }) => (
  <div className={styles.searchInputContainer}>
    <Search className={styles.searchIcon} />
    <input
      type="text"
      value={value}
      onChange={e => onChange(e.target.value)}
      placeholder={placeholder}
      className={styles.searchInput}
    />
    {value && (
      <button onClick={() => onChange('')} className={styles.clearButton}>
        <X className="w-4 h-4" />
      </button>
    )}
  </div>
);

export default SearchInput;
