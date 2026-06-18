import re
import time
from playwright.sync_api import sync_playwright

def get_temp_email_and_otp():
    with sync_playwright() as p:
        #  Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=1000)

        #  Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"  # Corrected quotes

        #  Create context with user-agent
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        page = context.new_page()
        page.goto("https://10times.com/events")
        print(" Open listing page")

        #  Apply Format filter by clicking on the specified <a> element
        page.locator("//button[normalize-space(.)='Trade Shows']").click()

        # Wait for the page to load after applying the filter
        page.wait_for_timeout(3000)  # You can adjust the timeout as per your requirement
        print(" Select Format")

        #  Close context and browser
        context.close()
        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()
