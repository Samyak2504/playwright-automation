import random
from playwright.sync_api import Playwright, sync_playwright

def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Step 1: Open login page
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()

    # Step 2: Login with credentials
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Step 3: Navigate to Fact & Figure section
    page.goto("https://login.10times.com/event/eadmin/928626/fact-figure")

    # Step 4: Click "Estimated Exhibitors"
    page.locator('(//a[@data-name="visitorsTotal"])[1]').click()

    # Step 5: Generate random number between 1 and 100
    random_number = str(random.randint(1, 100))

    # Step 6: Fill the input with the random number
    input_locator = page.locator('//input[@placeholder="Enter Number"]')
    input_locator.wait_for()  # Wait for input to appear
    input_locator.fill(random_number)

    # Optional: Press Enter to save (depends on site behavior)
    input_locator.press("Enter")

    # Wait to observe result (optional)
    page.wait_for_timeout(3000)

    # Cleanup
    context.close()
    browser.close()

def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)

if __name__ == "__main__":
    run()
