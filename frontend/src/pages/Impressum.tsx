import React from 'react';
import BackArrow from '../components/BackArrow';
import Header from '../components/Header';
import Footer from '../components/Footer';
import styles from './LegalPage.module.css';

const Impressum: React.FC = () => (
  <div className={styles.container}>
    <div className={styles.background} />
    <Header />
    <BackArrow />
    <div className={styles.contentBox}>
      <h1 className={styles.title}>Impressum</h1>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>Angaben gemäß § 5 TMG</h2>
        <p>Videoflix GmbH<br />Musterstraße 1<br />12345 Musterstadt</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>Vertreten durch</h2>
        <p>Max Mustermann</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>Kontakt</h2>
        <p>Telefon: 01234/567890<br />E-Mail: info@videoflix.de</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>Umsatzsteuer-ID</h2>
        <p>DE123456789</p>
      </div>
      <div className={styles.sectionBlock}>
        <h2 className={styles.sectionTitle}>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h2>
        <p>Max Mustermann, Adresse wie oben</p>
      </div>
    </div>
    <Footer />
  </div>
);

export default Impressum;
