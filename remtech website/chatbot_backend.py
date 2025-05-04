from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from transformers import AutoTokenizer, AutoModelForCausalLM, logging
import torch
import uuid
import json
import os
import re
from bs4 import BeautifulSoup
import sys
import subprocess

# Set logging level to display GPU info
logging.set_verbosity_info()

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials
app.config["SECRET_KEY"] = "remtech_secret_key"  # Change this in production
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # Session lifetime in seconds
Session(app)

# Detailed GPU diagnostics
def check_gpu():
    """Perform detailed GPU checks and return diagnostic information"""
    info = {"gpu_available": False, "details": {}}
    
    # Check CUDA availability
    if torch.cuda.is_available():
        info["gpu_available"] = True
        info["details"]["cuda_available"] = True
        info["details"]["cuda_version"] = torch.version.cuda
        info["details"]["gpu_count"] = torch.cuda.device_count()
        info["details"]["current_device"] = torch.cuda.current_device()
        info["details"]["device_name"] = torch.cuda.get_device_name(0)
        info["details"]["memory_allocated"] = f"{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB"
        info["details"]["memory_reserved"] = f"{torch.cuda.memory_reserved(0) / 1024**3:.2f} GB"
        
        try:
            # Try to run a simple CUDA operation to verify it works
            test_tensor = torch.tensor([1.0, 2.0]).cuda()
            test_result = test_tensor * 2
            info["details"]["test_passed"] = True
        except Exception as e:
            info["details"]["test_passed"] = False
            info["details"]["test_error"] = str(e)
    else:
        # Check why CUDA is not available
        info["details"]["cuda_available"] = False
        if hasattr(torch, 'version') and hasattr(torch.version, 'cuda'):
            info["details"]["cuda_version"] = torch.version.cuda
            info["details"]["reason"] = "CUDA is installed but not detected by PyTorch"
        else:
            info["details"]["reason"] = "CUDA not installed or PyTorch not built with CUDA support"
    
    # Check for nvidia-smi
    try:
        nvidia_smi = subprocess.check_output("nvidia-smi", shell=True).decode()
        info["details"]["nvidia_smi"] = "Available"
        # Extract driver version
        driver_match = re.search(r"Driver Version: (\d+\.\d+\.\d+)", nvidia_smi)
        if driver_match:
            info["details"]["nvidia_driver"] = driver_match.group(1)
    except:
        info["details"]["nvidia_smi"] = "Not available"
    
    return info

# Check GPU at startup
gpu_info = check_gpu()
print("\n==== GPU DIAGNOSTICS ====")
for key, value in gpu_info.items():
    print(f"{key}: {value}")
print("========================\n")

# Use GPU if available, otherwise CPU
device = torch.device('cuda' if gpu_info["gpu_available"] else 'cpu')
print(f"Using device: {device}")

# Optimize for GPU if available
print("Loading model and tokenizer...")

# Configure model loading options based on available hardware
try:
    import accelerate
    has_accelerate = True
