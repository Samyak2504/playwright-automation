<<<<<<< HEAD
=======
<<<<<<<< HEAD:scripts/e_unpublised_agenda.py
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda
from playwright.sync_api import Playwright, sync_playwright


def run_script(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True, slow_mo=2000)
<<<<<<< HEAD
=======
========
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_script(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, slow_mo=2000)
>>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda:scripts/edit_agenda_type.py
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda
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
<<<<<<< HEAD
    page.locator("(//input[@id='cb1'])").click()
    page.locator("(//button[text()='Edit'])[1]").click()
    page.get_by_placeholder("Session Type").click()
    page.get_by_role("link", name="Closing Ceremony", exact=True).click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("link", name="Listing").click()
=======
    page.locator("//label[@class='tgl-btn' and @for='b731313'][1]").click()
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda

    # ---------------------
    context.close()
    browser.close()


def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


<<<<<<< HEAD
=======
<<<<<<<< HEAD:scripts/e_unpublised_agenda.py
========

>>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda:scripts/edit_agenda_type.py
>>>>>>> 8840c4d9671bdf7019e6c9a4e489368757a98eda
if __name__ == "__main__":
    run()
