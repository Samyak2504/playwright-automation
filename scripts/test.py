from playwright.sync_api import sync_playwright
from datetime import date, timedelta
from urllib.parse import quote
from decimal import Decimal, ROUND_HALF_UP
import os
import time

# ---------------- Settings ----------------
PAGE_GROUPS = {
    "Home page": [
        "https://10times.com/",
    ],
    "Event listing": [
        "https://10times.com/usa/education-training",
        "https://10times.com/unitedkingdom/medical-pharma",
        "https://10times.com/germany/engineering",
        "https://10times.com/usa/social",
    ],
    "Event detail": [
        "https://10times.com/himtex",
        "https://10times.com/e1k3-k0pd-0fr4",
        "https://10times.com/e1k1-p2dr-4s1z",
        "https://10times.com/hongkong-baby-productsfair",
    ],
    "Venue listing": [
        "https://10times.com/venues/usa",
        "https://10times.com/venues/india",
        "https://10times.com/venues/canada",
        "https://10times.com/venues/unitedkingdom",
    ],
    "Venue details": [
        "https://10times.com/venues/excel-exhibition-centre",
        "https://10times.com/venues/melbourne-convention-and-exhibition-centre",
        "https://10times.com/venues/pragati-maidan",
        "https://10times.com/venues/china-import-export-fair-pazhou-complex",
    ],
    "Company": [
        "https://10times.com/company/bmc-training",
        "https://10times.com/company/national-business-institute",
        "https://10times.com/company/vdi-association-of-german-engineers",
        "https://10times.com/company/oregon-society-certified-public-accountants",
    ],
    "Profile": [
        "https://10times.com/profile/samir-shah-28070616",
        "https://10times.com/profile/haider-shaikh-68037252",
        "https://10times.com/profile/vikram-vasant-gade-18073599",
        "https://10times.com/profile/traket-india-67232843",
    ],
    "evinterest Thank you page": [
        "https://10times.com/evinterest/JcTtBmwE1Ipw1WdHVWekYQb1NB-ZXI85JtD0q-f4Pjo=",
        "https://10times.com/evinterest/KPI6UvxMIonqgIU5reBprLy1h_6HRUWdBybtKtfS5y4=",
        "https://10times.com/evinterest/FIysuu6X295MCKd0vXgbM6vpS5zDSKBRkwVZ9sgQURo=",
        "https://10times.com/evinterest/bQ4dqVuOlJVeu91ana-jct8fWvQLl0sBN7Nltn3B5nU=",
    ],
}
DEVICES = ["Desktop", "Mobile"]
CATEGORIES = ["Performance", "Accessibility", "Best Practices", "SEO"]
HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"   # true on GitHub
RETRIES = 2
# ------------------------------------------


def read_visible_scores(page):
    """Reads the 4 score circles of the tab that is currently shown."""
    page.locator(".lh-gauge__percentage:visible").first.wait_for(timeout=180000)
    time.sleep(3)
    scores = {}
    gauges = page.locator(".lh-gauge__wrapper:visible")
    for i in range(gauges.count()):
        gauge = gauges.nth(i)
        if gauge.locator(".lh-gauge__label").count() == 0:
            continue
        name = gauge.locator(".lh-gauge__label").first.inner_text().strip()
        value = gauge.locator(".lh-gauge__percentage").first.inner_text().strip()
        if name in CATEGORIES and name not in scores:
            scores[name] = int(value) if value.isdigit() else None
    return scores


def get_scores(page, url, device):
    report_url = (f"https://pagespeed.web.dev/report?url={quote(url, safe='')}"
                  f"&form_factor={device.lower()}")
    for attempt in range(1, RETRIES + 1):
        try:
            page.goto(report_url, timeout=60000)
            scores = read_visible_scores(page)
            if len(scores) == 4:
                return scores
            print(f"   attempt {attempt}: only found {list(scores)}")
        except Exception as exc:
            print(f"   attempt {attempt} failed: {str(exc).splitlines()[0]}")
        time.sleep(10)
    return {}


def fmt(value):
    if value is None:
        return "ERR"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:g}"


def average(values):
    """Average rounded to 2 decimals the same way Excel does (83.125 -> 83.13)."""
    nums = [v for v in values if v is not None]
    if not nums:
        return None
    avg = Decimal(sum(nums)) / Decimal(len(nums))
    return float(avg.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def print_group(group, device, urls, results):
    print(f"\n{group}    {device}")
    for i, url in enumerate(urls, 1):
        print(f"  U{i}: {url}")

    header = f"  {'Category':<16}" + "".join(f"{'U' + str(i):>7}" for i in range(1, len(urls) + 1)) + f"{'Avg':>9}"
    print(header)

    category_avgs = []
    for cat in CATEGORIES:
        values = [results[url].get(cat) for url in urls]
        avg = average(values)
        category_avgs.append(avg)
        row = f"  {cat:<16}" + "".join(f"{fmt(v):>7}" for v in values) + f"{fmt(avg):>9}"
        print(row)

    overall = average(category_avgs)
    print(f"  {'Overall':<16}{'':>{7 * len(urls)}}{(fmt(overall) + '%'):>9}")
    return category_avgs, overall


def run_weekly_report():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_label = f"{monday:%d %b} - {monday + timedelta(days=6):%d %b}"
    print(f"===== 10times PageSpeed report: {week_label} {today.year} =====")

    summary = []
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=HEADLESS, slow_mo=300)
        page = browser.new_page()

        for group, urls in PAGE_GROUPS.items():
            for device in DEVICES:
                results = {}
                for url in urls:
                    print(f" Checking [{group} | {device}] {url}")
                    results[url] = get_scores(page, url, device)
                category_avgs, overall = print_group(group, device, urls, results)
                summary.append((group, device, category_avgs, overall))

        browser.close()

    # Final overview of all groups
    print(f"\n===== SUMMARY {week_label} =====")
    print(f"  {'Page':<28}{'Device':<9}{'Perf':>8}{'Access':>8}{'BP':>8}{'SEO':>8}{'Overall':>10}")
    for group, device, avgs, overall in summary:
        print(f"  {group:<28}{device:<9}" + "".join(f"{fmt(a):>8}" for a in avgs)
              + f"{(fmt(overall) + '%'):>10}")

    # Also show the summary on the GitHub Actions run page
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(f"## 10times PageSpeed: {week_label}\n\n")
            f.write("| Page | Device | Performance | Accessibility | Best Practices | SEO | Overall |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for group, device, avgs, overall in summary:
                f.write(f"| {group} | {device} | " + " | ".join(fmt(a) for a in avgs)
                        + f" | {fmt(overall)}% |\n")


if __name__ == "__main__":
    run_weekly_report()
