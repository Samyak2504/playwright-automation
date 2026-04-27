from playwright.sync_api import sync_playwright
import time

def run_mobile():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=800)

        #  Mobile
        mobile_ua = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/15.0 Mobile/15E148 Safari/604.1 "
            "TenTimes internal Testing/tentimestesting10t112"
        )

        context = browser.new_context(
            user_agent=mobile_ua,
            viewport={"width": 390, "height": 844}  # mobile size
        )

        page = context.new_page()

        # -------- GOOGLE LOGIN --------
        page.goto("https://accounts.google.com/")
        time.sleep(3)

        page.locator("#identifierId").fill("Samyak@10times.com")
        page.get_by_role("button", name="Next").click()

        page.wait_for_selector("input[type='password']", timeout=15000)

        page.locator("input[type='password']").fill("Samyak@1996")
        page.get_by_role("button", name="Next").click()

        time.sleep(6)
        print(" Google login done")

        # -------- 10TIMES --------
        page2 = context.new_page()
        page2.goto("https://10times.com?olk")

        time.sleep(5)

        print("UA:", page2.evaluate("navigator.userAgent"))
        print("Width:", page2.evaluate("window.innerWidth"))

        # -------- MENU --------
        page2.locator("(//*[local-name()='svg']//*[local-name()='path'])[1]").click()
        time.sleep(2)

        page2.locator("text=Login").click()
        time.sleep(3)

        page2.locator("//div[@data-name='gLogin']").click()
        print("User login")

        time.sleep(10)
        browser.close()


if __name__ == "__main__":
    run_mobile()