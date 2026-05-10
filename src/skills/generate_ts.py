"""
generate_ts — Manifest-to-TypeScript Code Generator.

Design Patterns Applied:
  1. Strategy Pattern  — LocatorStrategy ABC with RoleLocatorStrategy and
                         SelectorLocatorStrategy implementations. New locator
                         types (e.g. getByTestId) can be added by creating a
                         new strategy without touching the generator logic.
  2. Builder Pattern   — TypeScriptBuilder accumulates lines via typed methods
                         and renders the final source string only on .build().
                         Eliminates f-string concatenation spaghetti.
  3. Page Object Model — Generates two files per test suite:
                           - {PageName}Page.ts  (Page Object class)
                           - {spec_name}.spec.ts (Test file that imports the POM)
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Strategy Pattern — Locator Resolution
# ---------------------------------------------------------------------------

class LocatorStrategy(ABC):
    """Abstract strategy for resolving a manifest action to a TypeScript locator."""

    @abstractmethod
    def can_handle(self, action: dict) -> bool:
        """Return True if this strategy can produce a locator for the given action."""

    @abstractmethod
    def locator_expression(self, action: dict) -> str:
        """Return the TypeScript locator expression (without await or interaction)."""


class RoleLocatorStrategy(LocatorStrategy):
    """Preferred strategy: uses getByRole when role + name metadata is available."""

    def can_handle(self, action: dict) -> bool:
        meta = action.get("meta", {})
        return bool(meta.get("role") and meta.get("name"))

    def locator_expression(self, action: dict) -> str:
        meta = action["meta"]
        return f"page.getByRole('{meta['role']}', {{ name: '{meta['name']}' }})"


class SelectorLocatorStrategy(LocatorStrategy):
    """Fallback strategy: uses CSS/ID selector when role metadata is absent."""

    def can_handle(self, action: dict) -> bool:
        return bool(action.get("selector"))

    def locator_expression(self, action: dict) -> str:
        return f"page.locator('{action['selector']}')"


# Ordered registry — first matching strategy wins (Role > Selector)
_LOCATOR_STRATEGIES: list[LocatorStrategy] = [
    RoleLocatorStrategy(),
    SelectorLocatorStrategy(),
]


def _resolve_locator(action: dict) -> str:
    for strategy in _LOCATOR_STRATEGIES:
        if strategy.can_handle(action):
            return strategy.locator_expression(action)
    raise ValueError(f"No locator strategy found for action: {action}")


# ---------------------------------------------------------------------------
# Builder Pattern — TypeScript Source Builder
# ---------------------------------------------------------------------------

@dataclass
class TypeScriptBuilder:
    """
    Accumulates TypeScript source lines and renders on .build().
    Provides typed methods that map 1-to-1 with Playwright API calls.
    """
    _lines: list[str] = field(default_factory=list)
    _indent: int = 0

    def _add(self, line: str = "") -> TypeScriptBuilder:
        prefix = "  " * self._indent
        self._lines.append(f"{prefix}{line}" if line else "")
        return self

    def blank(self) -> TypeScriptBuilder:
        return self._add()

    def raw(self, line: str) -> TypeScriptBuilder:
        return self._add(line)

    def import_stmt(self, names: str, source: str) -> TypeScriptBuilder:
        return self._add(f"import {{ {names} }} from '{source}';")

    def open_class(self, class_name: str) -> TypeScriptBuilder:
        self._add(f"export class {class_name} {{")
        self._indent += 1
        return self

    def constructor(self, param: str, param_type: str) -> TypeScriptBuilder:
        self._add(f"constructor(private readonly {param}: {param_type}) {{}}")
        return self

    def open_method(self, name: str, return_type: str = "Promise<void>") -> TypeScriptBuilder:
        self._add(f"async {name}(): {return_type} {{")
        self._indent += 1
        return self

    def close_block(self) -> TypeScriptBuilder:
        self._indent -= 1
        return self._add("}")

    def goto(self, url: str) -> TypeScriptBuilder:
        return self._add(f"await this.page.goto('{url}');")

    def fill(self, locator: str, value: str) -> TypeScriptBuilder:
        # Replace 'page.' with 'this.page.' for POM context
        loc = locator.replace("page.", "this.page.")
        return self._add(f"await {loc}.fill('{value}');")

    def click(self, locator: str) -> TypeScriptBuilder:
        loc = locator.replace("page.", "this.page.")
        return self._add(f"await {loc}.click();")

    def expect_text(self, text: str, locator: str = "this.page.locator('body')") -> TypeScriptBuilder:
        return self._add(f"await expect({locator}).toContainText('{text}');")

    def build(self) -> str:
        return "\n".join(self._lines) + "\n"


# ---------------------------------------------------------------------------
# Page Object Model Generator
# ---------------------------------------------------------------------------

def _sanitise_title(raw: str) -> str:
    """Remove characters that would break a TypeScript string literal."""
    return re.sub(r"['\"]", "", raw).strip()


def _to_class_name(page_name: str) -> str:
    """Convert a page name like 'login' to 'LoginPage'."""
    return page_name.strip().title().replace(" ", "") + "Page"


def _to_spec_name(goal: str) -> str:
    """Convert a goal string to a kebab-case spec file name."""
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", goal[:40]).strip()
    return re.sub(r"\s+", "_", cleaned).lower()


def generate_page_object(manifest: dict) -> tuple[str, str, str, str]:
    """
    Generates a Page Object class and a matching spec file from a manifest.

    Returns:
        (page_object_code, spec_code, page_filename, spec_filename)
    """
    goal = manifest.get("goal", "Autonomous QA Test")
    page_name = manifest.get("page_name", "Target")
    actions = manifest.get("actions", [])

    class_name = _to_class_name(page_name)
    spec_name = _to_spec_name(goal)
    page_filename = f"{class_name}.ts"
    spec_filename = f"{spec_name}.spec.ts"
    sanitised_goal = _sanitise_title(goal)

    # --- Page Object File ---
    po_builder = TypeScriptBuilder()
    (
        po_builder
        .import_stmt("Page, expect", "@playwright/test")
        .blank()
        .raw(f"/**")
        .raw(f" * {class_name} — Auto-generated Page Object")
        .raw(f" * Goal: {sanitised_goal}")
        .raw(f" * Generated by Agentic QA Lab v1.0")
        .raw(f" */")
        .open_class(class_name)
        .constructor("page", "Page")
        .blank()
    )

    # Group actions into logical POM methods
    # Navigations and interactions are collected into a single performActions method
    po_builder.open_method("performActions")
    for action in actions:
        action_type = action.get("type")
        if action_type == "navigate":
            po_builder.goto(action["url"])
        elif action_type == "fill":
            locator = _resolve_locator(action)
            po_builder.fill(locator, action.get("value", ""))
        elif action_type == "click":
            locator = _resolve_locator(action)
            po_builder.click(locator)
        elif action_type == "assert_text":
            po_builder.expect_text(action["text"])
    po_builder.close_block()  # close performActions

    po_builder.close_block()  # close class

    # --- Spec File ---
    spec_builder = TypeScriptBuilder()
    (
        spec_builder
        .import_stmt("test, expect", "@playwright/test")
        .import_stmt(class_name, f"./{class_name}")
        .blank()
        .raw(f"test('{sanitised_goal}', async ({{ page }}) => {{")
    )
    spec_builder._indent = 1
    spec_builder.raw(f"const {page_name.lower()}Page = new {class_name}(page);")
    spec_builder.raw(f"await {page_name.lower()}Page.performActions();")
    spec_builder._indent = 0
    spec_builder.raw("});")

    return po_builder.build(), spec_builder.build(), page_filename, spec_filename


# ---------------------------------------------------------------------------
# Public API — backwards-compatible entry point
# ---------------------------------------------------------------------------

def generate_typescript_from_manifest(manifest: dict) -> tuple[str, str, str, str]:
    """
    Converts a JSON manifest of test actions into Playwright TypeScript using
    the Page Object Model pattern.

    Returns:
        (page_object_code, spec_code, page_filename, spec_filename)
    """
    return generate_page_object(manifest)
