import React, { useState, useEffect } from 'react';
import './AIAssistant.css';
import CitationDisplay from './CitationDisplay';
import LoadingIndicator from './LoadingIndicator';
import ErrorMessage from './ErrorMessage';

const AIAssistant = ({ bookId, sessionId }) => {
  const [question, setQuestion] = useState('');
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedText, setSelectedText] = useState(null);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() && !selectedText) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await askQuestion(question, selectedText);
      setResponses(prev => [...prev, { question, response, id: Date.now() }]);
      setQuestion('');
      setSelectedText(null); // Clear selected text after asking
    } catch (err) {
      setError(err.message || 'An error occurred while processing your question.');
    } finally {
      setIsLoading(false);
    }
  };

  const askQuestion = async (question, selectedText = null) => {
    // In a real implementation, this would call the backend API
    // For now, we'll simulate an API call
    const response = await new Promise(resolve => {
      setTimeout(() => {
        resolve({
          response: "This is a simulated response based on the textbook content. The actual implementation would connect to the backend API to retrieve information from the textbook.",
          citations: ["Chapter 3 - Embodied Cognition (p. 45)", "Chapter 5 - Sensorimotor Learning (p. 78)"],
          grounding_status: "Valid"
        });
      }, 1500);
    });

    return response;
  };

  return (
    <div className="ai-assistant">
      <h3>Textbook AI Assistant</h3>
      <form onSubmit={handleSubmit} className="ai-form">
        {selectedText && (
          <div className="selected-text-preview">
            <p><strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</p>
          </div>
        )}
        
        <div className="input-group">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about the textbook content..."
            className="question-input"
            rows="3"
          />
          <button type="submit" disabled={isLoading} className="ask-button">
            {isLoading ? 'Asking...' : 'Ask Question'}
          </button>
        </div>
      </form>

      {isLoading && <LoadingIndicator message="Processing your question..." />}
      {error && <ErrorMessage message={error} />}

      <div className="responses">
        {responses.map((item) => (
          <div key={item.id} className="response-item">
            <div className="question">
              <strong>You:</strong> {item.question}
            </div>
            <div className="answer">
              <strong>AI Assistant:</strong> {item.response.response}
              {item.response.citations && item.response.citations.length > 0 && (
                <CitationDisplay citations={item.response.citations} />
              )}
              <div className={`grounding-status ${item.response.grounding_status.toLowerCase()}`}>
                Status: {item.response.grounding_status}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AIAssistant;