import React from 'react';
import styles from './ModulesSection.module.css';

interface ModuleItem {
  id: number;
  title: string;
  icon: string;
  topics: string[];
  duration: string;
}

const ModulesSection = () => {
  const modules: ModuleItem[] = [
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
    <section id="modules" className={styles.modulesSection}>
      <div className={styles.container}>
        <div className={styles.grid}>
          {modules.map((module) => (
            <div key={module.id} className={styles.moduleCard}>
              <div className={styles.cardContent}>
                <div className={styles.icon}>{module.icon}</div>
                <h3 className={styles.moduleTitle}>{module.title}</h3>
                <ul className={styles.topicsList}>
                  {module.topics.map((topic, index) => (
                    <li key={index} className={styles.topicItem}>• {topic}</li>
                  ))}
                </ul>
                <div className={styles.durationBadge}>{module.duration}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ModulesSection;