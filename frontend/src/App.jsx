import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import BookPage from './pages/BookPage';

function App() {
  return (
    <div className="App">
      <BookPage />
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

export default App;