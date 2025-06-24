<<<<<<< HEAD
from playwright.sync_api import Playwright, sync_playwright


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()

    page.locator("(//button[@class='close' and @aria-label='Close'])[4]").click()


    page.locator("(//a[@class='btn btn-default'])").click()
    page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()

    try:
        page.locator("(//a[@class='introjs-skipbutton'])").click()
    except:
        pass

    page.wait_for_timeout(3000)

    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)

=======
import re
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://login.10times.com/")
        page.get_by_role("link", name="Partner Login").click()
        page.get_by_placeholder("Email Address").fill("samyak@10times.com")
        page.get_by_placeholder("Password").fill("QWERTY")
        page.get_by_role("button", name="Login to your account").click()
        page.get_by_role("button", name="Close").click()

        page.locator("(//a[@class='btn btn-default'])").click()
        page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()
        page.locator("(//a[@class='introjs-skipbutton'])").click()

        page.wait_for_timeout(3000)

        context.close()
        browser.close()
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda

if __name__ == "__main__":
    run()
