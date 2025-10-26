# Install Tesseract OCR for Windows

## Option 1: Download and Install Manually
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest Windows installer (.exe)
3. Run the installer and follow the setup wizard
4. Add Tesseract to your system PATH:
   - The default installation path is usually: `C:\Program Files\Tesseract-OCR`
   - Add `C:\Program Files\Tesseract-OCR` to your system PATH environment variable

## Option 2: Using Windows Package Manager (if available)
```powershell
winget install UB-Mannheim.TesseractOCR
```

## Option 3: Using Chocolatey (if installed)
```powershell
choco install tesseract
```

## Verify Installation
After installation, open a new command prompt and run:
```
tesseract --version
```

You should see version information if installed correctly.

## Alternative: Use pytesseract with custom path
If you can't add Tesseract to PATH, you can specify the path in your Python code:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```