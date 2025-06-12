import asyncio
# import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.firefox.launch(headless=True, slow_mo=2000)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://login.10times.com/")
    await page.get_by_role("link", name="Partner Login").click()
    await page.get_by_placeholder("Email Address").click()
    await page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    await page.get_by_placeholder("Password").click()
    await page.get_by_placeholder("Password").fill("QWERTY")
    await page.get_by_role("button", name="Login to your account").click()
    await page.get_by_role("button", name="Close").click()
    await page.locator("(//a[@class='btn btn-default'])").click()
    await page.locator("(//span[@class='hidden-xs hidden-sm'])[1]").click()
    await page.locator("//input[@value='company']").click()

    # Fill in the value of the Business Name input using XPath
    address_input = page.locator("(//input[@id='change_name_company'])")
    await address_input.click()
    await address_input.fill("qwerty xxyz")  # Business Name  here

    # Fill in the value of the address input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='address'])")
    await address_input.click()
    await address_input.fill("14th Avenue , Gaur city 2")  # input here

    # Fill in  the value of the Pincode input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='pincode'])")
    await address_input.click()
    await address_input.fill("854318")  # fill the Pincode value here

    # Fill in the City  using XPath
    address_input = page.locator("(//input[@name='cityname'])")
    await address_input.click()
    await address_input.fill("noida ")  # Fill in the City



    # Fill in  the value of the Website input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='website'])")
    await address_input.click()
    await address_input.fill("https://xyz.com")  # fill in  the Website value here

    # Change the value of the Website input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/textarea[@id='description'])")
    await address_input.click()
    await address_input.fill(
        "XYZ Technologies is a leading provider of innovative IT solutions, delivering cutting-edge technology and services that help businesses streamline their operations and achieve digital transformation. Established in 2010, our company has grown to become a trusted partner for businesses of all sizes across industries including healthcare, finance, and retail.")  # Change the value here

    await page.locator("(//div[@class='box-footer']/button[text()='Save'])").click()
    await page.locator("(//div[@id='alert']//button[@id='ok-button' and text()='Ok'])").click()

    # Optional: wait to see the result
    await page.wait_for_timeout(3000)

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


# Run the main async function
asyncio.run(main())
