import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from src.config import (
    BROWSER_HEADLESS,
    BROWSER_TIMEOUT,
    BROWSER_VIEWPORT_WIDTH,
    BROWSER_VIEWPORT_HEIGHT,
    DOWNLOADS_DIR,
)
from src.utils.logger import get_logger

logger = get_logger("browser_controller")


class BrowserController:
    """Manages Playwright browser automation with comprehensive logging"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    async def initialize(self):
        """Initialize browser and context"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=BROWSER_HEADLESS)
        self.context = await self.browser.new_context(
            viewport={
                "width": BROWSER_VIEWPORT_WIDTH,
                "height": BROWSER_VIEWPORT_HEIGHT,
            }
        )
        self.page = await self.context.new_page()
        self.page.set_default_timeout(BROWSER_TIMEOUT)
        logger.info(f"Browser initialized with session {self.session_id}")

    async def close(self):
        """Close browser and cleanup"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info(f"Browser closed for session {self.session_id}")

    async def goto(self, url: str) -> Dict[str, Any]:
        """Navigate to URL"""
        try:
            await self.page.goto(url, wait_until="networkidle")
            logger.info(f"Navigated to {url}")
            return {
                "status": "success",
                "action": "goto",
                "url": url,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Navigation failed for {url}: {str(e)}")
            return {
                "status": "error",
                "action": "goto",
                "url": url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def click(self, selector: str, retry_count: int = 0) -> Dict[str, Any]:
        """Click element by selector"""
        try:
            await self.page.click(selector)
            logger.info(f"Clicked selector: {selector}")
            return {
                "status": "success",
                "action": "click",
                "selector": selector,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Click failed for {selector}: {str(e)}")
            return {
                "status": "error",
                "action": "click",
                "selector": selector,
                "error": str(e),
                "retry_count": retry_count,
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def fill(self, selector: str, value: str) -> Dict[str, Any]:
        """Fill input field"""
        try:
            await self.page.fill(selector, value)
            logger.info(f"Filled selector {selector} with value (length: {len(value)})")
            return {
                "status": "success",
                "action": "fill",
                "selector": selector,
                "value_length": len(value),
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Fill failed for {selector}: {str(e)}")
            return {
                "status": "error",
                "action": "fill",
                "selector": selector,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def wait_for_selector(
        self, selector: str, timeout: int = 10000
    ) -> Dict[str, Any]:
        """Wait for element to appear"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            logger.info(f"Selector appeared: {selector}")
            return {
                "status": "success",
                "action": "wait_for_selector",
                "selector": selector,
                "timeout": timeout,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Wait for selector failed: {selector}: {str(e)}")
            return {
                "status": "error",
                "action": "wait_for_selector",
                "selector": selector,
                "error": str(e),
                "timeout": timeout,
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def screenshot(self, name: str = None) -> str:
        """Take screenshot and return base64 encoded"""
        try:
            if name is None:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            screenshot_path = Path(DOWNLOADS_DIR) / name
            await self.page.screenshot(path=screenshot_path, full_page=False)

            # Read and encode to base64
            with open(screenshot_path, "rb") as f:
                screenshot_data = base64.b64encode(f.read()).decode("utf-8")

            logger.info(f"Screenshot taken: {name}")
            return screenshot_data
        except Exception as e:
            logger.error(f"Screenshot failed: {str(e)}")
            return None

    async def get_html(self) -> str:
        """Get current page HTML"""
        try:
            html = await self.page.content()
            logger.debug("HTML content retrieved")
            return html
        except Exception as e:
            logger.error(f"Failed to get HTML: {str(e)}")
            return ""

    async def scroll(self, direction: str = "down", amount: int = 3) -> Dict[str, Any]:
        """Scroll page"""
        try:
            if direction.lower() == "down":
                await self.page.evaluate(f"window.scrollBy(0, {amount * 300})")
            elif direction.lower() == "up":
                await self.page.evaluate(f"window.scrollBy(0, {-amount * 300})")
            else:
                return {
                    "status": "error",
                    "action": "scroll",
                    "error": f"Invalid direction: {direction}",
                }

            logger.info(f"Scrolled {direction} by {amount} steps")
            return {
                "status": "success",
                "action": "scroll",
                "direction": direction,
                "amount": amount,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Scroll failed: {str(e)}")
            return {
                "status": "error",
                "action": "scroll",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def download_file(self, trigger_selector: str) -> Dict[str, Any]:
        """Trigger file download by clicking on download button"""
        try:
            async with self.context.expect_download() as download_info:
                await self.page.click(trigger_selector)

            download = await download_info.value
            filename = download.suggested_filename
            filepath = DOWNLOADS_DIR / filename

            await download.save_as(filepath)
            logger.info(f"File downloaded: {filename}")

            return {
                "status": "success",
                "action": "download_file",
                "filename": filename,
                "filepath": str(filepath),
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Download failed for selector {trigger_selector}: {str(e)}")
            return {
                "status": "error",
                "action": "download_file",
                "selector": trigger_selector,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def press_key(self, key: str) -> Dict[str, Any]:
        """Press keyboard key"""
        try:
            await self.page.keyboard.press(key)
            logger.info(f"Pressed key: {key}")
            return {
                "status": "success",
                "action": "press_key",
                "key": key,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Press key failed: {str(e)}")
            return {
                "status": "error",
                "action": "press_key",
                "key": key,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def get_page_state(self) -> Dict[str, Any]:
        """Get current page state including DOM and metadata"""
        try:
            html = await self.get_html()
            title = await self.page.title()
            url = self.page.url

            return {
                "title": title,
                "url": url,
                "html": html,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to get page state: {str(e)}")
            return {"error": str(e)}

    async def execute_action(self, action_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single action from JSON specification"""
        action = action_spec.get("action")
        selector = action_spec.get("selector")
        value = action_spec.get("value")

        if action == "click":
            return await self.click(selector)
        elif action == "fill":
            return await self.fill(selector, value)
        elif action == "goto":
            return await self.goto(value)
        elif action == "wait":
            return await self.wait_for_selector(selector, timeout=10000)
        elif action == "download":
            return await self.download_file(selector)
        elif action == "scroll":
            direction = action_spec.get("direction", "down")
            amount = action_spec.get("amount", 3)
            return await self.scroll(direction, amount)
        elif action == "key":
            return await self.press_key(value)
        elif action == "screenshot":
            screenshot_data = await self.screenshot()
            return {
                "status": "success" if screenshot_data else "error",
                "action": "screenshot",
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            logger.warning(f"Unknown action: {action}")
            return {"status": "error", "error": f"Unknown action: {action}"}
