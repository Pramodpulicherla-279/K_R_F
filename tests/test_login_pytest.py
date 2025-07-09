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
        with open(os.path.join('locators', 'elements.json'), 'r') as f:
            xpaths = json.load(f)
        language_next_xpath = xpaths.get("next_button_language_login")

        with allure.step("1. next button on language selection screen"):
            print(f"[DEBUG] Using XPath for language next: {language_next_xpath}")
            next_button_language_login, used_ocr = smart_find_element(
            driver,
            name="next_button_language_login",
            xpath=language_next_xpath,
            fallback_text="Next"
            )
            if next_button_language_login is not None:
               next_button_language_login.click()
            elif not used_ocr:
               raise Exception("Next button in language selection not found after all fallback methods")
            
        with allure.step("1. Allow notifications"):
            allow_notifications_button, used_ocr = smart_find_element(
                driver,
                name="allow_notifications_button",
                xpath="//android.widget.Button[@text='Allow']",
                fallback_text="While using the app"
            )
            if allow_notifications_button is not None:
                allow_notifications_button.click()
            elif not used_ocr:
                raise Exception("Allow Notifications button not found after all fallback methods")
            
        with allure.step("2. Allow location access"):
            allow_location_button, used_ocr = smart_find_element(
                driver,
                name="allow_location_button",
                xpath="//android.widget.Button[@text='Allow']",
                fallback_text="While using"
            )
            if allow_location_button is not None:
                allow_location_button.click()
            elif not used_ocr:
                raise Exception("Allow Location button not found after all fallback methods")

        with allure.step("3. Allow camera access"):
            allow_camera_button, used_ocr = smart_find_element(
                driver,
                name="allow_camera_button",
                xpath="//android.widget.Button[@text='Allow']",
                fallback_text="While using"
            )
            if allow_camera_button is not None:
                allow_camera_button.click()
            elif not used_ocr:
                raise Exception("Allow Camera button not found after all fallback methods")
            
        with allure.step("4. Enter phone number"):
            phone_input, used_ocr = smart_find_element(
                driver,
                name="phone_number_input",
                xpath="//android.widget.EditText[@resource-id='phoneInput']",
                fallback_text="Phone"
            )
            
            if used_ocr:
                # If OCR was used to click, find the element again after focus
                phone_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@focused='true']"))
                )
                
            if phone_input is not None:
                phone_input.clear()
                phone_input.send_keys("7660852538")
                allure.attach(
                    "Entered phone number: 7660852538",
                    name="Phone Input",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                raise Exception("Phone input field not found after all fallback methods")

        with allure.step("5. Tap next button"):
            next_button, used_ocr = smart_find_element(
                driver,
                name="next_button_login",
                xpath="//android.widget.Button[@text='Next']",
                fallback_text="Next"
            )
            
            if next_button is not None:
                next_button.click()
            elif not used_ocr:
                raise Exception("Next button not found after all fallback methods")

        with allure.step("6. Wait for OTP and verify"):
            time.sleep(10)  # Wait for OTP
            verify_button, used_ocr = smart_find_element(
                driver,
                name="verify_button_login",
                xpath="//android.widget.Button[@text='Verify']",
                fallback_text="Verify"
            )
            
            if verify_button is not None:
                verify_button.click()
            elif not used_ocr:
                raise Exception("Verify button not found after all fallback methods")

        with allure.step("7. Verify dashboard appears"):
            dashboard = None
            timeout = time.time() + 30
            last_screenshot_time = time.time()
            
            while time.time() < timeout:
                dashboard, used_ocr = smart_find_element(
                    driver,
                    name="dashboard_title",
                    xpath="//android.widget.TextView[contains(@text, 'Dashboard')]",
                    fallback_text="Dashboard"
                )
                if dashboard or used_ocr:
                    break
                
                # Take screenshot every 5 seconds for OCR
                if time.time() - last_screenshot_time > 5:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name="Dashboard Check Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                    last_screenshot_time = time.time()
                    
                    try:
                        ocr_text = extract_text_with_coordinates(screenshot)
                        if any("dashboard" in item["text"].lower() for item in ocr_text):
                            break
                    except Exception as e:
                        print(f"OCR failed: {str(e)}")
                
                time.sleep(1)
            
            assert dashboard is not None or used_ocr, "Dashboard not found after login"
            allure.attach("Login successful", name="Result", attachment_type=allure.attachment_type.TEXT)