class RemTechChatbot {
    constructor(containerId, apiEndpoint = 'http://localhost:5000/chat') {
        this.container = document.getElementById(containerId);
        this.apiEndpoint = apiEndpoint;
        this.sessionId = null;
        this.isOpen = false;
        
        // Create the chatbot UI
        this.createChatbotUI();
        
        // Add event listeners
        this.attachEventListeners();
        
        console.log("RemTech Chatbot initialized");
    }
    
    createChatbotUI() {
        // Create the chatbot UI elements
        this.container.innerHTML = `
            <div class="chat-icon" id="chatIcon">
                <i class="fas fa-comment"></i>
            </div>
            
            <div class="chat-window" id="chatWindow" style="display: none;">
                <div class="chat-header">
                    <h3><i class="fas fa-bolt"></i> RemTech Assistant</h3>
                    <button id="closeChat"><i class="fas fa-times"></i></button>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot-message">
                        <div class="message-content">
                            Hi there! I'm your RemTech assistant. How can I help you today?
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <textarea id="chatInput" placeholder="Type your message here..." rows="2"></textarea>
                    <button id="sendMessage">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
                
                <div class="chat-footer">
                    <button id="resetChat">New Conversation</button>
                </div>
            </div>
        `;
        
        // Add CSS styles
        const style = document.createElement('style');
        style.textContent = `
            .chat-icon {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 65px;
                height: 65px;
                border-radius: 50%;
                background: #2c5282;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 6px 16px rgba(0,0,0,0.3);
                z-index: 1000;
                font-size: 28px;
                transition: all 0.3s ease;
            }
            
            .chat-icon:hover {
                background: #3182ce;
                transform: scale(1.05);
            }
            
            .chat-window {
                position: fixed;
                bottom: 110px;
                right: 30px;
                width: 420px;
                height: 600px;
                border-radius: 16px;
                background: white;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                z-index: 1000;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #2c5282, #3182ce);
                color: white;
                padding: 16px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .chat-header h3 {
                margin: 0;
                font-size: 18px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .chat-header button {
                background: transparent;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 18px;
                opacity: 0.8;
                transition: opacity 0.2s;
            }
            
            .chat-header button:hover {
                opacity: 1;
            }
            
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background-color: #f8fafc;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            .message {
                display: flex;
                flex-direction: column;
                max-width: 85%;
                word-wrap: break-word;
                position: relative;
                animation: fadeIn 0.3s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message-content {
                padding: 12px 16px;
                border-radius: 18px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                line-height: 1.5;
                font-size: 15px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .user-message {
                align-self: flex-end;
            }
            
            .user-message .message-content {
                background: #3182ce;
                color: white;
                border-bottom-right-radius: 4px;
            }
            
            .bot-message {
                align-self: flex-start;
            }
            
            .bot-message .message-content {
                background: white;
                color: #1a202c;
                border-bottom-left-radius: 4px;
                border: 1px solid #e2e8f0;
            }
            
            .chat-input-container {
                padding: 16px;
                border-top: 1px solid #e2e8f0;
                display: flex;
                background-color: white;
                align-items: flex-end;
                gap: 10px;
            }
            
            .chat-input-container textarea {
                flex: 1;
                padding: 12px 16px;
                border: 1px solid #cbd5e0;
                border-radius: 24px;
                resize: none;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
                line-height: 1.5;
                max-height: 120px;
                outline: none;
                transition: border 0.2s;
            }
            
            .chat-input-container textarea:focus {
                border-color: #3182ce;
            }
            
            .chat-input-container button {
                background: #3182ce;
                color: white;
                border: none;
                border-radius: 50%;
                width: 42px;
                height: 42px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            
            .chat-input-container button:hover {
                background: #2c5282;
            }
            
            .chat-footer {
                padding: 12px;
                display: flex;
                justify-content: center;
                background-color: white;
                border-top: 1px solid #e2e8f0;
            }
            
            .chat-footer button {
                background: #edf2f7;
                border: none;
                padding: 8px 16px;
                border-radius: 24px;
                cursor: pointer;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #4a5568;
                font-size: 14px;
                transition: background-color 0.2s;
            }
            
            .chat-footer button:hover {
                background: #e2e8f0;
            }
            
            .typing-indicator {
                display: flex;
                padding: 12px 16px;
                background: white;
                align-self: flex-start;
                border-radius: 18px;
                border-bottom-left-radius: 4px;
                border: 1px solid #e2e8f0;
                align-items: center;
                gap: 4px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                animation: fadeIn 0.3s ease;
            }
            
            .typing-indicator span {
                height: 8px;
                width: 8px;
                background-color: #a0aec0;
                border-radius: 50%;
                display: inline-block;
                animation: typing 1.4s infinite ease-in-out both;
            }
            
            .typing-indicator span:nth-child(1) {
                animation-delay: 0s;
            }
            
            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            
            .message a {
                color: inherit;
                text-decoration: underline;
            }
            
            @media (max-width: 520px) {
                .chat-window {
                    width: 90%;
                    right: 5%;
                    bottom: 80px;
                    height: 70vh;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    attachEventListeners() {
        // Toggle chat window
        document.getElementById('chatIcon').addEventListener('click', () => this.toggleChat());
        document.getElementById('closeChat').addEventListener('click', () => this.toggleChat());
        
        // Send message
        document.getElementById('sendMessage').addEventListener('click', () => this.sendMessage());
        const chatInput = document.getElementById('chatInput');
        
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea as user types
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Reset conversation
        document.getElementById('resetChat').addEventListener('click', () => this.resetConversation());
    }
    
    toggleChat() {
        const chatWindow = document.getElementById('chatWindow');
        this.isOpen = !this.isOpen;
        chatWindow.style.display = this.isOpen ? 'flex' : 'none';
        
        if (this.isOpen) {
            document.getElementById('chatInput').focus();
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (message === '') return;
        
        // Clear input while preserving the message
        const userMessage = message;
        input.value = '';
        input.style.height = 'auto'; // Reset height if using auto-resize
        
        // Display user message
        this.addMessage(userMessage, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            console.log("Sending message to backend...");
            // Send message to API
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: userMessage,
                    session_id: this.sessionId
                }),
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Received response:", data);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Store session ID if provided
            if (data.session_id) {
                this.sessionId = data.session_id;
            }
            
            // Display bot response with typing effect
            if (data.reply) {
                console.log("Adding reply to chat:", data.reply.substring(0, 50) + "...");
                this.addMessageWithTypingEffect(data.reply, 'bot');
            } else if (data.error) {
                console.error("Error from server:", data.error);
                this.addMessage(`Sorry, I encountered an error: ${data.error}`, 'bot');
            } else {
                console.error("No reply or error in response");
                this.addMessage("Sorry, I didn't get a proper response. Please try again.", 'bot');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered a technical issue. Please try again later.', 'bot');
        }
    }
    
    addMessage(message, sender) {
        console.log(`Adding ${sender} message: ${message.substring(0, 50)}...`);
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(`${sender}-message`);
        
        // Convert URLs to clickable links
        const messageWithLinks = message.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank">$1</a>'
        );
        
        // Add message content inside a wrapper
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.innerHTML = messageWithLinks;
        messageElement.appendChild(contentElement);
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    addMessageWithTypingEffect(message, sender, speed = 10) {
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(`${sender}-message`);
        
        // Create content element
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        messageElement.appendChild(contentElement);
        
        // Append the empty message first
        chatMessages.appendChild(messageElement);
        
        // Convert URLs to clickable links
        const messageWithLinks = message.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank">$1</a>'
        );
        
        // Typing effect
        let i = 0;
        const typeWriterEffect = () => {
            if (i < messageWithLinks.length) {
                // Add one character at a time
                contentElement.innerHTML = messageWithLinks.substring(0, i + 1);
                i++;
                
                // Scroll as we type
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // Schedule next character
                setTimeout(typeWriterEffect, speed);
            }
        };
        
        // Start typing effect
        typeWriterEffect();
    }
    
    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.id = 'typingIndicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    async resetConversation() {
        try {
            await fetch('http://localhost:5000/reset_conversation', {
                method: 'POST',
                credentials: 'include'
            });
            
            // Clear chat messages except the first welcome message
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        Hi there! I'm your RemTech assistant. How can I help you today?
                    </div>
                </div>
            `;
            
        } catch (error) {
            console.error('Error resetting conversation:', error);
        }
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, initializing chatbot");
    // Check if the chat container exists, if not create it
    let chatContainer = document.getElementById('remtech-chatbot');
    if (!chatContainer) {
        console.log("Creating chatbot container");
        chatContainer = document.createElement('div');
        chatContainer.id = 'remtech-chatbot';
        document.body.appendChild(chatContainer);
    }
    
    // Initialize the chatbot
    console.log("Creating RemTechChatbot instance");
    const chatbot = new RemTechChatbot('remtech-chatbot');
});
