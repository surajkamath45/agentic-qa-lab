def generate_typescript_from_manifest(manifest):
    """
    Converts a JSON manifest of test actions into a Playwright TypeScript file.
    """
    ts_code = "import { test, expect } from '@playwright/test';\n\n"
    ts_code += f"test('{manifest.get('goal', 'Autonomous QA Test')}', async ({{ page }}) => {{\n"
    
    for action in manifest.get('actions', []):
        type = action.get('type')
        meta = action.get('meta', {})
        
        if type == 'navigate':
            ts_code += f"    await page.goto('{action['url']}');\n"
        
        elif type == 'fill':
            role = meta.get('role')
            name = meta.get('name')
            value = action.get('value', '')
            if role and name:
                ts_code += f"    await page.getByRole('{role}', {{ name: '{name}' }}).fill('{value}');\n"
            else:
                ts_code += f"    await page.locator('{action['selector']}').fill('{value}');\n"
                
        elif type == 'click':
            role = meta.get('role')
            name = meta.get('name')
            if role and name:
                ts_code += f"    await page.getByRole('{role}', {{ name: '{name}' }}).click();\n"
            else:
                ts_code += f"    await page.locator('{action['selector']}').click();\n"
        
        elif type == 'assert_text':
            ts_code += f"    await expect(page.locator('body')).toContainText('{action['text']}');\n"

    ts_code += "});\n"
    return ts_code
