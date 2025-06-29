from playwright.sync_api import Playwright, sync_playwright
import time


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Login
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Close popup if it exists
    try:
        page.locator("(//button[@class='close' and @aria-label='Close'])[4]").click(timeout=5000)
    except:
        print("Popup close button not found or already closed")

    # Go to Agenda Page
    page.goto("https://login.10times.com/event/eadmin/928626/agenda")
    page.get_by_role("button", name=" Add Session").click()

    # Fill Agenda Form
    unique_title = f"Auto Agenda {int(time.time())}"
    page.get_by_placeholder("Agenda Title").fill(unique_title)

    page.get_by_placeholder("Session Type").click()
    page.get_by_role("link", name="Break", exact=True).click()

    # Set Date
    page.get_by_placeholder("Date").click()
    page.get_by_role("cell", name="12", exact=True).click()

    # Dismiss datepicker
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Set Time
    page.get_by_placeholder("Start time").click()
    page.get_by_placeholder("End time").click()

    # Click into the iframe to trigger description input
    page.get_by_text("Timings Start time should be").click()
    page.frame_locator("#agenda_form iframe").get_by_text("Add a brief description about").click()

    # Save agenda (no navigation expected)
    page.locator("button#submit1").click()
    page.wait_for_timeout(3000)  # Wait for AJAX/UI update

    # Optional: Check for success message
    try:
        page.wait_for_selector("text=Session Successfully Added", timeout=5000)
        print("✅ Agenda saved successfully.")
    except Exception as e:
        print("⚠️ Agenda save confirmation not found: ", repr(e))

    # Debug: Save screenshot and HTML after save
    page.screenshot(path="debug_after_submit.png", full_page=True)
    with open("debug_after_submit.html", "w") as f:
        f.write(page.content())

    # Try clicking the 'Listing' link
    try:
        page.wait_for_selector("a:has-text('Listing')", timeout=10000)
        page.locator("a:has-text('Listing')").click()
        print("✅ Navigated to 'Listing' successfully.")
    except Exception as e:
        print("❌ Failed to click 'Listing':", e)
        page.screenshot(path="error_listing_not_found.png", full_page=True)

    # Cleanup
    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


if __name__ == "__main__":
    run()
