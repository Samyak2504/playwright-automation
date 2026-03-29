from playwright.sync_api import sync_playwright
import time

def get_temp_email_and_otp_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=800)

        device = p.devices["iPhone 13."].copy()

        # (optional) override values SAFELY
        device["viewport"] = {"width": 390, "height": 844}
        device["is_mobile"] = True
        device["has_touch"] = True

        context = browser.new_context(**device)

        page = context.new_page()

        # --- Google login ---
        page.goto("https://accounts.google.com/")
        page.wait_for_load_state("networkidle")

        page.locator("#identifierId").fill("Samyak@10times.com")
        page.get_by_role("button", name="Next").click()
        time.sleep(4)

        page.locator("input[type='password']").fill("Samyak@1996")
        page.get_by_role("button", name="Next").click()
        time.sleep(6)

        # --- Open 10times ---
        page2 = context.new_page()
        page2.goto("https://10times.com/events?olk", wait_until="networkidle")
        time.sleep(5)

        # MOBILE menu
        # Apply 1st filter

        page2.locator("//button[@id='type-tab']").click()
        print("Open the format filter")
        time.sleep(5)

        page2.locator("//input[@name='Format' and @value='Tradeshows']").click()
        print("Select any format filter")
        time.sleep(5)

        page2.locator("//button[normalize-space(text())='Apply']").click()
        print("Apply format filter")
        time.sleep(5)

        # Apply 2nd Filter
        page2.locator("//button[normalize-space(text())='Category']").click()
        print("Open the category filter")
        time.sleep(5)

        page2.locator("//input[@type='radio' and @value='Medical & Pharma']").click()
        print("Select any category filter")
        time.sleep(5)

        page2.locator("//button[normalize-space(text())='Apply']").click()
        print("Apply category filter")
        time.sleep(5)

        # 3rd Filter
        page2.locator("//button[@id='location-tab']").click()
        print("Open the Location filter")
        time.sleep(5)

        page2.locator("//input[@type='radio' and @value='London']").click()
        print("Select any Location filter")
        time.sleep(5)

        page2.locator("//button[normalize-space(text())='Apply']").click()
        print("Apply Location filter")
        time.sleep(10)


        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp_mobile()
