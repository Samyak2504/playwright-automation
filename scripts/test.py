from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from urllib.parse import quote
from decimal import Decimal, ROUND_HALF_UP
from zoneinfo import ZoneInfo
import os
import sys
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

# 2 pages per batch -> the IP changes between batches
BATCHES = [
    ["Home page", "Event listing"],
    ["Event detail", "Venue listing"],
    ["Venue details", "Company"],
    ["Profile", "evinterest Thank you page"],
]

DEVICES = ["Desktop", "Mobile"]
CATEGORIES = ["Performance", "Accessibility", "Best Practices", "SEO"]
HEADLESS = os.environ.get("HEADLESS", "fasle").lower() == "true"     # true on GitHub
RETRIES = 2
PAUSE_BETWEEN_URLS = 20      # seconds between two checks
PAUSE_BETWEEN_BATCHES = 60   # seconds after the IP changes

# How the IP changes between batches:
#   "manual" - script pauses; you switch VPN / mobile hotspot, then press Enter (on your Mac)
#   "proxy"  - each batch uses the next proxy from PROXIES (comma separated), e.g.
#              PROXIES="http://user:pass@1.2.3.4:8080,http://user:pass@5.6.7.8:8080"
#   "none"   - no change (used on GitHub, where every batch runs on a new machine)
IP_MODE = os.environ.get("IP_MODE", "manual")
PROXIES = [p.strip() for p in os.environ.get("PROXIES", "").split(",") if p.strip()]

# Run only one batch (1-4). Empty = all batches. GitHub sets this per job.
ONLY_BATCH = os.environ.get("BATCH", "")

# Monday-only guard. Set FORCE_RUN=true to test on another day.
FORCE_RUN = os.environ.get("FORCE_RUN", "true").lower() == "true"
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
                # Warn about the "blocked page" pattern seen in earlier runs
                if (scores["Performance"] == 100 and scores["Best Practices"] == 92
                        and scores["SEO"] == 83):
                    print("   SUSPECT: 100 / 92 / 83 pattern - check this URL manually")
                return scores
            print(f"   attempt {attempt}: only found {list(scores)}")
        except Exception as exc:
            print(f"   attempt {attempt} failed: {str(exc).splitlines()[0]}")
        time.sleep(15)
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
    print(f"  {'Category':<16}" + "".join(f"{'U' + str(i):>7}" for i in range(1, len(urls) + 1))
          + f"{'Avg':>9}")

    category_avgs = []
    for cat in CATEGORIES:
        values = [results[url].get(cat) for url in urls]
        avg = average(values)
        category_avgs.append(avg)
        print(f"  {cat:<16}" + "".join(f"{fmt(v):>7}" for v in values) + f"{fmt(avg):>9}")

    overall = average(category_avgs)
    print(f"  {'Overall':<16}{'':>{7 * len(urls)}}{(fmt(overall) + '%'):>9}")
    return category_avgs, overall


def current_ip(page):
    try:
        return page.request.get("https://api.ipify.org", timeout=15000).text().strip()
    except Exception:
        return "unknown"


def change_ip(batch_no):
    """Returns the proxy setting for this batch (or None)."""
    if IP_MODE == "proxy":
        if not PROXIES:
            sys.exit("IP_MODE=proxy but PROXIES is empty")
        server = PROXIES[(batch_no - 1) % len(PROXIES)]
        print(f" Using proxy #{(batch_no - 1) % len(PROXIES) + 1} for this batch")
        return {"server": server}
    if IP_MODE == "manual" and batch_no > 1:
        input("\n>>> Change your IP now (switch VPN server / mobile hotspot), then press Enter... ")
    return None


def run_batch(p, batch_no, groups):
    print(f"\n######## Batch {batch_no}: {' + '.join(groups)} ########")
    proxy = change_ip(batch_no)
    if batch_no > 1 and IP_MODE != "none":
        print(f" Waiting {PAUSE_BETWEEN_BATCHES}s before starting...")
        time.sleep(PAUSE_BETWEEN_BATCHES)

    launch_args = {"headless": HEADLESS, "slow_mo": 300}
    if proxy:
        launch_args["proxy"] = proxy
    browser = p.firefox.launch(**launch_args)
    page = browser.new_page()
    print(f" Current IP: {current_ip(page)}")

    summary = []
    for group in groups:
        urls = PAGE_GROUPS[group]
        for device in DEVICES:
            results = {}
            for url in urls:
                print(f" Checking [{group} | {device}] {url}")
                results[url] = get_scores(page, url, device)
                time.sleep(PAUSE_BETWEEN_URLS)
            category_avgs, overall = print_group(group, device, urls, results)
            summary.append((group, device, category_avgs, overall))

    browser.close()
    return summary


def run_weekly_report():
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    if now.weekday() != 0 and not FORCE_RUN:
        print(f"Today is {now:%A}. This report runs only on Monday "
              f"(set FORCE_RUN=true to run anyway).")
        return

    monday = now.date() - timedelta(days=now.weekday())
    week_label = f"{monday:%d %b} - {monday + timedelta(days=6):%d %b}"
    print(f"===== 10times PageSpeed report: {week_label} {now.year} =====")

    batches = list(enumerate(BATCHES, 1))
    if ONLY_BATCH:
        batches = [b for b in batches if str(b[0]) == ONLY_BATCH]

    summary = []
    with sync_playwright() as p:
        for batch_no, groups in batches:
            summary += run_batch(p, batch_no, groups)

    print(f"\n===== SUMMARY {week_label} =====")
    print(f"  {'Page':<28}{'Device':<9}{'Perf':>8}{'Access':>8}{'BP':>8}{'SEO':>8}{'Overall':>10}")
    for group, device, avgs, overall in summary:
        print(f"  {group:<28}{device:<9}" + "".join(f"{fmt(a):>8}" for a in avgs)
              + f"{(fmt(overall) + '%'):>10}")

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            title = f"Batch {ONLY_BATCH}" if ONLY_BATCH else "All batches"
            f.write(f"## 10times PageSpeed: {week_label} ({title})\n\n")
            f.write("| Page | Device | Performance | Accessibility | Best Practices | SEO | Overall |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for group, device, avgs, overall in summary:
                f.write(f"| {group} | {device} | " + " | ".join(fmt(a) for a in avgs)
                        + f" | {fmt(overall)}% |\n")


if __name__ == "__main__":
    run_weekly_report()
