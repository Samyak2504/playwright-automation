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
        page2.goto("https://10times.com/venues/gaylord-national-resort-convention-center", wait_until="networkidle")
        time.sleep(5)

        page.locator("//button[normalize-space()='Reviews']").click()
        print(" Redirection Reviews block  ")

        page2.locator("(//button[normalize-space()='Report'])[1]").click()
        page2.locator("//span[normalize-space()='Continue with Google']").click()
        print("Login via Helpful")

        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp_mobile()
