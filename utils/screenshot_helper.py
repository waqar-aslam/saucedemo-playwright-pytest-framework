from pathlib import Path
from playwright.sync_api import Page


class ScreenshotHelper:
    """Captures screenshots for failed tests."""

    ROOT_DIR = Path(__file__).resolve().parent.parent
    SCREENSHOT_DIR = ROOT_DIR / "screenshots"

    @classmethod
    def capture(cls, page: Page, test_name: str) -> Path:
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(
            c if c.isalnum() or c in "._-" else "_"
            for c in test_name
        )

        screenshot_path = cls.SCREENSHOT_DIR / f"{safe_name}.png"

        page.screenshot(path=str(screenshot_path), full_page=True)
        return screenshot_path
