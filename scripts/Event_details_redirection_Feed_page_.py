from playwright.sync_api import sync_playwright

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser in headed mode with delay (for visibility)
        browser = p.firefox.launch(headless=True, slow_mo=1000)

        # ✅ Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        # ✅ Create browser context with user-agent and custom headers
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # ✅ Create a new page
        page = context.new_page()

        # ✅ Navigate to the initial URL
        page.goto("https://10times.com/magic")

        # ✅ Click the "Feed" tab using no_wait_after to prevent TimeoutError
        page.locator('//a[contains(@class, "tt-tabs-other") and normalize-space(text())="Feed"]').click(no_wait_after=True)

        # ✅ Wait for a few seconds to observe the change or load new content
        page.wait_for_timeout(5000)

        # ✅ (Optional) Screenshot to verify navigation
        page.screenshot(path="feed_page.png")

        # ✅ Close browser context and browser
        context.close()
        browser.close()

# ✅ Entry point
if __name__ == "__main__":
    get_temp_email_and_otp()
