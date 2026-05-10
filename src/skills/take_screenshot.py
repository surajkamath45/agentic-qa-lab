from playwright.sync_api import sync_playwright

def take_screenshot(url, output_path="output/logs/screenshot.png"):
    """
    Captures a screenshot of the given URL.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=output_path)
        browser.close()
    return f"Screenshot saved to {output_path}"
