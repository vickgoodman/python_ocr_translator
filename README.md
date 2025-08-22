# Instagram OCR Translator

An automated Python application that downloads Instagram posts, extracts text using OCR, translates content, and reposts with translated captions.

## Features

- **Automated Post Download**: Downloads new posts from specified Instagram accounts
- **OCR Text Extraction**: Uses Tesseract to extract text from images
- **AI Translation**: Leverages OpenAI API for intelligent text translation
- **Smart Filtering**: Skips carousel posts and videos
- **Automated Scheduling**: Posts content 3-4 times daily with configurable intervals
- **Session Management**: Maintains Instagram login sessions for reliability
- **Comprehensive Logging**: Tracks all operations with timestamped logs
- **Error Handling**: Robust error handling and retry mechanisms

## Project Structure

```
python_ocr_translator/
├── main.py                 # Main entry point
├── download_posts.py       # Instagram post downloader
├── create_posts.py         # OCR processing and translation
├── upload_posts.py         # Post upload to Instagram
├── upload.sh            	# Shell script for upload pipeline
├── config.py               # Configuration settings
├── main.sh                 # Shell script for main pipeline
├── requirements.txt        # Python dependencies
├── downloaded_posts/       # Raw downloaded images
├── created_posts/          # Processed images with translations
├── logs/                   # Application logs
└── .env                    # Environment variables (not tracked)
```

## Prerequisites

- Python 3.8+
- Tesseract OCR
- Instagram account credentials
- OpenAI API key

### Install Tesseract

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**

```bash
brew install tesseract
```

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/vickgoodman/python_ocr_translator.git
cd python_ocr_translator
```

2. **Create virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
   Create a `.env` file with:

```bash
SOURCE_PASSWORD=your_instagram_password
OPENAI_API_KEY=your_openai_api_key
```

5. **Configure settings:**
   Edit [`config.py`](config.py) with your Instagram usernames and preferences.

## Usage

### Manual Execution

**Download and create posts pipeline:**

```bash
python3 main.sh
```

**Upload a single post:**

```bash
python3 upload.sh
```

## Configuration

### [`config.py`](config.py)

```python
SOURCE_USERNAME = "your_source_account"
TARGET_USERNAME = "account_to_download_from"
```

### Scheduling Times

- **9:00**: Download and process new posts
- **08:00-13:00, 13:00-18:00, 18:00-23:00**: Post content (at random 0 to 5 hour interval)

## System Integration

### Cronjob (Linux)

```bash
crontab -e
```

### Download and create posts every day at 09:00

```bash
0 9 * * * cd ~/path/to/project && ./main.sh
```

### Schedule posts

```bash
# 1st post: 08:00-13:00
0 8 * * * cd ~/path/to/project && ./upload.sh
```

```bash
# 2nd post: 13:00-18:00
0 13 * * * cd ~/path/to/project && ./upload.sh
```

```bash
# 3rd post: 18:00-23:00
0 18 * * * cd ~/path/to/project && ./upload.sh
```

## Monitoring

### View Logs

```bash
ls -la logs/main/
ls -la logs/upload/
```

## Key Files

- **[`downloaded_posts.json`](downloaded_posts.json)**: Tracks processed posts and metadata
- **[`session.json`](session.json)**: Instagram session data (auto-generated)
- **[`logs/`](logs/)**: All application logs organized by component

## Error Handling

The application includes comprehensive error handling for:

- Network connectivity issues
- Instagram API rate limits
- OCR processing failures
- OpenAI API errors
- File system operations

## Security

- Environment variables for sensitive data
- Session management for Instagram authentication
- Automatic retry mechanisms for failed operations
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Ensure compliance with Instagram's Terms of Service and API usage policies.

## Troubleshooting

### Common Issues

**"No existing session found"**

- Delete [`session.json`](session.json) and restart to re-authenticate

**OCR not working**

- Verify Tesseract installation: `tesseract --version`
- Check image quality and format

**OpenAI API errors**

- Verify API key in `.env` file
- Check API quota and billing

**Permission errors**

- Ensure proper file permissions: `chmod +x main.sh`
- Check directory write permissions

### Getting Help

For Instagram-related issues, refer to the [instaloader documentation](https://instaloader.github.io/).
