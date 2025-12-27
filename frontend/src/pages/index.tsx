import React, { JSX } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import HeroSection from '@site/src/components/Homepage/HeroSection';
import WhyThisMattersSection from '@site/src/components/Homepage/WhyThisMattersSection';
import ModulesSection from '@site/src/components/Homepage/ModulesSection';
import StartWhereYouAreSection from '@site/src/components/Homepage/StartWhereYouAreSection';
import FinalCTASection from '@site/src/components/Homepage/FinalCTASection';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description={siteConfig.tagline}>
      <HeroSection />
      <main>
        <WhyThisMattersSection />
        <ModulesSection />
        <StartWhereYouAreSection />
        <HomepageFeatures />
        <FinalCTASection />
      </main>
    </Layout>
  );
}