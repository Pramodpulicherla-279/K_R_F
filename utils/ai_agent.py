import os
from openai import OpenAI
import json

class AIAgent:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)

    def suggest_new_tests(self, flow_file_path, test_file_path):
        """
        Suggests new test cases based on a successful test flow and existing test code.
        """
        try:
            with open(flow_file_path, 'r') as f:
                current_flow = json.load(f)
        except FileNotFoundError:
            return "Could not find the test flow file."

        try:
            with open(test_file_path, 'r') as f:
                existing_test_code = f.read()
        except FileNotFoundError:
            return "Could not find the test code file."

        prompt = f"""
        As a Senior QA Automation Engineer, your task is to suggest new test cases for an Android mobile application.

        **Application Context:**
        The application is a farmer assistance app named 'Krishivaas Farmer'. The current test focuses on the user login flow, which involves language selection, granting permissions, entering a phone number, and verifying with an OTP.

        **Existing Successful Test Flow:**
        Here are the steps from a successful login test:
        {json.dumps(current_flow, indent=2)}

        **Existing Test Code:**
        Here is the Pytest code for the existing test:
        ```python
        {existing_test_code}
        ```

        **Your Task:**
        Based on the successful flow and the existing code, suggest 3 new, distinct test cases to improve the test coverage of the login functionality. For each suggestion, provide:
        1.  A clear, descriptive test case title.
        2.  A list of steps for the new test case in plain English.
        3.  The primary reason or justification for this new test.

        Focus on edge cases, negative paths, and variations that are not covered in the current 'happy path' test. Examples include invalid inputs, permission denials, or user interruptions.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content