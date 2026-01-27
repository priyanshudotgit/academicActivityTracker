import pygetwindow as gw
import time
import os

def getActiveWindowInfo():
    try:
        window = gw.getActiveWindow()
        if window:
            return window.title
        return None
    except Exception:
        return None

def main():
    print("Window Info Running")
    
    last_window = ""

    while True:
        current_window = getActiveWindowInfo()
        
        # Only print if the window actually changed (reduces console spam)
        if current_window and current_window != last_window:
            
            # Clear console for a dashboard effect
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"[-] Previous: {last_window}")
            print(f"[+] Active:   {current_window}")
            
            last_window = current_window

        # -----------------------------------------------------
        # Prints Continuously every second
        # print(f"[-] Previous: {last_window}")
        # print(f"[+] Active:   {current_window}")
        # -----------------------------------------------------
        
        # Check every 1 second
        time.sleep(1)

if __name__ == "__main__":
    main()