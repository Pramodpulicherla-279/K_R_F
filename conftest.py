import pytest
from appium import webdriver
import os
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException

APK_PATH = os.getenv("APK_PATH", "F:\\K_R_F\\Krishivaas_Farmer_UI_RN(V0.12.34).apk")

@pytest.fixture(scope="session")
def driver():
    # Configure capabilities
    options = UiAutomator2Options()
    
    # Required capabilities
    options.platform_name = "Android"
    options.automation_name = "uiautomator2"  # Explicitly set automation engine
    
    # Device capabilities - adjust these to match your device
    options.device_name = "emulator-5554"  # Use actual device name from 'adb devices'
    options.udid = os.getenv("ANDROID_DEVICE_UDID", None)  # Optional but recommended
    
    # App capabilities
    options.app = APK_PATH  # Make sure this path is correct
    options.app_package = "com.krishivaas"
    options.app_activity = "com.krishivaas.MainActivity"
    
    # Optional settings
    options.no_reset = True
    options.auto_grant_permissions = True
    
    try:
        # Initialize driver with error handling
        driver = webdriver.Remote(
            "http://localhost:4723",  # Try without /wd/hub for newer Appium versions
            options=options
        )
        yield driver
    except WebDriverException as e:
        pytest.fail(f"Failed to initialize Appium driver: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()