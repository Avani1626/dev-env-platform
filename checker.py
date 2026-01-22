import shutil

TOOLS = {
    "Python": "python",
    "Git": "git",
    "Docker": "docker",
    "Node.js": "node",
}

def check_tools():
    print("🔍 Checking development environment:\n")
    for name, cmd in TOOLS.items():
        if shutil.which(cmd):
            print(f"✅ {name} is installed")
        else:
            print(f"❌ {name} is NOT installed")

if __name__ == "__main__":
    check_tools()
