import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useFormValidation, LOGIN_VALIDATION_CONFIG } from '../hooks/useFormValidation';
import { useToastContext } from '../context/ToastContext';
import passwordSvg from '../assets/password.svg';
import styles from './PasswordPage.module.css';
import Button from '../components/Button';
import ValidatedInput from '../components/ValidatedInput';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImageLanding from '../components/BackgroundImageLanding';
import BackArrow from '../components/BackArrow';

const PasswordPage: React.FC = () => {
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { showToast } = useToastContext();
  const { validationState, validateField, validateForm, clearAllErrors } = useFormValidation(LOGIN_VALIDATION_CONFIG);

  useEffect(() => {
    // Get email from navigation state or localStorage
    const emailFromState = location.state?.email;
    const emailFromStorage = localStorage.getItem('email');
    
    if (emailFromState) {
      setEmail(emailFromState);
    } else if (emailFromStorage) {
      setEmail(emailFromStorage);
    } else {
      // If no email is available, redirect back to landing page
      navigate('/');
    }
  }, [location.state, navigate]);

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handlePasswordBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    validateField('password', e.target.value, { email, password: e.target.value });
  };

  const extractErrorMessages = (errorData: any): string[] => {
    const messages: string[] = [];
    
    if (typeof errorData === 'string') {
      return [errorData];
    }
    
    if (Array.isArray(errorData)) {
      return errorData.flat();
    }
    
    if (typeof errorData === 'object' && errorData !== null) {
      Object.values(errorData).forEach(value => {
        if (Array.isArray(value)) {
          messages.push(...value);
        } else if (typeof value === 'string') {
          messages.push(value);
        } else if (typeof value === 'object' && value !== null) {
          messages.push(...extractErrorMessages(value));
        }
      });
    }
    
    return messages;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearAllErrors();

    // Validate password
    if (!validateForm({ email, password })) {
      showToast('Please enter a valid password', 'error');
      return;
    }

    setIsLoading(true);
    try {
      await login({ email, password });
      showToast('Login successful!', 'success');
      // Clear email from localStorage after successful login
      localStorage.removeItem('email');
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      
      if (err.response?.data) {
        const errorMessages = extractErrorMessages(err.response.data);
        if (errorMessages.length > 0) {
          showToast(errorMessages.join('. '), 'error');
        } else {
          showToast('Invalid password', 'error');
        }
      } else {
        showToast('Login failed. Please try again.', 'error');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BackgroundImageLanding>
      <div className={styles.container}>
        <Header />

        {/* Back Arrow */}
        <BackArrow to="/" />

        {/* Main Content */}
        <div className={styles.body}>
          <div className={styles.hero}>
            <div className={styles.heroContent}>
              {/* Hero Title */}
              <h1 className={styles.title}>
                Welcome back!
              </h1>
              
              {/* Show Email */}
              <p className={styles.emailDisplay}>
                {email}
              </p>
              
              {/* Hero Description */}
              <p className={styles.description}>
                Enter your password to continue.
              </p>
              
              {/* Password Form */}
              <form onSubmit={handleSubmit}>
                <div className={styles.passwordGroup}>
                  <ValidatedInput
                    type="password"
                    name="password"
                    value={password}
                    onChange={handlePasswordChange}
                    onBlur={handlePasswordBlur}
                    placeholder="Password"
                    icon={passwordSvg}
                    iconAlt="Password"
                    hasError={validationState.password?.hasError}
                    errorMessage={validationState.password?.errorMessage}
                    autoComplete="current-password"
                    variant="landing"
                    showPasswordToggle={true}
                  />
                  <Button 
                    type="submit" 
                    variant="small"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Signing In...' : 'Sign In'}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <Footer />
      </div>
    </BackgroundImageLanding>
  );
};

export default PasswordPage;
