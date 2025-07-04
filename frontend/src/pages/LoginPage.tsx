import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import logoSvg from '../assets/Logo.svg';
import mailSvg from '../assets/mail.svg';
import passwordSvg from '../assets/password.svg';
import visibilitySvg from '../assets/visibility.svg';
import backgroundImage from '../assets/background_LogIn.jpg';
import styles from './LoginPage.module.css';
import Button from '../components/Button';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div 
      className={styles.container}
    >
      {/* Background Image + Gradient Overlay */}
      <div
        className={styles.background}
        style={{
          backgroundImage: `linear-gradient(180deg, rgba(0,0,0,0.8) -27.44%, rgba(0,0,0,0.44) 44.23%, rgba(0,0,0,0.8) 100%), url(${backgroundImage})`,
        }}
      />

      {/* Header */}
      <header 
        className={styles.header}
      >
        <img src={logoSvg} alt="Videoflix Logo" />
      </header>

      {/* Error Message */}
      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}

      {/* Content Body */}
      <div className={styles.body}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formBox}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', alignItems: 'center', justifyContent: 'center' }}>
              {/* Login Title */}
              <h1 className={styles.title}>Log in</h1>

              {/* Input Fields Container */}
              <div className={styles.inputGroup}>
                {/* Email Input */}
                <div className={styles.inputRow}>
                  <img src={mailSvg} alt="Mail" className={styles.inputIcon} />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email Address"
                    required
                    className={styles.inputField}
                  />
                </div>

                {/* Password Input */}
                <div className={styles.inputRow}>
                  <img src={passwordSvg} alt="Password" className={styles.inputIcon} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                    className={`${styles.inputField} ${styles.inputFieldPassword}`}
                  />
                  <img 
                    src={visibilitySvg} 
                    alt="Toggle visibility" 
                    className={styles.visibilityIcon}
                    onClick={() => setShowPassword(!showPassword)}
                  />
                </div>
              </div>

              {/* Bottom Container */}
              <div className={styles.bottomGroup}>
                {/* Login Button */}
                <Button
                  type="submit"
                  disabled={isLoading}
                >
                  {isLoading ? 'Logging in...' : 'Log in'}
                </Button>

                {/* Forgot Password */}
                <div className={styles.forgotPassword}>
                  <Link
                    to="/forgot-password"
                    className={styles.forgotPasswordLink}
                  >
                    Forgot password?
                  </Link>
                </div>

                {/* Sign Up */}
                <div className={styles.signUpRow}>
                  <span className={styles.signUpText}>
                    New to Videoflix?
                  </span>
                  <Link
                    to="/register"
                    className={styles.signUpLink}
                  >
                    Sign Up now
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>

      {/* Footer Links */}
      <div className={styles.footer}>
        <Link
          to="/datenschutz"
          className={styles.footerLink}
        >
          Datenschutz
        </Link>
        <Link
          to="/impressum"
          className={styles.footerLink}
        >
          Impressum
        </Link>
      </div>
    </div>
  );
}
