import React from 'react';
import Link from '@docusaurus/Link';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Profile(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Profile - ${siteConfig.title}`}
      description="Manage your RoboLearn profile and settings">
      <Head>
        <title>Profile - RoboLearn</title>
        <meta name="description" content="Manage your RoboLearn profile and settings" />
      </Head>

      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className="padding--lg">
              <h1 className="text--center">Your Profile</h1>
              
              <div className="margin-vert--lg">
                <div className="card">
                  <div className="card__header">
                    <h3>Account Information</h3>
                  </div>
                  <div className="card__body">
                    <form>
                      <div className="row margin-bottom--md">
                        <div className="col col--6">
                          <label htmlFor="firstName">First Name</label>
                          <input
                            type="text"
                            id="firstName"
                            className="form-control"
                            placeholder="John"
                          />
                        </div>
                        <div className="col col--6">
                          <label htmlFor="lastName">Last Name</label>
                          <input
                            type="text"
                            id="lastName"
                            className="form-control"
                            placeholder="Doe"
                          />
                        </div>
                      </div>
                      
                      <div className="margin-bottom--md">
                        <label htmlFor="email">Email Address</label>
                        <input
                          type="email"
                          id="email"
                          className="form-control"
                          placeholder="your@email.com"
                        />
                      </div>
                      
                      <div className="margin-bottom--md">
                        <label htmlFor="bio">Bio</label>
                        <textarea
                          id="bio"
                          className="form-control"
                          placeholder="Tell us about yourself..."
                          rows={4}
                        />
                      </div>
                      
                      <div className="margin-bottom--md">
                        <label htmlFor="learningGoals">Learning Goals</label>
                        <textarea
                          id="learningGoals"
                          className="form-control"
                          placeholder="What do you want to achieve with Physical AI?"
                          rows={3}
                        />
                      </div>
                      
                      <div className="margin-bottom--md">
                        <label className="form-label">Current Skill Level</label>
                        <div className="form-group">
                          <label className="radio">
                            <input type="radio" name="skillLevel" defaultChecked /> Beginner
                          </label>
                          <label className="radio margin-left--md">
                            <input type="radio" name="skillLevel" /> Intermediate
                          </label>
                          <label className="radio margin-left--md">
                            <input type="radio" name="skillLevel" /> Advanced
                          </label>
                        </div>
                      </div>
                      
                      <button type="submit" className="button button--primary button--lg">
                        Save Changes
                      </button>
                    </form>
                  </div>
                </div>
                
                <div className="margin-vert--lg text--center">
                  <Link className="button button--secondary button--lg" to="/docs/intro">
                    Continue Learning
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}