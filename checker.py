import platform
import subprocess
import json
import argparse
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Check developer environment setup"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Do not generate JSON report"
    )

    parser.add_argument(
        "--only",
        type=str,
        help="Check only a specific tool (e.g. Python, Git)"
    )

    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List supported tools and exit"
    )

    return parser.parse_args()




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

TOOLS = {
    "Python": "python --version",
    "Git": "git --version",
    "Docker": "docker --version",
    "Node": "node --version"
}



def main():
    args = parse_arguments()

    print("\n🔍 Developer Environment Checker\n")

    if args.list_tools:
        print("🧰 Supported tools:")
        for tool in TOOLS.keys():
            print(f"- {tool}")
        return

    os_name = get_os()
    print(f"🖥️  OS Detected: {os_name}\n")

    tools_to_check = TOOLS

    if args.only:
        tool_name = args.only.capitalize()
        if tool_name not in TOOLS:
            print(f"❌ Tool '{args.only}' is not supported.")
            return
        tools_to_check = {tool_name: TOOLS[tool_name]}

    results = {}

    for tool, command in tools_to_check.items():
        tool_result = check_tool(tool, command)
        results[tool] = tool_result

        if tool_result["installed"]:
            print(f"✅ {tool} installed ({tool_result['version']})")
        else:
            print(f"❌ {tool} not installed")

    if not args.no_report:
        generate_report(os_name, results)
