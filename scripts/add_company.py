import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
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
    page.locator("(//a[@class='btn btn-default'])").click()
    page.locator("(//span[@class='hidden-xs hidden-sm'])[1]").click()
    page.locator("//input[@value='company']").click()

    # Fill in the Business Name
    page.locator("(//input[@id='change_name_company'])").fill("Company oneone")

    # Fill in the Address
    page.locator("(//div[@class='col-sm-4']/input[@id='address'])").fill("14th Avenue , Gaur city 2")

    # Fill in the Pincode
    page.locator("(//div[@class='col-sm-4']/input[@id='pincode'])").fill("854318")

    # Fill in the City
    page.locator("(//input[@name='cityname'])").fill("noida ")

    # Fill in the Website
    page.locator("(//div[@class='col-sm-4']/input[@id='website'])").fill("https://xyz.com")

    # Fill in the Description
    page.locator("(//div[@class='col-sm-4']/textarea[@id='description'])").fill(
        "XYZ Technologies is a leading provider of innovative IT solutions, delivering cutting-edge technology and services that help businesses streamline their operations and achieve digital transformation. Established in 2010, our company has grown to become a trusted partner for businesses of all sizes across industries including healthcare, finance, and retail."
    )

    # Click Save and OK
    page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()
    page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()

    page.wait_for_timeout(3000)
    context.close()
    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()
