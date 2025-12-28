import React, { useState } from 'react';
import Layout from '@theme/Layout';
import './ProfilePage.css';

const ProfilePage = () => {
  const [formData, setFormData] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: 'your@email.com',
    bio: '',
    learningGoals: '',
    skillLevel: 'beginner'
  });

  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    // Simulate API call
    setTimeout(() => {
      setIsSaving(false);
      setIsEditing(false);
    }, 1000);
  };

  return (
    <Layout title="Your Profile" description="Manage your learning profile">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar">
            <div className="avatar-circle">
              {formData.firstName.charAt(0)}{formData.lastName.charAt(0)}
            </div>
            <button className="avatar-edit-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
            </button>
          </div>
          <div className="profile-title">
            <h1>Your Profile</h1>
            <p>Manage your learning journey and preferences</p>
          </div>
          <div className="profile-actions">
            {!isEditing ? (
              <button className="edit-btn" onClick={() => setIsEditing(true)}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
                Edit Profile
              </button>
            ) : (
              <div className="edit-actions">
                <button className="cancel-btn" onClick={() => setIsEditing(false)}>
                  Cancel
                </button>
                <button className="save-btn" onClick={handleSave} disabled={isSaving}>
                  {isSaving ? (
                    <div className="loading-spinner"></div>
                  ) : (
                    'Save Changes'
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="profile-content">
          <div className="profile-section">
            <h2>Account Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="firstName">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="form-group full-width">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>About You</h2>
            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                placeholder="Tell us about yourself..."
                disabled={!isEditing}
                rows={4}
              />
            </div>
          </div>

          <div className="profile-section">
            <h2>Learning Preferences</h2>
            <div className="form-group">
              <label htmlFor="learningGoals">Learning Goals</label>
              <textarea
                id="learningGoals"
                name="learningGoals"
                value={formData.learningGoals}
                onChange={handleChange}
                placeholder="What do you want to achieve with Physical AI?"
                disabled={!isEditing}
                rows={3}
              />
            </div>
            
            <div className="form-group">
              <label>Current Skill Level</label>
              <div className="radio-group">
                <label className="radio-option">
                  <input
                    type="radio"
                    name="skillLevel"
                    value="beginner"
                    checked={formData.skillLevel === 'beginner'}
                    onChange={handleChange}
                    disabled={!isEditing}
                  />
                  <span className="radio-custom"></span>
                  <div className="radio-content">
                    <strong>Beginner</strong>
                    <p>New to robotics and AI</p>
                  </div>
                </label>
                
                <label className="radio-option">
                  <input
                    type="radio"
                    name="skillLevel"
                    value="intermediate"
                    checked={formData.skillLevel === 'intermediate'}
                    onChange={handleChange}
                    disabled={!isEditing}
                  />
                  <span className="radio-custom"></span>
                  <div className="radio-content">
                    <strong>Intermediate</strong>
                    <p>Some experience with robotics concepts</p>
                  </div>
                </label>
                
                <label className="radio-option">
                  <input
                    type="radio"
                    name="skillLevel"
                    value="advanced"
                    checked={formData.skillLevel === 'advanced'}
                    onChange={handleChange}
                    disabled={!isEditing}
                  />
                  <span className="radio-custom"></span>
                  <div className="radio-content">
                    <strong>Advanced</strong>
                    <p>Experienced in robotics and AI</p>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>Learning Progress</h2>
            <div className="progress-stats">
              <div className="stat-card">
                <div className="stat-number">8</div>
                <div className="stat-label">Chapters Completed</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">67%</div>
                <div className="stat-label">Course Progress</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">24</div>
                <div className="stat-label">Hours Studied</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">156</div>
                <div className="stat-label">Questions Asked</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProfilePage;