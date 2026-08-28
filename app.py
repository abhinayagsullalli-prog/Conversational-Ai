import os
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def get_gemini_api_key() -> str:
    load_dotenv(override=True)
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    return key


def get_model_name() -> str:
    load_dotenv(override=True)
    return (os.getenv("GEMINI_MODEL") or "gemini-3.6-flash").strip()


def build_history_prompt(message: str, history: list[dict[str, Any]] | None) -> str:
    history = history or []
    prompt_lines: list[str] = []

    for item in history[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if not isinstance(content, str):
            continue
        content = content.strip()
        if not content:
            continue
        if role == "user":
            prompt_lines.append(f"User: {content}")
        else:
            prompt_lines.append(f"Assistant: {content}")

    prompt_lines.append(f"User: {message}")
    prompt_lines.append("Assistant:")
    return "\n".join(prompt_lines)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({"error": "Message must be a string."}), 400

    message = message.strip()
    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    if len(message) > 4000:
        return jsonify({"error": "Message is too long."}), 400

    api_key = get_gemini_api_key()
    if not api_key or api_key == "your_api_key_here":
        return jsonify({"error": "Gemini API key is not configured on the server."}), 500

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(get_model_name())
        history = data.get("conversation_history")
        prompt = build_history_prompt(message, history if isinstance(history, list) else [])

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 800,
            },
        )

        text = getattr(response, "text", "").strip()
        if not text:
            candidate_text = ""
            for candidate in getattr(response, "candidates", []) or []:
                content = getattr(candidate, "content", None)
                if content is None:
                    continue
                parts = getattr(content, "parts", []) or []
                for part in parts:
                    part_text = getattr(part, "text", "")
                    if part_text:
                        candidate_text += part_text
            text = candidate_text.strip()

        if not text:
            return jsonify({"error": "The AI returned an empty response."}), 502

        return jsonify({"response": text})

    except Exception as exc:  # pragma: no cover - safety fallback
        app.logger.exception("Gemini request failed")
        error_msg = str(exc) if app.debug else "Unable to generate a response right now."
        return jsonify({"error": error_msg}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
