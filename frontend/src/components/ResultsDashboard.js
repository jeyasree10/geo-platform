import React, { useState } from 'react';

/**
 * ResultsDashboard Component
 * Displays analysis results with multiple sections
 */
function ResultsDashboard({ results, onReset }) {
  const [activeTab, setActiveTab] = useState('overview');

  /**
   * Render AI Answer section
   */
  const renderAIAnswer = () => (
    <div className="result-section">
      <h3>🤖 AI-Generated Answer</h3>
      <div className="ai-answer-box">
        <div className="format-badge">{results.answer_format}</div>
        <div className="answer-content">
          {results.ai_answer}
        </div>
      </div>
    </div>
  );

  /**
   * Render Topics Comparison section
   */
  const renderTopicsComparison = () => (
    <div className="result-section">
      <h3>📊 Topics Analysis</h3>
      
      <div className="comparison-grid">
        {/* AI Topics */}
        <div className="comparison-column">
          <h4>AI Covered Topics</h4>
          <div className="topics-list">
            {results.ai_topics.map((topic, index) => (
              <span key={index} className="topic-tag ai-topic">
                {topic}
              </span>
            ))}
          </div>
        </div>

        {/* Website Topics */}
        <div className="comparison-column">
          <h4>Your Website Topics</h4>
          <div className="topics-list">
            {results.website_topics.map((topic, index) => (
              <span key={index} className="topic-tag website-topic">
                {topic}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Missing Topics */}
      {results.missing_topics.length > 0 && (
        <div className="missing-topics-section">
          <h4>⚠️ Missing Topics (AI covers, but your site doesn't)</h4>
          <div className="topics-list">
            {results.missing_topics.map((topic, index) => (
              <span key={index} className="topic-tag missing-topic">
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  /**
   * Render Content Gaps section
   */
  const renderContentGaps = () => (
    <div className="result-section">
      <h3>🔍 Content Gaps Detected</h3>
      
      {results.content_gaps.length > 0 ? (
        <ul className="gaps-list">
          {results.content_gaps.map((gap, index) => (
            <li key={index} className="gap-item">
              {gap}
            </li>
          ))}
        </ul>
      ) : (
        <p className="no-gaps">
          ✅ Great! No significant content gaps detected.
        </p>
      )}
    </div>
  );

  /**
   * Render Recommendations section
   */
  const renderRecommendations = () => (
    <div className="result-section recommendations-section">
      <h3>💡 Optimization Recommendations</h3>
      
      <div className="recommendations-list">
        {results.recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <div className="recommendation-number">{index + 1}</div>
            <div className="recommendation-content">{rec}</div>
          </div>
        ))}
      </div>

      <div className="action-tip">
        <strong>💪 Action Plan:</strong> Implement these recommendations in order of priority 
        to improve your content's visibility in AI search results.
      </div>
    </div>
  );

  /**
   * Render Overview tab
   */
  const renderOverview = () => (
    <div className="overview-container">
      {/* Summary Cards */}
      <div className="summary-grid">
        <div className="summary-card">
          <div className="summary-icon">📝</div>
          <div className="summary-content">
            <h4>Answer Format</h4>
            <p>{results.answer_format}</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">🎯</div>
          <div className="summary-content">
            <h4>Missing Topics</h4>
            <p>{results.missing_topics.length} topics</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">⚠️</div>
          <div className="summary-content">
            <h4>Content Gaps</h4>
            <p>{results.content_gaps.length} gaps found</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">💡</div>
          <div className="summary-content">
            <h4>Recommendations</h4>
            <p>{results.recommendations.length} actions</p>
          </div>
        </div>
      </div>

      {/* Quick Insights */}
      <div className="quick-insights">
        <h3>📈 Quick Insights</h3>
        <div className="insight-item">
          <span className="insight-label">AI Answer Length:</span>
          <span className="insight-value">{results.ai_answer.split(' ').length} words</span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Structure Match:</span>
          <span className="insight-value">
            {results.content_gaps.some(g => g.includes('structure')) ? 
              '⚠️ Needs Improvement' : '✅ Good Match'}
          </span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Topic Coverage:</span>
          <span className="insight-value">
            {Math.round((1 - results.missing_topics.length / results.ai_topics.length) * 100)}%
          </span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="results-dashboard">
      {/* Dashboard Header */}
      <div className="dashboard-header">
        <h2>📊 Analysis Results</h2>
        <button className="btn btn-secondary" onClick={onReset}>
          ← New Analysis
        </button>
      </div>

      {/* Tabs Navigation */}
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'ai-answer' ? 'active' : ''}`}
          onClick={() => setActiveTab('ai-answer')}
        >
          AI Answer
        </button>
        <button 
          className={`tab ${activeTab === 'topics' ? 'active' : ''}`}
          onClick={() => setActiveTab('topics')}
        >
          Topics
        </button>
        <button 
          className={`tab ${activeTab === 'gaps' ? 'active' : ''}`}
          onClick={() => setActiveTab('gaps')}
        >
          Content Gaps
        </button>
        <button 
          className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'ai-answer' && renderAIAnswer()}
        {activeTab === 'topics' && renderTopicsComparison()}
        {activeTab === 'gaps' && renderContentGaps()}
        {activeTab === 'recommendations' && renderRecommendations()}
      </div>
    </div>
  );
}

export default ResultsDashboard;