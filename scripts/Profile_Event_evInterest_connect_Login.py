from playwright.sync_api import sync_playwright
import time

def get_temp_email_and_otp():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=800)
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # --- STEP 1: Login to Gmail ---
        page = context.new_page()
        page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&dsh=S354686971%3A1761497156648717&ifkv=ARESoU0qmqppoC3UIBVFO5kmjaQouD9hvAamE5YlKMBKACKKhrXo9V3bRcIyn8_quzm2WA2qXtqT4g&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        page.wait_for_selector('//input[@id="identifierId"]')
        page.fill('//input[@id="identifierId"]', "Samyak@10times.com")
        page.click("//span[text()='Next']")
        time.sleep(4)

        page.wait_for_selector("//input[@aria-label='Enter your password']")
        page.fill("//input[@aria-label='Enter your password']", "Samyak@1998")
        page.click("//span[text()='Next']")
        time.sleep(6)
        print(" Logged into Gmail successfully!")

        # --- STEP 2: Open profile page ---
        page2 = context.new_page()
        page2.goto("https://10times.com")
        page2.get_by_role("button", name="Login").click()
        page2.locator("//div[@data-name='gLogin']").click()
        print(" User login ")
        time.sleep(10)

        page2.goto("https://10times.com/profile/amar-louni-70833003?olk?")

        # Slight scroll to load filters (scroll just 300px)
        page2.evaluate("window.scrollBy(0, 100);")
        time.sleep(2)  # Wait for content to load
        print(" Profile page loaded")

        # --- STEP 3: Click on first event (which opens in a new tab) ---
        with context.expect_page() as new_page_info:
            page2.locator("(//div[contains(@class, 'dashboardeventcard_style_bigName__')])[1]").click()
        page3 = new_page_info.value  # This is the new tab (event page)
        page3.wait_for_load_state("domcontentloaded")
        print(" Switched to Event tab")

        # --- STEP 4: Click 'Connect' button on the Event page ---
        page3.wait_for_selector("//button[normalize-space()='Connect']", timeout=10000)
        page3.locator("//button[normalize-space()='Connect']").click()
        print(" Clicked 'Connect' button")


        time.sleep(20)
        browser.close()


if __name__ == "__main__":
    get_temp_email_and_otp()
