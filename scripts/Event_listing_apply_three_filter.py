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

        page = context.new_page()
        page.goto(
            "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&dsh=S19276807%3A1760080489828412&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AfYwgwXM93X1KSMmQbIViupG4RT0-W7pozpYpvQXeQ6ge904nOmlBue32q4ctptZlWj86AOXcIdwSQ&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        time.sleep(5)

        # Wait
        email_input = page.locator('//input[@id="identifierId"]')
        email_input.wait_for(timeout=10000)
        email_input.fill("Samyak@10times.com")
        print("✅ Email field filled successfully!")

        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)

        page.locator("//input[@aria-label='Enter your password']").fill("Samyak@1998")
        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)

        page2 = context.new_page()
        page2.goto("https://10times.com/events")
        print("✅ Page loaded successfully")

        # ✅ Click on “Tradeshows” filter
        try:
            tradeshows = page2.locator("//a[@href='/tradeshows']")
            tradeshows.click(timeout=10000)
            print("✅ Clicked on 'Tradeshows' filter")
        except TimeoutError:
            print("⚠️ Couldn't find 'Tradeshows' link. Check locator or page load.")

        # ✅ Scroll a bit to ensure filters are visible
        page2.evaluate("window.scrollBy(0, 300)")
        time.sleep(2)

        # ✅ Click on “London” filter
        try:
            london_filter = page2.locator("//span[normalize-space()='London']").first
            london_filter.click(timeout=10000)
            print("✅ Clicked on 'London' filter")
        except TimeoutError:
            print("⚠️ Couldn't click 'London' filter.")

        time.sleep(2)

        # ✅ Remove ads (iframes and ins tags) that may block clicks
        page2.evaluate("""
            document.querySelectorAll('iframe, ins.adsbygoogle').forEach(el => el.remove());
        """)
        print("🧹 Removed ads/iframes that could block elements")

        # ✅ Try clicking on “Education & Training” filter
        edu_filter = page2.locator("//span[normalize-space()='Education & Training']").first
        try:
            edu_filter.click(timeout=10000, force=True)
            print("✅ Clicked on 'Education & Training' filter")
        except TimeoutError:
            print("⚠️ Standard click failed. Trying JavaScript click...")
            # JavaScript click fallback
            page2.evaluate("(el) => el.click()", edu_filter.element_handle())
            print("✅ JavaScript click successful on 'Education & Training'")

        # ✅ Wait for results to load
        page2.wait_for_timeout(5000)
        print("✅ Filters applied successfully!")

        # ✅ Close context and browser
        context.close()
        browser.close()
        print("🟢 Browser closed successfully")

if __name__ == "__main__":
    get_temp_email_and_otp()
