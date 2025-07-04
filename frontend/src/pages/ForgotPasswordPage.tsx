import { useState } from 'react';
import mailSvg from '../assets/mail.svg';
import styles from './ForgotPasswordPage.module.css';
import Button from '../components/Button';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImage from '../components/BackgroundImage';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (!email) {
      setError('Please enter your email address');
      return;
    }

    setIsLoading(true);
    try {
      // TODO: Implement password reset API call
      // await api.requestPasswordReset({ email });
      setMessage('If an account with this email exists, you will receive a password reset link.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BackgroundImage>
      <div className={styles.container}>
        <Header />

        {/* Error Message */}
        {error && (
          <div className={styles.error}>
            {error}
          </div>
        )}

        {/* Success Message */}
        {message && (
          <div className={styles.success}>
            {message}
          </div>
        )}

        {/* Content Body */}
        <div className={styles.body}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formBox}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', alignItems: 'center', justifyContent: 'center' }}>
                {/* Reset Password Title */}
                <h1 className={styles.title}>Forgot your password?</h1>
                
                {/* Description */}
                <p className={styles.description}>
                  We will send you an email with instructions to reset your password.
                </p>
                
                {/* Input Fields Container */}
                <div className={styles.inputGroup}>
                  {/* Email Input */}
                  <div className={styles.inputRow}>
                    <img src={mailSvg} alt="Mail" className={styles.inputIcon} />
                    <input
                      type="email"
                      name="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Email Address"
                      required
                      className={styles.inputField}
                    />
                  </div>
                </div>

                {/* Bottom Container */}
                <div className={styles.bottomGroup}>
                  {/* Reset Button */}
                  <Button
                    type="submit"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Sending...' : 'Send Email'}
                  </Button>

                  {/* Back to Login
                  <div className={styles.backToLogin}>
                    <span className={styles.backText}>
                      Remember your password?
                    </span>
                    <Link
                      to="/"
                      className={styles.backLink}
                    >
                      Sign In
                    </Link>
                  </div> */}
                </div>
              </div>
            </div>
          </form>
        </div>

        <Footer />
      </div>
    </BackgroundImage>
  );
}
