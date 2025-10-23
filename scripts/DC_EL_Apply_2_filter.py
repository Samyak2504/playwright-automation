import re
import time
from playwright.sync_api import sync_playwright

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=1000)

        # ✅ Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"  # Corrected quotes

        # ✅ Create context with user-agent
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # ✅ Create page from context
        page = context.new_page()
        page.goto("https://10times.com/events")

        # ✅ Apply Format filter by clicking on the specified <a> element
        page.locator("//a[@class='d-flex btn btn-sm w-100 text-start px-0 py-2 c-ga' and @href='/tradeshows' and @data-ga-category='Listing Filter' and @data-ga-action='City' and @data-ga-label='Event Listing | Filter | Tradeshows']").click()

        # ✅ Slight scroll to load filters (scroll just 300px)
        page.evaluate("window.scrollBy(0, 100);")
        time.sleep(2)  # Wait for content to load

        # ✅ Use exact XPath to click "London" filter
        locator = page.locator("//span[@class='d-flex justify-content-between' and normalize-space()='London']")
        locator.first.click()  # Use .first in case of duplicates

        # Wait for the page to load after applying the filter
        page.wait_for_timeout(5000)  # You can adjust the timeout as per your requirement

        # ✅ Capture email or OTP (if needed, implement further steps here)
        # You can add code to capture email or OTP as per your need.

        # ✅ Close context and browser
        context.close()
        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()