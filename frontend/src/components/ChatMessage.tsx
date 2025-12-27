import React from 'react';

// Define the citation structure
interface Citation {
  title: string;
  url: string;
  chapter?: string;
}

interface MessageProps {
  text: string;
  timestamp: Date;
  sources?: Citation[]; // Using Citation[] instead of string[]
}

export const UserMessage: React.FC<MessageProps> = ({ text, timestamp }) => {
  return (
    <div
      className="flex justify-end mb-4"
      role="listitem"
      aria-label={`User message: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`}
    >
      <div
        className="bg-blue-500 text-white p-3 rounded-lg max-w-[80%]"
        role="region"
        aria-live="polite"
      >
        <p>{text}</p>
        <p className="text-xs opacity-70 mt-1 text-right" aria-label={`Message sent at ${timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`}>
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};

export const AssistantMessage: React.FC<MessageProps> = ({ text, timestamp, sources }) => {
  return (
    <div
      className="flex justify-start mb-4"
      role="listitem"
      aria-label={`Assistant message: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`}
    >
      <div
        className="bg-gray-100 p-3 rounded-lg max-w-[80%] border border-gray-200"
        role="region"
        aria-live="polite"
      >
        <div className="flex items-start">
          <span className="mr-2" aria-hidden="true">🤖</span>
          <span className="text-gray-800">{text}</span>
        </div>
        {sources && sources.length > 0 && (
          <div
            className="mt-2 pt-2 border-t border-gray-200"
            role="region"
            aria-labelledby="sources-title"
          >
            <p id="sources-title" className="text-xs font-medium text-gray-500 mb-1">Sources:</p>
            <ul
              className="text-xs text-gray-600 list-disc pl-5 space-y-1"
              aria-label="Cited sources"
            >
              {sources.map((citation, index) => (
                <li key={index}>
                  <a
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`Source: ${citation.title || citation.url}`}
                  >
                    {citation.title || citation.url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="text-xs opacity-70 mt-1" aria-label={`Message sent at ${timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`}>
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};