except ImportError:
    has_accelerate = False
    print("Accelerate library not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "accelerate"])
        import accelerate
        has_accelerate = True
        print("Accelerate installed successfully")
    except Exception as e:
        print(f"Failed to install accelerate: {e}")

model_loading_options = {}

# If GPU available, use half precision
if gpu_info["gpu_available"]:
    model_loading_options["torch_dtype"] = torch.float16
    print("Using GPU with float16 precision")
    
    if has_accelerate:
        model_loading_options["device_map"] = "auto"  # Only use device_map if accelerate is available
        print("Using accelerate for device mapping")
    else:
        print("Accelerate library not available, will move model to GPU manually")
else:
    print("WARNING: Using CPU. This will be slow!")

try:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b-it")
    
    print("Loading model with options:", model_loading_options)
    model = AutoModelForCausalLM.from_pretrained("google/gemma-3-1b-it", **model_loading_options)
    print("Model loaded successfully")
    
    # Force model to GPU if available and not automatically moved
    model_device = next(model.parameters()).device
    if gpu_info["gpu_available"] and model_device.type != 'cuda':
        print(f"Model is on {model_device}, moving to GPU manually...")
        model.to('cuda')
        model_device = next(model.parameters()).device
        
except Exception as e:
    print(f"Error loading model: {e}")
    print("Falling back to CPU with minimal settings")
    try:
        # Try again with minimal settings
        model = AutoModelForCausalLM.from_pretrained("google/gemma-3-1b-it", device_map=None)
        model_device = torch.device('cpu')
        model.to(model_device)  # Explicitly put on CPU
    except Exception as e2:
        print(f"Critical error loading model: {e2}")
        sys.exit(1)

# Verify model device
print(f"Model is on device: {model_device}")

# Services cache
services = []

def load_services():
    """Load services from the services.html file"""
    try:
        services_file = "C:\\Users\\robbi\\Rpasquale\\remtech website\\services.html"
        with open(services_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        extracted_services = []
        
        # Find service items
        service_items = soup.find_all('div', class_='service-item')
        
        if service_items:
            for item in service_items:
                name_elem = item.find('h3')
                desc_elem = item.find('p')
                
                service_name = name_elem.text.strip() if name_elem else "Unknown Service"
                description = desc_elem.text.strip() if desc_elem else ""
                
                extracted_services.append({
                    "name": service_name,
                    "description": description
                })
            
            print(f"Found {len(extracted_services)} services in the HTML")
            return extracted_services
        
        # Fallback strategies similar to before
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            if 'service' in heading.text.lower():
                service_name = heading.text.strip()
                description = ""
                
                next_elem = heading.find_next_sibling()
                if next_elem and next_elem.name == 'p':
                    description = next_elem.text.strip()
                
                extracted_services.append({
                    "name": service_name,
                    "description": description
                })
                
        return extracted_services
    except Exception as e:
        print(f"Error loading services: {e}")
        return []

def get_session_id():
    """Get or create a unique session ID for the current user"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_conversation_history(session_id):
    """Get conversation history for a session"""
    os.makedirs("conversations", exist_ok=True)
    history_file = f"conversations/{session_id}.json"
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return {"messages": []}

def save_conversation_history(session_id, history):
    """Save conversation history for a session"""
    os.makedirs("conversations", exist_ok=True)
    with open(f"conversations/{session_id}.json", 'w') as file:
        json.dump(history, file)

def create_enhanced_prompt(user_message, history):
    """Create an enhanced prompt with context and service information"""
    # Format conversation history into a context
    conversation_context = ""
    for msg in history["messages"][-5:]:  # Use last 5 messages
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_context += f"{role}: {msg['content']}\n"
    
    # Create service context
    service_context = "Available services:\n"
    for service in services:
        service_context += f"- {service['name']}: {service['description']}\n"
    
    # Create system instructions with clearer formatting for extraction
    system_instructions = """You are a helpful assistant for RemTech website. Your goal is to help users understand 
our services and guide them to the right solutions. When users express interest in hiring:

1. Ask about their project requirements and timeline
2. Collect relevant details about their needs
3. Suggest the most appropriate service from our offerings

Answer questions based on the provided service information. If you don't have enough 
information, ask follow-up questions to better understand the user's needs.
Be friendly, professional and concise."""
    
    # Combine everything into a final prompt with clear delineation
    final_prompt = f"System Instructions:\n{system_instructions}\n\nAvailable Services:\n{service_context}\n\nConversation History:\n{conversation_context}\n\nUser: {user_message}\nAssistant:"
    
    print(f"Prompt length: {len(final_prompt)} characters, ~{len(final_prompt)/4} tokens")
    return final_prompt

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("prompt", "")
        
        print(f"Received message: {user_message[:50]}...")
        
        # Get session and history
        session_id = get_session_id()
        history = get_conversation_history(session_id)
        
        # Add user message to history
        history["messages"].append({"role": "user", "content": user_message})
        
        # Create an enhanced prompt with context
        enhanced_prompt = create_enhanced_prompt(user_message, history)
        
        print("Generating response...")
        # Generate response
        with torch.no_grad():  # Disable gradient calculation for inference
            # Ensure inputs are on the same device as model
            inputs = tokenizer.encode(enhanced_prompt, return_tensors='pt').to(model_device)
            
            # Track time for performance measurement
            start_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
            end_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
            
            if start_time:
                start_time.record()
            
            # Significantly increase max_length for longer responses
            outputs = model.generate(
                inputs, 
                max_length=2048,       # Increased from 500 to 2048
                min_length=100,        # Set a minimum length to encourage detailed responses
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id  # Ensure proper padding
            )
            
            if end_time:
                end_time.record()
                torch.cuda.synchronize()
                generation_time = start_time.elapsed_time(end_time) / 1000  # convert to seconds
                print(f"Generation took {generation_time:.2f} seconds")
            
            reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"Full response length: {len(reply)} characters")
        print(f"Full response snippet: {reply[:100]}...")
        
        # Extract just the assistant's response from the generated text using improved logic
        if "Assistant:" in reply:
            # Find the last occurrence of "Assistant:" in case it appears in the conversation history
            assistant_start_idx = reply.rfind("Assistant:")
            assistant_reply = reply[assistant_start_idx + len("Assistant:"):].strip()
        else:
            # If "Assistant:" marker isn't found, use a fallback approach
            # Look for the last user message and extract everything after it
            user_pattern = f"User: {user_message}"
            if user_pattern in reply:
                user_idx = reply.find(user_pattern)
                remaining_text = reply[user_idx + len(user_pattern):].strip()
                # Now look for any text after "Assistant:" if present
                if "Assistant:" in remaining_text:
                    assistant_reply = remaining_text.split("Assistant:", 1)[1].strip()
                else:
                    assistant_reply = remaining_text
            else:
                # Last resort fallback
                assistant_reply = reply
        
        print(f"Extracted reply length: {len(assistant_reply)} characters")
        print(f"Extracted reply snippet: {assistant_reply[:100]}...")
        
        # Add assistant response to history
        history["messages"].append({"role": "assistant", "content": assistant_reply})
        save_conversation_history(session_id, history)
        
        return jsonify({
            "reply": assistant_reply,
            "session_id": session_id
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    """Reset the conversation history for the current session"""
    session_id = get_session_id()
    save_conversation_history(session_id, {"messages": []})
    return jsonify({"status": "success", "message": "Conversation reset successfully"})

@app.route('/refresh_services', methods=['POST'])
def refresh_services():
    """Admin endpoint to refresh the services cache"""
    global services
    services = load_services()
    return jsonify({"status": "success", "message": "Services refreshed successfully"})

# Add GPU diagnostics endpoint
@app.route('/gpu_status', methods=['GET'])
def gpu_status():
    """Endpoint to check GPU status"""
    info = check_gpu()
    if info["gpu_available"]:
        # Add model specific info
        info["model"] = {
            "device": str(next(model.parameters()).device),
            "memory_usage": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB / {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB"
        }
    return jsonify(info)

if __name__ == "__main__":
    # Load services on startup
    services = load_services()
    print(f"Loaded {len(services)} services")
    print("Starting enhanced chatbot server on http://localhost:5000")
    print("\nTo verify GPU usage, visit: http://localhost:5000/gpu_status")
    app.run(port=5000, debug=True)
