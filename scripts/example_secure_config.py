#!/usr/bin/env python3
"""
Example: Secure Configuration Management
Demonstrates how to use environment variables instead of hardcoded secrets
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SecureConfig:
    """Example of secure configuration management"""
    
    def __init__(self):
        # Load API keys from environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.database_url = os.getenv('DATABASE_URL')
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self):
        """Ensure all required configuration is present"""
        required_vars = {
            'OPENAI_API_KEY': self.openai_api_key,
            'DATABASE_URL': self.database_url,
        }
        
        missing = [var for var, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please set them in your .env file or environment."
            )
    
    def get_api_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }

def create_example_env_file():
    """Create an example .env file"""
    env_example = """# Example environment configuration
# Copy this to .env and fill in your actual values

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-key-here

# GitHub Configuration
GITHUB_TOKEN=ghp_your-token-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
API_RATE_LIMIT=100
"""
    
    env_path = Path('.env.example')
    env_path.write_text(env_example)
    print(f"Created {env_path}")

if __name__ == "__main__":
    # Example usage
    try:
        config = SecureConfig()
        print("✅ Configuration loaded successfully!")
        print(f"OpenAI API Key: {config.openai_api_key[:10]}..." if config.openai_api_key else "OpenAI API Key: Not set")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nCreating example .env file...")
        create_example_env_file()
        print("\nPlease copy .env.example to .env and add your actual API keys.")
