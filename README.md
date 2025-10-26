# StockTwits Scraper

This project is a simple scraper that captures a screenshot of the most active stocks from StockTwits and extracts the relevant information into a text file.

## Project Structure

```
stocktwits-scraper
├── src
│   ├── main.py                # Entry point of the application
│   ├── screenshot_capture.py   # Contains functions to capture screenshots
│   ├── text_extraction.py      # Contains functions to extract stock information
│   └── utils
│       └── __init__.py        # Utility functions and constants
├── output
│   └── .gitkeep               # Keeps the output directory tracked by Git
├── requirements.txt            # Lists project dependencies
├── config.py                  # Configuration settings for the project
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd stocktwits-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Open `config.py` and set the desired URL if necessary.
2. Run the main script:
   ```
   python src/main.py
   ```

This will capture a screenshot of the specified URL and extract the most active stocks into a text file.

## Dependencies

- PyAutoGUI
- Other libraries for image processing and text extraction (as specified in `requirements.txt`).

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.