import os
import time
from datetime import datetime

os.system("adb devices")
# Function to check if the device is idle
def is_device_idle():
    print(f"{datetime.now()} - Checking if the device is idle...")
    # Run the ADB command to check idle state
    result = os.popen("shizuku adb shell dumpsys deviceidle").read()
    print(result)
    # Check for idle states in the result
    if "mLightIdleState=IDLE" in result or "mDeepIdleState=IDLE" in result:
        print(f"{datetime.now()} - Device is idle.")
        return True
    else:
        print(f"{datetime.now()} - Device is not idle.")
        return False

# Function to launch Quetta Browser
def launch_quetta_browser():
    print(f"{datetime.now()} - Launching Quetta Browser...")
    # Use ADB command to launch the browser
    os.system("shizuku adb shell monkey -p com.quettatech.browser 1")
    print(f"{datetime.now()} - Quetta Browser launched.")

# Main automation function
def automate_depin_nodes(test_mode=False):
    if test_mode:
        print(f"{datetime.now()} - Test mode enabled. Forcing execution now...")
        launch_quetta_browser()
        return

    while True:
        # Wait for 30 minutes
        print(f"{datetime.now()} - Waiting for 30 minutes...")
        time.sleep(30 * 60)  # 30 minutes

        # Check if the device is idle
        if is_device_idle():
            # Launch Quetta Browser
            launch_quetta_browser()
        else:
            print(f"{datetime.now()} - Device is not idle. Retrying after 30 minutes...")

# Run the script
if __name__ == "__main__":
    # Set test_mode=True to force execution now
    automate_depin_nodes(test_mode=True)