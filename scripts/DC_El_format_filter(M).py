from playwright.sync_api import sync_playwright
import time

def get_temp_email_and_otp_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=800)

        device = p.devices["iPhone 13"].copy()

        # (optional) override values SAFELY
        device["viewport"] = {"width": 390, "height": 844}
        device["is_mobile"] = True
        device["has_touch"] = True

        context = browser.new_context(**device)

        page = context.new_page()

        # --- Open 10times ---
        page2 = context.new_page()
        page2.goto("https://10times.com/events?olk", wait_until="networkidle")
        time.sleep(5)

        # MOBILE menu

        page2.locator("//button[@id='type-tab']").click()
        print("Open the format filter")
        time.sleep(5)

        page2.locator("//input[@name='Format' and @value='Tradeshows']").click()
        print("Select any format filter")
        time.sleep(5)

        page2.locator("//button[normalize-space(text())='Apply']").click()
        print("Apply format filter")
        time.sleep(10)

        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp_mobile()