from playwright.sync_api import Playwright, sync_playwright


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
    page.locator("(//button[@class='close' and @aria-label='Close'])[4]").click()
    page.goto("https://login.10times.com/event/eadmin/928626/agenda")
    page.get_by_role("button", name=" Add Session").click()
    page.get_by_placeholder("Agenda Title").click()
    page.get_by_placeholder("Agenda Title").fill("Qwerty 122345")
    page.get_by_placeholder("Session Type").click()
    page.get_by_role("link", name="Break", exact=True).click()
    page.get_by_placeholder("Date").click()
    page.get_by_role("cell", name="12", exact=True).click()
    page.get_by_placeholder("Start time").click()
    page.get_by_placeholder("End time").click()
    page.get_by_text("Timings Start time should be").click()
    page.frame_locator("#agenda_form iframe").get_by_text("Add a brief description about").click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("link", name="Listing").click()

    # ---------------------
    context.close()
    browser.close()

def run() -> None:
    with sync_playwright() as playwright:
        run_script(playwright)


if __name__ == "__main__":
    run()
