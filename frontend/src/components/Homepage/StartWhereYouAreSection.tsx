import React from 'react';
import styles from './StartWhereYouAreSection.module.css';

interface Tag {
  text: string;
  color: string;
}

interface StartOption {
  id: number;
  title: string;
  icon: string;
  tags: Tag[];
  price: string;
  priceDetail: string;
  features: string[];
}

const StartWhereYouAreSection = () => {
  const options: StartOption[] = [
    {
      id: 1,
      title: 'Workstation',
      icon: '💻',
      tags: [
        { text: 'High Performance', color: 'blue' },
        { text: 'Hardware Included', color: 'green' },
        { text: 'Max Flexibility', color: 'purple' }
      ],
      price: '$1,500+',
      priceDetail: 'Hardware Investment',
      features: [
        'NVIDIA RTX 4080+ GPU',
        '32GB+ RAM',
        'ROS 2 Compatible OS',
        'Robot Hardware'
      ]
    },
    {
      id: 2,
      title: 'Cloud + Edge',
      icon: '☁️',
      tags: [
        { text: 'Cost Effective', color: 'yellow' },
        { text: 'Scalable', color: 'green' },
        { text: 'Hybrid Approach', color: 'purple' }
      ],
      price: '$50/month',
      priceDetail: 'Ongoing Costs',
      features: [
        'Cloud GPU Resources',
        'Edge Computing',
        'Data Streaming',
        'Development Hardware'
      ]
    },
    {
      id: 3,
      title: 'Simulation Only',
      icon: '🎮',
      tags: [
        { text: 'Budget Option', color: 'red' },
        { text: 'Quick Start', color: 'blue' },
        { text: 'Software Focus', color: 'purple' }
      ],
      price: '$0',
      priceDetail: 'No Hardware Required',
      features: [
        'Physics Simulators',
        'Virtual Sensors',
        'Open-source Tools',
        'Community Models'
      ]
    }
  ];

  const getTagClass = (color: string) => {
    switch(color) {
      case 'blue': return styles.blueTag;
      case 'green': return styles.greenTag;
      case 'purple': return styles.purpleTag;
      case 'yellow': return styles.yellowTag;
      case 'red': return styles.redTag;
      default: return styles.defaultTag;
    }
  };

  return (
    <section id="start" className={styles.startSection}>
      <div className={styles.container}>
        <div className={styles.textCenter}>
          <h2 className={styles.sectionTitle}>Start Where You Are</h2>
          <p className={styles.sectionSubtitle}>
            Choose your path based on available resources and preferences
          </p>
        </div>
        <div className={styles.cardsGrid}>
          {options.map((option) => (
            <div key={option.id} className={styles.optionCard}>
              <h3 className={styles.cardTitle}>{option.title}</h3>
              <div className={styles.icon}>{option.icon}</div>
              <div className={styles.tagsContainer}>
                {option.tags.map((tag, index) => (
                  <div key={index} className={`${styles.tag} ${getTagClass(tag.color)}`}>
                    {tag.text}
                  </div>
                ))}
              </div>
              <div className={styles.priceTag}>{option.price}</div>
              <div className={styles.priceDetail}>{option.priceDetail}</div>
              <ul className={styles.featuresList}>
                {option.features.map((feature, index) => (
                  <li key={index} className={styles.featureItem}>• {feature}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StartWhereYouAreSection;