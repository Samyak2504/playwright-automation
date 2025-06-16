import re

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
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
    page.locator("(//input[@id='cb1'])").click()
    page.locator("(//button[text()='Delete'])[1]").click()


    # ---------------------
    context.close()
    browser.close()


def main() -> None:
    async with sync_playwright() as playwright:
        run(playwright)


asyncio.run(main())
