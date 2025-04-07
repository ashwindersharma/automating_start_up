import os
import subprocess
import sys
import json
import requests

def is_service_running(service_name):
    """Check if a service is running."""
    try:
        output = subprocess.check_output(f'tasklist | findstr {service_name}', shell=True, text=True)
        return service_name in output
    except subprocess.CalledProcessError:
        return False

def is_xampp_control_panel_running():
    """Check if the XAMPP Control Panel is running."""
    try:
        output = subprocess.check_output('tasklist | findstr xampp-control.exe', shell=True, text=True)
        return 'xampp-control.exe' in output
    except subprocess.CalledProcessError:
        return False

def start_xampp_dashboard():
    """Start the XAMPP Control Panel."""
    xampp_path = r'D:\\xampp'  # Update this path if XAMPP is installed elsewhere
    if not is_xampp_control_panel_running():
        subprocess.Popen([xampp_path + "\\xampp-control.exe"], shell=True)
        print("XAMPP Control Panel started.")
    else:
        print("XAMPP Control Panel is already running.")

def start_xampp_services():
    """Start Apache and MySQL services if not running."""
    xampp_path = r'D:\\xampp'  # Update this path if XAMPP is installed elsewhere

    apache_service = "httpd.exe"
    mysql_service = "mysqld.exe"

    if not is_service_running(apache_service):
        print("Starting Apache...")
        # Use PowerShell to start Apache
        subprocess.Popen([f'powershell.exe', f'Start-Process "{xampp_path}\\apache_start.bat"'], shell=True)
    else:
        print("Apache is already running.")

    if not is_service_running(mysql_service):
        print("Starting MySQL...")
        # Use PowerShell to start MySQL
        subprocess.Popen([f'powershell.exe', f'Start-Process "{xampp_path}\\mysql_start.bat"'], shell=True)
    else:
        print("MySQL is already running.")


def send_slack_message(message):
    url = ""
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": message
    }

    # Send a POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print("slack message delivered successfully...")


    # """Send a message to Slack."""
    # slack_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXX"
    # payload = {
    #     "text": message
    # }
    # response = requests.post(slack_url, json=payload)
    # if response.status_code != 200:
    #     print(f"Failed to send message to Slack: {response.status_code}")

def main():
    start_xampp_dashboard()
    start_xampp_services()
    # send_slack_message("Xamp has been setup successfully")
    return "XampDone"

# if __name__ == "__main__":
#    main()
