import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        response = {
            "command": command,
            "retval": result.returncode,
            "stdout": result.stdout.strip().split("\n"),
            "stderr": result.stderr.strip().split("\n"),
            "status": "completed",
            "passFail": "PASS" if result.returncode == 0 else "FAIL",
        }
        return response
    except Exception as e:
        return {
            "command": command,
            "retval": -1,
            "stdout": [],
            "stderr": [f"Error: {str(e)}"],
            "status": "failed",
            "passFail": "FAIL",
        }

