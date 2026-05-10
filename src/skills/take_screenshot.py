"""
take_screenshot — Visual Evidence Skill.

Captures a full-page screenshot for audit trails and failure diagnostics.
Uses BrowserSession for efficient resource management.
"""
import os

from skills.browser_session import BrowserSession


def take_screenshot(url: str, output_path: str = "output/logs/screenshot.png") -> str:
    """
    Captures a screenshot of the given URL and saves it to output_path.
    Returns the path to the saved screenshot.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with BrowserSession(url) as page:
        page.screenshot(path=output_path)
    return f"Screenshot saved to {output_path}"
