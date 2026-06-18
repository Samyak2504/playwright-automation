from playwright.sync_api import sync_playwright
import re
import time

def get_temp_email_and_otp():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=1000)
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        page = context.new_page()
        page.goto("https://10times.com/experts")

        #  Use exact XPath to click 1st "London" filter
        locator = page.locator("//a[normalize-space()='London']")
        locator.first.click()  # Use .first in case of duplicates
        print(" Apply 1st filter")

        #  Wait after click
        time.sleep(2)

        #  Use exact XPath to click 2nd  filter
        locator = page.locator("//a[normalize-space()='Education & Training']")
        locator.first.click()  # Use .first in case of duplicates
        print(" Apply 2nd filter")

        #  Wait after click
        time.sleep(2)


        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()