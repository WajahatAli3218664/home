// frontend/src/components/Auth/SigninForm.jsx
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../UI/LoadingSpinner';
import ErrorMessage from '../UI/ErrorMessage';

const SigninForm = ({ onSigninSuccess }) => {
  const { signin, user, initializeAuth } = useAuth();  // Use the main AuthContext's signin method
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }

    // Validate password
    if (!formData.password || formData.password.length < 1) {
      setError('Password is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Use the main context's signin method
      const result = await signin(formData.email, formData.password);

      if (result?.success) {
        // Initialize auth to update the context state with fresh user data
        await initializeAuth();

        if (onSigninSuccess) {
          // Use the updated user from the context after successful sign in
          onSigninSuccess(result.user);
        }
      } else {
        setError(result.error || 'Signin failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during signin');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <ErrorMessage message={error} />}

      <div className="mb-4">
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="your@email.com"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your password"
        />
      </div>

      <div className="mt-6">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-300 disabled:opacity-50 flex justify-center items-center"
        >
          {loading ? (
            <>
              <LoadingSpinner size="small" />
              <span className="ml-2">Signing In...</span>
            </>
          ) : (
            'Sign In'
          )}
        </button>
      </div>
    </form>
  );
};

export default SigninForm;