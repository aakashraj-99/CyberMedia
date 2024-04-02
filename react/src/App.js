import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import logo from './logo.png'; // Replace with your actual logo path

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [userPrompt, setUserPrompt] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!videoUrl || !userPrompt) {
      alert("Please fill in both fields.");
      return;
    }
    const newMessages = [...messages, { type: 'user', text: userPrompt }];
    setMessages(newMessages);
    setUserPrompt('');
    try {
      const { data } = await axios.post('http://localhost/process_video', {
        video_url: videoUrl,
        user_input: userPrompt,
      });
      setMessages([...newMessages, { type: 'bot', text: data.response }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([...newMessages, { type: 'bot', text: "Failed to fetch response." }]);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <img src={logo} alt="CyberMedia Logo" className="app-logo" />
      </header>
      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="YouTube Link"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            className="youtube-input"
          />
          <input
            type="text"
            placeholder="What do you want to ask?"
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            className="question-input"
          />
          <button onClick={handleSend} className="send-button">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
