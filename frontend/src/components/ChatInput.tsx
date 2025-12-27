import React, { useState, useRef, useEffect } from 'react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  placeholder?: string;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, placeholder = "Type your message...", disabled = false }) => {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [inputValue]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any); // Type assertion to FormEvent
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form" role="form" aria-label="Chat input form">
      <div className="input-container" role="group" aria-labelledby="chat-input-label">
        <span id="chat-input-label" className="sr-only">Type your message</span>
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          aria-label="Type your message"
          aria-describedby="chat-instructions"
          rows={1}
          className="chat-input-textarea"
        />
        <button
          type="submit"
          disabled={disabled || !inputValue.trim()}
          aria-label="Send message"
          className="send-button"
        >
          <span aria-hidden="true">➤</span>
        </button>
        <div id="chat-instructions" className="sr-only">
          Press Enter to submit your message, Shift+Enter for a new line
        </div>
      </div>
    </form>
  );
};

export default ChatInput;