from playwright.sync_api import sync_playwright

def get_temp_email_and_otp_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)

        # iPhone 13. emulation
        device = p.devices["iPhone 13."].copy()
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
        page.wait_for_timeout(4000)

        page.locator("input[type='password']").fill("Samyak@1996")
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(6000)

        # --- Open 10times ---
        page2 = context.new_page()
        page2.goto("https://10times.com/company")
        page2.get_by_role("button", name="Login").click()
        page2.locator("//div[@data-name='gLogin']").click()
        time.sleep(10)

        # --- Scroll to bottom (infinite scroll handling) ---
        print("Scrolling to load all results...")

        previous_height = 0

        while True:
            current_height = page2.evaluate("document.body.scrollHeight")

            if current_height == previous_height:
                break

            page2.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page2.wait_for_timeout(3000)

            previous_height = current_height

        print(" Reached bottom, all results loaded")

        # Optional: Count results (update locator if needed)
        # items = page2.locator("//div[contains(@class,'company')]")
        # print("Total results:", items.count())

        page2.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    get_temp_email_and_otp_mobile()