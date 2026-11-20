import os
from pathlib import Path
from fastmcp import FastMCP
from playwright.sync_api import sync_playwright

mcp = FastMCP("Facebook Personal Agent")

DEFAULT_PROFILE_DIR = os.environ.get(
    "FB_BROWSER_PROFILE_DIR",
    str(Path.home() / ".facebook_mcp" / "browser_profile")
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0.0.0 Safari/537.36"
)

def _get_context(p, headless=True):
    os.makedirs(DEFAULT_PROFILE_DIR, exist_ok=True)
    return p.chromium.launch_persistent_context(
        user_data_dir=DEFAULT_PROFILE_DIR,
        headless=headless,
        viewport={"width": 1280, "height": 800},
        user_agent=USER_AGENT,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )

@mcp.tool()
def check_login_status() -> str:
    """Check if the user is authenticated on Facebook."""
    with sync_playwright() as p:
        context = _get_context(p, headless=True)
        page = context.new_page()
        try:
            page.goto("https://www.facebook.com/", timeout=25000)
            page.wait_for_timeout(3000)

            if "login" in page.url:
                return "Not logged in. Please run `facebook-mcp-login` first."
            return f"Authenticated successfully! Current URL: {page.url}"
        except Exception as e:
            return f"Error checking login: {str(e)}"
        finally:
            context.close()

@mcp.tool()
def read_newsfeed(limit: int = 5) -> str:
    """Read recent posts from your personal Facebook newsfeed."""
    with sync_playwright() as p:
        context = _get_context(p, headless=True)
        page = context.new_page()
        try:
            page.goto("https://www.facebook.com/", timeout=25000)
            page.wait_for_timeout(4000)

            if "login" in page.url:
                return "Not logged in. Please run `facebook-mcp-login` first."

            for _ in range(2):
                page.mouse.wheel(0, 800)
                page.wait_for_timeout(1500)

            articles = page.locator('div[role="feed"] > div, div[role="article"]').all()
            results = []
            count = 0
            for art in articles:
                text = art.inner_text().strip()
                if len(text) > 40:
                    count += 1
                    preview = text[:400] + ("..." if len(text) > 400 else "")
                    results.append(f"Post #{count}:\n{preview}")
                    if count >= limit:
                        break

            if not results:
                return "No posts found on feed."
            return "\n\n---\n\n".join(results)
        except Exception as e:
            return f"Error reading newsfeed: {str(e)}"
        finally:
            context.close()

@mcp.tool()
def post_personal_status(content: str) -> str:
    """Publish a status post to your personal Facebook profile."""
    with sync_playwright() as p:
        context = _get_context(p, headless=True)
        page = context.new_page()
        try:
            page.goto("https://www.facebook.com/", timeout=25000)
            page.wait_for_timeout(3500)

            if "login" in page.url:
                return "Not logged in. Please run `facebook-mcp-login` first."

            trigger = page.locator(
                'div[role="button"]:has-text("What\'s on your mind"), '
                'div[role="button"]:has-text("Bạn đang nghĩ gì")'
            ).first

            if trigger.count() == 0:
                trigger = page.locator('div[data-pagelet="ProfileComposer"] div[role="button"]').first

            if trigger.count() == 0:
                return "Composer button not found."

            trigger.click()
            page.wait_for_timeout(2000)

            editor = page.locator('div[role="dialog"] div[role="textbox"][contenteditable="true"]').first
            if editor.count() == 0:
                return "Status input editor not found."

            editor.click()
            editor.fill(content)
            page.wait_for_timeout(1500)

            post_btn = page.locator(
                'div[role="dialog"] div[aria-label="Post"], '
                'div[role="dialog"] div[aria-label="Đăng"], '
                'div[role="dialog"] div[role="button"]:has-text("Post"), '
                'div[role="dialog"] div[role="button"]:has-text("Đăng")'
            ).first

            if post_btn.count() == 0:
                return "Post button not found."

            post_btn.click()
            page.wait_for_timeout(5000)
            return f"Status posted successfully: {content}"
        except Exception as e:
            return f"Error posting status: {str(e)}"
        finally:
            context.close()

@mcp.tool()
def search_facebook(query: str, category: str = "top") -> str:
    """Search Facebook for people, posts, groups, or pages."""
    valid_categories = ["top", "posts", "people", "groups", "pages"]
    cat = category.lower() if category.lower() in valid_categories else "top"
    search_url = f"https://www.facebook.com/search/{cat}/?q={query}"

    with sync_playwright() as p:
        context = _get_context(p, headless=True)
        page = context.new_page()
        try:
            page.goto(search_url, timeout=25000)
            page.wait_for_timeout(4000)

            if "login" in page.url:
                return "Not logged in. Please run `facebook-mcp-login` first."

            cards = page.locator('div[role="feed"] > div, div[role="main"] div[role="article"]').all()
            items = []
            for i, card in enumerate(cards[:8]):
                txt = card.inner_text().strip()
                if len(txt) > 20:
                    items.append(f"Result #{i+1}:\n{txt[:250]}...")

            if not items:
                return f"No results found for query: {query}"
            return "\n\n---\n\n".join(items)
        except Exception as e:
            return f"Error searching: {str(e)}"
        finally:
            context.close()

@mcp.tool()
def read_page_or_group(url: str) -> str:
    """Navigate to any Facebook URL and extract visible text."""
    if not url.startswith("http"):
        url = "https://" + url

    with sync_playwright() as p:
        context = _get_context(p, headless=True)
        page = context.new_page()
        try:
            page.goto(url, timeout=25000)
            page.wait_for_timeout(4000)

            if "login" in page.url:
                return "Not logged in. Please run `facebook-mcp-login` first."

            title = page.title()
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(1500)

            articles = page.locator('div[role="feed"] > div, div[role="article"]').all()
            posts = []
            for i, art in enumerate(articles[:5]):
                txt = art.inner_text().strip()
                if len(txt) > 30:
                    posts.append(f"Post #{i+1}:\n{txt[:300]}...")

            res = f"Title: {title}\nURL: {url}\n\n"
            if posts:
                res += "\n\n---\n\n".join(posts)
            else:
                main_txt = page.locator('div[role="main"]').inner_text().strip()
                res += main_txt[:1000]
            return res
        except Exception as e:
            return f"Error reading page: {str(e)}"
        finally:
            context.close()

def main():
    mcp.run()

if __name__ == "__main__":
    main()
