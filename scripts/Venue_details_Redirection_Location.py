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
        page.goto("https://10times.com/venues/gaylord-national-resort-convention-center")
        page.locator("//button[normalize-space()='Location']").click()
        print(" Redirection Location block  ")
        time.sleep(10)
        time.sleep(10)



        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()