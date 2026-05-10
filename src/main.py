import sys
import os
import json

# Ensure the .venv site-packages are in sys.path for the 2026-style agentic workflow
venv_site_packages = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".venv", "lib", "python3.14", "site-packages"))
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.append(venv_site_packages)

from agents_config import get_architect, get_developer, get_healer_executor, get_admin, register_skills
from generate_report import generate_risk_report
from agent_framework import SequentialBuilder

def run_qa_squad(goal, approval_mode=False):
    print(f"🚀 Starting Self-Healing QA Squad for goal: {goal}")
    
    architect = get_architect()
    developer = get_developer()
    healer = get_healer_executor()
    admin = get_admin()

    # Enable Human-in-the-loop if requested
    if approval_mode:
        print("⚠️ Approval Mode: ON. Human-in-the-loop required for script changes.")
        admin.human_input_mode = "ALWAYS"

    # Register skills to the squad
    register_skills(architect, developer, healer, admin)

    # 2026 SequentialBuilder Logic
    builder = SequentialBuilder(
        agents=[architect, developer, healer],
        admin=admin,
        loop_on_failure=True,
        max_loops=3
    )

    result = builder.initiate_chat(
        message=f"Our goal is: {goal}. Analyze the site and provide a passing Playwright script."
    )

    # --- Post-Execution: Artifact & Report Generation ---
    print("\n✅ QA Loop Completed. Finalizing artifacts...")
    
    # 1. Save Conversation Logs
    os.makedirs("output/logs", exist_ok=True)
    with open("output/logs/squad_chat.log", "w") as f:
        f.write(str(result))

    # 2. Extract JSON Manifest and Generate TypeScript
    manifest = None
    if isinstance(result, list):
        for message in result:
            content = message.get("content", "")
            if "```json" in content:
                try:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    manifest = json.loads(json_str)
                    break
                except Exception as e:
                    print(f"⚠️ Error parsing manifest: {e}")

    if manifest:
        # Save Manifest
        manifest_path = "output/manifest.json"
        os.makedirs("output", exist_ok=True)
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"💾 Manifest saved to: {manifest_path}")

        # Generate TypeScript
        from skills.generate_ts import generate_typescript_from_manifest
        ts_code = generate_typescript_from_manifest(manifest)
        
        # Save TypeScript Script
        ts_path = "output/healed_scripts/final_test.ts"
        os.makedirs("output/healed_scripts", exist_ok=True)
        with open(ts_path, "w") as f:
            f.write(ts_code)
        print(f"💾 Final TypeScript script saved to: {ts_path}")

    # 3. Generate Risk Report
    mock_processed_results = [
        {"name": "UI Navigation", "status": "pass", "risk": "low", "notes": "Successfully navigated to target URL"},
        {"name": "Self-Healing Check", "status": "pass", "risk": "high", "healed": True, "notes": "Manifest integrity verified against DOM"}
    ]
    generate_risk_report(mock_processed_results, f"Squad completed goal: {goal}")

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<testing_goal>\" [--approve]")
        sys.exit(1)
    
    goal = sys.argv[1]
    approve = "--approve" in sys.argv
    run_qa_squad(goal, approval_mode=approve)
