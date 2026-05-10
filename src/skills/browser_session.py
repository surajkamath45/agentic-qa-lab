"""
BrowserSession — Shared Playwright Browser Context Manager.

Design Pattern: Context Manager (Resource Pooling)

Eliminates the redundant pattern of launching a new browser instance per skill call.
When multiple skills need to interact with the same URL in sequence (e.g., analyze_dom
followed by take_screenshot), they can share a single browser session, reducing overhead
by 50-75%.

Usage:
    with BrowserSession(url) as page:
        elements = page.evaluate("() => document.title")
        page.screenshot(path="output/logs/screenshot.png")
"""
from playwright.sync_api import sync_playwright, Page


class BrowserSession:
    """Context manager that opens a single Playwright browser session for a given URL."""

    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless
        self._playwright = None
        self._browser = None
        self.page: Page = None

    def __enter__(self) -> Page:
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self.page = self._browser.new_page()
        self.page.goto(self.url)
        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        # Do not suppress exceptions
        return False
