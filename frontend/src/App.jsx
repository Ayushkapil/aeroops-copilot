import React, { useState, useEffect } from 'react';
import UnifiedConsole from './pages/UnifiedConsole';

export default function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('aeroops-theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('aeroops-theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  return <UnifiedConsole theme={theme} toggleTheme={toggleTheme} />;
}
