from playwright.sync_api import sync_playwright
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

        # ✅ Create page from context
        page = context.new_page()
        page.goto("https://10times.com/event/928626")

        # ✅ Click the Followers
        page.locator("//span[text()='Exhibitors']").click()

        page.wait_for_timeout(5000)

        # ✅ Close context and browser
        context.close()
        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()