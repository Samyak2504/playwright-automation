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

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)

# Run the asyncio event loop and execute the `main()` coroutine/method to start the program
asyncio.run(main())