// frontend/src/pages/signup.jsx
import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import SignupForm from '../components/Auth/SignupForm';

const SignupPage = () => {
  const { isAuthenticated } = useAuth();

  // If already authenticated, redirect to profile page
  React.useEffect(() => {
    if (isAuthenticated) {
      window.location.href = '/profile';
    }
  }, [isAuthenticated]);

  const handleSignupSuccess = (user) => {
    // After successful signup, redirect to homepage
    window.location.href = '/';
  };

  // If authenticated, don't show the form
  if (isAuthenticated) {
    return (
      <Layout title="Redirecting..." description="Already signed in">
        <div className="container mx-auto my-8 px-4">
          <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
            <h1 className="text-2xl font-bold text-center text-gray-800 mb-8">Redirecting...</h1>
            <p className="text-center">You are already signed in. Redirecting to your profile...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Sign Up" description="Create your account on the AI-driven textbook platform">
      <div className="container mx-auto my-8 px-4">
        <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-8">Create Your Account</h1>

          <SignupForm onSignupSuccess={handleSignupSuccess} />

          <div className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <a href="/signin" className="font-medium text-blue-600 hover:text-blue-500">
              Sign in
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;