import subprocess
import os
import tempfile

def execute_playwright(code: str):
    """
    Executes a Playwright script and returns the result.
    The code should be a full Python script.
    """
    # Ensure code is wrapped in necessary imports if not present
    if "from playwright" not in code:
        code = "from playwright.sync_api import sync_playwright\n" + code

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as f:
        f.write(code)
        temp_path = f.name

    try:
        import sys
        
        # Ensure the subprocess has access to the same site-packages (Playwright)
        env = os.environ.copy()
        current_path = os.pathsep.join(sys.path)
        env["PYTHONPATH"] = current_path
        
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        output = result.stdout
        error = result.stderr
        
        if result.returncode == 0:
            return f"SUCCESS\nOutput: {output}"
        else:
            return f"FAILURE\nExit Code: {result.returncode}\nError: {error}"
            
    except Exception as e:
        return f"ERROR during execution: {str(e)}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
