from playwright.sync_api import sync_playwright
import re
import time

def get_temp_email_and_otp():
    with sync_playwright() as p:
        # ✅ Launch browser
        browser = p.firefox.launch(headless=True, slow_mo=1000)

        # ✅ Define custom user-agent
        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        # ✅ Create context with user-agent
        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # Create a new page using that context
        page = context.new_page()

        # Step 1: Navigate to Temp-Mail
        page.goto("https://tempmailo.com")
        time.sleep(5)  # Wait for the email to load

        # Step 2: Get Temporary Email Address
        temp_email = page.locator("input#i-email").input_value()
        print(f"Temporary Email: {temp_email}")

        # Step 3: Use temp_email for signup on the target site
        page2 = context.new_page()
        page2.goto("https://10times.com")  # Replace with your signup page URL

        # Fill the signup form
        page2.get_by_role("button", name="Login").click()
        page2.get_by_placeholder("Email").click()
        page2.fill("input[name='email1']", temp_email)
        page2.click("input[type='submit']")  # Submit the form

        # Wait for OTP email to arrive in Temp-Mail inbox
        page.bring_to_front()  # Switch back to the Temp-Mail page
        otp = None

        try:
            page.wait_for_selector("text=mail@10times.com", timeout=30000)
            page.locator("text=mail@10times.com").first.click()
            time.sleep(2)

            otp_element = page.locator("div.mail-item-sub").text_content()
            otp_match = re.search(r'OTP - (\d+)', otp_element)
            if otp_match:
                otp = otp_match.group(1)
                print(f"Extracted OTP: {otp}")
            else:
                print("OTP not found!")

        except Exception as e:
            print("Error while waiting for OTP email:", e)

        if otp:
            try:
                for i, digit in enumerate(otp, start=1):
                    page2.fill(f"#otp{i}", digit)

                page2.click("input[type='submit']")  # Adjust if needed
                print("Signup process automated successfully!")

            except Exception as e:
                print("Failed to enter OTP.")
                print(f"Error: {e}")
        else:
            print("OTP not found, signup aborted.")

        browser.close()

# Run the function
if __name__ == "__main__":
    get_temp_email_and_otp()