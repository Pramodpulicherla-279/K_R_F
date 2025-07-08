from selenium.webdriver.common.by import By  # <-- Fix this import
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.ocr_utils import click_element_by_ocr_text

def smart_find_element(driver, name, xpath, fallback_text=None, screenshot_path="screenshots/ocr_fallback.png"):
    try:
        # Try finding by XPath first
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except:
        print(f"[❌] Element '{name}' not found via XPath. Trying OCR fallback...")

        # Take screenshot
        driver.save_screenshot(screenshot_path)

        # Try clicking by text via OCR
        if fallback_text:
            found = click_element_by_ocr_text(driver, fallback_text, screenshot_path)
            if found:
                print(f"[✅] OCR clicked on '{fallback_text}' successfully.")
                return None  # No element returned, but action was done
            else:
                print(f"[⚠️] OCR failed to find '{fallback_text}' on screen.")

        return None
