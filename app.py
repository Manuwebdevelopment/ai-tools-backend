from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import os
openai.api_key = os.environ.get("OPENAI_API_KEY")


def call_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or gpt-3.5-turbo with chat API format
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()

@app.route("/summarize", methods=["POST"])
def summarize():
    user_input = request.json["text"]
    prompt = f"""You are a helpful assistant that summarizes books clearly and concisely.
Summarize the following book or passage into 3 to 5 bullet points.

Text:
{user_input}

Summary:"""
    return jsonify({"result": call_openai(prompt)})

@app.route("/quiz", methods=["POST"])
def quiz():
    user_input = request.json["text"]
    prompt = f"""You are a creative educational assistant. Generate a 5-question quiz (MCQ or short answer) based on this:

Text:
{user_input}

Quiz:"""
    return jsonify({"result": call_openai(prompt)})

@app.route("/ideas", methods=["POST"])
def ideas():
    user_input = request.json["text"]
    prompt = f"""You are a creative idea generator. Give me 10 unique ideas based on the following topic:

Topic:
{user_input}

Ideas:"""
    return jsonify({"result": call_openai(prompt)})

@app.route("/")
def home():
    return "AI Tools Backend is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)
