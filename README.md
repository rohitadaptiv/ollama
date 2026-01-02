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

## Security Note
Ensure AWS Security Group allows Inbound TCP traffic on port `11434` from your IP (or 0.0.0.0/0 for public access).
