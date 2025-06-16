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

    # Fill in the value of the Business Name input using XPath
    address_input = page.locator("(//input[@id='change_name_company'])")
    address_input.click()
    address_input.fill("qwerty xxyz")  # Business Name  here

    # Fill in the value of the address input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='address'])")
    address_input.click()
    address_input.fill("14th Avenue , Gaur city 2")  # input here

    # Fill in  the value of the Pincode input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='pincode'])")
    address_input.click()
    address_input.fill("854318")  # fill the Pincode value here

    # Fill in the City  using XPath
    address_input = page.locator("(//input[@name='cityname'])")
    address_input.click()
    address_input.fill("noida ")  # Fill in the City



    # Fill in  the value of the Website input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='website'])")
    address_input.click()
    address_input.fill("https://xyz.com")  # fill in  the Website value here

    # Change the value of the Website input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/textarea[@id='description'])")
    address_input.click()
    address_input.fill(
        "XYZ Technologies is a leading provider of innovative IT solutions, delivering cutting-edge technology and services that help businesses streamline their operations and achieve digital transformation. Established in 2010, our company has grown to become a trusted partner for businesses of all sizes across industries including healthcare, finance, and retail.")  # Change the value here

    page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()
    page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()

    # Optional: wait to see the result
    page.wait_for_timeout(3000)

    # ---------------------
    context.close()
    browser.close()


def main() -> None:
    async with sync_playwright() as playwright:
        run(playwright)


# Run the main async function
asyncio.run(main())
