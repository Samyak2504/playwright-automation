<<<<<<< HEAD
from playwright.sync_api import Playwright, sync_playwright
=======
import re
from playwright.sync_api import Playwright, sync_playwright, expect
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://login.10times.com/")
    page.get_by_role("link", name="Partner Login").click()
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("QWERTY")
    page.get_by_role("button", name="Login to your account").click()
    page.get_by_role("button", name="Close").click()
    page.goto("https://login.10times.com/event/eadmin/1154170/agenda")
    page.locator("//label[@class='tgl-btn' and @for='b731313'][1]").click()

    # ---------------------
    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


<<<<<<< HEAD
if __name__ == "__main__":
    run()
=======
asyncio.run(main())
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda
