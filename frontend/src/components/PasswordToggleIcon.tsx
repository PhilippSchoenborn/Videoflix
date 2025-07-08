import React from 'react';
import visibilityOffSvg from '../assets/visibility_off.svg';
import visibilitySvg from '../assets/visibility.svg';
import styles from './ValidatedInput.module.css';

type PasswordToggleIconProps = {
  show: boolean;
  onClick: () => void;
};

const PasswordToggleIcon: React.FC<PasswordToggleIconProps> = ({ show, onClick }) => (
  <img
    src={show ? visibilityOffSvg : visibilitySvg}
    alt="Toggle password visibility"
    className={styles.visibilityIcon}
    onClick={onClick}
  />
);

export default PasswordToggleIcon;
