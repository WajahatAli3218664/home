import React from 'react';
import styles from './WhyThisMattersSection.module.css';

interface WhyMatterItem {
  id: number;
  icon: string;
  title: string;
  description: string;
}

const WhyThisMattersSection = () => {
  const items: WhyMatterItem[] = [
    {
      id: 1,
      icon: '🤖',
      title: 'Embodied Intelligence',
      description: 'Learn how AI meets the physical world through sensors and actuators'
    },
    {
      id: 2,
      icon: '👨‍👩‍👧‍👦',
      title: 'Human-Centered Design',
      description: 'Build robots that collaborate naturally with humans'
    },
    {
      id: 3,
      icon: '🏭',
      title: 'Production-Ready Skills',
      description: 'Industry-relevant tools and practices from day one'
    },
    {
      id: 4,
      icon: '💬',
      title: 'Conversational Robotics',
      description: 'Build robots that understand and respond to human language'
    },
    {
      id: 5,
      icon: '🌍',
      title: 'Sim-to-Real Transfer',
      description: 'Accelerate learning with simulation and bridge to reality'
    },
    {
      id: 6,
      icon: '🛠️',
      title: 'Advanced Manipulation',
      description: 'Master dexterous manipulation in complex environments'
    }
  ];

  return (
    <section id="why-matters" className={styles.whyThisMattersSection}>
      <div className={styles.container}>
        <div className={styles.textCenter}>
          <h2 className={styles.sectionTitle}>Why This Matters</h2>
          <p className={styles.sectionSubtitle}>
            The next generation of robotics requires new skills in embodied AI
          </p>
        </div>
        <div className={styles.grid}>
          {items.map((item) => (
            <div key={item.id} className={styles.infoCard}>
              <div className={styles.icon}>{item.icon}</div>
              <h3 className={styles.cardTitle}>{item.title}</h3>
              <p className={styles.cardDescription}>{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default WhyThisMattersSection;