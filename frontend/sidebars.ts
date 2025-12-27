import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Textbook Modules',
      link: {
        type: 'generated-index',
        description: 'Complete textbook on Physical AI & Humanoid Robotics organized into 4 comprehensive modules',
      },
      items: [
        {
          type: 'category',
          label: 'Module 1: Foundations & Design',
          link: {
            type: 'doc',
            id: 'modules/module-1-intro',
          },
          items: [
            'modules/module-1-intro',
            'chapters/foundations-of-physical-ai', // Chapter 1
            'chapters/humanoid-robot-design-principles', // Chapter 2
            'chapters/locomotion-and-bipedal-walking', // Chapter 3
          ],
        },
        {
          type: 'category',
          label: 'Module 2: Perception & Control',
          link: {
            type: 'doc',
            id: 'modules/module-2-intro',
          },
          items: [
            'modules/module-2-intro',
            'chapters/manipulation-and-grasping', // Chapter 4
            'chapters/perception-and-sensing', // Chapter 5
            'chapters/planning-and-decision-making', // Chapter 6
            'chapters/control-systems-and-dynamics', // Chapter 7
          ],
        },
        {
          type: 'category',
          label: 'Module 3: Learning & Interaction',
          link: {
            type: 'doc',
            id: 'modules/module-3-intro',
          },
          items: [
            'modules/module-3-intro',
            'chapters/learning-and-adaptation', // Chapter 8
            'chapters/human-robot-interaction', // Chapter 9
          ],
        },
        {
          type: 'category',
          label: 'Module 4: Applications & Future',
          link: {
            type: 'doc',
            id: 'modules/module-4-intro',
          },
          items: [
            'modules/module-4-intro',
            'chapters/applications-and-use-cases', // Chapter 10
            'chapters/ethics-and-society', // Chapter 11
            'chapters/future-directions-and-conclusions', // Chapter 12
          ],
        },
      ],
    }
  ],
};

export default sidebars;
