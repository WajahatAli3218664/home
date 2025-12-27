// frontend/src/pages/signin.jsx
import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import SigninForm from '../components/Auth/SignInForm';

const SigninPage = () => {
  const { isAuthenticated } = useAuth();

  // If already authenticated, redirect to profile page
  React.useEffect(() => {
    if (isAuthenticated) {
      window.location.href = '/profile';
    }
  }, [isAuthenticated]);

  const handleSigninSuccess = (user) => {
    // After successful signin, redirect to homepage
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
    <Layout title="Sign In" description="Sign in to your account on the AI-driven textbook platform">
      <div className="container mx-auto my-8 px-4">
        <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-8">Access Your Account</h1>

          <SigninForm onSigninSuccess={handleSigninSuccess} />

          <div className="mt-6 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="/signup" className="font-medium text-blue-600 hover:text-blue-500">
              Sign up
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SigninPage;