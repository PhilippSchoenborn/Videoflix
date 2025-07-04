import React from 'react';
import styles from './LegalPage.module.css';

interface LegalPageProps {
  title: string;
  children: React.ReactNode;
}

const LegalPage: React.FC<LegalPageProps> = ({ title, children }) => {
  return (
    <div className={styles.container}>
      <div className={styles.background} />
      <div className={styles.contentBox}>
        <h1 className={styles.title}>{title}</h1>
        <div className={styles.content}>{children}</div>
      </div>
    </div>
  );
};

export default LegalPage;
