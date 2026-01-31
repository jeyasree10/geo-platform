import React, { useState } from 'react';
import InputForm from './components/InputForm';
import ResultsDashboard from './components/ResultsDashboard';
import './styles.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handle form submission
   * Sends request to backend API and updates state with results
   */
  const handleAnalyze = async (url, question) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, question }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze. Please check your inputs and try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reset the application state
   */
  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <h1>🚀 GEO Platform</h1>
          <p className="subtitle">Optimize Your Content for AI Search Engines</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container">
        {/* Show input form when no results */}
        {!results && (
          <InputForm 
            onAnalyze={handleAnalyze} 
            loading={loading}
            error={error}
          />
        )}

        {/* Show loading state */}
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Analyzing your website...</p>
            <p className="loading-steps">
              Scraping content → Querying AI → Comparing results → Generating recommendations
            </p>
          </div>
        )}

        {/* Show results dashboard */}
        {results && !loading && (
          <ResultsDashboard 
            results={results}
            onReset={handleReset}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>Built for Hackathon 2026 | Powered by Gemini AI & Firecrawl</p>
        </div>
      </footer>
    </div>
  );
}

export default App;