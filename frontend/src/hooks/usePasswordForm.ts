import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useFormValidation, LOGIN_VALIDATION_CONFIG } from './useFormValidation';
import { useToastContext } from '../context/ToastContext';

/**
 * Custom hook to manage password form logic for PasswordPage.
 * Handles state, validation, error extraction, and login submission.
 */
export function usePasswordForm() {
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { showToast } = useToastContext();
  const { validationState, validateField, validateForm, clearAllErrors } = useFormValidation(LOGIN_VALIDATION_CONFIG);

  useEffect(() => {
    const emailFromState = location.state?.email;
    const emailFromStorage = localStorage.getItem('email');
    if (emailFromState) setEmail(emailFromState);
    else if (emailFromStorage) setEmail(emailFromStorage);
    else navigate('/');
  }, [location.state, navigate]);

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value);

  const handlePasswordBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    validateField('password', e.target.value, { email, password: e.target.value });
  };

  const extractErrorMessages = (errorData: any): string[] => {
    if (typeof errorData === 'string') return [errorData];
    if (Array.isArray(errorData)) return errorData.flat();
    if (typeof errorData === 'object' && errorData !== null) {
      return Object.values(errorData).flatMap((value) =>
        Array.isArray(value)
          ? value
          : typeof value === 'string'
          ? [value]
          : typeof value === 'object' && value !== null
          ? extractErrorMessages(value)
          : []
      );
    }
    return [];
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearAllErrors();
    if (!validateForm({ email, password })) {
      showToast('Please enter a valid password', 'error');
      return;
    }
    setIsLoading(true);
    try {
      await login({ email, password });
      showToast('Login successful!', 'success');
      localStorage.removeItem('email');
      navigate('/dashboard');
    } catch (err: any) {
      if (err.response?.data) {
        const errorMessages = extractErrorMessages(err.response.data);
        showToast(errorMessages.length > 0 ? errorMessages.join('. ') : 'Invalid password', 'error');
      } else {
        showToast('Login failed. Please try again.', 'error');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    email,
    password,
    isLoading,
    validationState,
    handlePasswordChange,
    handlePasswordBlur,
    handleSubmit,
  };
}
