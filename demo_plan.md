# 🎥 Demo Plan: The "Showstopper" Video

This document outlines the script and visual cues for the 2-minute demo video.

## Video Script

| Time | Scene | Dialogue/Narration |
| :--- | :--- | :--- |
| **0:00 - 0:20** | **The Setup** | "Welcome to Quality Engineering 2.0. Instead of writing scripts, I orchestrate a squad of agents. Watch as I tell the squad to test our e-commerce site." |
| **0:20 - 0:50** | **The Brains** | "The Architect defines the plan, and the Developer writes the Playwright code in real-time. Notice how they communicate in the logs." |
| **0:50 - 1:20** | **The Magic** | "Now, I'll break the site. I'm changing the 'Checkout' button to 'Proceed to Payment'. The test fails, but the Healer agent detects the shift and automatically fixes the code." |
| **1:20 - 2:00** | **The Result** | "The test passes on the second try. This isn't just automation; it's an autonomous, self-healing QA pipeline running in GitHub Actions." |

## Key Visuals to Capture
1.  **Terminal View**: Running `python src/main.py "Test purchase flow"`.
2.  **Agent Logs**: The conversation between Architect, Developer, and Healer.
3.  **The "Healing" Log**: `[Healer] I detected a UI shift. Adjusting selector from 'Checkout' to 'Proceed to Payment'...`
4.  **GitHub Actions**: The green checkmark on a commit that was automatically "healed".

---
*Created for the Agentic QA Portfolio.*
