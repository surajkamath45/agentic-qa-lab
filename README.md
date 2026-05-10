# Agentic QA Lab: The Self-Healing QA Squad

By mid-2026, the Microsoft Agent Framework (AutoGen 1.0) has stabilized, allowing for production-grade agentic workflows. This repository demonstrates a "Quality Engineer 2.0" approach, moving away from writing scripts and toward orchestrating intelligence.

## 🚀 Overview

This project implements a **Self-Healing QA Squad** that can:
1. Receive a natural language testing goal.
2. Architect a test plan.
3. Write Playwright/TypeScript code.
4. Execute the tests.
5. **Automatically fix itself** if the UI changes (Self-Healing).

## 🤖 The QA Squad

- **The Architect**: Analyzes website URLs and defines the "Test Plan".
- **The Developer**: Writes modern Playwright code (using `getByRole`, etc.).
- **The Healer/Executor**: Runs the code and triggers a fix loop upon failure.

## 📁 Repository Structure

- `.github/workflows/agent-ci.yml`: 2026-style Agent CI.
- `src/agents_config.py`: Persona and LLM settings.
- `src/skills/`: Custom tools for screenshots and DOM analysis.
- `output/`: Healed scripts and agent conversation logs.

## 🛠 Setup

```bash
# Install dependencies
pip install agent-framework playwright
playwright install

# Run the squad
python src/main.py --goal "Test the purchase flow of https://demo-ecommerce.com"
```

## 🧠 Self-Healing Logic

If the Executor returns an `Exit Code 1`, the error stack trace and current DOM state are routed back to the Developer. The Healer agent analyzes the shift (e.g., "Checkout" button became "Proceed to Payment") and adjusts the script in real-time.

---
*Built with ❤️ for the future of Quality Engineering.*
