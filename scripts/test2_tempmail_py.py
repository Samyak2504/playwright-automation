import time
from playwright.sync_api import sync_playwright, TimeoutError

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=500)

        # ✅ Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        # ✅ Create context with user-agent
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # ✅ Open the events page
        page = context.new_page()
        page.goto("https://10times.com/events", wait_until="networkidle")
        print("✅ Page loaded successfully")

        # ✅ Click on “Tradeshows” filter
        try:
            page.locator("//a[@href='/tradeshows']").click(timeout=10000)
            print("✅ Clicked on 'Tradeshows' filter")
        except TimeoutError:
            print("⚠️ Could not find 'Tradeshows' filter")

        # ✅ Scroll slightly
        page.evaluate("window.scrollBy(0, 200)")
        time.sleep(2)

        # ✅ Click “London” filter
        try:
            london = page.locator("//span[normalize-space()='London']").first
            london.click(timeout=10000)
            print("✅ Clicked on 'London' filter")
        except TimeoutError:
            print("⚠️ 'London' filter not clickable")

        # ✅ Remove ad iframes before category filters
        print("🧹 Removing Google Ads iframes...")
        page.evaluate("""
            document.querySelectorAll('iframe, ins.adsbygoogle').forEach(el => el.remove());
        """)

        # ✅ Function to click filters safely
        def safe_click(label):
            locator = page.locator(f"//span[normalize-space()='{label}']").first
            try:
                locator.click(timeout=10000, force=True)
                print(f"✅ Clicked '{label}' filter")
            except TimeoutError:
                print(f"⚠️ Timeout on '{label}' — trying JS click")
                try:
                    handle = locator.element_handle()
                    if handle:
                        page.evaluate("(el) => el.click()", handle)
                        print(f"✅ JS clicked '{label}' successfully")
                    else:
                        print(f"❌ Could not find element for '{label}'")
                except Exception as e:
                    print(f"❌ Failed to JS click '{label}': {e}")

        # ✅ Apply remaining filters
        safe_click("Education & Training")
        time.sleep(2)
        safe_click("HR, Jobs & Career")

        # ✅ Wait for content to update
        page.wait_for_timeout(5000)
        print("✅ All filters applied successfully!")

        # ✅ Close browser
        context.close()
        browser.close()
        print("🟢 Browser closed cleanly")

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()
