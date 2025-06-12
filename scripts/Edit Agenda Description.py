import asyncio
from playwright.async_api import Playwright, async_playwright


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True, slow_mo=2000)
    context = await browser.new_context()
    page = await context.new_page()

    # Step 1: Go to login page and log in
    await page.goto("https://login.10times.com/")
    await page.get_by_role("link", name="Partner Login").click()
    await page.get_by_placeholder("Email Address").click()
    await page.get_by_placeholder("Email Address").fill("samyak@10times.com")
    await page.get_by_placeholder("Password").click()
    await page.get_by_placeholder("Password").fill("QWERTY")
    await page.get_by_role("button", name="Login to your account").click()
    await page.get_by_role("button", name="Close").click()

    # Step 2: Go to agenda page
    await page.goto("https://login.10times.com/event/eadmin/1154170/agenda")

    # Step 3: Click checkbox and Edit button
    await page.locator("(//input[@id='cb1'])").click()
    await page.locator("(//button[text()='Edit'])[1]").click()

    # Step 4: Switch to iframe and modify editor content
    frame = page.frame_locator("#agenda_form iframe")
    editor_body = frame.locator("body")  # or use a more specific selector if needed

    await editor_body.click()
    await editor_body.press("Control+A")
    await editor_body.press("Backspace")
    await editor_body.type(" Qwertyufgh")

    # Step 5: Save changes and return to listing
    await page.get_by_role("button", name="Save").click()
    await page.get_by_role("link", name="Listing").click()

    # Cleanup
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
