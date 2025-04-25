import React, { useState } from 'react';
import './App.css';
import DicomViewer from './components/DicomViewer';
import Login from './components/Login';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access_token'));

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsLoggedIn(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MediConnect</h1>
        {isLoggedIn && <button onClick={handleLogout}>Se déconnecter</button>}
      </header>
      <main>
        {isLoggedIn ? <DicomViewer /> : <Login onLogin={handleLogin} />}
      </main>
    </div>
  );
}

export default App;