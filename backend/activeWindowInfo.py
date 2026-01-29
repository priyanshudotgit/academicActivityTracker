import pygetwindow as gw
import time
import requests
import os
from db import addTime, fetchTime

STUDY_APPS = ["Visual Studio Code", "Terminal", "PowerShell", "Command Prompt", "Obsidian", "Notion"]
STUDY_SITES = ["stackoverflow.com", "github.com", "udemy.com", "chatgpt.com", "localhost", "w3schools.com"]

def get_browser_url():
    """Asks our local server for the current URL."""
    try:
        response = requests.get("http://localhost:5000/get-current-url", timeout=0.5)
        if response.status_code == 200:
            return response.json().get("url", "")
    except:
        return ""
    return ""

def is_study_time(window_title, url):
    """The Logic Core: Decides if we are working or slacking."""
    window_title = window_title.lower() if window_title else ""
    url = url.lower()

    # Case 1: Desktop Apps
    for app in STUDY_APPS:
        if app.lower() in window_title:
            return True, f"App: {app}"

    # Case 2: Browser (Check URL)
    # Adjust this if you use Chrome, Firefox, etc.
    if "brave" in window_title or "chrome" in window_title:
        for site in STUDY_SITES:
            if site in url:
                return True, f"Web: {site}"
    
    return False, "Distraction"

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

# def getActiveWindowInfo():
#     try:
#         window = gw.getActiveWindow()
#         if window:
#             return window.title
#         return None
#     except Exception:
#         return None

def main():
    print("Window Info Running")

    while True:
        try:
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else ""
            current_url = ""
        
            if "brave" in window_title.lower() or "chrome" in window_title.lower():
                    current_url = get_browser_url()
                
            is_productive, activity = is_study_time(window_title, current_url)

            if is_productive:
                    addTime(1)

            total_seconds = fetchTime()
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"--- STUDY TRACKER ---")
            print(f"Status:   {'✅ STUDIOUS' if is_productive else '❌ SLACKING'}")
            print(f"Activity: {activity}")
            print(f"Window:   {window_title}")
            print(f"Total:    {format_time(total_seconds)}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)

if __name__ == "__main__":
    main()