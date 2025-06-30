import random
import string
from playwright.sync_api import Playwright, sync_playwright

def generate_random_exhibitor_name(prefix="exh_", length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Step 1: Go to login page
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()

    # Step 2: Fill in credentials
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Optional: Close modal if it appears
    try:
        page.get_by_role("button", name="Close").click()
    except:
        pass  # If "Close" button doesn't appear, just continue

    # Step 3: Go to Add Exhibitor page
    page.goto("https://login.10times.com/event/eadmin/928626/exhibitors?type=add")

    # Step 4: Generate random exhibitor name and email
    random_exhibitor = generate_random_exhibitor_name()
    random_email = f"{random_exhibitor.lower()}@example.com"

    # Step 5: Fill in exhibitor info
    page.locator("#add_comp").click()
    page.locator("#add_comp").fill(random_exhibitor)
    page.locator("#user_email").click()
    page.locator("#user_email").fill(random_email)

    # Step 6: Submit form
    page.locator('#submission').click()

    # Optional: Print what was submitted
    print(f"Submitted Exhibitor: {random_exhibitor}, Email: {random_email}")

    # Cleanup
    context.close()
    browser.close()

def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()