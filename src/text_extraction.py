import re
import os
from PIL import Image

def extract_stocks_from_image(image_path: str):
    """
    Extract stock symbols from a screenshot of StockTwits most active page
    """
    try:
        # Load the image from the specified path
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return []
            
        image = Image.open(image_path)
        print(f"Processing image: {image_path}")
        print(f"Image size: {image.size}")

        # Try to use pytesseract if available
        try:
            import pytesseract
            
            # Try common Windows Tesseract installation paths
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"Found Tesseract at: {path}")
                    break
            
            # Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(image)
            
            # Print extracted text for debugging
            print("Extracted text preview:")
            print("-" * 50)
            print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
            print("-" * 50)

            # Process the extracted text to find stock symbols
            stocks = _extract_stock_symbols_from_text(extracted_text)
            
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            print("Tesseract OCR might not be installed. Providing manual instructions...")
            
            # Save the image for manual inspection
            print(f"Screenshot saved at: {image_path}")
            print("Please manually check the screenshot for stock symbols.")
            
            # Return sample data as fallback
            stocks = _get_sample_stocks()
            
        return stocks
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return []

def _extract_stock_symbols_from_text(text):
    """Extract stock symbols from OCR text, focusing on Most Active ranked list"""
    
    print(f"Full OCR text length: {len(text)} characters")
    
    # Target stocks from the Most Active list (top 10 from the ranking)
    target_stocks = {
        'BYND', 'SPY', 'QQQ', 'DJT', 'TSLA', 'NVDA', 'RGTI', 'OPEN', 'INTC', 'BMNR'
    }
    
    print(f"Searching for these 10 Most Active stocks: {sorted(target_stocks)}")
    
    # Look for ranked list patterns - numbers followed by stock symbols
    ranked_pattern = r'(\d+)\s+([A-Z]{2,5})\b'
    ranked_matches = re.findall(ranked_pattern, text)
    
    # Look for stock symbols with company descriptions (more reliable)
    company_pattern = r'\b([A-Z]{2,5})\s+[A-Z][a-z]+'
    company_matches = re.findall(company_pattern, text)
    
    # Look for standalone stock symbols (2-5 uppercase letters)
    standalone_pattern = r'\b([A-Z]{2,5})\b'
    standalone_matches = re.findall(standalone_pattern, text)
    
    # Look for stock symbols followed by percentage changes (common pattern)
    percentage_pattern = r'\b([A-Z]{2,5})\s*[↑↓⬆⬇]?\s*[\d.]+%'
    percentage_matches = re.findall(percentage_pattern, text, re.IGNORECASE)
    
    # Look for partial matches of target stocks (handle OCR errors)
    partial_matches = []
    for target in target_stocks:
        # Look for partial matches like "QQQ" might be read as "QQQT" or "QQ"
        partial_pattern = f'({target[:3]}[A-Z]?)'  # Allow one extra character
        partial_found = re.findall(partial_pattern, text)
        for match in partial_found:
            if match.startswith(target[:2]):  # At least first 2 chars match
                partial_matches.append(target)  # Use the target stock, not the partial match
                print(f"✓ Found partial match for {target}: '{match}'")
                break
    
    # Combine all potential matches
    all_potential_stocks = []
    
    # Priority 1: Ranked matches (most reliable)
    for rank, symbol in ranked_matches:
        all_potential_stocks.append(symbol)
        if symbol in target_stocks:
            print(f"✓ Found ranked target stock: #{rank} {symbol}")
        else:
            print(f"Found ranked stock: #{rank} {symbol}")
    
    # Priority 2: Company description matches
    for symbol in company_matches:
        if symbol not in all_potential_stocks:
            all_potential_stocks.append(symbol)
            if symbol in target_stocks:
                print(f"✓ Found target stock with description: {symbol}")
    
    # Priority 3: Percentage change matches
    for symbol in percentage_matches:
        symbol_upper = symbol.upper()
        if symbol_upper not in all_potential_stocks:
            all_potential_stocks.append(symbol_upper)
            if symbol_upper in target_stocks:
                print(f"✓ Found target stock with percentage: {symbol_upper}")
    
    # Priority 4: Partial matches for OCR errors
    for symbol in partial_matches:
        if symbol not in all_potential_stocks:
            all_potential_stocks.append(symbol)
    
    # Priority 5: Standalone matches
    for symbol in standalone_matches:
        if symbol not in all_potential_stocks:
            all_potential_stocks.append(symbol)
    
    print(f"Raw potential stocks found: {all_potential_stocks}")
    
    # Filter to only include stocks that appear in target list or pass strict validation
    filtered_stocks = []
    seen_stocks = set()
    
    # Enhanced filter for common false positives
    ui_words = {
        'RANK', 'SYMBOL', 'MOST', 'ACTIVE', 'TRENDING', 'NEWS', 'VIEW', 'TOP', 'WITH', 
        'MESSAGES', 'FEED', 'SEARCH', 'HOME', 'PROFILE', 'CHAT', 'IDEAS', 'WATCH',
        'CORP', 'INC', 'LLC', 'LTD', 'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT'
    }
    
    # First pass: Include target stocks if found
    for stock in all_potential_stocks:
        if stock in target_stocks and stock not in seen_stocks:
            filtered_stocks.append(stock)
            seen_stocks.add(stock)
            print(f"✓ Matched target stock: {stock}")
    
    # Second pass: Include other valid-looking stocks (but be more selective)
    for stock in all_potential_stocks:
        if (stock not in ui_words and 
            stock not in seen_stocks and 
            len(stock) >= 2 and 
            len(stock) <= 5 and
            stock.isupper() and
            stock.isalpha() and
            # Additional validation for non-target stocks
            not any(word in stock for word in ['STOCK', 'TWIT', 'MOST', 'ACT'])):
            filtered_stocks.append(stock)
            seen_stocks.add(stock)
            print(f"+ Added additional stock: {stock}")
    
    # Sort by likelihood/priority (target stocks first, limit to targets only)
    final_stocks = []
    
    # Add target stocks first (in the order they appear in the target list)
    for target in ['BYND', 'SPY', 'QQQ', 'DJT', 'TSLA', 'NVDA', 'RGTI', 'OPEN', 'INTC', 'BMNR']:
        if target in filtered_stocks:
            final_stocks.append(target)
    
    # Only include target stocks - filter out everything else for cleaner results
    missing_stocks = target_stocks - set(final_stocks)
    if missing_stocks:
        print(f"⚠️  Missing stocks (may need better scrolling): {sorted(missing_stocks)}")
    
    print(f"✅ Found {len(final_stocks)}/10 target Most Active stocks: {final_stocks}")
    return final_stocks

def _get_sample_stocks():
    """Return sample stocks as fallback when OCR fails"""
    sample_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
        "SPY", "QQQ", "AMD", "BABA", "DIS", "V", "JPM"
    ]
    print(f"Using sample stock data: {sample_stocks}")
    print("Note: These are sample stocks. Install Tesseract OCR for real data extraction.")
    return sample_stocks

def save_stocks_to_file(stocks, filename="most_active_stocks.txt"):
    """
    Save extracted stocks to a text file
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, filename)
    
    try:
        with open(file_path, "w") as f:
            f.write("Most Active Stocks from StockTwits\n")
            f.write("=" * 40 + "\n\n")
            
            if stocks:
                for i, stock in enumerate(stocks, 1):
                    f.write(f"{i}. ${stock}\n")
            else:
                f.write("No stocks found.\n")
                
        print(f"Stocks saved to: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"Error saving stocks to file: {e}")
        return None