import { useState, useEffect } from 'react';

function App() {
  const [isTracking, setIsTracking] = useState(true);
  const [currentHost, setCurrentHost] = useState("Loading...");
  const [sessionTime, setSessionTime] = useState("");

  useEffect(() => {
    // Load saved state
    chrome.storage.local.get(['trackingEnabled'], (result) => {
      setIsTracking(result.trackingEnabled !== false);
    });

    // Get current tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        try {
          setCurrentHost(new URL(tabs[0].url).hostname);
        } catch {
          setCurrentHost("System Page");
        }
      }
    });
  }, []);

  const toggleTracking = () => {
    const newState = !isTracking;
    setIsTracking(newState);
    chrome.storage.local.set({ trackingEnabled: newState });
  };

  return (
    <div className="p-4 bg-gray-900 text-white min-h-[300px] flex flex-col font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-6 border-b border-gray-700 pb-3">
        <h1 className="text-lg font-bold text-indigo-400">Study Snitch</h1>
        
        {/* Toggle Switch */}
        <button 
          onClick={toggleTracking}
          className={`w-12 h-6 rounded-full p-1 transition-colors duration-300 ${isTracking ? 'bg-indigo-600' : 'bg-gray-600'}`}
        >
          <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ${isTracking ? 'translate-x-6' : 'translate-x-0'}`}></div>
        </button>
      </div>

      {/* Status Indicator */}
      <div className={`text-center py-2 rounded mb-4 text-xs font-bold tracking-wider uppercase ${isTracking ? 'bg-indigo-900/30 text-indigo-300 border border-indigo-700' : 'bg-red-900/30 text-red-300 border border-red-700'}`}>
        {isTracking ? "● System Active" : "○ Paused"}
      </div>

      {/* Data Cards */}
      <div className="space-y-3 mb-5">
        <div className="bg-gray-800 p-3 rounded border border-gray-700">
          <p className="text-gray-400 text-xs uppercase mb-1">Current Focus</p>
          <p className="font-mono text-sm truncate text-emerald-400">{currentHost}</p>
        </div>

        <div className="bg-gray-800 p-3 rounded border border-gray-700 opacity-60">
          <p className="text-gray-400 text-xs uppercase mb-1">Session Time</p>
          <p className="font-mono text-sm">00:12:45</p>
        </div>
      </div>

      {/* Reset Timer */}
      <div className={`text-center py-2 rounded mb-4 text-xs font-bold tracking-wider uppercase ${isTracking ? 'bg-indigo-600' : 'bg-gray-600'}`}>
        <button>Reset Timer</button>
      </div>

      {/* Footer */}
      <div className="mt-auto pt-4 text-center">
        <p className="text-[10px] text-gray-500">Connected to Localhost:5000</p>
      </div>
    </div>
  );
}

export default App;