import React from 'react';
import Link from '@docusaurus/Link';
import styles from './HeroSection.module.css';

const HeroSection = () => {
  return (
    <section className={styles.heroSection}>
      <div className={styles.heroContainer}>
        <div className={styles.platformLabel}>ROBOLEARN PLATFORM</div>
        <h1 className={styles.heroTitle}>
          Build robots that
          <br />
          understand
          <br />
          the physical world.
        </h1>
        <p className={styles.heroSubtitle}>
          Master Physical AI and robotics through hands-on projects. Learn to build embodied intelligence that bridges simulation and reality.
        </p>
        <div className={styles.heroButtons}>
          <Link
            to="/docs/intro"
            className={styles.getStartedBtn}
          >
            Get Started
          </Link>
          <Link
            to="/docs/intro"
            className={styles.browseContentBtn}
          >
            Browse Content
          </Link>
        </div>
        <div className={styles.technologyPills}>
          <span className={styles.techPill}>ROS 2</span>
          <span className={styles.techPill}>Isaac Sim</span>
          <span className={styles.techPill}>Gazebo</span>
          <span className={styles.techPill}>VLA Models</span>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;