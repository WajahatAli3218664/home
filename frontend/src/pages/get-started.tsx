import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './get-started.module.css';

const GetStartedPage = () => {
  return (
    <Layout title="Get Started" description="Begin your journey in Physical AI and robotics">
      <main className={styles.getStartedPage}>
        <div className={styles.contentContainer}>
          <h1 className={styles.headline}>The Future is Physical AI</h1>
          <p className={styles.subheadline}>Robots That Think, Move, and Collaborate</p>
          
          <div className={styles.ctaContainer}>
            <Link to="/modules" className={styles.primaryButton}>
              Get Started Free
            </Link>
            <Link to="/docs/intro" className={styles.secondaryButton}>
              View Curriculum
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default GetStartedPage;