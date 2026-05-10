import os

# pyrefly: ignore [missing-import]
from agent_framework import AssistantAgent, UserProxyAgent

# Import skill modules
from skills.analyze_dom import analyze_dom
from skills.take_screenshot import take_screenshot
from skills.execute_playwright import execute_playwright

# LLM Configuration (2026 Standard)
llm_config = {
    "model": "gpt-4o-2026-production",  # Hypothesized 2026 model
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.2,
}


def get_architect():
    return AssistantAgent(
        name="Architect",
        system_message="""You are a Senior QA Architect.
        Your task is to analyze a website URL and a testing goal.
        Define a clear, step-by-step Test Plan.
        Focus on high-risk areas and user flows.
        Output the plan in markdown format.""",
        llm_config=llm_config,
    )


def get_developer():
    return AssistantAgent(
        name="Developer",
        system_message="""You are a Lead Automation Engineer.
        Your task is to write Playwright/TypeScript code based on a Test Plan.
        Use modern locators like getByRole, getByText, etc.
        If you receive an error message and HTML snippet, you MUST fix the script to handle the UI shift.
        Output ONLY the code in a triple-backtick block.""",
        llm_config=llm_config,
    )


def get_healer_executor():
    return AssistantAgent(
        name="HealerExecutor",
        system_message="""You are a Self-Healing Execution Engine.
        Your task is to execute the Playwright scripts.
        If a script fails, capture the error stack trace and the current HTML of the page.
        Explain WHY it failed (e.g., 'Selector not found') and suggest the fix to the Developer.
        You have access to the 'take_screenshot' and 'analyze_dom' skills.""",
        llm_config=llm_config,
    )


def get_admin():
    return UserProxyAgent(
        name="Admin",
        human_input_mode="NEVER",  # 2026 focus on autonomy
        max_consecutive_auto_reply=10,
    )


def register_skills(architect, developer, healer, admin):
    """
    Registers the skills to the appropriate agents.
    In 2026, skills are registered for both LLM suggestion and Execution.
    """
    for skill in [analyze_dom, take_screenshot, execute_playwright]:
        healer.register_for_llm(name=skill.__name__, description=skill.__doc__)(skill)
        admin.register_for_execution(name=skill.__name__)(skill)
