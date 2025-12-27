import React, { useEffect, useState } from 'react';
import Layout from '@theme-original/Layout';
import { AuthProvider } from '../contexts/AuthContext';
import ChatbotButton from '../components/ChatbotButton';
import type { Props } from '@theme/Layout';

export default function LayoutWrapper(props: Props): JSX.Element {
  const [backendUrl, setBackendUrl] = useState<string>('http://localhost:8000');

  useEffect(() => {
    // Get backend URL from window object or default
    // We check for window.REACT_APP_API_BASE_URL which is set via our client module
    const url = (window as any).BACKEND_URL ||
               (window as any).REACT_APP_API_BASE_URL ||
               'http://localhost:8000';
    setBackendUrl(url);
  }, []);

  return (
    <AuthProvider>
      <Layout {...props}>
        {props.children}
        <ChatbotButton backendUrl={backendUrl} />
      </Layout>
    </AuthProvider>
  );
}