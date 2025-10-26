import subprocess
import sys

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed!")
            print(f"Version info: {result.stdout.split()[1] if result.stdout.split() else 'Unknown'}")
            return True
        else:
            print("❌ Tesseract OCR command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
        print("❌ Tesseract OCR is not installed or not in PATH")
        print(f"Error: {e}")
        print("\nTo install Tesseract OCR on Windows:")
        print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install the .exe file")
        print("3. Add to PATH or set TESSDATA_PREFIX environment variable")
        return False

if __name__ == "__main__":
    check_tesseract()