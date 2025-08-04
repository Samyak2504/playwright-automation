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
        page.goto("https://10times.com/top100")

        # Simulate scroll and wait
        page.mouse.move(100, 100)
        page.mouse.wheel(0, 100)
        page.wait_for_timeout(2000)

        # ✅ Click the Canada filter
        canada_xpath = '(//a[contains(@class, "text-decoration-none") and contains(@class, "xn") and @href="https://10times.com/top100/canada"])[1]'
        page.wait_for_selector(canada_xpath)
        page.locator(canada_xpath).click()

        # ✅ Wait for any network activity to settle after filter
        page.wait_for_load_state("networkidle")
        time.sleep(2)  # optional buffer

        # ✅ Click the Travel & Tourism filter
        tourism_xpath = '(//a[contains(@class, "text-decoration-none") and contains(@class, "xn") and @href="https://10times.com/top100/canada/travel-tourism"])[1]'
        page.wait_for_selector(tourism_xpath)
        page.locator(tourism_xpath).click()

        # Wait a bit to observe result
        page.wait_for_timeout(5000)

        # ✅ Close context and browser
        context.close()
        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()
