from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Go to login page
    page.goto("https://login.10times.com/")

    # Click on Partner Login
    page.get_by_role("link", name="Partner Login").click()

    # Fill in login credentials
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Close any popup if visible
    try:
        page.get_by_role("button", name="Close").click(timeout=3000)
    except:
        pass  # Ignore if not found

    # Go to ticket fees page
    page.goto("https://login.10times.com/event/eadmin/1154170/fees")

    # Count existing tickets (adjust selector based on actual ticket list row)
    existing_ticket_buttons = page.locator("button[id^='submitTicketIdN']").all()
    next_ticket_number = len(existing_ticket_buttons)  # 0-based

    # Add new ticket
    page.get_by_role("button", name=" Add New").click()
    page.get_by_placeholder("Ticket Type").fill(f"qwerty{1000 + next_ticket_number}")
    page.get_by_placeholder("Quantity").fill("11")

    # Construct dynamic ID
    dynamic_button_id = f"#submitTicketIdN{next_ticket_number}"
    page.locator(dynamic_button_id).click()

    page.wait_for_timeout(5000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
