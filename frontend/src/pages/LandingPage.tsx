import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './LandingPage.module.css';
import Button from '../components/Button';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImageLanding from '../components/BackgroundImageLanding';

const LandingPage: React.FC = () => {
  const [email, setEmail] = useState('');

  return (
    <BackgroundImageLanding>
      <div className={styles.container}>
        <Header />

        {/* Main Content */}
        <div className={styles.body}>
          <div className={styles.hero}>
            <div className={styles.heroContent}>
              {/* Hero Title */}
              <h1 className={styles.title}>
                Movies, TV shows, and more
              </h1>
              
              {/* Hero Description */}
              <p className={styles.description}>
                Enter your email to create or restart your subscription.
              </p>
              
              {/* Email Input and Sign In Button */}
              <div className={styles.emailGroup}>
                <div className={styles.inputRow}>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email Address"
                    className={styles.inputField}
                  />
                </div>
                <Link to="/login" className={styles.loginLink}>
                  <Button>Sign In</Button>
                </Link>
              </div>
            </div>
          </div>
        </div>

        <Footer />
      </div>
    </BackgroundImageLanding>
  );
};

export default LandingPage;
