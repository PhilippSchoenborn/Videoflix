import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useToastContext } from '../context/ToastContext';
import Button from './Button';
import styles from './Button.module.css';

const LogoutButton: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { showToast } = useToastContext();

  const handleLogout = async () => {
    try {
      await logout();
      showToast('Successfully logged out', 'success');
      navigate('/');
    } catch (error) {
      console.error('Logout error:', error);
      showToast('Logout failed', 'error');
    }
  };

  return (
    <Button onClick={handleLogout} className={styles.logoutButton}>
      Logout
    </Button>
  );
};

export default LogoutButton;
