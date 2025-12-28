import React, { useState } from 'react';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';

const AuthManager = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const openLogin = () => {
    setShowSignup(false);
    setShowLogin(true);
  };

  const openSignup = () => {
    setShowLogin(false);
    setShowSignup(true);
  };

  const closeAll = () => {
    setShowLogin(false);
    setShowSignup(false);
  };

  // Make functions available globally
  React.useEffect(() => {
    window.openLogin = openLogin;
    window.openSignup = openSignup;
    
    return () => {
      delete window.openLogin;
      delete window.openSignup;
    };
  }, []);

  return (
    <>
      {showLogin && (
        <LoginForm 
          onClose={closeAll}
          onSwitchToSignup={openSignup}
        />
      )}
      {showSignup && (
        <SignupForm 
          onClose={closeAll}
          onSwitchToLogin={openLogin}
        />
      )}
    </>
  );
};

export default AuthManager;