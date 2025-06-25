from playwright.sync_api import Playwright, sync_playwright


def run_script(playwright: Playwright) -> None:
import re
from playwright.sync_api import Playwright, sync_playwright

def run_test(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    # Navigate and login
    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    page.locator("(//button[@class='close' and @aria-label='Close'])[4]").click()


    page.locator("(//a[@class='btn btn-default'])").click()
    page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()

    page.locator("(//a[@class='introjs-skipbutton'])").click()

    # Change the value of the Pincode input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='pincode'])")
    address_input.click()
    address_input.fill("85418")  # Change the value here

    page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()
    page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()

    page.wait_for_timeout(3000)

    context.close()
    browser.close()

def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)

        run_test(playwright)

if __name__ == "__main__":
    run()
