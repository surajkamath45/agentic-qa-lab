from playwright.sync_api import sync_playwright

def analyze_dom(url):
    """
    Extracts key interactive elements and their roles from the DOM.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        # 2026-style: Focus on Accessibility Tree / getByRole targets
        elements = page.evaluate('''() => {
            return Array.from(document.querySelectorAll('button, a, input, select')).map(el => ({
                tag: el.tagName,
                text: el.innerText || el.placeholder || el.value,
                role: el.getAttribute('role') || 'n/a',
                id: el.id,
                className: el.className
            }));
        }''')
        browser.close()
    return elements
