from openai import OpenAI
import json

class AIAgent:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)

    def suggest_missing_tests(self, current_flow_json):
        prompt = f"""Given these steps:\n{json.dumps(current_flow_json, indent=2)}\nSuggest one or more additional test steps to verify login screen fully."""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def suggest_fix(self, error_message, screenshot_path):
        return f"🔍 Suggesting fix for: {error_message}\n[Visual data at {screenshot_path}]"
