from playwright.sync_api import sync_playwright, TimeoutError
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
        page.goto("https://temp-mail.org/en/")
        time.sleep(5)

        # Wait for temp email to load (polling for 30s)
        max_wait_seconds = 30
        temp_email = None

        for i in range(max_wait_seconds):
            try:
                value = page.locator("input#mail").input_value()
                if value and value.strip().lower() != "loading":
                    temp_email = value.strip()
                    print(f"✅ Temporary Email fetched: {temp_email}")
                    break
            except Exception:
                pass
            time.sleep(1)

        if not temp_email:
            print("❌ Temp email input never loaded or remained as 'Loading'")
            page.screenshot(path="temp_email_error.png")
            raise TimeoutError("Could not fetch temp email in time.")

        print(f"Temporary Email: {temp_email}")

        # Open the event registration page
        page2 = context.new_page()
        page2.goto("https://10times.com/event/928626")
        page2.locator('//span[@data-param="going" and normalize-space(text())="Going"]').click()
        page2.get_by_placeholder("Email").click()
        page2.fill("input[name='email1']", temp_email)

        # Handle checkbox
        try:
            checkbox = page2.locator("//*[contains(@class, 'server_check_box') and @role='button']")
            if checkbox.is_visible():
                checkbox.click()
                print("✔ Checkbox clicked.")
            else:
                print("⚠ Checkbox not visible.")
        except Exception as e:
            print(f"⚠ Checkbox not found or error occurred: {e}")

        # Submit the form
        page2.click("input[type='submit']")
        print("➡ Submit button clicked after handling checkbox.")

        # Wait for OTP email
        page.bring_to_front()
        otp = None
        try:
            page.wait_for_selector("text=mail@10times.com", timeout=30000)
            page.locator("text=mail@10times.com").first.click()
            time.sleep(3)

            page.wait_for_selector("div.user-data-subject h4")
            otp_text = page.locator("div.user-data-subject h4").text_content()
            print("OTP text raw:", otp_text)

            otp_match = re.search(r'\b(\d{4,6})\b', otp_text)
            if otp_match:
                otp = otp_match.group(1)
                print(f"Extracted OTP: {otp}")
            else:
                print("OTP not found!")

        except Exception as e:
            print("Error while waiting for OTP email:", e)

        # Continue if OTP was found
        if otp:
            try:
                for i, digit in enumerate(otp, start=1):
                    page2.fill(f"#otp{i}", digit)
                page2.click("input[type='submit']")

                # Fill Full Name
                page2.wait_for_selector('//input[@placeholder="Enter your full name"]', timeout=10000)
                page2.locator('//input[@placeholder="Enter your full name"]').fill("Samyak")

                # Fill Company Name
                page2.locator('//input[@placeholder="Company Name"]').fill("Techno")

                # Fill Designation
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

                # Fill Location
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

                # Fill Mobile Number
                page2.locator('//input[@placeholder="Mobile"]').fill("9029765526")

                # Final submit
                page2.locator('//input[@value="Finish"]').click()
                print("Form submitted successfully.")

                print("✅ Signup process automated successfully!")
            except Exception as e:
                print("❌ Failed to enter OTP or complete signup:", e)
        else:
            print("❌ OTP not found, signup aborted.")

        browser.close()

if __name__ == "__main__":
    get_temp_email_and_otp()
