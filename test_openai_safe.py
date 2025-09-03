#!/usr/bin/env python3
import openai
import os
import sys

# --- Load API key from safe file ---
key_path = os.path.expanduser("~/.openai_key")

try:
    with open(key_path, "r") as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    print(f"❌ API key file not found: {key_path}")
    sys.exit(1)

# --- Example prompt ---
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello from PythonAnywhere! Please keep it short."}
]

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=150
    )
    
    # Print response
    answer = response.choices[0].message.content
    print("✅ API key works! Response:")
    print(answer)

except openai.error.AuthenticationError:
    print("❌ Authentication error: Check your API key.")
except openai.error.RateLimitError:
    print("⚠️ Rate limit reached: Reduce frequency or wait.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
