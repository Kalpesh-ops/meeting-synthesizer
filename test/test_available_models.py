import os
from google import genai
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Initialize the new SDK client
client = genai.Client()

def test_models():
    print("--- Fetching All Available Models ---")
    try:
        # Fetch all models from the API
        models_pager = client.models.list()
        
        # Filter for generative text/chat models
        # We ignore embedding models, AQA, and the explicitly deprecated 1.5-flash
        testable_models = [
            m.name for m in models_pager 
            if "gemini" in m.name 
            and "embedding" not in m.name 
            and "aqa" not in m.name
            and "1.5-flash" not in m.name
        ]
        
        print(f"Found {len(testable_models)} potential Gemini models. Ping testing now...\n")

        working_models = []
        for model_name in testable_models:
            # The API sometimes returns names with 'models/' prepended. We strip it for cleaner usage.
            clean_name = model_name.replace("models/", "")
            
            print(f"Pinging {clean_name}...", end=" ")
            try:
                # Send a tiny prompt to check if it's alive and has quota
                response = client.models.generate_content(
                    model=clean_name,
                    contents="Hi"
                )
                print("✅ SUCCESS!")
                working_models.append(clean_name)
            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    print("❌ FAILED: Quota Exceeded (429)")
                elif "503" in error_str:
                    print("❌ FAILED: Service Unavailable / Busy (503)")
                elif "404" in error_str:
                    print("❌ FAILED: Not Found (404)")
                else:
                    # Print the first line of any other error
                    print(f"❌ FAILED: {error_str.split('.')[0]}")

        print("\n========================================")
        print("🟢 WORKING MODELS READY FOR PRODUCTION 🟢")
        print("========================================")
        if not working_models:
            print("CRITICAL: No models are currently responding. You may need to wait a few minutes for quotas to reset or generate a new API key.")
        else:
            for wm in working_models:
                print(f"'{wm}',")
            print("\nCopy the working models above and paste them into me so we can update your agents.py fallback cascade!")

    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    test_models()