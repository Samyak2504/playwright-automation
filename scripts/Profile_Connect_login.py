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
        page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&dsh=S19276807%3A1760080489828412&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AfYwgwXM93X1KSMmQbIViupG4RT0-W7pozpYpvQXeQ6ge904nOmlBue32q4ctptZlWj86AOXcIdwSQ&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        time.sleep(5)

        # Wait
        email_input = page.locator('//input[@id="identifierId"]')
        email_input.wait_for(timeout=10000)
        email_input.fill("Samyak@10times.com")
        print(" Email field filled successfully!")

        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)

        page.locator("//input[@aria-label='Enter your password']").fill("Samyak@1998")
        page.locator(".VfPpkd-vQzf8d", has_text="Next").click()
        time.sleep(5)
        print(" Password field filled successfully!")

        page2 = context.new_page()
        page2.goto("https://10times.com/profile/amar-louni-70833003")
        page2.locator("//button[normalize-space()='Connect']").click()

        page2.locator("//div[contains(@class, 'social_button') and contains(text(), 'Continue with Google')]").click()
        print(" User login ")
        print(" Request Sent ")

        time.sleep(20)

        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()
