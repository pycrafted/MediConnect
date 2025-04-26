import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import Login from './components/Login';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Appointments from './pages/Appointments';
import MedicalRecord from './pages/MedicalRecord';
import DicomViewer from './components/DicomViewer';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access_token'));

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
  }, []);

  return (
    <Router>
      <div className="flex">
        {isAuthenticated && <Sidebar onLogout={handleLogout} />}
        <div className="flex-1 p-6">
          <Routes>
            <Route
              path="/login"
              element={
                isAuthenticated ? <Navigate to="/" /> : <Login onLogin={handleLogin} />
              }
            />
            <Route
              path="/"
              element={
                isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/profile"
              element={
                isAuthenticated ? <Profile /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/appointments"
              element={
                isAuthenticated ? <Appointments /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/medical-record"
              element={
                isAuthenticated ? <MedicalRecord /> : <Navigate to="/login" />
              }
            />
            <Route
              path="/dicom-viewer"
              element={
                isAuthenticated ? <DicomViewer /> : <Navigate to="/login" />
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;