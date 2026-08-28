# Gemini AI Assistant

A beginner-friendly AI chatbot built with Python Flask, HTML, CSS, and vanilla JavaScript. It sends chat messages to the Google Gemini API and displays responses in a modern dark-themed interface.

## Project structure

```text
ai-chatbot/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## 1. Create the project folder

```bash
mkdir ai-chatbot
cd ai-chatbot
```

## 2. Create a Python virtual environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Add the Gemini API key to .env

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

> Keep the API key private. Do not expose it in frontend code or HTML.

## 5. Start the Flask server

```bash
python app.py
```

The app runs at:

```text
http://127.0.0.1:5000
```

## 6. Open the chatbot in the browser

Visit:

```text
http://127.0.0.1:5000
```

## Features

- Chat with Gemini using a Flask backend
- Responsive dark glassmorphism interface
- Message history saved in browser localStorage
- New chat and clear chat actions
- Typing indicator while AI is thinking
- Copy AI responses
- Enter to send, Shift + Enter for new line
- Mobile sidebar support
- Theme toggle

## Notes

- The frontend never receives the API key.
- Validation is done on the backend before sending requests to Gemini.
- If Gemini fails, the backend returns a friendly error without leaking internal details.
