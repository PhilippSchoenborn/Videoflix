import React from 'react';
import LegalPage from './LegalPage';
import BackArrow from '../components/BackArrow';
import Header from '../components/Header';
import styles from './LegalPage.module.css';

const Datenschutz: React.FC = () => (
  <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
    <Header />
    <BackArrow />
    <LegalPage title="Datenschutzerklärung">
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>1. Datenschutz auf einen Blick</h2>
        <p>Allgemeine Hinweise<br />Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen.</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>2. Datenerfassung auf unserer Website</h2>
        <p>Wer ist verantwortlich für die Datenerfassung auf dieser Website?<br />Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Impressum dieser Website entnehmen.</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>3. Ihre Rechte</h2>
        <p>Sie haben jederzeit das Recht unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung, Sperrung oder Löschung dieser Daten zu verlangen.</p>
        <p>Weitere Informationen finden Sie in unserer vollständigen Datenschutzerklärung.</p>
      </div>
    </LegalPage>
  </div>
);

export default Datenschutz;
