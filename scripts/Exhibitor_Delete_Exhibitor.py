from playwright.sync_api import Playwright, sync_playwright

def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Step 1: Login
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Step 2: Navigate to exhibitor list
    page.goto("https://login.10times.com/event/eadmin/928626/exhibitors")

    # Step 3: Click the first Delete button
    page.locator("(//a[@onclick='ex_delete(this)' and contains(text(), 'Delete')])[1]").click()

    # Step 4: Confirm deletion by clicking "YES"
    page.locator('//button[@id="testingbtn"]').click()

    # Cleanup
    context.close()
    browser.close()

def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)

if __name__ == "__main__":
    run()
