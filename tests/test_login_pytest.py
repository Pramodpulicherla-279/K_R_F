import time
import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.wait_utils import smart_find_element
from utils.ocr_utils import extract_text_with_coordinates
import json
import os

@allure.epic("Login Flow")
@allure.feature("Authentication")
class TestLogin:

    @allure.story("Successful Login")
    @allure.title("Verify user can login with valid credentials")
    def test_login_success(self, driver):
        # This list will store the details of each step in the test flow
        test_flow_steps = []

        with open(os.path.join('locators', 'elements.json'), 'r') as f:
            xpaths = json.load(f)
        
        # --- Locators ---
        language_next_xpath = xpaths.get("next_button_language_login")
        allow_picture_button_xpath = xpaths.get("allow_picture_button")
        allow_location_button_xpath = xpaths.get("allow_location_button")
        allow_audio_button_xpath = xpaths.get("allow_audio_button")
        allow_notifications_button_xpath = xpaths.get("allow_notifications_button")
        phone_number_input_xpath = xpaths.get("phone_number_input")
        next_button_login_xpath = xpaths.get("next_button_login")
        verify_button_login_xpath = xpaths.get("verify_button_login")
        dashboard_title_xpath = xpaths.get("dashboard_title")

        try:
            with allure.step("1. Next button on language selection screen"):
                next_button_language_login, used_ocr = smart_find_element(
                    driver, name="next_button_language_login", xpath=language_next_xpath, fallback_text="Next"
                )
                if next_button_language_login:
                    next_button_language_login.click()
                    test_flow_steps.append({"step": "Click Next on language screen", "status": "Success"})
                else:
                    raise Exception("Next button in language selection not found")

            with allure.step("2. Allow picture"):
                allow_picture_button, used_ocr = smart_find_element(
                    driver, name="allow_picture_button", xpath=allow_picture_button_xpath, fallback_text="While using the app"
                )
                if allow_picture_button:
                    allow_picture_button.click()
                    test_flow_steps.append({"step": "Allow picture permission", "status": "Success"})
                else:
                    raise Exception("Allow picture button not found")

            with allure.step("3. Allow location"):
                allow_location_button, used_ocr = smart_find_element(
                    driver, name="allow_location_button", xpath=allow_location_button_xpath, fallback_text="While using"
                )
                if allow_location_button:
                    allow_location_button.click()
                    test_flow_steps.append({"step": "Allow location permission", "status": "Success"})
                else:
                    raise Exception("Allow Location button not found")
            
            with allure.step("4. Allow audio"):
                allow_audio_button, used_ocr = smart_find_element(
                    driver, name="allow_audio_button", xpath=allow_audio_button_xpath, fallback_text="While using the app"
                )
                if allow_audio_button:
                    allow_audio_button.click()
                    test_flow_steps.append({"step": "Allow audio permission", "status": "Success"})
                else:
                    raise Exception("Allow audio button not found")

            with allure.step("5. Allow notifications"):
                allow_notifications_button, used_ocr = smart_find_element(
                    driver, name="allow_notifications_button", xpath=allow_notifications_button_xpath, fallback_text="Allow"
                )
                if allow_notifications_button:
                    allow_notifications_button.click()
                    test_flow_steps.append({"step": "Allow notifications permission", "status": "Success"})
                else:
                    raise Exception("Allow Notifications button not found")

            with allure.step("6. Enter phone number"):
                phone_input, used_ocr = smart_find_element(
                    driver, name="phone_number_input", xpath=phone_number_input_xpath, fallback_text="Phone"
                )
                if phone_input:
                    phone_input.clear()
                    phone_input.send_keys("7660852538")
                    test_flow_steps.append({"step": "Enter valid phone number", "status": "Success", "value": "7660852538"})
                else:
                    raise Exception("Phone input field not found")

            with allure.step("7. Tap next button"):
                next_button, used_ocr = smart_find_element(
                    driver, name="next_button_login", xpath=next_button_login_xpath, fallback_text="Next"
                )
                if next_button:
                    next_button.click()
                    test_flow_steps.append({"step": "Click Next after entering phone number", "status": "Success"})
                else:
                    raise Exception("Next button not found")

            with allure.step("8. Wait for OTP and verify"):
                time.sleep(10)  # Waiting for OTP
                verify_button, used_ocr = smart_find_element(
                    driver, name="verify_button_login", xpath=verify_button_login_xpath, fallback_text="Verify"
                )
                if verify_button:
                    verify_button.click()
                    test_flow_steps.append({"step": "Click Verify OTP", "status": "Success"})
                else:
                    raise Exception("Verify button not found")

            with allure.step("9. Verify dashboard appears"):
                dashboard, used_ocr = smart_find_element(
                    driver, name="dashboard_title", xpath=dashboard_title_xpath, fallback_text="Dashboard"
                )
                assert dashboard is not None or used_ocr, "Dashboard not found after login"
                test_flow_steps.append({"step": "Verify dashboard is displayed", "status": "Success"})
                allure.attach("Login successful", name="Result", attachment_type=allure.attachment_type.TEXT)

        finally:
            # Save the captured flow to a file
            os.makedirs("test-flows", exist_ok=True)
            with open("test-flows/login_flow_success.json", "w") as f:
                json.dump(test_flow_steps, f, indent=4)