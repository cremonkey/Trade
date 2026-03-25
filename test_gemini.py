from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: No GOOGLE_API_KEY found in .env")
        return

    print(f"📡 API Key detected (starts with {api_key[:8]}...)")
    
    try:
        client = genai.Client(api_key=api_key)
        
        # 1. List Available Models
        print("\n📋 1. Checking Available Models:")
        available_models = []
        for model in client.models.list():
            available_models.append(model.name)
            print(f"   - {model.name}")
            
        # 2. Test Generation with User's preferred model
        target_model = "gemini-2.5-flash"
        print(f"\n🧪 2. Testing Generation with '{target_model}'...")
        
        if target_model in available_models or any(target_model in m for m in available_models):
             response = client.models.generate_content(
                model=target_model,
                contents="Say 'Antigravity v5.0 Sovereign Brain Online' in Arabic."
            )
             print(f"✅ Success! Response: {response.text}")
        else:
            print(f"⚠️ Warning: '{target_model}' not found in your available models list.")
            if available_models:
                fallback = "gemini-2.0-flash" if "gemini-2.0-flash" in str(available_models) else available_models[0]
                print(f"🔄 Retrying with fallback: {fallback}")
                response = client.models.generate_content(model=fallback, contents="Hello!")
                print(f"✅ Fallback Success: {response.text}")

    except Exception as e:
        print(f"❌ Error during test: {str(e)}")

if __name__ == "__main__":
    test_connection()
