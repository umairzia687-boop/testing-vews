import time
import random
from playwright.sync_api import sync_playwright

SITE_URL = "https://www.learnwithroyal.shop/"
REFERRERS = [
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://t.co/",
    "https://www.bing.com/"
]

def run_bot(view_count):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        source = random.choice(REFERRERS)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={"Referer": source}
        )
        
        page = context.new_page()
        print(f"🚀 Visiting from: {source}")

        try:
            # 1. Website Open Karna
            page.goto(SITE_URL, wait_until="networkidle")
            
            # 2. 30-45 Sec Random Delay (Insaan ki tarah stay)
            wait_time = random.randint(30, 45)
            print(f"⏱️ Staying for {wait_time}s...")
            time.sleep(wait_time)

            # 3. Random Scroll
            page.mouse.wheel(0, random.randint(500, 1500))
            time.sleep(5)

            # 4. Random Post/Link Click (Har 4-5 view baad)
            if view_count % random.randint(4, 5) == 0:
                print("📖 Clicking a random internal link...")
                links = page.query_selector_all("a")
                if links:
                    random.choice(links).click()
                    time.sleep(15)

            # 5. Ad Click Logic (1-2% CTR)
            if random.randint(1, 100) <= 2:
                print("🎯 Strategy: Random Ad Click Triggered!")
                page.mouse.click(random.randint(100, 500), random.randint(100, 500))
                time.sleep(35) 

            print("✅ View Cycle Complete.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        browser.close()

if __name__ == "__main__":
    run_bot(random.randint(1, 10))
