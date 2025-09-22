import subprocess
import time
import subprocess
from datetime import datetime

def open_app(app_package):
    subprocess.run(f"am start -n {app_package}", shell=True)
    print("App opened")


def perform_interaction(x, y):
    try:
        time.sleep(10)
        subprocess.run(f"adb shell input tap {x} {y}", shell=True, check=True)
        print("UI Interaction complete")
    except subprocess.CalledProcessError:
        print("Error: ADB command failed")
        
def check_running_apps():
    target_apps = ["com.arlosoft.macrodriod", "com.termux", "com.google.android.as", "com.android.launcher3", "com.google.android.dialer", "com.gazlaws.codeboard", "com.google.android.ext.services", "com.gogle.android.gms.persistent", "com.google.android.apps.messaging:rcs", "com.android.settings", "com.google.android.apps.wellbeing", "com.hmdglobal.memorycleaner"]
    try:
        output = subprocess.check_output("ps -ef", shell=True)
        output = output.decode("utf-8")
        running_apps = [app for app in target_apps if app in output]
        print(running_apps)
        non_target_apps = [line for line in output.splitlines() if any(word in line for word in ["com.", "org."]) and not any(app in line for app in target_apps)]
        if len(running_apps) > 0:
            print("At least one permitted app is running")
            if len(non_target_apps) > 0:
                print("The following non-target apps are running:")
                print(output)
                print(non_target_apps)
                for app in non_target_apps:
                    print(app)
            else:
                print("No non-target apps are running")
                print(non_target_apps)
            return True
        else:
            print("No permitted apps are running")
            return False
    except subprocess.CalledProcessError:
        print("Error running ps command")
        return False

def check_time():
    current_time = datetime.now().strftime("%H:%M")
    start_time = "23:00"
    end_time = "04:00"
    if (start_time <= current_time and current_time <= "23:59") or (current_time >= "00:00" and current_time <= end_time):
        print("It's time")
        return True
    else:
        print("It's not yet time")
        return False

app_open = False

def main():
    global app_open
    if (check_time() or check_running_apps()) and not app_open:
        print("All the conditions are right let depin nodes mining begin")
        open_app("net.quetta.browser/com.google.android.apps.chrome.IntentDispatcher")
        perform_interaction(727, 1180)
        app_open = True
        perform_interaction(525,1157)
    elif not (check_time() or check_running_apps()) and app_open:
        print("Something is still off, we will check back very soon")
        app_open = False
    print("Checking back in Ten minutes")

while True:
    main()
    time.sleep(600)