from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Go to login page
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()

    # Enter credentials
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")

    # Submit login form
    page.get_by_role("button", name="Login to your account").click()

    # Close popup if it appears
    try:
        page.get_by_role("button", name="Close").click(timeout=3000)
    except:
        pass

    # Navigate to ticket fees page
    page.goto("https://login.10times.com/event/eadmin/928626/fees")

    # Handle confirmation dialog
    def handle_dialog(dialog):
        print("Dialog text:", dialog.message)
        dialog.accept()

    page.once("dialog", handle_dialog)

    # Click the delete icon for the first ticket
    page.locator("//button[@type='button' and contains(@onclick, \"deleteTicketN('1',-1)\")]//i[contains(@class, 'glyphicon-trash')]").click()

    # Wait to let deletion complete
    page.wait_for_timeout(5000)

    # Cleanup
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
