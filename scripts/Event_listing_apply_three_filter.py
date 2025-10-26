import time
from playwright.sync_api import sync_playwright, TimeoutError

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=500)

        # ✅ Custom user-agent setup
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        # ✅ Create browser context
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # ✅ Create and open page
        page = context.new_page()
        page.goto("https://10times.com/events", wait_until="networkidle")
        print("✅ Page loaded successfully")

        # ✅ Click on “Tradeshows” filter
        try:
            tradeshows = page.locator("//a[@href='/tradeshows']")
            tradeshows.click(timeout=10000)
            print("✅ Clicked on 'Tradeshows' filter")
        except TimeoutError:
            print("⚠️ Couldn't find 'Tradeshows' link. Check locator or page load.")

        # ✅ Scroll a bit to ensure filters are visible
        page.evaluate("window.scrollBy(0, 300)")
        time.sleep(2)

        # ✅ Click on “London” filter
        try:
            london_filter = page.locator("//span[normalize-space()='London']").first
            london_filter.click(timeout=10000)
            print("✅ Clicked on 'London' filter")
        except TimeoutError:
            print("⚠️ Couldn't click 'London' filter.")

        time.sleep(2)

        # ✅ Remove ads (iframes and ins tags) that may block clicks
        page.evaluate("""
            document.querySelectorAll('iframe, ins.adsbygoogle').forEach(el => el.remove());
        """)
        print("🧹 Removed ads/iframes that could block elements")

        # ✅ Try clicking on “Education & Training” filter
        edu_filter = page.locator("//span[normalize-space()='Education & Training']").first
        try:
            edu_filter.click(timeout=10000, force=True)
            print("✅ Clicked on 'Education & Training' filter")
        except TimeoutError:
            print("⚠️ Standard click failed. Trying JavaScript click...")
            # JavaScript click fallback
            page.evaluate("(el) => el.click()", edu_filter.element_handle())
            print("✅ JavaScript click successful on 'Education & Training'")

        # ✅ Wait for results to load
        page.wait_for_timeout(5000)
        print("✅ Filters applied successfully!")

        # ✅ Close context and browser
        context.close()
        browser.close()
        print("🟢 Browser closed successfully")

if __name__ == "__main__":
    get_temp_email_and_otp()
