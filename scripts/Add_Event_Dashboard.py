from playwright.sync_api import sync_playwright
import re
import time


def get_temp_email_and_otp():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=1000)
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

        page2 = context.new_page()
        page2.goto("https://10times.com")
        page2.get_by_role("button", name="Login").click()
        page2.locator("//div[@data-name='gLogin']").click()
        time.sleep(10)

        page2.goto("https://10times.com/dashboard/addevent")
        page2.locator("//textarea[@placeholder='Event Name']").fill("Samyak New")
        page2.locator("//span[text()='Tradeshow']").click()
        time.sleep(10)

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

        # Wait for suggestions
        page2.wait_for_timeout(3000)

        # Wait for suggestions and click the first match
        #suggestion = page2.locator("(//span[contains(text(),'Noida')])[1]")
        # suggestion.wait_for(timeout=5000)
        #suggestion.click()

        #  Add your description
        page2.locator("(//div[normalize-space()='Add Description'])[1]").click()
        page2.locator("(//div[@data-placeholder='Write something...'])[1]").fill("This is new Event")
        page2.locator("(//span[contains(text(),'Save changes')])[1]").click()
        time.sleep(5)

        #  Click on the "Add to calendar" button
        page2.locator("//button[normalize-space()='Add to calendar']").click()
        time.sleep(10)


        browser.close()


if __name__ == "__main__":
    get_temp_email_and_otp()