import os
import pytest
from utils.ai_agent import AIAgent

def run_tests():
    """Main function to execute tests with Allure reporting"""
    # Create necessary directories
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # Run pytest with Allure options
    pytest.main([
        "tests/test_login_pytest.py",
        "--alluredir=allure-results",
        "--clean-alluredir",
        "-v",
        "-W", "ignore::pytest.PytestAssertRewriteWarning"
    ])

if __name__ == "__main__":
    run_tests()