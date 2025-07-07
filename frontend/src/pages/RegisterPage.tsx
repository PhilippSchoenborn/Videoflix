import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useFormValidation, REGISTER_VALIDATION_CONFIG } from '../hooks/useFormValidation';
import { useToastContext } from '../context/ToastContext';
import mailSvg from '../assets/mail.svg';
import passwordSvg from '../assets/password.svg';
import styles from './RegisterPage.module.css';
import Button from '../components/Button';
import ValidatedInput from '../components/ValidatedInput';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackgroundImageSignUp from '../components/BackgroundImageSignUp';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState('');

  const { register } = useAuth();
  const navigate = useNavigate();
  const { showToast } = useToastContext();
  const { validationState, validateField, validateForm, clearAllErrors } = useFormValidation(REGISTER_VALIDATION_CONFIG);

  // Pre-fill email from localStorage if available
  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    if (storedEmail) {
      setFormData(prev => ({
        ...prev,
        email: storedEmail
      }));
      // Clear from localStorage after using it
      localStorage.removeItem('email');
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear server error when user starts typing
    if (serverError) {
      setServerError('');
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    validateField(name, value, formData);
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
    setServerError('');
    clearAllErrors();

    // Validate form
    if (!validateForm(formData)) {
      showToast('Please correct the errors in the form', 'error');
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
      showToast('Registration successful! Please check your email for activation.', 'success');
      navigate('/login');
    } catch (err: any) {
      console.error('Registration error:', err);
      
      // Handle different types of errors
      if (err.response?.data) {
        const errorMessages = extractErrorMessages(err.response.data);
        if (errorMessages.length > 0) {
          setServerError(errorMessages.join('. '));
          showToast(errorMessages.join('. '), 'error');
        } else {
          setServerError('Registration failed. Please try again.');
          showToast('Registration failed. Please try again.', 'error');
        }
      } else if (err.message) {
        setServerError(err.message);
        showToast(err.message, 'error');
      } else {
        setServerError('Registration failed. Please try again.');
        showToast('Registration failed. Please try again.', 'error');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BackgroundImageSignUp>
      <div className={styles.container}>
        <Header />

        {/* Error Message */}
        {serverError && (
          <div className={styles.error}>
            {serverError}
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
                  <ValidatedInput
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Email Address"
                    icon={mailSvg}
                    iconAlt="Mail"
                    required
                    hasError={validationState.email?.hasError}
                    errorMessage={validationState.email?.errorMessage}
                    autoComplete="email"
                  />

                  {/* Password Input */}
                  <ValidatedInput
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Password"
                    icon={passwordSvg}
                    iconAlt="Password"
                    required
                    hasError={validationState.password?.hasError}
                    errorMessage={validationState.password?.errorMessage}
                    autoComplete="new-password"
                    showPasswordToggle
                  />

                  {/* Confirm Password Input */}
                  <ValidatedInput
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    placeholder="Confirm Password"
                    icon={passwordSvg}
                    iconAlt="Password"
                    required
                    hasError={validationState.confirmPassword?.hasError}
                    errorMessage={validationState.confirmPassword?.errorMessage}
                    autoComplete="new-password"
                    showPasswordToggle
                  />
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
