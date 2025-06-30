from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Go to login page
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()

    # Fill login credentials
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")

    # Click Login
    page.get_by_role("button", name="Login to your account").click()

    # Close popup (if exists)
    try:
        page.get_by_role("button", name="Close").click(timeout=3000)
    except:
        pass  # Ignore if popup not shown

    # Navigate to Fees page
    page.goto("https://login.10times.com/event/eadmin/1154170/fees")

    # Toggle the first switch
    page.locator("(//span[@class='slider round'])[1]").click()

    # Wait 5 seconds
    page.wait_for_timeout(5000)

    # Cleanup
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
