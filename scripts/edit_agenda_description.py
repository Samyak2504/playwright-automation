import re
from playwright.sync_api import Playwright, sync_playwright


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Step 1: Go to login page and log in
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()
    page.get_by_role("button", name="Close").click()

    # Step 2: Go to agenda page
    page.goto("https://login.10times.com/event/eadmin/1154170/agenda")

    # Step 3: Click checkbox and Edit button
    page.locator("(//input[@id='cb1'])").click()
    page.locator("(//button[text()='Edit'])[1]").click()

    # Step 4: Switch to iframe and modify editor content
    frame = page.frame_locator("#agenda_form iframe")
    editor_body = frame.locator("body")  # or use a more specific selector if needed

    editor_body.click()
    editor_body.press("Control+A")
    editor_body.press("Backspace")
    editor_body.type(" Qwertyufgh")

    # Step 5: Save changes and return to listing
    page.get_by_role("button", name="Save").click()
    page.get_by_role("link", name="Listing").click()

    # Cleanup
    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


if __name__ == "__main__":
    run()
