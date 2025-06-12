import asyncio
from playwright.async_api import Playwright, async_playwright


async def run(playwright: Playwright) -> None:
    browser = await playwright.firefox.launch(headless=True, slow_mo=2000)
    context = await browser.new_context()
    page = await context.new_page()

    # Navigate and login
    await page.goto("https://login.10times.com/")
    await page.get_by_role("link", name="Partner Login").click()
    await page.get_by_placeholder("Email Address").click()
    await page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    await page.get_by_placeholder("Password").click()
    await page.get_by_placeholder("Password").fill("QWERTY")
    await page.get_by_role("button", name="Login to your account").click()
    await page.get_by_role("button", name="Close").click()

    await page.locator("(//a[@class='btn btn-default'])").click()
    await page.locator("(//a[@class='btn btn-default btn-xs profileAcc'])[1]").click()

    await page.locator("(//a[@class='introjs-skipbutton'])").click()


    # Change the value of the Pincode input using XPath
    address_input = page.locator("(//div[@class='col-sm-4']/input[@id='pincode'])")
    await address_input.click()
    await address_input.fill("854318")  # Change the value here

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
