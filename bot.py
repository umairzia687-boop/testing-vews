import time
import random
import os
from playwright.sync_api import sync_playwright

SITE_URL = "https://www.learnwithroyal.shop/"
REFERRERS = [
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://t.co/",
    "https://www.bing.com/"
]

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        source = random.choice(REFERRERS)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={"Referer": source}
        )
        
        page = context.new_page()
        print(f"🌐 Target Site: {SITE_URL}")
        print(f"🚀 Traffic Source: {source}")

        try:
            # 1. Home Page Open Karein
            page.goto(SITE_URL, wait_until="networkidle", timeout=60000)
            print("✅ Home Page Opened.")
            
            # 20 Seconds Wait
            print("⏱️ Waiting 20s on Home Page...")
            time.sleep(20)
            
            # Screenshot 1: Home Page
            page.screenshot(path="screenshot_home.png")
            print("📸 Home Page Screenshot Taken.")

            # 2. Ad Close Logic
            ad_close_selectors = ["text=Close", "text=X", "[aria-label='Close']", ".close-button"]
            for selector in ad_close_selectors:
                try:
                    if page.is_visible(selector):
                        page.click(selector)
                        print(f"✅ Ad closed: {selector}")
                except: continue

            # 3. Random 1-2 Posts Open Karein
            posts_to_open = random.randint(1, 2)
            for i in range(posts_to_open):
                links = page.query_selector_all("a[href*='learnwithroyal.shop']")
                internal_links = [l for l in links if l.get_attribute("href") != SITE_URL]
                
                if internal_links:
                    target_post = random.choice(internal_links)
                    print(f"📖 Opening Post {i+1}...")
                    target_post.click()
                    time.sleep(10) # Post load hone ka wait
                    
                    # Screenshot 2: Post Page (Sirf pehli post ka)
                    if i == 0:
                        page.screenshot(path="screenshot_post.png")
                        print("📸 Post Page Screenshot Taken.")
                    
                    # Scrolling and Staying
                    for _ in range(3):
                        page.mouse.wheel(0, random.randint(400, 700))
                        time.sleep(random.randint(5, 10))

            # 4. Total Stay Time (Ensuring 1 Min+)
            final_wait = random.randint(20, 30)
            print(f"⏱️ Final stay for {final_wait}s...")
            time.sleep(final_wait)

            print("✅ All tasks completed successfully.")
        except Exception as e:
            print(f"❌ Error occurred: {e}")
        
        browser.close()

if __name__ == "__main__":
    run_bot()
