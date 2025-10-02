from playwright.sync_api import sync_playwright
import re
import time

def get_temp_email_and_otp():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=1000)

        custom_user_agent = "TenTimes internal Testing/tentimestesting10t112"

        context = browser.new_context(
            user_agent=custom_user_agent,
            extra_http_headers={"User-Agent": custom_user_agent}
        )

        # Open tempmailo and get email
        page = context.new_page()
        page.goto("https://tempmailo.com")
        page.wait_for_selector("input#i-email", timeout=10000)
        temp_email = page.locator("input#i-email").input_value()
        print(f"Temporary Email: {temp_email}")

        # Open event page and submit email
        page2 = context.new_page()
        page2.goto("https://10times.com/event/928626")
        page2.wait_for_load_state("networkidle")

        # Click "Going" button
        page2.locator('//span[@data-param="going" and normalize-space(text())="Going"]').click()

        # Fill email
        page2.get_by_placeholder("Email").click()
        page2.fill("input[name='email1']", temp_email)

        # Optional: click checkbox if present
        checkbox_locator = page2.locator("//svg[contains(@class, 'server_check_box')]")
        if checkbox_locator.count() > 0:
            try:
                checkbox_locator.first.wait_for(state="visible", timeout=5000)
                checkbox_locator.first.scroll_into_view_if_needed()
                checkbox_locator.first.click()
                print("Checkbox clicked.")
            except Exception as e:
                print("Checkbox was found but not clickable:", e)
        else:
            print("Checkbox not found — continuing without clicking.")

        # Submit email to receive OTP
        page2.click("input[type='submit']")

        # Switch back to email page and wait for OTP
        page.bring_to_front()
        otp = None
        start_time = time.time()
        max_wait = 60  # seconds

        try:
            while time.time() - start_time < max_wait:
                emails = page.locator("div.mails div.mail")
                if emails.count() > 0:
                    emails.first.click()
                    time.sleep(2)

                    email_body = page.locator("div.mail-item-sub").text_content()
                    print("Email Content:", email_body)

                    otp_match = re.search(r'\b(\d{4,8})\b', email_body)
                    if otp_match:
                        otp = otp_match.group(1)
                        print(f"Extracted OTP: {otp}")
                        break
                time.sleep(2)

            if not otp:
                print("OTP not found. Signup aborted.")
                browser.close()
                return

        except Exception as e:
            print("Error while waiting for OTP email:", e)
            browser.close()
            return

        # Fill OTP and complete form
        try:
            page2.bring_to_front()
            for i, digit in enumerate(otp, start=1):
                page2.fill(f"#otp{i}", digit)

            page2.click("input[type='submit']")
            print("OTP submitted, waiting for name field...")

            # Full Name
            page2.wait_for_selector('//input[@placeholder="Enter your full name"]', timeout=10000)
            page2.locator('//input[@placeholder="Enter your full name"]').fill("Samyak")

            # Company Name
            page2.locator('//input[@placeholder="Company Name"]').fill("Techno")

            # Designation
            try:
                designation_input = page2.locator("input#GautocompleteDesignation")
                designation_input.scroll_into_view_if_needed()
                designation_input.click(force=True)
                page2.wait_for_timeout(500)

                designation_input.type("Manager", delay=100)
                page2.wait_for_timeout(1000)

                dropdown_item = page2.locator("ul.typeaheadmap >> li.dropdown-item", has_text="Manager Admin")
                if dropdown_item.count() > 0:
                    dropdown_item.first.click()
                    print("Designation selected: Manager Admin")
                else:
                    page2.keyboard.press("ArrowDown")
                    page2.wait_for_timeout(500)
                    page2.keyboard.press("Enter")
                    print("Designation selected with fallback")

            except Exception as e:
                print("Error handling Designation input:", e)

            # Location
            try:
                location_input = page2.locator('//input[@placeholder="Your location"]')
                location_input.scroll_into_view_if_needed()
                location_input.click(force=True)
                location_input.fill("")
                location_input.type("Noida", delay=100)
                page2.wait_for_timeout(1500)

                location_dropdown_item = page2.locator(
                    '//li[contains(@class, "dropdown-item") and contains(@data-value, "Noida")]'
                )

                if location_dropdown_item.count() > 0:
                    location_dropdown_item.first.click()
                    print("Location selected: Noida")
                else:
                    print("Dropdown item not found, trying fallback")
                    page2.keyboard.press("ArrowDown")
                    page2.wait_for_timeout(500)
                    page2.keyboard.press("Enter")

                location_input.evaluate("el => el.blur()")
                page2.wait_for_timeout(1000)

            except Exception as e:
                print("Error while selecting location:", e)

            # Mobile
            page2.locator('//input[@placeholder="Mobile"]').fill("9529765526")

            # Submit final form
            page2.locator('//input[@value="Finish"]').click()
            print("Form submitted successfully.")

        except Exception as e:
            print("Error after OTP:", e)

        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()
