import os
import pytest
import subprocess
from utils.ai_agent import AIAgent

def run_tests_and_get_suggestions():
    """
    Main function to execute tests, and if they pass,
    invoke the AI agent to suggest new test flows.
    """
    # Create necessary directories
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("test-flows", exist_ok=True)

    # Define paths
    test_file = "tests/test_login_pytest.py"
    allure_dir = "allure-results"
    
    # Run pytest with Allure options
    result = pytest.main([
        test_file,
        f"--alluredir={allure_dir}",
        "--clean-alluredir",
        "-v"
    ])

    # If tests passed, run the AI agent
    if result == pytest.ExitCode.OK:
        print("\n" + "="*80)
        print("✅ All tests passed. Asking AI for new test case suggestions...")
        print("="*80 + "\n")

        # Ensure you have your OpenAI API key in an environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("🛑 Error: OPENAI_API_KEY environment variable not set.")
            return

        ai_agent = AIAgent(key=api_key)
        
        flow_file = "test-flows/login_flow_success.json"
        
        suggestions = ai_agent.suggest_new_tests(flow_file, test_file)
        
        print("🤖 AI-Generated Test Suggestions:\n")
        print(suggestions)
        
        # Optionally, save suggestions to a file
        with open("ai_test_suggestions.md", "w") as f:
            f.write(suggestions)
        print(f"\n💡 Suggestions also saved to 'ai_test_suggestions.md'")

    else:
        print("\n" + "="*80)
        print("❌ Tests failed. Skipping AI suggestion step.")
        print("="*80 + "\n")
        
    # To view the report, run: allure serve allure-results
    print(f"\nTo view the detailed test report, run: allure serve {allure_dir}")

if __name__ == "__main__":
    run_tests_and_get_suggestions()