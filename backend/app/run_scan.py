import platform
import requests
import subprocess
import datetime

# Backend endpoint
BACKEND_URL = "http://127.0.0.1:9100/scan"

# 🔥 PASTE YOUR FULL COGNITO ACCESS TOKEN BELOW (INSIDE QUOTES)
ACCESS_TOKEN = "eyJraWQiOiJscThWNnZ0Vmpndm40dWlRRytjR09GT1I0aEVTcGlJY01XdVVwcThuWFVRPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NGE4YTQ3OC02MDAxLTcwYWMtOTZhYy1mYWU3YWQwYWZiZmUiLCJjb2duaXRvOmdyb3VwcyI6WyJhZG1pbnMiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfNjViN0REdGcyIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiM2FnNTNmZzNpb3R1MDMyaDZ0b2hmNWM1cHQiLCJvcmlnaW5fanRpIjoiMjI1MDlkZGQtZGM1Ny00M2Q4LThlNDctOWUxNDNjNjcxM2IxIiwiZXZlbnRfaWQiOiIyODVhMGQzMy1lYjFkLTQ1YTEtYWE2Yy05YjU4N2ZjOTFhNDQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6Im9wZW5pZCBlbWFpbCIsImF1dGhfdGltZSI6MTc3MTU3NTIxMiwiZXhwIjoxNzcxNTc4ODEyLCJpYXQiOjE3NzE1NzUyMTIsImp0aSI6Ijg3MTdhNTYwLWViOGMtNDVjNi1iOTA5LTg0NDllMDE3OTFlOCIsInVzZXJuYW1lIjoiNjRhOGE0NzgtNjAwMS03MGFjLTk2YWMtZmFlN2FkMGFmYmZlIn0.J4GwOXmTx13HNGpRWySuRybD6w6187_ZHeId1Sgbb065m2csH5dzRlYeJODi1Hn4zWNdJXC3mqicb2W88C3RKXpJojy0hYN20WbQev-QsQMeHDox9LQ-eznu3ZkYdKzHjpCZ_XlBvLjfZFarb0m_sNJKFv8Cf5rUiNf4xcmBf0w3JLMV7SaO4EeWQTrrDSNvkS9JLcyd83gcGSDqXITftNUNMjL5I8pkN_Y0FP0izH_y2VQygui8Akq082-vdDqhowhuIb2yzfH-9UkVWi82iJiAiK9nKmeXTXXnLQk7NJtDXLJDs7-RVn_rfdVjCHySImAoGFNk7LyOg3S9ttwYyw"


# ----------------------------
# SCANNER MODULES (Empty for now)
# ----------------------------

def scan_system():
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }



def scan_python():
    packages = []

    try:
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            lines = result.stdout.splitlines()

            for line in lines:
                if "==" in line:
                    name, version = line.split("==", 1)
                    packages.append({
                        "name": name,
                        "version": version
                    })

    except Exception as e:
        print("Error scanning python packages:", e)

    return {
        "python_version": platform.python_version(),
        "packages": packages
    }



def scan_node():
    node_data = {
        "node_version": None,
        "npm_version": None,
        "global_packages": []
    }

    try:
        # Get Node version
        node_result = subprocess.run(
            ["node", "-v"],
            capture_output=True,
            text=True
        )

        if node_result.returncode == 0:
            node_data["node_version"] = node_result.stdout.strip()

        # Get npm version
        npm_version_result = subprocess.run(
            ["npm", "-v"],
            capture_output=True,
            text=True
        )

        if npm_version_result.returncode == 0:
            node_data["npm_version"] = npm_version_result.stdout.strip()

        # Get globally installed npm packages
        npm_list_result = subprocess.run(
            ["npm", "list", "-g", "--depth=0"],
            capture_output=True,
            text=True
        )

        if npm_list_result.returncode == 0:
            lines = npm_list_result.stdout.splitlines()

            for line in lines:
                if "@" in line and "──" in line:
                    cleaned = line.strip().replace("├──", "").replace("└──", "").strip()
                    if "@" in cleaned:
                        name, version = cleaned.split("@", 1)
                        node_data["global_packages"].append({
                            "name": name.strip(),
                            "version": version.strip()
                        })

    except Exception as e:
        print("Node scan error:", e)

    return node_data



def scan_docker():
    docker_data = {
        "installed": False,
        "version": None,
        "images": []
    }

    try:
        # Check Docker version
        version_result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )

        if version_result.returncode == 0:
            docker_data["installed"] = True
            docker_data["version"] = version_result.stdout.strip()

            # Get Docker images
            images_result = subprocess.run(
                ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
                capture_output=True,
                text=True
            )

            if images_result.returncode == 0:
                lines = images_result.stdout.splitlines()
                for line in lines:
                    docker_data["images"].append(line.strip())

    except Exception as e:
        print("Docker scan error:", e)

    return docker_data



def scan_cli_tools():
    tools = {}

    commands = {
        "git": ["git", "--version"],
        "aws": ["aws", "--version"],
        "java": ["java", "-version"],
        "python": ["python", "--version"]
    }

    for tool_name, command in commands.items():
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Some tools print version in stderr (like java)
                output = result.stdout.strip() if result.stdout else result.stderr.strip()
                tools[tool_name] = {
                    "installed": True,
                    "version": output
                }
            else:
                tools[tool_name] = {
                    "installed": False,
                    "version": None
                }

        except Exception:
            tools[tool_name] = {
                "installed": False,
                "version": None
            }

    return tools



# ----------------------------
# BUILD FULL SCAN STRUCTURE
# ----------------------------

def build_full_scan():
    scan_id = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

    return {
        "scan_id": scan_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "system": scan_system(),
        "python": scan_python(),
        "node": scan_node(),
        "docker": scan_docker(),
        "cli_tools": scan_cli_tools(),
        "metadata": {}
    }


# ----------------------------
# SEND TO BACKEND
# ----------------------------

def send_to_backend(scan_data):
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN
    }

    print("Sending scan to backend...")

    response = requests.post(
        BACKEND_URL,
        json=scan_data,
        headers=headers
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)


# ----------------------------
# MAIN ENTRY
# ----------------------------

if __name__ == "__main__":
    full_scan = build_full_scan()
    send_to_backend(full_scan)
