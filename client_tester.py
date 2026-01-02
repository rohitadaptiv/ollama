import requests
import json
import sys

# Default to localhost, but allow user to override via input
DEFAULT_HOST = "http://localhost:11434"

MODELS = {
    "1": "llama3.1",
    "2": "mistral" 
}

def check_server(base_url):
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ Served is reachable at {base_url}")
            return True
        else:
            print(f"⚠️ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {base_url}")
        print("   Make sure the server is running and the IP/Port is correct.")
        print("   If remote, check AWS Security Groups (Port 11434).")
        return False

def pull_verification(base_url, model_name):
    # Check if model exists, if not, try to pull (optional, might timeout on client, but good to know)
    print(f"🔍 Checking if model '{model_name}' is available on server...")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        if response.status_code == 200:
            models = [m['name'] for m in response.json()['models']]
            # Check for partial match (e.g. llama3.1:latest)
            if any(model_name in m for m in models):
                print(f"✅ Model '{model_name}' is ready.")
            else:
                print(f"⚠️ Model '{model_name}' not found in list. It might need to be pulled on the server first.")
                print(f"   Run on server: docker exec -it ollama_standalone ollama pull {model_name}")
    except:
        pass

def run_chat(base_url, model):
    print(f"\n💬 Starting chat with {model} (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": user_input}],
            "stream": True
        }
        
        try:
            print(f"{model}: ", end="", flush=True)
            with requests.post(f"{base_url}/api/chat", json=payload, stream=True, timeout=300) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        body = json.loads(line)
                        if "message" in body:
                            content = body["message"].get("content", "")
                            print(content, end="", flush=True)
                        if body.get("done", False):
                            print()
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    print("--- Ollama Remote Tester ---")
    host = input(f"Enter Ollama Server URL (default: {DEFAULT_HOST}): ").strip()
    if not host:
        host = DEFAULT_HOST
    
    # Normalize URL
    host = host.rstrip("/")
    if not host.startswith("http"):
        host = "http://" + host

    if not check_server(host):
        return

    print("\nSelect Model:")
    print("1. Llama 3.1 (Robust, Standard)")
    print("2. Mistral (Fast, High Quality)")
    
    choice = input("Choice (1/2): ").strip()
    model = MODELS.get(choice, "llama3.1")
    
    pull_verification(host, model)
    run_chat(host, model)

if __name__ == "__main__":
    main()
