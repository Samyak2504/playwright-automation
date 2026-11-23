import re
from playwright.sync_api import sync_playwright, expect


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.google.com/ncr", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        try:
            page.get_by_role("button", name="Accept all").click(timeout=5000)
        except Exception:
            print("No popup to accept")

        page.get_by_role("combobox", name="Search").fill("Playwright python")
        page.keyboard.press("Enter")

        expect(page).to_have_title(re.compile("Playwright", re.IGNORECASE))
        browser.close()


if __name__ == "__main__":
    main()
