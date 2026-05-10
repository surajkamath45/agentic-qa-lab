# Agentic QA Lab: The Self-Healing QA Squad

> Powered by the Microsoft Agent Framework (2026) · Playwright · TypeScript · Python 3.14

By mid-2026, the Microsoft Agent Framework has stabilised, enabling production-grade agentic workflows. This repository demonstrates a **Quality Engineer 2.0** approach — moving away from writing scripts and toward **orchestrating intelligence**.

## 🚀 Overview

This project implements a **Self-Healing QA Squad** that can:
1. Receive a **natural language testing goal**.
2. **Analyze** the live DOM of any target URL using Playwright.
3. **Record** a structured JSON manifest of actions, locators, and metadata.
4. **Generate** production-grade Playwright TypeScript code following the **Page Object Model** pattern.
5. **Verify** manifest integrity against the live browser.
6. **Automatically self-heal** if the UI changes — without human intervention.

## 🤖 The QA Squad

| Agent | Role | Responsibility |
|:---|:---|:---|
| **Architect** | Senior QA Architect | Analyzes the site DOM and defines the Test Plan |
| **Developer** | Lead Automation Engineer | Records the JSON manifest of actions and locators |
| **Healer/Executor** | Self-Healing Engine | Verifies the manifest and triggers repair loops on failure |
| **Admin** | Orchestrator | Controls the sequential workflow and governance |

## 📐 Design Patterns

| Pattern | Where Applied | Purpose |
|:---|:---|:---|
| **Page Object Model** | `generate_ts.py` | Generated tests follow POM — a `Page.ts` class + `.spec.ts` test file |
| **Strategy Pattern** | `generate_ts.py` | Swappable locator strategies: `RoleLocatorStrategy`, `SelectorLocatorStrategy` |
| **Builder Pattern** | `generate_ts.py` | `TypeScriptBuilder` accumulates lines via typed methods, no f-string concatenation |
| **Context Manager** | `browser_session.py` | `BrowserSession` shares a single browser instance across skills for efficiency |

## 📁 Repository Structure

```
src/
├── main.py              — Orchestration entry point
├── agents_config.py     — Agent persona and LLM configuration
├── agent_framework.py   — Framework abstraction (mock/real adapter)
├── generate_report.py   — Risk Coverage Dashboard generator
└── skills/
    ├── browser_session.py   — Shared Playwright context manager
    ├── analyze_dom.py       — DOM accessibility tree extraction
    ├── take_screenshot.py   — Visual evidence capture
    ├── execute_playwright.py — Isolated subprocess test runner
    └── generate_ts.py       — Manifest → TypeScript POM generator

output/
├── manifest.json              — Structured action blueprint (JSON)
├── risk_report.md             — Risk Coverage Dashboard
├── healed_scripts/
│   ├── LoginPage.ts           — Generated Page Object class
│   └── login_flow.spec.ts     — Generated Playwright test
└── logs/
    ├── squad_chat.log         — Agent conversation history
    └── screenshot.png         — Visual evidence (on failure)
```

## 🛠 Setup

```bash
# 1. Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install agent-framework playwright
playwright install

# 2. Node.js environment (for TypeScript test execution)
npm install -D @playwright/test
```

## 🚀 Running the Squad

```bash
# Standard autonomous run
python3 src/main.py "Test the login flow on https://saucedemo.com"

# Human-in-the-loop governance mode
python3 src/main.py "Test the checkout flow" --approve

# Execute the generated TypeScript test
npx playwright test output/healed_scripts/ --headed
```

## 📊 Output Artifacts

After each run, the squad generates:
- **`output/manifest.json`** — The AI's structured understanding of the test journey.
- **`output/healed_scripts/{Page}Page.ts`** — Page Object Model class (TypeScript).
- **`output/healed_scripts/{goal}.spec.ts`** — Playwright test spec that imports the POM.
- **`output/risk_report.md`** — Risk Coverage Dashboard ranked by business impact.
- **`output/logs/squad_chat.log`** — Full agent conversation for audit trails.

## 📖 Documentation

See [Documentation.md](./Documentation.md) for the full solution architecture, Mermaid diagrams, design pattern details, and component breakdown.
