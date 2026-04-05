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
        page2.goto("https://10times.com?olk", wait_until="networkidle")
        time.sleep(5)

        # MOBILE menu
        page2.locator("(//*[local-name()='svg']//*[local-name()='path'])[1]").click()
        time.sleep(2)

        page2.locator("text=Login").click()
        time.sleep(3)

        page2.locator("//div[@data-name='gLogin']").click()
        print("user Login ")

        # profile page open
        page2.goto("https://10times.com/profile/amar-louni-70833003?olk")

        # Click on close button
        page2.locator("(//button[.//*[name()='svg']])[3]").click()
        print("Close modal  ")
        time.sleep(5)

        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp_mobile()