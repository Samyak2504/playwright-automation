from playwright.sync_api import sync_playwright, TimeoutError

def collect_top100_event_links():
    with sync_playwright() as p:
        # Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=500)
        context = browser.new_context(
            user_agent="TenTimes internal Testing/tentimestesting10t112",
            extra_http_headers={"User-Agent": "TenTimes internal Testing/tentimestesting10t112"}
        )
        page = context.new_page()
        page.goto("https://10times.com/top100")
        page.wait_for_timeout(3000)  # Wait for page to load

        # Scroll to reveal filters
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(1000)

        page.locator("//a[@aria-label='1' and normalize-space(text())='1']").click()
        print("Event redirect")
        time.sleep(5)

        browser.close()

if __name__ == "__main__":
    collect_top100_event_links()
