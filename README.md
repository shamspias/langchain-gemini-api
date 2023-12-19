# langchain-gemini-api

## Overview

`langchain-gemini-api` is an AI-powered conversation API that integrates Google's Gemini API, designed to facilitate
advanced text and image-based interactions. This project combines the capabilities of modern deep learning models with
FastAPI for high performance and scalability, Langchain for sophisticated conversational workflows, and Redis for
ephemeral conversation storage.

## Key Features

- **Asynchronous API**: Utilizing FastAPI for enhanced performance and scalability.
- **Langchain Integration**: Advanced conversational workflows using multiple AI models.
- **Google Gemini API**: Incorporating Gemini, Gemini Pro, and Gemini Pro Vision for superior conversation understanding
  and generation.
- **Ephemeral Conversation Storage**: Implementing Redis for data privacy and efficient memory usage.
- **User-Friendly Interface**: Simplified API endpoints for easy integration.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- FastAPI
- Uvicorn
- Redis
- Access to Google Gemini API

### Installation

#### Install Redis

1. Install Redis:
   ```bash
   sudo apt update
   sudo apt install redis-server
   ```
   Windows users can download Redis from [here](https://github.com/tporadowski/redis/releases)
2. Test Redis:
   ```bash
   redis-cli ping
   ```
   If Redis is running, it will return `PONG`.

#### Install Python Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/shamspias/langchain-gemini-api.git
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
   for Windows:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
    source venv/bin/activate
    ```
4. Navigate to the project directory and install dependencies:
    ```bash
    cd langchain-gemini-api
    pip install -r requirements.txt
    ```

## Running the API

1. Start fastapi server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

- **/conversations/<conversation_id>**: Endpoint for text-based conversations.
- **/vision-conversations/<conversation_id>**: Endpoint for image-based conversations.
- **/delete/<conversation_id>**: Endpoint to delete conversation data.

## Acknowledgments

- Google Gemini API team
- Langchain contributors
- FastAPI community