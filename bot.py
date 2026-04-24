import time
import random
import requests
from playwright.sync_api import sync_playwright

SITE_URL = "https://www.learnwithroyal.shop/"
REFERRERS = [
    "https://www.google.com/", "https://www.facebook.com/", 
    "https://t.co/", "https://www.bing.com/", 
    "https://www.linkedin.com/", "https://www.duckduckgo.com/"
]

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=10).text
    except:
        return "Unknown"

def run_view_cycle(page, index):
    source = random.choice(REFERRERS)
    print(f"🚀 [View {index+1}] Starting from: {source}")
    
    # Page Load
    page.goto(SITE_URL, wait_until="domcontentloaded", timeout=60000)
    print(f"✅ [View {index+1}] Home Page Loaded.")
    
    # 20s Wait & Screenshot (Only for the first view as proof)
    time.sleep(20)
    if index == 0:
        page.screenshot(path=f"screenshot_ip_check.png")

    # Ad Close Attempt (Escape Key & Random Click)
    page.keyboard.press("Escape")
    page.mouse.click(random.randint(0, 100), random.randint(0, 100))

    # Randomly Open 1 Internal Post (100% Probability)
    try:
        links = page.query_selector_all("a")
        internal = [l for l in links if l.get_attribute("href") and "learnwithroyal.shop" in l.get_attribute("href") and l.get_attribute("href") != SITE_URL]
        
        if internal:
            target = random.choice(internal)
            print(f"📖 [View {index+1}] Opening Internal Post...")
            target.scroll_into_view_if_needed()
            time.sleep(2)
            target.click(force=True)
            time.sleep(random.randint(30, 40)) # Post Stay Time
            print(f"✅ [View {index+1}] Post Viewed Successfully.")
    except Exception as e:
        print(f"⚠️ [View {index+1}] Post click skipped: {e}")

def run():
    print(f"🌍 SERVER IP: {get_ip()}") # IP show karega har computer ki
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Ek computer 5 baar browser kholega alag session ke liye
        for i in range(5):
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            try:
                run_view_cycle(page, i)
            except Exception as e:
                print(f"❌ Cycle {i} Error: {e}")
            context.close()
            time.sleep(random.randint(2, 5))
        browser.close()

if __name__ == "__main__":
    run()
