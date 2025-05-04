# RemTech Electrical Website Chatbot

This project implements an AI-powered chatbot for the RemTech Electrical website, designed to assist visitors by answering questions about services and providing information based on the website's content.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [How it Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The RemTech chatbot provides an interactive chat interface embedded within the RemTech website (`index.html`, `services.html`, `projects.html`). It uses the `google/gemma-3-1b-it` language model via the Hugging Face `transformers` library to understand user queries and generate relevant responses. The backend is built with Flask and dynamically incorporates information about RemTech's services by parsing the `services.html` page.

## Features

-   **Interactive Chat Interface:** User-friendly chat window embedded on website pages.
-   **AI-Powered Responses:** Utilizes the Gemma 3.1B Instruct model for natural language understanding and generation.
-   **Service Awareness:** Automatically extracts service information from `services.html` to provide contextually relevant answers.
-   **Conversation History:** Maintains session-based conversation history stored server-side.
-   **GPU Acceleration:** Supports NVIDIA GPU acceleration via PyTorch and `accelerate` for faster responses (with CPU fallback).
-   **Typing Indicator:** Frontend shows a typing indicator while waiting for the backend response.
-   **Reset Conversation:** Allows users to start a new conversation session.
-   **Dynamic UI:** Frontend JavaScript (`chatbot_frontend.js`) dynamically creates the chat icon and window.

## Technology Stack

-   **Backend:** Python, Flask, Flask-CORS, Flask-Session
-   **AI/ML:** Hugging Face Transformers, PyTorch, Accelerate
-   **Frontend:** Vanilla JavaScript, HTML, CSS
-   **Parsing:** BeautifulSoup4

## Installation

### Prerequisites
-   Python 3.8+ and pip
-   NVIDIA GPU with CUDA drivers (Recommended for performance). Ensure PyTorch recognizes your CUDA installation.
-   Git (Optional, for cloning)

### Setup Instructions

1.  **Clone or Download:** Place the project files (including the `remtech website` directory) into a suitable location (e.g., `/c:/Users/robbi/Rpasquale/remtech-chatbot/`).
    ```bash
    # Example using git
    # git clone <your-repo-url> remtech-chatbot
    cd /c:/Users/robbi/Rpasquale/remtech-chatbot/remtech website/
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This will install Flask, Transformers, PyTorch, Accelerate, and other necessary libraries.*

4.  **Model Download:** The `google/gemma-3-1b-it` model will be automatically downloaded by the `transformers` library the first time the backend (`chatbot_backend.py`) is run. Ensure you have sufficient disk space (~3-4 GB).

5.  **Verify `services.html` Path:** The backend (`chatbot_backend.py`) expects `services.html` at `C:\\Users\\robbi\\Rpasquale\\remtech website\\services.html`. Ensure this path is correct or modify it in the `load_services` function within `chatbot_backend.py`.

## Running the Application

1.  **Start the Backend Server:**
    Make sure your virtual environment is activated.
    ```bash
    python chatbot_backend.py
    ```
    The server will start, typically on `http://localhost:5000`. It will load the model (downloading if necessary) and parse `services.html`. Check the console output for GPU status and any errors.

2.  **Access the Frontend:**
    Open one of the HTML files (`index.html`, `services.html`, or `projects.html`) directly in your web browser. The `chatbot_frontend.js` script included in these files will initialize the chatbot UI and connect to the backend running on `http://localhost:5000`.

## How it Works

1.  **Frontend Initialization:** When an HTML page loads, `chatbot_frontend.js` runs. It creates the chat icon and the hidden chat window UI elements.
2.  **User Interaction:** The user clicks the chat icon to open the window and types a message.
3.  **API Request:** The frontend sends the user's message and the current `session_id` (if available) to the backend `/chat` endpoint (`http://localhost:5000/chat`).
4.  **Backend Processing:**
    *   The Flask server receives the request.
    *   It retrieves or creates a session ID and loads the conversation history for that session from the `conversations/` directory.
    *   It constructs a detailed prompt including system instructions, service information (loaded from `services.html`), conversation history, and the new user message.
    *   The prompt is tokenized and fed into the loaded Gemma model (running on GPU or CPU).
    *   The model generates a response.
    *   The backend extracts the relevant part of the generated text.
    *   The assistant's reply is added to the conversation history and saved.
    *   The reply and session ID are sent back to the frontend.
5.  **Display Response:** The frontend receives the JSON response, displays the bot's message (with a typing effect), and updates its internal `sessionId`.

## API Endpoints

The backend (`chatbot_backend.py`) provides the following endpoints:

-   `POST /chat`: Receives user prompts, generates responses, and manages conversation history.
    -   Request Body: `{ "prompt": "User message", "session_id": "optional_session_id" }`
    -   Response Body: `{ "reply": "Bot response", "session_id": "current_session_id" }` or `{ "error": "Error message" }`
-   `POST /reset_conversation`: Clears the conversation history for the current session.
-   `GET /gpu_status`: Returns diagnostic information about GPU availability and usage.
-   `POST /refresh_services`: (Admin endpoint) Reloads service information from `services.html`.

## Configuration

-   **Backend (`chatbot_backend.py`):**
    -   `SECRET_KEY`: Used for Flask session management. Change for production.
    *   `SESSION_TYPE`: Set to `filesystem`. Session data stored in a `flask_session` directory.
    *   `PERMANENT_SESSION_LIFETIME`: Session duration (default 1 hour).
    *   Model Name: Hardcoded as `google/gemma-3-1b-it`.
    *   `services.html` Path: Hardcoded in `load_services`.
    *   Model Generation Parameters: `max_length`, `temperature`, `top_p` within the `/chat` endpoint.
-   **Frontend (`chatbot_frontend.js`):**
    -   `apiEndpoint`: Hardcoded to `http://localhost:5000/chat` in the `RemTechChatbot` constructor default and potentially in the initialization call (though the current initialization doesn't override it).

## Troubleshooting

-   **Slow Responses:** Check the backend console output. If it says "Using device: cpu", responses will be slow. Ensure CUDA is installed correctly and recognized by PyTorch (`/gpu_status` endpoint can help diagnose).
-   **Model Loading Errors:** Ensure sufficient RAM/VRAM and disk space. Check console for specific errors from the `transformers` library. Network issues might prevent model download.
-   **Connection Errors (Frontend):** Verify the backend server is running and accessible at `http://localhost:5000`. Check browser console (F12) for CORS errors or network issues. Flask-CORS is enabled, but network configurations could still interfere.
-   **Service Information Incorrect:** Ensure `services.html` is correctly formatted and the path in `chatbot_backend.py` is accurate. Use `/refresh_services` if you update the HTML while the server is running.
-   **GPU Not Detected:** Verify NVIDIA drivers, CUDA toolkit installation, and PyTorch CUDA compatibility. Run `python -c "import torch; print(torch.cuda.is_available())"` in your venv. Check `/gpu_status`.

