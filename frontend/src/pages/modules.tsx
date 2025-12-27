import React from 'react';
import Layout from '@theme/Layout';
import styles from './modules.module.css';

const ModulesPage = () => {
  const modules = [
    {
      id: 1,
      title: 'Robot Middleware (ROS 2 Fundamentals)',
      icon: '🤖',
      topics: [
        'Node Communication Patterns',
        'Services and Actions',
        'Parameter Systems',
        'Lifecycle Nodes',
        'Real-time Performance'
      ],
      duration: 'Weeks 1–5'
    },
    {
      id: 2,
      title: 'Simulation (Digital Twins)',
      icon: '🔄',
      topics: [
        'Physics-Based Simulators',
        'Domain Randomization',
        'Sensor Simulation',
        'Environment Generation',
        'Sim-to-Real Transfer'
      ],
      duration: 'Weeks 6–7'
    },
    {
      id: 3,
      title: 'AI-Powered NVIDIA Isaac',
      icon: '🧠',
      topics: [
        'Isaac Lab Framework',
        'RL Training Pipelines',
        'Perception Networks',
        'Motion Generation',
        'Manipulation Skills'
      ],
      duration: 'Weeks 8–10'
    },
    {
      id: 4,
      title: 'Capstone (Vision-Language-Action)',
      icon: '🎓',
      topics: [
        'Vision-Language Models',
        'Multimodal Fusion',
        'Task Planning',
        'Interactive Learning',
        'Real-World Deployment'
      ],
      duration: 'Weeks 11–13'
    }
  ];

  return (
    <Layout title="Modules" description="Learning roadmap for RoboLearn">
      <main className={styles.modulesPage}>
        <div className={styles.pageHeader}>
          <h1 className={styles.pageTitle}>Learning Roadmap</h1>
          <p className={styles.pageSubtitle}>Master Physical AI and robotics through our structured curriculum</p>
        </div>

        <div className={styles.modulesGrid}>
          {modules.map((module) => (
            <div key={module.id} className={styles.moduleCard}>
              <div className={styles.cardHeader}>
                <div className={styles.icon}>{module.icon}</div>
                <h2 className={styles.moduleTitle}>{module.title}</h2>
              </div>
              
              <ul className={styles.topicsList}>
                {module.topics.map((topic, index) => (
                  <li key={index} className={styles.topicItem}>• {topic}</li>
                ))}
              </ul>
              
              <div className={styles.durationBadge}>{module.duration}</div>
            </div>
          ))}
        </div>
      </main>
    </Layout>
  );
};

export default ModulesPage;