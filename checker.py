import platform
import subprocess
import json
from datetime import datetime


def get_os():
    """
    Detect the operating system.
    """
    return platform.system()


def check_tool(tool_name, version_command):
    """
    Check if a tool is installed and fetch its version.
    """
    try:
        result = subprocess.check_output(
            version_command,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True
        ).strip().split("\n")[0]

        return {
            "installed": True,
            "version": result
        }

    except Exception:
        return {
            "installed": False,
            "version": None
        }


def generate_report(os_name, results):
    """
    Generate a JSON report of the environment check.
    """
    report = {
        "operating_system": os_name,
        "checked_at": datetime.now().isoformat(),
        "tools": results
    }

    with open("dev_env_report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("\n📄 Environment report saved as dev_env_report.json")


def main():
    print("\n🔍 Developer Environment Checker\n")

    os_name = get_os()
    print(f"🖥️  OS Detected: {os_name}\n")

    tools = {
        "Python": "python --version",
        "Git": "git --version",
        "Docker": "docker --version",
        "Node": "node --version"
    }

    results = {}

    for tool, command in tools.items():
        tool_result = check_tool(tool, command)
        results[tool] = tool_result

        if tool_result["installed"]:
            print(f"✅ {tool} installed ({tool_result['version']})")
        else:
            print(f"❌ {tool} not installed")

    generate_report(os_name, results)


if __name__ == "__main__":
    main()
