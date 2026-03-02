from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=300)

        # 📱 iPhone 13 Mobile Emulation
        device = p.devices["iPhone 13"]
        context = browser.new_context(**device)

        # ---------------- TAB 1 : GOOGLE LOGIN ----------------
        google_page = context.new_page()
        google_page.goto("https://accounts.google.com/", wait_until="networkidle")

        google_page.fill("#identifierId", "samyak@10times.com")
        google_page.get_by_role("button", name="Next").click()

        password_input = google_page.get_by_label("Enter your password")
        password_input.wait_for()
        password_input.fill("Samyak@1998")

        google_page.get_by_role("button", name="Next").click()
        google_page.wait_for_load_state("networkidle")

        print("✅ Google Login Done (Mobile View)")

        # ---------------- TAB 2 : 10TIMES ----------------
        page2 = context.new_page()
        page2.goto("https://10times.com?olk", wait_until="networkidle")

        # MOBILE menu
        page2.locator("(//*[local-name()='svg']//*[local-name()='path'])[1]").click()
        time.sleep(2)

        page2.locator("text=Login").click()
        time.sleep(3)

        page2.locator("//div[@data-name='gLogin']").click()
        print("user Login ")

        # Same tab me profile open
        page2.goto(
            "https://10times.com/profile/amar-louni-70833003?olk",
            wait_until="networkidle"
        )

        print("✅ Profile Page Opened (Mobile)")

        # ---------------- CLOSE POPUP IF PRESENT ----------------
        # Click on close button
        page2.locator("(//button[.//*[name()='svg']])[3]").click()
        print("Expand the calender  ")
        time.sleep(5)

        # Click on Backward button
        page2.locator("//button[.//*[name()='svg' and contains(@class,'lucide-chevron-left')]]").click()
        print(" calender Backward  ")
        time.sleep(5)

        event_page.wait_for_timeout(5000)

        browser.close()


if __name__ == "__main__":
    run()