import platform
import requests

# Backend endpoint
BACKEND_URL = "http://127.0.0.1:9100/scan"

# 🔥 PASTE YOUR FULL COGNITO ACCESS TOKEN BELOW (INSIDE QUOTES)
ACCESS_TOKEN = "eyJraWQiOiJscThWNnZ0Vmpndm40dWlRRytjR09GT1I0aEVTcGlJY01XdVVwcThuWFVRPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NGE4YTQ3OC02MDAxLTcwYWMtOTZhYy1mYWU3YWQwYWZiZmUiLCJjb2duaXRvOmdyb3VwcyI6WyJhZG1pbnMiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfNjViN0REdGcyIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiM2FnNTNmZzNpb3R1MDMyaDZ0b2hmNWM1cHQiLCJvcmlnaW5fanRpIjoiYjU2MDQwNGUtYTE4Yi00YzM1LTkwZWYtZDIwMDMyMjg3NWFjIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQgZW1haWwiLCJhdXRoX3RpbWUiOjE3NzE0OTA4MTAsImV4cCI6MTc3MTQ5NDQxMCwiaWF0IjoxNzcxNDkwODEwLCJqdGkiOiIyMzUwMGRmNy0yMTQxLTRiMmQtODljMy0zNjMzNWY1MjlmYjgiLCJ1c2VybmFtZSI6IjY0YThhNDc4LTYwMDEtNzBhYy05NmFjLWZhZTdhZDBhZmJmZSJ9.cEZdp51NPurudjM1sTICDxG-r9kEBPlZFO7et6gUJGsJRQB9iNKwQ97hLdmVIRbM6PAuLeHC_bfr3pkcX0B6OcTPvr1WotqQpDYe7lKVwNlVvXORyGEQRsAoUcAyY7VtgWfXRjhOw1yiPTDKSNFHzduEsx_8Jb-P05rlmLR0U_0QkVDozLMnuHHi5TZ9OtfE42sKz1sBBWDFGdfDAiD_w9xprl3TIrng38g7OYVeHE8zGtfSVxH-Idw2SxywGuXjwmE3WplUN9bsBr2VbdHhRI7HIWZetCCNl9uz2YU5VprHrIlT9pRjQjfYhzfoNo2RHrV5aIsFrB_2tohu7u05oA"


def collect_environment():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
    }


def collect_tools():
    return [
        {"name": "python", "version": platform.python_version()},
    ]


def run_scan():
    payload = {
        # Backend will extract developer_id from JWT
        "environment": collect_environment(),
        "tools": collect_tools(),
        "metadata": {},
    }

    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN
    }

    print("Sending scan to backend...")

    response = requests.post(
        BACKEND_URL,
        json=payload,
        headers=headers
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    run_scan()
