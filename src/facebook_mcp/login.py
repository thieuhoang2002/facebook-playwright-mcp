import os
from pathlib import Path
from playwright.sync_api import sync_playwright

DEFAULT_PROFILE_DIR = os.environ.get(
    "FB_BROWSER_PROFILE_DIR",
    str(Path.home() / ".facebook_mcp" / "browser_profile")
)

def interactive_login(profile_dir: str = None):
    """Open a visible browser window to authenticate and save session."""
    target_dir = profile_dir or DEFAULT_PROFILE_DIR
    os.makedirs(target_dir, exist_ok=True)

    print("=" * 60)
    print("   FACEBOOK PLAYWRIGHT LOGIN HELPER")
    print("=" * 60)
    print(f"Profile directory: {target_dir}")
    print("\nLaunching browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=target_dir,
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.facebook.com/")

        print("\nPlease log into Facebook in the browser window.")
        print("Press ENTER in this console when your newsfeed is loaded...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nCancelled.")
            browser.close()
            return

        if "login" in page.url:
            print("Warning: Login may not be completed yet.")
        else:
            print("Session saved successfully!")

        browser.close()
        print("Browser closed. Ready for MCP.")

if __name__ == "__main__":
    interactive_login()
