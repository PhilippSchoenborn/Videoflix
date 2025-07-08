import React from 'react';
import styles from './VideoDetailModal.module.css';

type ModalBackdropProps = {
  onClick: (e: React.MouseEvent) => void;
  children: React.ReactNode;
};

const ModalBackdrop: React.FC<ModalBackdropProps> = ({ onClick, children }) => (
  <div className={styles.modalBackdrop} onClick={onClick}>
    {children}
  </div>
);

export default ModalBackdrop;
