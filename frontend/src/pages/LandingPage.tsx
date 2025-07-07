import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useFormValidation, LOGIN_VALIDATION_CONFIG } from '../hooks/useFormValidation';
import styles from './LandingPage.module.css';
import Button from '../components/Button';
import ValidatedInput from '../components/ValidatedInput';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImageLanding from '../components/BackgroundImageLanding';
import mailSvg from '../assets/mail.svg';

const LandingPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  const { validationState, validateField } = useFormValidation(LOGIN_VALIDATION_CONFIG);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleEmailBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    validateField('email', e.target.value);
  };

  const handleSignIn = () => {
    if (email && !validationState.email?.hasError) {
      // Store email and navigate to password page
      localStorage.setItem('email', email);
      navigate('/password', { state: { email } });
    } else if (email) {
      // Email has validation error, validate it to show error
      validateField('email', email);
    } else {
      // No email entered, go to normal login page
      navigate('/login');
    }
  };

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
                <ValidatedInput
                  type="email"
                  name="email"
                  value={email}
                  onChange={handleEmailChange}
                  onBlur={handleEmailBlur}
                  placeholder="Email Address"
                  icon={mailSvg}
                  iconAlt="Mail"
                  hasError={validationState.email?.hasError}
                  errorMessage={validationState.email?.errorMessage}
                  autoComplete="email"
                  variant="landing"
                />
                <Button 
                  variant="small" 
                  onClick={handleSignIn}
                  type="button"
                >
                  Sign In
                </Button>
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
