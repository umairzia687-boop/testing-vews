import time
import random
from playwright.sync_api import sync_playwright

SITE_URL = "https://www.learnwithroyal.shop/"
REFERRERS = ["https://www.google.com/", "https://www.facebook.com/", "https://t.co/", "https://www.bing.com/"]

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

        try:
            # 1. Home Page
            page.goto(SITE_URL, wait_until="load", timeout=60000)
            print("✅ Home Page Opened.")
            time.sleep(20)
            page.screenshot(path="screenshot_home.png")

            # 2. Ad Close (Try catch for each)
            try:
                page.keyboard.press("Escape") # Key board se close karne ki koshish
                page.mouse.click(10, 10) # Side pe click taake ad band ho jaye
            except: pass

            # 3. Post Opening Fix
            print("📖 Finding Post...")
            # Sirf wahi links jo posts ke ho sakte hain
            links = page.query_selector_all("a")
            internal_links = [l for l in links if l.get_attribute("href") and "learnwithroyal.shop" in l.get_attribute("href") and l.get_attribute("href") != SITE_URL]

            if internal_links:
                target_post = random.choice(internal_links)
                # Scroll to the link first
                target_post.scroll_into_view_if_needed()
                time.sleep(2)
                # Force click added here
                target_post.click(force=True, timeout=10000)
                print("✅ Post Clicked Successfully.")
                time.sleep(10)
                page.screenshot(path="screenshot_post.png")
            else:
                print("⚠️ No internal links found, staying on home page.")

            # 4. Stay for 1 Min+
            for _ in range(5):
                page.mouse.wheel(0, random.randint(300, 600))
                time.sleep(10)

            print("✅ Cycle Complete.")
        except Exception as e:
            print(f"❌ Error occurred: {e}")
        
        browser.close()

if __name__ == "__main__":
    run_bot()
