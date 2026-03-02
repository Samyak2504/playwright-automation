from playwright.sync_api import sync_playwright

def open_10times_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)

        device = p.devices["iPhone 13"]
        context = browser.new_context(**device)
        page = context.new_page()

        page.goto("https://10times.com/experts", wait_until="networkidle")

        # Open location filter
        page.locator("//li[@id='by-location']").first.click()
        print("Opened location filter")

        # Select London
        page.locator("//a[normalize-space()='London']").first.click()
        print("Selected London")

        # Wait for page update
        page.wait_for_load_state("networkidle")

        # Get current URL
        current_url = page.url
        print("Original URL:", current_url)

        # Add ?olk properly
        if "?olk" not in current_url:
            if "?" in current_url:
                new_url = current_url + "&olk"
            else:
                new_url = current_url + "?olk"
        else:
            new_url = current_url

        print("Modified URL:", new_url)

        # Open modified URL
        page.goto(new_url, wait_until="networkidle")

        print("Opened URL with ?olk in MOBILE view")

        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    open_10times_mobile()