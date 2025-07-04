import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import mailSvg from '../assets/mail.svg';
import passwordSvg from '../assets/password.svg';
import visibilitySvg from '../assets/visibility.svg';
import styles from './RegisterPage.module.css';
import Button from '../components/Button';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImageSignUp from '../components/BackgroundImageSignUp';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);
    try {
      // Generate username from email (part before @)
      const username = formData.email.split('@')[0];
      
      const registerData = {
        email: formData.email,
        username: username,
        password: formData.password,
        password_confirm: formData.confirmPassword,
      };
      await register(registerData);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BackgroundImageSignUp>
      <div className={styles.container}>
        <Header />

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
                {/* Register Title */}
                <h1 className={styles.title}>Get Started</h1>
                
                {/* Input Fields Container */}
                <div className={styles.inputGroup}>
                  {/* Email Input */}
                  <div className={styles.inputRow}>
                    <img src={mailSvg} alt="Mail" className={styles.inputIcon} />
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
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
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
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

                  {/* Confirm Password Input */}
                  <div className={styles.inputRow}>
                    <img src={passwordSvg} alt="Password" className={styles.inputIcon} />
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      placeholder="Confirm Password"
                      required
                      className={`${styles.inputField} ${styles.inputFieldPassword}`}
                    />
                    <img 
                      src={visibilitySvg} 
                      alt="Toggle visibility" 
                      className={styles.visibilityIcon}
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    />
                  </div>
                </div>

                {/* Bottom Container */}
                <div className={styles.bottomGroup}>
                  {/* Register Button */}
                  <Button
                    type="submit"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Creating Account...' : 'Get Started'}
                  </Button>
                </div>
              </div>
            </div>
          </form>
        </div>

        <Footer />
      </div>
    </BackgroundImageSignUp>
  );
}
