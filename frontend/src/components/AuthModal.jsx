import React, { useState, useEffect } from 'react';
import { signIn, signOut, getSession } from '../services/authClient';
import '../styles/ChatWindow.css'; // Using same styles for modal consistency

const AuthModal = ({ onClose, onAuthSuccess, onError }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [authError, setAuthError] = useState('');
  const [isEmailFormVisible, setIsEmailFormVisible] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [hasAttemptedSubmit, setHasAttemptedSubmit] = useState(false);

  // Close modal with Escape key
  useEffect(() => {
    const handleEscKey = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEscKey);
    return () => window.removeEventListener('keydown', handleEscKey);
  }, [onClose]);

  const handleProviderLogin = async (provider) => {
    setIsLoading(true);
    setAuthError('');
    setHasAttemptedSubmit(true);

    try {
      // Attempt to sign in with the selected provider
      const result = await signIn[provider]({
        callbackURL: window.location.href, // Redirect back to current page after auth
        redirect: false
      });

      if (result?.error) {
        throw new Error(result.error?.message || result?.error || 'Authentication failed');
      }

      // Authentication successful
      onAuthSuccess(); // Notify parent component of successful auth
    } catch (err) {
      console.error(`Login error with ${provider}:`, err);
      const errorMsg = err.message || `Failed to log in with ${provider}. Please try again.`;
      setAuthError(errorMsg);
      onError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmailAuth = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setAuthError('');
    setHasAttemptedSubmit(true);

    try {
      // For Better Auth, we sign in using the email provider method
      const result = await signIn.email({
        email,
        password,
        callbackURL: window.location.href,
        redirect: false
      });

      if (result?.error) {
        throw new Error(result.error?.message || result?.error || (isSignUp ? 'Registration failed' : 'Login failed'));
      }

      // Authentication successful
      onAuthSuccess(); // Notify parent component of successful auth
    } catch (err) {
      console.error('Email authentication error:', err);
      const errorMsg = err.message || (isSignUp ? 'Registration failed' : 'Login failed');
      setAuthError(errorMsg);
      onError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to determine if a field has an error for WCAG
  const hasFieldError = (fieldValue, fieldName) => {
    if (!hasAttemptedSubmit) return false;

    switch (fieldName) {
      case 'email':
        return !fieldValue || !/\S+@\S+\.\S+/.test(fieldValue);
      case 'password':
        return !fieldValue || fieldValue.length < 6;
      case 'confirmPassword':
        return isSignUp && fieldValue !== password;
      default:
        return false;
    }
  };

  return (
    <div
      className="modal-overlay"
      onClick={onClose}
      aria-modal="true"
      role="dialog"
      aria-labelledby="auth-modal-title"
      tabIndex="-1"
    >
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        role="document"
      >
        <div className="modal-header">
          <h3 id="auth-modal-title">{isEmailFormVisible ? (isSignUp ? 'Create Account' : 'Sign In') : 'Sign in to Chat'}</h3>
          <button
            className="modal-close-button"
            onClick={onClose}
            aria-label="Close authentication modal"
            tabIndex="0"
          >
            ×
          </button>
        </div>

        <div className="modal-body">
          {!isEmailFormVisible ? (
            <>
              <p>Please sign in to access the AI textbook assistant.</p>

              <div className="auth-options">
                <button
                  className="auth-provider-btn google-auth"
                  onClick={() => handleProviderLogin('google')}
                  disabled={isLoading}
                  aria-label="Sign in with Google"
                  tabIndex="0"
                >
                  Sign in with Google
                </button>

                <button
                  className="auth-provider-btn email-auth"
                  onClick={() => setIsEmailFormVisible(true)}
                  disabled={isLoading}
                  aria-label="Sign in with email"
                  tabIndex="0"
                >
                  Sign in with Email
                </button>
              </div>
            </>
          ) : (
            <form onSubmit={handleEmailAuth} className="email-auth-form" noValidate>
              <div className="form-group">
                <label htmlFor="email">Email:</label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="your@email.com"
                  aria-invalid={hasFieldError(email, 'email')}
                  aria-describedby={hasFieldError(email, 'email') ? "email-error" : undefined}
                  tabIndex="0"
                />
                {hasFieldError(email, 'email') && (
                  <span id="email-error" className="error-message" role="alert" aria-live="assertive">
                    Please enter a valid email address
                  </span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="password">Password:</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength="6"
                  disabled={isLoading}
                  placeholder="At least 6 characters"
                  aria-invalid={hasFieldError(password, 'password')}
                  aria-describedby={hasFieldError(password, 'password') ? "password-error" : undefined}
                  tabIndex="0"
                />
                {hasFieldError(password, 'password') && (
                  <span id="password-error" className="error-message" role="alert" aria-live="assertive">
                    Password must be at least 6 characters
                  </span>
                )}
              </div>

              {isSignUp && (
                <div className="form-group">
                  <label htmlFor="confirmPassword">Confirm Password:</label>
                  <input
                    type="password"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    disabled={isLoading}
                    placeholder="Confirm your password"
                    aria-invalid={hasFieldError(confirmPassword, 'confirmPassword')}
                    aria-describedby={hasFieldError(confirmPassword, 'confirmPassword') ? "confirm-password-error" : undefined}
                    tabIndex="0"
                  />
                  {hasFieldError(confirmPassword, 'confirmPassword') && (
                    <span id="confirm-password-error" className="error-message" role="alert" aria-live="assertive">
                      Passwords must match
                    </span>
                  )}
                </div>
              )}

              {authError && (
                <div className="auth-error-message" role="alert" aria-live="assertive">
                  {authError}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit-btn"
                disabled={isLoading ||
                  !email ||
                  !password ||
                  (isSignUp && password !== confirmPassword)}
                tabIndex="0"
              >
                {isLoading ? 'Processing...' : (isSignUp ? 'Create Account' : 'Sign In')}
              </button>

              <div className="auth-toggle">
                <button
                  type="button"
                  className="auth-toggle-btn"
                  onClick={() => setIsSignUp(!isSignUp)}
                  tabIndex="0"
                >
                  {isSignUp
                    ? 'Already have an account? Sign In'
                    : 'Need an account? Sign Up'}
                </button>
              </div>

              <button
                type="button"
                className="back-to-providers"
                onClick={() => setIsEmailFormVisible(false)}
                tabIndex="0"
              >
                Back to Social Login
              </button>
            </form>
          )}

          {isLoading && (
            <div
              className="loading-overlay"
              role="alert"
              aria-live="polite"
              aria-label="Processing authentication"
            >
              <div className="loading-spinner" aria-hidden="true"></div>
              <p>Processing authentication...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthModal;