import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True, slow_mo=2000)
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
    await page.goto("https://login.10times.com/event/eadmin/928626/agenda")
    await page.get_by_role("button", name=" Add Session").click()
    await page.get_by_placeholder("Agenda Title").click()
    await page.get_by_placeholder("Agenda Title").fill("Qwerty 122345")
    await page.get_by_placeholder("Session Type").click()
    await page.get_by_role("link", name="Break", exact=True).click()
    await page.get_by_placeholder("Date").click()
    await page.get_by_role("cell", name="9", exact=True).click()
    await page.get_by_placeholder("Start time").click()
    await page.get_by_placeholder("End time").click()
    await page.get_by_text("Timings Start time should be").click()
    await page.frame_locator("#agenda_form iframe").get_by_text("Add a brief description about").click()
    await page.get_by_role("button", name="Save").click()
    await page.get_by_role("link", name="Listing").click()









    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())