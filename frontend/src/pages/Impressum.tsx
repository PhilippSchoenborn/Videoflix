import Header from '../components/Header';
import Footer from '../components/Footer';
import BackArrow from '../components/BackArrow';
import styles from './LegalPage.module.css';
import React from 'react';
import BackgroundImage from '../components/BackgroundImage';

const Impressum: React.FC = () => (
  <BackgroundImage>
    <div className={styles.pageWrapper}>
      <Header />
      <BackArrow />
      <div className={styles.bodyWrapper}>
        <div className={styles.contentContainer}>
          <div className={styles.scrollContent}>
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
        </div>
      </div>
      <Footer />
    </div>
  </BackgroundImage>
);

export default Impressum;
