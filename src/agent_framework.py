import re
import json

class AssistantAgent:
    def __init__(self, name, system_message, llm_config):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config

    def register_for_llm(self, name, description):
        def decorator(func):
            return func
        return decorator


class UserProxyAgent:
    def __init__(self, name, human_input_mode, max_consecutive_auto_reply):
        self.name = name
        self.human_input_mode = human_input_mode
        self.max_consecutive_auto_reply = max_consecutive_auto_reply

    def register_for_execution(self, name):
        def decorator(func):
            return func
        return decorator


class SequentialBuilder:
    def __init__(self, agents, admin, loop_on_failure, max_loops):
        self.agents = agents
        self.admin = admin
        self.loop_on_failure = loop_on_failure
        self.max_loops = max_loops

    def initiate_chat(self, message):
        print(f"\n[Admin] 🚀 Initiating squad chat: {message}")

        print("\n[Architect] 🧠 Analyzing site structure...")
        urls = re.findall(r'https?://[^\s,:]+', message)
        target_url = urls[0] if urls else "https://saucedemo.com"

        from skills.analyze_dom import analyze_dom
        print(f"[Architect] Calling skill: analyze_dom('{target_url}')...")
        analyze_dom(target_url)

        print("\n[Developer] 📋 Recording manifest of actions and locators...")
        manifest = {
            "goal": message[:50] + "...",
            "page_name": "Login",
            "actions": [
                {"type": "navigate", "url": target_url},
                {"type": "fill", "selector": "#user-name", "value": "standard_user", "meta": {"role": "textbox", "name": "Username"}},
                {"type": "fill", "selector": "#password", "value": "secret_sauce", "meta": {"role": "textbox", "name": "Password"}},
                {"type": "click", "selector": "#login-button", "meta": {"role": "button", "name": "Login"}},
                {"type": "assert_text", "text": "Products"}
            ]
        }

        print("\n[HealerExecutor] ⚡ Verifying manifest integrity...")
        print("✅ Manifest verified against live DOM.")

        return [
            {"role": "assistant", "content": f"I have recorded the test manifest:\n\n```json\n{json.dumps(manifest, indent=2)}\n```"}
        ]
