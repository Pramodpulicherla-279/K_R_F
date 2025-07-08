import json
import time
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.ocr_utils import extract_text_from_image
from utils.ai_agent import AIAgent

# Load test case & locators
with open("test_cases/login.json") as f:
    test_steps = json.load(f)
with open("locators/elements.json") as f:
    locators = json.load(f)

# Modern approach with options
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "13971098400008K"  # Use actual device name from 'adb devices'
options.app = "F:\\K_R_F\\Krishivaas_Farmer_UI_RN(V0.12.34).apk"  # Full absolute path
options.automation_name = "uiautomator2"
options.auto_grant_permissions = True

# Initialize driver with error handling
try:
    # Try both common Appium server URLs
    for url in ["http://localhost:4723", "http://localhost:4723/wd/hub"]:
        try:
            driver = webdriver.Remote(url, options=options)
            break
        except:
            continue
    else:
        raise ConnectionError("Could not connect to Appium server at either URL")

except Exception as e:
    print(f"Error initializing Appium driver: {str(e)}")
    raise
    
agent = AIAgent(key="YOUR_OPENAI_KEY")

@allure.step("Run test steps")
def run_test_steps():
    for step in test_steps:
        element_name = step["element"]
        xpath = locators.get(element_name)
        value = step.get("value", "")
        try:
            elem = extract_text_from_image(driver, xpath)
            if not elem:
                raise Exception("Element not found")

            if step["action"] == "click":
                elem.click()
            elif step["action"] == "input":
                elem.send_keys(value)
            allure.attach(f"Step {step['step_id']} passed", name=f"Step {step['step_id']}", attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            screenshot = f"screenshots/failed_step_{step['step_id']}.png"
            driver.save_screenshot(screenshot)
            allure.attach.file(screenshot, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            print(agent.suggest_fix(str(e), screenshot))
            text_found = extract_text_from_image(screenshot)
            print("🧠 OCR text found:", text_found)
            allure.attach(str(text_found), name="OCR Text", attachment_type=allure.attachment_type.TEXT)

run_test_steps()
driver.quit()