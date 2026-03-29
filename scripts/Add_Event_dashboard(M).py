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
        time.sleep(5)

        # Same tab me profile open
        page2.goto("https://10times.com/dashboard/addevent", wait_until="networkidle")
        print("✅ Add event page Opened (Mobile)")
        time.sleep(5)

        # ---------------- Add name and select Event type ----------------
        page2.locator("//textarea[@placeholder='Event Name']").fill("Samyak New")
        page2.locator("//span[text()='Tradeshow']").click()

        print("Add name and select Event type")
        time.sleep(5)

        # Add event location
        page2.locator("//div[text()='Add Event Location']").click()

        location_input = page2.locator("//input[contains(@placeholder,'Enter location')]")
        location_input.wait_for(state="visible", timeout=10000)
        location_input.click()

        # Type like a real user
        page2.keyboard.type("noida")

        page2.locator(
            "//div[contains(@class,'max-h') and contains(@class,'overflow-y-auto')]"
        ).wait_for(timeout=10000)

        # Click first Noida suggestion
        page2.locator(
            "//div[contains(@class,'cursor-pointer') and .//span[normalize-space()='Noida,']]"
        ).first.click()
        print("location select from dropdown")

        # Wait for suggestions
        page2.wait_for_timeout(3000)

        # Wait for suggestions and click the first match
        # suggestion = page2.locator("(//span[contains(text(),'Noida')])[1]")
        # suggestion.wait_for(timeout=5000)
        # suggestion.click()

        #  Add your description
        page2.locator("(//div[normalize-space()='Add Description'])[1]").click()
        page2.locator("(//div[@data-placeholder='Write something...'])[1]").fill("This is new Event")
        page2.locator("(//span[contains(text(),'Save changes')])[1]").click()
        print("description Added")
        time.sleep(5)

        #  Click on the "Add to calendar" button
        page2.locator("//button[normalize-space()='Submit']").click()
        print("Event created successful")
        time.sleep(10)

        browser.close()


if __name__ == "__main__":
    run()