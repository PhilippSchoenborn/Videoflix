import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useToastContext } from '../context/ToastContext';
import { apiService } from '../services/api';
import styles from './EmailVerificationPage.module.css';
import Footer from '../components/Footer';
import BackgroundImage from '../components/BackgroundImage';
import logoSvg from '../assets/Logo.svg';

export default function EmailVerificationPage() {
  const [verificationStatus, setVerificationStatus] = useState<'processing' | 'success' | 'error'>('processing');
  const [message, setMessage] = useState('');

  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const { showToast } = useToastContext();

  useEffect(() => {
    const verifyEmail = async () => {
      if (!token) {
        setVerificationStatus('error');
        setMessage('Invalid verification link');
        return;
      }

      try {
        await apiService.verifyEmail(token);
        setVerificationStatus('success');
        setMessage('Email verified successfully! You can now log in.');
        showToast('Email verified successfully!', 'success');
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } catch (error: any) {
        console.error('Email verification error:', error);
        setVerificationStatus('error');
        
        if (error.response?.data?.error) {
          setMessage(error.response.data.error);
        } else {
          setMessage('Email verification failed. The link may be invalid or expired.');
        }
        showToast('Email verification failed', 'error');
      }
    };

    verifyEmail();
  }, [token, navigate, showToast]);

  const getStatusIcon = () => {
    switch (verificationStatus) {
      case 'processing':
        return '⏳';
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⏳';
    }
  };

  const getStatusTitle = () => {
    switch (verificationStatus) {
      case 'processing':
        return 'Verifying Email...';
      case 'success':
        return 'Email Verified!';
      case 'error':
        return 'Verification Failed';
      default:
        return 'Verifying Email...';
    }
  };

  return (
    <BackgroundImage>
      <div className={styles.container}>
        {/* Header */}
        <header className={styles.header}>
          <img src={logoSvg} alt="Videoflix Logo" />
          <Link to="/" className={styles.backToHomeButton}>
            Back to Home
          </Link>
        </header>

        {/* Content Body */}
        <div className={styles.body}>
          <div className={styles.verificationBox}>
            <div className={styles.content}>
              <h1 className={`${styles.title} ${styles[verificationStatus]}`}>
                {getStatusIcon()} {getStatusTitle()}
              </h1>
              
              <p className={styles.message}>
                {message}
              </p>

              {verificationStatus === 'success' && (
                <p className={styles.redirectMessage}>
                  Redirecting to login...
                </p>
              )}

              <div className={styles.actions}>
                {verificationStatus === 'error' && (
                  <Link to="/login" className={styles.loginButton}>
                    Go to Login
                  </Link>
                )}
                
                {verificationStatus === 'success' && (
                  <Link to="/login" className={styles.loginButton}>
                    Continue to Login
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>

        <Footer />
      </div>
    </BackgroundImage>
  );
}
