import React, { useState, useEffect } from 'react';
import BookReader from '../components/BookReader';
import ChatInterface from '../components/ChatInterface';
import SelectionHandler from '../components/SelectionHandler';
import { v4 as uuidv4 } from 'uuid';
import apiClient from '../services/api';
import './BookPage.css';

const BookPage = () => {
  const [bookContent, setBookContent] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(uuidv4()); // Generate a new session ID for this session
  const [selectedText, setSelectedText] = useState('');
  const [bookId, setBookId] = useState(''); // This would normally come from props or URL

  // For demo purposes, we'll use sample book content
  useEffect(() => {
    // In a real implementation, you would fetch the book content based on the bookId
    // For now, we'll use sample content
    const sampleContent = `# Introduction to Physical AI and Robotics

Physical AI is an interdisciplinary field that combines artificial intelligence with physical systems, particularly robotics. This field focuses on creating intelligent agents that can interact with the physical world effectively.

## Chapter 1: Fundamentals of Robotics

Robotics is the branch of technology that deals with the design, construction, operation, and application of robots. It involves mechanical engineering, electrical engineering, information engineering, and computer science.

Key components of a robot include:
- Sensors: To perceive the environment
- Actuators: To interact with the environment
- Controller: To process information and make decisions
- Power source: To operate the system

## Chapter 2: Artificial Intelligence in Robotics

AI in robotics involves creating algorithms that allow robots to perform tasks autonomously. This includes:
- Perception: Understanding the environment
- Planning: Deciding what actions to take
- Control: Executing actions effectively

Machine learning, particularly reinforcement learning, has shown great promise in robotics applications.`;
    
    setBookContent(sampleContent);
    setBookId('sample-book-id'); // Set a sample book ID
  }, []);

  const handleTextSelect = (selectedText) => {
    setSelectedText(selectedText);
  };

  const handleSend = async (query, selectedTextForQuery = '') => {
    setLoading(true);
    
    try {
      // Add user message to the chat
      const userMessage = {
        text: query,
        isUser: true
      };
      
      setMessages(prev => [...prev, userMessage]);
      
      // Prepare the request payload
      const payload = {
        session_id: sessionId,
        book_id: bookId,
        query: query
      };
      
      // Include selected text if available
      if (selectedTextForQuery) {
        payload.selected_text = selectedTextForQuery;
      }
      
      // Call the backend API
      const response = await apiClient.post('/chat', payload);
      
      // Add the assistant's response to the chat
      const assistantMessage = {
        text: response.data.answer,
        isUser: false,
        confidence: response.data.confidence_level
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      const errorMessage = {
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        isUser: false
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearSelection = () => {
    setSelectedText('');
  };

  return (
    <div className="book-page">
      <header className="book-header">
        <h1>Physical AI & Robotics Textbook</h1>
      </header>
      
      <div className="book-content-area">
        <div className="book-reader-container">
          <BookReader 
            bookContent={bookContent} 
            onTextSelect={handleTextSelect} 
          />
        </div>
        
        <div className="chat-container">
          <SelectionHandler 
            selectedText={selectedText} 
            onClearSelection={handleClearSelection} 
          />
          <ChatInterface 
            sessionId={sessionId}
            bookId={bookId}
            messages={messages}
            loading={loading}
            onSend={handleSend}
          />
        </div>
      </div>
    </div>
  );
};

export default BookPage;