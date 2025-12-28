import React from 'react';
import Layout from '@theme-original/Layout';
import { AuthProvider } from '../contexts/AuthContext';
import ChatInterface from '../components/ChatInterface';
import AuthManager from '../components/AuthManager';
import type { Props } from '@theme/Layout';

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <AuthProvider>
      <Layout {...props}>
        {props.children}
        <ChatInterface />
        <AuthManager />
      </Layout>
    </AuthProvider>
  );
}