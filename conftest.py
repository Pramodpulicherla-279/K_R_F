import os
import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    """Appium driver fixture with Allure attachments"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "13971098400008K"
    options.app = os.path.abspath("F:\\K_R_F\\Krishivaas_Farmer_UI_RN(V0.12.34).apk")
    options.automation_name = "uiautomator2"
    options.auto_grant_permissions = True

    with allure.step("Initialize Appium Driver"):
        allure.attach(
            str(options.capabilities),
            name="Driver Capabilities",
            attachment_type=allure.attachment_type.JSON
        )
        driver = webdriver.Remote("http://localhost:4723", options=options)
        yield driver
        
        # Teardown
        with allure.step("Close Appium Session"):
            driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add Allure attachments on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {str(e)}")