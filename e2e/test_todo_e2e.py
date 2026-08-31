import os
import subprocess

import pytest
import requests
from playwright.sync_api import Page, expect, sync_playwright

GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://localhost:8000")
APP_URL = os.environ.get("APP_URL", "http://localhost:5173")
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))


def _wait_http(url: str, timeout_s: int = 60) -> None:
    for _ in range(timeout_s):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass
        import time

        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for {url}")


class TestTodoAppE2E:
    """End-to-end tests against the Docker Compose Graftcode stack."""

    @pytest.fixture(scope="session", autouse=True)
    def require_stack(self):
        _wait_http(f"{GATEWAY_URL}/npm")
        _wait_http(APP_URL)

    @pytest.fixture(scope="session")
    def browser(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            yield browser
            browser.close()

    @pytest.fixture(scope="session")
    def browser_context(self, browser):
        context = browser.new_context(viewport={"width": 1280, "height": 720}, ignore_https_errors=True)
        yield context
        context.close()

    @pytest.fixture
    def page(self, browser_context):
        page = browser_context.new_page()
        page.set_default_timeout(10000)
        page.set_default_navigation_timeout(10000)
        yield page
        page.close()

    @pytest.fixture(autouse=True)
    def cleanup_todos(self):
        subprocess.run(
            ["node", "scripts/clear-todos.mjs"],
            cwd=FRONTEND_DIR,
            check=False,
            env={**os.environ, "GRAFT_HOST": "ws://localhost:8000/ws"},
        )
        yield

    def test_app_title(self, page: Page):
        page.goto(APP_URL)
        expect(page.locator("h1")).to_contain_text("Todo List App")

    def test_empty_state(self, page: Page):
        page.goto(APP_URL)
        expect(page.locator("text=No todos yet")).to_be_visible()

    def test_create_todo(self, page: Page):
        page.goto(APP_URL)
        page.fill('[data-testid="todo-title-input"]', "Buy groceries")
        page.fill('[data-testid="todo-description-input"]', "Milk, bread, eggs")
        page.click('[data-testid="create-todo-btn"]')
        expect(page.locator('[data-testid^="todo-"]').first).to_be_visible()
        expect(page.get_by_text("Buy groceries")).to_be_visible()
        expect(page.get_by_text("Milk, bread, eggs")).to_be_visible()

    def test_toggle_todo_completion(self, page: Page):
        page.goto(APP_URL)
        page.fill('[data-testid="todo-title-input"]', "Complete me")
        page.click('[data-testid="create-todo-btn"]')
        row = page.locator('[data-testid^="todo-"]').first
        expect(row).to_be_visible()
        checkbox = row.locator('input[type="checkbox"]')
        expect(checkbox).not_to_be_checked()
        checkbox.click()
        expect(checkbox).to_be_checked()
        checkbox.click()
        expect(checkbox).not_to_be_checked()

    def test_delete_todo(self, page: Page):
        page.goto(APP_URL)
        page.fill('[data-testid="todo-title-input"]', "Delete me")
        page.click('[data-testid="create-todo-btn"]')
        row = page.locator('[data-testid^="todo-"]').first
        expect(row).to_be_visible()
        row.get_by_label("Delete").click()
        expect(page.locator("text=No todos yet")).to_be_visible()
