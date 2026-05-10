"""
analyze_dom — DOM Intelligence Skill.

Extracts the complete interactive surface of a page using the Playwright
Accessibility Tree. Uses BrowserSession for efficient resource management.
"""
from skills.browser_session import BrowserSession


def analyze_dom(url: str) -> list:
    """
    Extracts key interactive elements and their roles from the DOM.
    Returns a list of element descriptors for the AI Architect to reason about.
    """
    with BrowserSession(url) as page:
        elements = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button, a, input, select')).map(el => ({
                tag: el.tagName,
                text: el.innerText || el.placeholder || el.value || '',
                role: el.getAttribute('role') || 'n/a',
                id: el.id,
                className: el.className
            }));
        }""")
    return elements
