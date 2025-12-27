import React from 'react';
import Link from '@docusaurus/Link';
import styles from './FinalCTASection.module.css';

const FinalCTASection = () => {
  return (
    <section className={styles.finalCtaSection}>
      <div className={styles.container}>
        <h2 className={styles.sectionTitle}>The Future is Physical AI</h2>
        <p className={styles.sectionSubtitle}>
          Robots That Think, Move, and Collaborate
        </p>
        <Link
          to="/docs/intro"
          className={styles.ctaButton}
        >
          Get Started Free
        </Link>
      </div>
    </section>
  );
};

export default FinalCTASection;