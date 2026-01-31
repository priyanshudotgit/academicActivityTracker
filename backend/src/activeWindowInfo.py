import pygetwindow as gw
import time
import requests
import os
from db import addTime, fetchTime

STUDY_APPS = ["Visual Studio Code", "Terminal", "PowerShell", "Command Prompt", "Obsidian", "Notion"]
STUDY_SITES = ["stackoverflow.com", "github.com", "udemy.com", "chatgpt.com", "localhost", "w3schools.com", "gemini.google.com"]

def getUrl():
    try:
        response = requests.get("http://localhost:5000/get-current-url", timeout=0.5)
        if response.status_code == 200:
            return response.json().get("url", "")
    except:
        return ""
    return ""

def isStudying(windowTitle, url):

    windowTitle = windowTitle.lower() if windowTitle else ""
    print(f"{windowTitle}")
    url = url.lower()

    for app in STUDY_APPS:
        if app.lower() in windowTitle:
            return True, f"App: {app}"

    if "brave" in windowTitle or "chrome" in windowTitle:
        for site in STUDY_SITES:
            if site in url:
                return True, f"Web: {site}"

    return False, "notStudying"

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def main():
    print("Window Info Running")

    last_known_url = ""
    last_window_title = ""

    while True:
        try:
            activeWindow = gw.getActiveWindow()
            windowTitle = activeWindow.title if activeWindow else ""

            current_url = ""
            isProductive = False
            activity = "notStudying"

            if windowTitle == "":
                if "brave" in last_window_title.lower() or "chrome" in last_window_title.lower():
                    isProductive = True
                    activity = "Checking Extension"
                    current_url = last_known_url
                else:
                    activity = "System UI"
            
            else:
                last_window_title = windowTitle
                
                isBrowser = "brave" in windowTitle.lower() or "chrome" in windowTitle.lower()
                
                if isBrowser:
                    fetched_url = getUrl()
                    if fetched_url:
                        current_url = fetched_url
                        last_known_url = fetched_url
                    else:
                        current_url = last_known_url

                isProductive, activity = isStudying(windowTitle, current_url)

            if isProductive:
                    addTime(1)

            totalTime = fetchTime()

            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"--- STUDY TRACKER ---")
            print(f"Status:   {'✅' if isProductive else '❌'}")
            print(f"Activity: {activity}")
            print(f"Window:   {windowTitle}")
            print(f"URL:   {current_url}")
            print(f"Total:    {format_time(totalTime)}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    main()