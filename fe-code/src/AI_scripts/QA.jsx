import React, { useState } from 'react';

export default function QA() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([
    { text: 'What do you need help with from the document?', isUser: false },
  ]);
 
  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (inputText.trim()) {
      const newMessage = { text: inputText, isUser: true };
      setMessages([...messages, newMessage]);

      // This is where we make the api requests
      setTimeout(() => {
        const botResponse = {
          text: `From your prompt: ${inputText}`, // Bot response can be more complex based on your logic
          isUser: false,
        };
        setMessages((prevMessages) => [...prevMessages, botResponse]);
      }, 1000);

      setInputText(''); // Clear input field
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <div
        style={{
          height: '400px',
          overflowY: 'scroll',
          border: '1px solid #ccc',
          padding: '10px',
          marginBottom: '10px',
          backgroundColor: '#f9f9f9',
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              textAlign: message.isUser ? 'right' : 'left',
              marginBottom: '10px',
            }}
          >
            <div
              style={{
                display: 'inline-block',
                padding: '10px',
                borderRadius: '10px',
                backgroundColor: message.isUser ? '#daf8e3' : '#e2e2e2',
                maxWidth: '80%',
                wordWrap: 'break-word',
              }}
            >
              {message.text}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex' }}>
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
          placeholder="Type your message..."
          style={{
            flexGrow: 1,
            padding: '10px',
            borderRadius: '5px',
            border: '1px solid #ccc',
          }}
        />
        <button
          type="submit"
          style={{
            padding: '10px',
            marginLeft: '10px',
            borderRadius: '5px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}
