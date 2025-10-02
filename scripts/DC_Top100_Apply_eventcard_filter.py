from playwright.sync_api import sync_playwright
import re
import time

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=1000)

        # ✅ Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        # ✅ Create context with user-agent
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # Create a new page using that context
        page = context.new_page()
        page.goto("https://10times.com/top100")
        page.mouse.move(100, 100)  # simulate mouse movement
        page.mouse.wheel(0, 50)  # simulate scroll down

        page.wait_for_timeout(3000)
        page.locator("(//a[contains(@class, \"text-decoration-none\") and contains(@class, \"xn\") and @href=\"https://10times.com/top100/canada\"])[1]").click()

        context.close()
        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()