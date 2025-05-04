"""
Configuration for selecting different LLM models.
Edit this file to switch between models or adjust settings.
"""

# Available model options
MODEL_OPTIONS = {
    "default": {
        "name": "google/gemma-3-1b-it",
        "description": "Default 1B parameter model, balanced performance and speed"
    },
    "larger": {
        "name": "google/gemma-7b-it",
        "description": "7B parameter model for more complex reasoning"
    },
    "local_7b": {
        "name": "TheBloke/gemma-7b-it-GPTQ",
        "description": "Quantized 7B model for better performance on limited hardware"
    }
}

# Current model selection
CURRENT_MODEL = "default"

# Advanced generation settings
GENERATION_CONFIG = {
    "max_length": 2048,      # Maximum length of generated text
    "min_length": 100,      # Minimum length of generated text
    "temperature": 0.7,     # Higher = more random, Lower = more deterministic
    "top_p": 0.9,           # Nucleus sampling parameter
    "do_sample": True       # Use sampling instead of greedy decoding
}

# System prompt template
SYSTEM_PROMPT_TEMPLATE = """You are a helpful assistant for RemTech website. Your goal is to help users understand 
our services and guide them to the right solutions. When users express interest in hiring:

1. Ask about their project requirements and timeline
2. Collect relevant details about their needs
3. Suggest the most appropriate service from our offerings

Answer questions based on the provided service information. If you don't have enough 
information, ask follow-up questions to better understand the user's needs.
Be friendly, professional and concise.

Remember to address questions directly and completely.
"""
