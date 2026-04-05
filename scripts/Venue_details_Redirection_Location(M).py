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
        page = context.new_page()
        page.goto("https://10times.com/venues/gaylord-national-resort-convention-center", wait_until="networkidle")
        time.sleep(5)

        # MOBILE menu

        page.locator("//button[normalize-space()='Location']").click()
        print(" Redirection Location block  ")
        time.sleep(10)

        browser.close()


if __name__ == "__main__":
    get_temp_email_and_otp_mobile()
