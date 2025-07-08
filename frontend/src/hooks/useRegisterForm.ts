import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useFormValidation, REGISTER_VALIDATION_CONFIG } from './useFormValidation';
import { useToastContext } from '../context/ToastContext';

/**
 * Custom Hook für das Registrierungsformular.
 * Kapselt State, Validierung, Fehlerbehandlung und Submit-Logik.
 */
export function useRegisterForm() {
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

  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    if (storedEmail) {
      setFormData(prev => ({ ...prev, email: storedEmail }));
      localStorage.removeItem('email');
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (serverError) setServerError('');
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    validateField(name, value, formData);
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
    setServerError('');
    clearAllErrors();
    if (!validateForm(formData)) {
      showToast('Bitte korrigiere die Fehler im Formular', 'error');
      return;
    }
    setIsLoading(true);
    try {
      const username = formData.email.split('@')[0];
      const registerData = {
        email: formData.email,
        username,
        password: formData.password,
        password_confirm: formData.confirmPassword,
      };
      await register(registerData);
      showToast('Registrierung erfolgreich! Bitte E-Mail zur Aktivierung prüfen.', 'success');
      navigate('/login');
    } catch (err: any) {
      if (err.response?.data) {
        const errorMessages = extractErrorMessages(err.response.data);
        setServerError(errorMessages.length > 0 ? errorMessages.join('. ') : 'Registrierung fehlgeschlagen. Bitte erneut versuchen.');
        showToast(errorMessages.length > 0 ? errorMessages.join('. ') : 'Registrierung fehlgeschlagen. Bitte erneut versuchen.', 'error');
      } else if (err.message) {
        setServerError(err.message);
        showToast(err.message, 'error');
      } else {
        setServerError('Registrierung fehlgeschlagen. Bitte erneut versuchen.');
        showToast('Registrierung fehlgeschlagen. Bitte erneut versuchen.', 'error');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    formData,
    isLoading,
    serverError,
    validationState,
    handleChange,
    handleBlur,
    handleSubmit,
  };
}
