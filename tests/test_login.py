import json
import allure
import pytest
import os
from utils.wait_utils import smart_find_element
from utils.ai_agent import AIAgent
from utils.ocr_utils import extract_text_with_coordinates
import time

# Load locators from JSON
with open("locators/elements.json") as f:
    locators = json.load(f)

# Optional: Load API key from env
AI_KEY = os.getenv("OPENAI_API_KEY", "")
ai_agent = AIAgent(key=AI_KEY)

@allure.epic("Login Flow")
@allure.title("Test valid login with fallback OCR and AI suggestions")
def test_login_success(driver):
    try:
        # STEP 1: Enter phone number
        phone_input = smart_find_element(
            driver,
            name="phone_number_input",
            xpath=locators["phone_number_input"],
            fallback_text="Phone"
        )
        
        if phone_input is not None:
            phone_input.send_keys("7660852538")
        else:
            # After OCR click, try to send keys using the driver
            # This assumes the field is now focused
            for digit in "7660852538":
                driver.press_keycode(7 + int(digit))  # Keycode 7 is '0'


        # STEP 2: Tap next button
        next_button = smart_find_element(
            driver,
            name="next_button_login",
            xpath=locators["next_button_login"],
            fallback_text="Next"
        )
        if next_button is not None:
            next_button.click()
        else:
            # If OCR fallback was used, assume the click was successful and continue
            print("[INFO] Next button clicked by OCR fallback.")
        
        # STEP 3: Wait for OTP to arrive before clicking Verify
        print("[INFO] Waiting for OTP to arrive...")
        time.sleep(10)  # Adjust as needed for your OTP delivery time

        verify_button = smart_find_element(
            driver,
            name="verify_button_login",
            xpath=locators["verify_button_login"],
            fallback_text="Verify"
        )
        if verify_button is not None:
            verify_button.click()
        else:
            print("[INFO] Verify button clicked by OCR fallback.")

        # STEP 4: Wait for dashboard or success screen (explicit wait)
        print("[INFO] Waiting for dashboard screen...")
        dashboard = None
        timeout = 30  # seconds
        poll_interval = 1
        start_time = time.time()
        ocr_dashboard_found = False
        
        while time.time() - start_time < timeout:
            dashboard = smart_find_element(
                driver,
                name="dashboard_title",
                xpath=locators["dashboard_title"],
                fallback_text="Dashboard"
            )
            if dashboard is not None:
                break
            # OCR fallback: check if "Dashboard" is present in the last OCR result
            screenshot_path = "screenshots/dashboard_check.png"
            driver.save_screenshot(screenshot_path)
            ocr_text = extract_text_with_coordinates(screenshot_path)
            if any("dashboard" in item["text"].lower() for item in ocr_text):
                ocr_dashboard_found = True
                print("[INFO] Dashboard detected by OCR.")
                break
            time.sleep(poll_interval)
        
        assert dashboard is not None or ocr_dashboard_found, "❌ Login likely failed: Dashboard not found"

        allure.attach("✅ Login success", name="Test Result", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        screenshot_path = "screenshots/failed_login.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

        # OCR text capture
        ocr_text = extract_text_with_coordinates(screenshot_path)
        print("🧠 OCR Detected Text:\n", ocr_text)

        # AI agent suggestion (if enabled)
        if AI_KEY:
            fix = ai_agent.suggest_fix(str(e), screenshot_path)
            allure.attach(fix, name="AI Fix Suggestion", attachment_type=allure.attachment_type.TEXT)

        raise AssertionError(f"❌ Test failed: {str(e)}")
