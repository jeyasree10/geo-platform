import React, { useState } from 'react';

/**
 * Sample questions bank for quick testing
 */
const SAMPLE_QUESTIONS = [
  "What are the best practices for web development?",
  "How does artificial intelligence improve healthcare?",
  "What are the benefits of renewable energy?",
  "How can small businesses leverage social media marketing?",
  "What are the key principles of user experience design?",
  "How does blockchain technology ensure security?",
  "What are effective strategies for remote team management?",
  "How can companies reduce their carbon footprint?",
  "What are the latest trends in mobile app development?",
  "How does machine learning differ from traditional programming?",
  "What are the best practices for cybersecurity in 2026?",
  "How can content marketing drive business growth?",
  "What are the advantages of cloud computing for enterprises?",
  "How does sustainable fashion impact the environment?",
  "What are effective techniques for data visualization?",
  "How can meditation improve mental health?",
  "What are the essential components of a startup pitch?",
  "How does quantum computing work?",
  "What are the benefits of agile project management?",
  "How can automation transform customer service?",
  "What are the most effective SEO strategies in 2026?",
  "How does cryptocurrency work and why is it valuable?",
  "What are the benefits of electric vehicles?",
  "How can businesses implement sustainable practices?",
  "What are the key trends in artificial intelligence?",
  "How does 5G technology improve connectivity?",
  "What are the best practices for email marketing?",
  "How can companies build a strong employer brand?",
  "What are the fundamentals of financial planning?",
  "How does influencer marketing drive sales?",
  "What are the advantages of microservices architecture?",
  "How can mindfulness practices reduce stress?",
  "What are the essential skills for data scientists?",
  "How does edge computing differ from cloud computing?",
  "What are the benefits of plant-based diets?",
  "How can virtual reality transform education?",
  "What are the key factors in successful e-commerce?",
  "How does natural language processing work?",
  "What are the best strategies for time management?",
  "How can businesses leverage big data analytics?",
  "What are the principles of ethical AI development?",
  "How does solar energy contribute to sustainability?",
  "What are the advantages of containerization in DevOps?",
  "How can companies improve customer retention?",
  "What are the health benefits of regular exercise?"
];

/**
 * InputForm Component
 * Collects URL and question from user and initiates analysis
 */
function InputForm({ onAnalyze, loading, error }) {
  const [url, setUrl] = useState('');
  const [question, setQuestion] = useState('');
  const [showQuestions, setShowQuestions] = useState(false);

  /**
   * Validate and submit form
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!url.trim()) {
      alert('Please enter a website URL');
      return;
    }
    
    if (!question.trim()) {
      alert('Please enter a question or topic');
      return;
    }

    // Ensure URL has protocol
    let validUrl = url.trim();
    if (!validUrl.startsWith('http://') && !validUrl.startsWith('https://')) {
      validUrl = 'https://' + validUrl;
    }

    // Call parent handler
    onAnalyze(validUrl, question.trim());
  };

  /**
   * Load example data for quick testing with random question
   */
  const loadExample = () => {
    const randomIndex = Math.floor(Math.random() * SAMPLE_QUESTIONS.length);
    setUrl('https://example.com');
    setQuestion(SAMPLE_QUESTIONS[randomIndex]);
  };

  /**
   * Load a random question from the sample bank
   */
  const loadRandomQuestion = () => {
    const randomIndex = Math.floor(Math.random() * SAMPLE_QUESTIONS.length);
    setQuestion(SAMPLE_QUESTIONS[randomIndex]);
    setShowQuestions(false);
  };

  /**
   * Select a specific question from the list
   */
  const selectQuestion = (selectedQuestion) => {
    setQuestion(selectedQuestion);
    setShowQuestions(false);
  };

  return (
    <div className="input-form-container">
      <div className="card">
        <h2>Analyze Your Website</h2>
        <p className="description">
          Enter your website URL and a topic or question to see how AI search engines 
          interpret your content and get optimization recommendations.
        </p>

        <form onSubmit={handleSubmit} className="input-form">
          {/* URL Input */}
          <div className="form-group">
            <label htmlFor="url">Website URL</label>
            <input
              type="text"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              disabled={loading}
              className="form-input"
            />
            <small className="form-hint">Enter the full URL of the page you want to analyze</small>
          </div>

          {/* Question Input */}
          <div className="form-group">
            <label htmlFor="question">Topic or Question</label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What are the benefits of sustainable energy?"
              disabled={loading}
              className="form-textarea"
              rows="4"
            />
            <small className="form-hint">
              Enter a question or topic related to your website's content
            </small>
            {/* Questions Modal */}
            {showQuestions && (
              <div className="questions-modal">
                <div className="questions-header">
                  <h4>Select a Question</h4>
                  <button 
                    className="close-modal"
                    onClick={() => setShowQuestions(false)}
                  >
                    ✕
                  </button>
                </div>
                <div className="questions-list">
                  {SAMPLE_QUESTIONS.map((q, index) => (
                    <div 
                      key={index}
                      className="question-item"
                      onClick={() => selectQuestion(q)}
                    >
                      <span className="question-number">{index + 1}</span>
                      <span className="question-text">{q}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Analyzing...' : '🔍 Analyze Now'}
            </button>
            
            <button 
              type="button" 
              className="btn btn-secondary"
              onClick={loadExample}
              disabled={loading}
            >
              Load Example
            </button>
          </div>
        </form>

        {/* Info Box */}
        <div className="info-box">
          <h3>How it works:</h3>
          <ol>
            <li>We scrape your website's content</li>
            <li>We ask AI the same question</li>
            <li>We compare both to find gaps</li>
            <li>We provide actionable recommendations</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default InputForm;