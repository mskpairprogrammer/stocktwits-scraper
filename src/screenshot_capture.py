import pyautogui
import time
import webbrowser
import os
from datetime import datetime

def capture_screenshot(url: str, filename: str):
    """
    Capture a screenshot of a given URL
    """
    print(f"Opening URL: {url}")
    
    # Open the URL in a new browser window (not tab)
    webbrowser.open_new(url)  # open_new() opens in a new window instead of tab
    
    # Wait for the page to load completely
    print("Waiting for page to load...")
    time.sleep(5)  # Reduced wait time from 15 to 5 seconds
    
    # Focus on the browser window for scrolling
    try:
        # Move mouse to center of screen to ensure we're focused on the browser
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()  # Click to focus on browser
        time.sleep(1)
        
        print("Scrolling to ensure all Most Active stocks are visible...")
        
        # Scroll down more thoroughly to make sure we can see all 10 stocks
        # First, scroll to top to start from a known position
        pyautogui.scroll(10)  # Scroll up first
        time.sleep(0.5)  # Reduced from 1 second to 0.5
        
        # Then scroll down gradually to reveal all stocks, but not too much
        for i in range(10):  # Optimal range - not too little, not too much
            pyautogui.scroll(-3)  # Smaller scroll steps for precision
            time.sleep(0.2)  # Slightly slower for better control
        
        # Scroll back up slightly to center the Most Active list
        time.sleep(1)
        for i in range(2):
            pyautogui.scroll(2)  # Small upward scrolls
            time.sleep(0.3)
        
        # Wait a moment for scroll to settle
        time.sleep(2)
        
        # Optional: Try to click on the "Most Active" tab to ensure it's selected
        # This helps ensure we're viewing the right section
        print("Ensuring Most Active tab is selected...")
        time.sleep(1)
        
    except Exception as e:
        print(f"Warning: Could not perform scrolling actions: {e}")
        print("Continuing with screenshot capture...")
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Add timestamp to filename for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name, ext = os.path.splitext(filename)
    filename_with_timestamp = f"{base_name}_{timestamp}{ext}"
    
    # Full path for the screenshot
    screenshot_path = os.path.join(output_dir, filename_with_timestamp)
    
    print("Capturing screenshot...")
    try:
        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None