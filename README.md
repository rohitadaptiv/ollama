# Ollama Server

Standalone Ollama instance configuration for EC2.

## Quick Start

1. **Start Server**
   ```bash
   docker-compose up -d
   ```

2. **Pull Model**
   ```bash
   docker exec -it ollama_standalone ollama pull llama3.1
   ```

3. **Test Locally (EC2)**
   ```bash
   curl http://localhost:11434/api/tags
   ```

4. **Test Remotely (Postman)**
   - Method: `POST`
   - URL: `http://<EC2-PUBLIC-IP>:11434/api/generate`
   - Body:
     ```json
     {
       "model": "llama3.1",
       "prompt": "Why is the sky blue?",
       "stream": false
     }
     ```

## Multi-Model Support

To use the `client_tester.py` effectively, pull the supported models on your EC2 server:

```bash
# 1. Main Model
docker exec -it ollama_standalone ollama pull llama3.1

# 2. Alternative Model (Mistral)
docker exec -it ollama_standalone ollama pull mistral
```

## Testing with Python Client

You can run `client_tester.py` from your local machine (if you clone this repo locally) or from anywhere.

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Run Tester:**
   ```bash
   python client_tester.py
   ```

3. **Follow Prompts:**
   - Enter your EC2 Public URL (e.g., `http://13.23.45.67:11434`).
   - Choose Model (Llama 3.1 or Mistral).
   - Chat!

