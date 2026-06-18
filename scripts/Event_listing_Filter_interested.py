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


        page2 = context.new_page()
        page2.goto("https://10times.com/events")

        page2.evaluate("window.scrollBy(0, 450);")
        time.sleep(2)

        page2.locator("//span[normalize-space()='Education & Training']")
        time.sleep(2)

        page2.locator("(//span[@class='action' and text()='Interested'])[1]").click()
        page2.locator("//span[contains(text(), 'Continue with Google')]").click()
        print("Event redirection from event listing page")


        time.sleep(20)

        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()
