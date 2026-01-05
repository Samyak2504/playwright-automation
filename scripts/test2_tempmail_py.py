from playwright.sync_api import sync_playwright


def add_event_10times():
    with sync_playwright() as p:
        # Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=500)
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        page = context.new_page()
        page.goto(
            "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&dsh=S19276807%3A1760080489828412&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AfYwgwXM93X1KSMmQbIViupG4RT0-W7pozpYpvQXeQ6ge904nOmlBue32q4ctptZlWj86AOXcIdwSQ&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        time.sleep(5)

        # Wait and fill email/phone field
        email_input = page.locator('//input[@id="identifierId"]')
        email_input.wait_for(timeout=10000)
        email_input.fill("Samyak@10times.com")
        print("✅ Email field filled successfully!")

        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)

        page.locator("//input[@aria-label='Enter your password']").fill("Samyak@2512")
        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)

        # Wait for redirect back to 10times login
        page2 = context.new_page()
        page2.goto("https://10times.com")
        page2.get_by_role("button", name="Login").click()
        page2.locator("//div[@data-name='gLogin']").click()
        time.sleep(10)
        print(" Google login successful!")

        # -----------------------------
        # Step 2: Navigate to Add Event Page
        # -----------------------------
        page.goto("https://10times.com/dashboard/addevent")
        page.wait_for_selector("//textarea[@placeholder='Event Name']", timeout=15000)

        # -----------------------------
        # Step 3: Fill Event Name & Type
        # -----------------------------
        page.fill("//textarea[@placeholder='Event Name']", "Samyak New")
        page.locator("//span[text()='Tradeshow']").click()

        # -----------------------------
        # Step 4: Add Event Location
        # -----------------------------
        page.locator("//div[text()='Add Event Location']").click()
        page.fill("//input[contains(@placeholder,'Enter location')]", "noida")
        page.locator("(//span[contains(text(),'Noida')])[1]").click()

        # -----------------------------
        # Step 5: Add Description
        # -----------------------------
        page.locator("(//div[normalize-space()='Add Description'])[1]").click()
        page.fill("(//div[@data-placeholder='Write something...'])[1]", "This is new Event")
        page.locator("(//span[contains(text(),'Save changes')])[1]").click()

        # -----------------------------
        # Step 6: Add to Calendar
        # -----------------------------
        page.locator("//button[normalize-space()='Add to calendar']").click()

        print(" Event added successfully!")

        # Close browser
        browser.close()


if __name__ == "__main__":
    add_event_10times()
