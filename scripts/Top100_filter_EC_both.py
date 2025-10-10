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

        # -------- Apply Canada filter --------
        canada_filter = page.locator("(//a[contains(@class,'xn') and text()='Canada'])[1]")
        canada_filter.wait_for(state="visible", timeout=10000)
        canada_filter.click()
        print("✅ Canada filter clicked")

        # Wait for events to load
        try:
            page.locator("//a[contains(@href,'/event/')]").first.wait_for(state="visible", timeout=15000)
            print("✅ Canada events loaded")
        except TimeoutError:
            print("⚠️ No events found for Canada filter")

        # -------- Apply Travel & Tourism filter --------
        travel_filter = page.locator("(//a[contains(@class,'xn') and text()='Travel & Tourism'])[1]")
        travel_filter.wait_for(state="visible", timeout=10000)
        travel_filter.click()
        print("✅ Travel & Tourism filter clicked")

        # Wait for events to load again
        try:
            page.locator("//a[contains(@href,'/event/')]").first.wait_for(state="visible", timeout=15000)
            print("✅ Travel & Tourism events loaded")
        except TimeoutError:
            print("⚠️ No events found for Travel & Tourism filter")

        # -------- Scroll to load all events --------
        previous_height = 0
        while True:
            page.mouse.wheel(0, 1000)  # scroll down
            page.wait_for_timeout(2000)
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            previous_height = current_height

        # -------- Collect all event links --------
        event_links = page.locator("//a[contains(@href,'/event/')]").all()
        event_urls = [link.get_attribute("href") for link in event_links if link.get_attribute("href")]

        print(f"✅ Total events collected: {len(event_urls)}")
        for url in event_urls:
            print(url)

        # Close browser
        context.close()
        browser.close()
        print("✅ Script finished")

if __name__ == "__main__":
    collect_top100_event_links()
