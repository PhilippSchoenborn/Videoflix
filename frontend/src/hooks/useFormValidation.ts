import { useState, useCallback } from 'react';

interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  customValidation?: (value: string) => boolean;
}

interface FieldConfig {
  [fieldName: string]: {
    rules: ValidationRule;
    errorMessage: string;
  };
}

interface ValidationState {
  [fieldName: string]: {
    hasError: boolean;
    errorMessage: string;
  };
}

interface FormValidationHook {
  validationState: ValidationState;
  validateField: (fieldName: string, value: string, additionalData?: Record<string, string>) => boolean;
  validateForm: (formData: Record<string, string>) => boolean;
  clearFieldError: (fieldName: string) => void;
  clearAllErrors: () => void;
  hasErrors: boolean;
}

export function useFormValidation(config: FieldConfig): FormValidationHook {
  const [validationState, setValidationState] = useState<ValidationState>(() => {
    const initialState: ValidationState = {};
    Object.keys(config).forEach(fieldName => {
      initialState[fieldName] = {
        hasError: false,
        errorMessage: ''
      };
    });
    return initialState;
  });

  const validateField = useCallback((
    fieldName: string, 
    value: string, 
    additionalData?: Record<string, string>
  ): boolean => {
    const fieldConfig = config[fieldName];
    if (!fieldConfig) return true;

    const { rules, errorMessage } = fieldConfig;
    let isValid = true;

    // Required validation
    if (rules.required && (!value || value.trim().length === 0)) {
      isValid = false;
    }

    // Min length validation
    if (isValid && rules.minLength && value.trim().length < rules.minLength) {
      isValid = false;
    }

    // Max length validation
    if (isValid && rules.maxLength && value.trim().length > rules.maxLength) {
      isValid = false;
    }

    // Pattern validation (e.g., email)
    if (isValid && rules.pattern && !rules.pattern.test(value.trim())) {
      isValid = false;
    }

    // Custom validation
    if (isValid && rules.customValidation && !rules.customValidation(value.trim())) {
      isValid = false;
    }

    // Special case for password confirmation
    if (isValid && fieldName === 'confirmPassword' && additionalData?.password) {
      if (value.trim() !== additionalData.password.trim()) {
        isValid = false;
      }
    }

    setValidationState(prev => ({
      ...prev,
      [fieldName]: {
        hasError: !isValid,
        errorMessage: isValid ? '' : errorMessage
      }
    }));

    return isValid;
  }, [config]);

  const validateForm = useCallback((formData: Record<string, string>): boolean => {
    let formIsValid = true;
    
    Object.keys(config).forEach(fieldName => {
      const isFieldValid = validateField(fieldName, formData[fieldName] || '', formData);
      if (!isFieldValid) {
        formIsValid = false;
      }
    });

    return formIsValid;
  }, [config, validateField]);

  const clearFieldError = useCallback((fieldName: string) => {
    setValidationState(prev => ({
      ...prev,
      [fieldName]: {
        hasError: false,
        errorMessage: ''
      }
    }));
  }, []);

  const clearAllErrors = useCallback(() => {
    const clearedState: ValidationState = {};
    Object.keys(config).forEach(fieldName => {
      clearedState[fieldName] = {
        hasError: false,
        errorMessage: ''
      };
    });
    setValidationState(clearedState);
  }, [config]);

  const hasErrors = Object.values(validationState).some(field => field.hasError);

  return {
    validationState,
    validateField,
    validateForm,
    clearFieldError,
    clearAllErrors,
    hasErrors
  };
}

// Pre-defined validation patterns
export const EMAIL_PATTERN = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

// More comprehensive email pattern covering edge cases
export const COMPREHENSIVE_EMAIL_PATTERN = /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$/;

// Strong password pattern - at least 8 characters, one letter, one number
export const STRONG_PASSWORD_PATTERN = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/;

// Login validation config
export const LOGIN_VALIDATION_CONFIG: FieldConfig = {
  email: {
    rules: {
      required: true,
      pattern: COMPREHENSIVE_EMAIL_PATTERN
    },
    errorMessage: 'Please enter a valid email address.'
  },
  password: {
    rules: {
      required: true,
      minLength: 1
    },
    errorMessage: 'Password is required.'
  }
};

// Registration validation config
export const REGISTER_VALIDATION_CONFIG: FieldConfig = {
  email: {
    rules: {
      required: true,
      pattern: COMPREHENSIVE_EMAIL_PATTERN
    },
    errorMessage: 'Please enter a valid email address.'
  },
  password: {
    rules: {
      required: true,
      minLength: 8,
      pattern: STRONG_PASSWORD_PATTERN
    },
    errorMessage: 'Password must be at least 8 characters long and contain at least one letter and one number.'
  },
  confirmPassword: {
    rules: {
      required: true,
      customValidation: () => true // Will be handled in validateField for password matching
    },
    errorMessage: 'Passwords do not match.'
  }
};
