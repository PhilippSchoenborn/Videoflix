import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './BurgerMenu.module.css';
import Button from './Button';

const BurgerMenu: React.FC = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className={styles.burgerMenuWrapper}>
      <button
        className={styles.burgerButton}
        aria-label="Open menu"
        onClick={() => setOpen((prev) => !prev)}
      >
        <span className={styles.burgerIcon}>
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>
      {open && (
        <div className={styles.menuDropdown}>
          <Link to="/login" className={styles.menuLink} onClick={() => setOpen(false)}>
            <Button>Login</Button>
          </Link>
        </div>
      )}
    </div>
  );
};

export default BurgerMenu;
