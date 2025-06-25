import re
from playwright.sync_api import Playwright, sync_playwright


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Navigate and login
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    # Try to close any popup if it appears
    page.locator("(//button[@class='close' and @aria-label='Close'])[4]").click()


    # Navigate to profile edit page
    page.locator("(//a[@class='btn btn-default'])").click()
    page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()

    # Skip the intro/tour if visible
    try:
        if page.locator("(//a[@class='introjs-skipbutton'])").is_visible():
            page.locator("(//a[@class='introjs-skipbutton'])").click()
            print("Skipped intro.")
    except Exception as e:
        print(f"No intro to skip or error occurred: {e}")

    # Update the address/description
    description_locator = page.locator("(//div[@class='col-sm-4']/textarea[@id='description'])")
    description_locator.click()
    description_locator.fill(
        "XYZbvj b is a leading provider of innovative IT solutions, delivering cutting-edge technology and services "
        "that help businesses streamline their operations and achieve digital transformation. Established in 2010, "
        "our company has grown to become a trusted partner for businesses of all sizes across industries including "
        "healthcare, finance, and retail."
    )

    # Save the updated profile
    page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()

    # Handle confirmation popup
    try:
        page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()
    except Exception as e:
        print(f"No confirmation popup appeared or error occurred: {e}")

    # Optional pause to view result
    page.wait_for_timeout(3000)

=======
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()
    page.get_by_role("button", name="Close").click()

    page.locator("(//a[@class='btn btn-default'])").click()
    page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()

    page.locator("(//a[@class='introjs-skipbutton'])").click()


    # Change the value of the Website input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/textarea[@id='description'])")
    address_input.click()
    address_input.fill("XYZbvj b Technologies is a leading provider of innovative IT solutions, delivering cutting-edge technology and services that help businesses streamline their operations and achieve digital transformation. Established in 2010, our company has grown to become a trusted partner for businesses of all sizes across industries including healthcare, finance, and retail.")  # Change the value here

    page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()
    page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()

    # Optional: wait to see the result
    page.wait_for_timeout(3000)

    # ---------------------
    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


if __name__ == "__main__":
    run()
