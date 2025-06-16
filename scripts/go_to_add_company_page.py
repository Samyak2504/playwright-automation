import re
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=1000)
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

if __name__ == "__main__":
    run()
