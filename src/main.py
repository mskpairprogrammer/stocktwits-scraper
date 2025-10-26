import time
import os
from screenshot_capture import capture_screenshot
from text_extraction import extract_stocks_from_image, save_stocks_to_file

def main():
    """
    Main function to capture StockTwits screenshot and extract stocks
    """
    url = "https://stocktwits.com/sentiment/most-active"
    screenshot_filename = "most_active_stocks.png"
    
    print("Starting StockTwits stock extraction process...")
    print(f"Target URL: {url}")
    
    # Capture the screenshot
    screenshot_path = capture_screenshot(url, screenshot_filename)
    
    if screenshot_path is None:
        print("Failed to capture screenshot. Exiting.")
        return
    
    # Allow some time for the screenshot to be saved
    time.sleep(2)
    
    # Extract stocks from the screenshot
    print("\nExtracting stock symbols from screenshot...")
    stocks = extract_stocks_from_image(screenshot_path)
    
    # Save the extracted stocks to a text file
    if stocks:
        print(f"\nFound {len(stocks)} stock symbols")
        save_stocks_to_file(stocks)
        print("\nProcess completed successfully!")
    else:
        print("\nNo stock symbols found. You may need to:")
        print("1. Check if the page loaded correctly")
        print("2. Verify pytesseract is properly installed")
        print("3. Try adjusting the wait time for page loading")

if __name__ == "__main__":
    main()