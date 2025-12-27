import React, { createContext, useContext, useReducer } from 'react';

// Initial state for the chat context
const initialState = {
  sessionId: null,
  messages: [],
  currentQuery: '',
  selectedText: null,
  isProcessing: false,
  error: null,
};

// Define action types
const actionTypes = {
  SET_SESSION_ID: 'SET_SESSION_ID',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_CURRENT_QUERY: 'SET_CURRENT_QUERY',
  SET_SELECTED_TEXT: 'SET_SELECTED_TEXT',
  CLEAR_SELECTED_TEXT: 'CLEAR_SELECTED_TEXT',
  SET_PROCESSING: 'SET_PROCESSING',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  RESET_CHAT: 'RESET_CHAT',
};

// Reducer function to handle state changes
const chatReducer = (state, action) => {
  switch (action.type) {
    case actionTypes.SET_SESSION_ID:
      return {
        ...state,
        sessionId: action.payload,
      };
    case actionTypes.ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };
    case actionTypes.SET_CURRENT_QUERY:
      return {
        ...state,
        currentQuery: action.payload,
      };
    case actionTypes.SET_SELECTED_TEXT:
      return {
        ...state,
        selectedText: action.payload,
      };
    case actionTypes.CLEAR_SELECTED_TEXT:
      return {
        ...state,
        selectedText: null,
      };
    case actionTypes.SET_PROCESSING:
      return {
        ...state,
        isProcessing: action.payload,
      };
    case actionTypes.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        isProcessing: false,
      };
    case actionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case actionTypes.RESET_CHAT:
      return {
        ...initialState,
        sessionId: state.sessionId, // Preserve session ID when resetting
      };
    default:
      return state;
  }
};

// Create the context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const setSessionId = (sessionId) => {
    dispatch({ type: actionTypes.SET_SESSION_ID, payload: sessionId });
  };

  const addMessage = (message) => {
    dispatch({ type: actionTypes.ADD_MESSAGE, payload: message });
  };

  const setCurrentQuery = (query) => {
    dispatch({ type: actionTypes.SET_CURRENT_QUERY, payload: query });
  };

  const setSelectedText = (text) => {
    dispatch({ type: actionTypes.SET_SELECTED_TEXT, payload: text });
  };

  const clearSelectedText = () => {
    dispatch({ type: actionTypes.CLEAR_SELECTED_TEXT });
  };

  const setProcessing = (processing) => {
    dispatch({ type: actionTypes.SET_PROCESSING, payload: processing });
  };

  const setError = (error) => {
    dispatch({ type: actionTypes.SET_ERROR, payload: error });
  };

  const clearError = () => {
    dispatch({ type: actionTypes.CLEAR_ERROR });
  };

  const resetChat = () => {
    dispatch({ type: actionTypes.RESET_CHAT });
  };

  return (
    <ChatContext.Provider
      value={{
        ...state,
        setSessionId,
        addMessage,
        setCurrentQuery,
        setSelectedText,
        clearSelectedText,
        setProcessing,
        setError,
        clearError,
        resetChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};