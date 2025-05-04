document.addEventListener('DOMContentLoaded', function() {
  // Create chat widget structure
  const chatHTML = `
    <div class="chat-toggle">Chat</div>
    <div class="chat-container">
      <div class="chat-header">
        <div>Remtech Assistant</div>
        <div class="chat-close">×</div>
      </div>
      <div class="chat-messages" id="chatMessages">
        <div>Hello! How can I help you with Remtech's electrical services?</div>
      </div>
      <div class="chat-input">
        <textarea id="userChatMessage" placeholder="Type your question..."></textarea>
        <button onclick="sendChatMessage()">Send</button>
      </div>
    </div>
  `;
  
  // Create widget and add to page
  const chatWidget = document.createElement('div');
  chatWidget.className = 'chat-widget';
  chatWidget.innerHTML = chatHTML;
  document.body.appendChild(chatWidget);
  
  // Toggle chat open/close
  document.querySelector('.chat-toggle').addEventListener('click', function() {
    document.querySelector('.chat-container').classList.add('chat-visible');
  });
  
  // Close chat
  document.querySelector('.chat-close').addEventListener('click', function() {
    document.querySelector('.chat-container').classList.remove('chat-visible');
  });
});

// Send message to API
async function sendChatMessage() {
  const messageInput = document.getElementById('userChatMessage');
  const userMessage = messageInput.value;
  if (!userMessage.trim()) return;
  
  // Add user message to chat
  const userDiv = document.createElement('div');
  userDiv.style.textAlign = 'right';
  userDiv.style.marginBottom = '10px';
  userDiv.textContent = userMessage;
  document.getElementById('chatMessages').appendChild(userDiv);
  
  // Clear input
  messageInput.value = '';
  
  try {
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: userMessage })
    });
    
    const data = await response.json();
    
    // Add bot response to chat
    const botDiv = document.createElement('div');
    botDiv.style.marginBottom = '10px';
    botDiv.textContent = data.reply;
    document.getElementById('chatMessages').appendChild(botDiv);
    
    // Scroll to bottom
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
  } catch (error) {
    console.error("Error connecting to chatbot:", error);
  }
}
