from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Flask setup
app = Flask(__name__)
CORS(app)

# Home route
@app.route("/")
def home():
    return "AI Tools Backend is running"

# Call OpenAI (chat-based)
def call_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # You can also use "gpt-4" if you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Book Summary
@app.route("/summarize", methods=["POST"])
def summarize():
    user_input = request.json["text"]
    prompt = f"""
You are a helpful assistant that summarizes books clearly and in detail.

Given a book title (and optionally the author), provide:
1. A detailed paragraph of at least 3 full sentences summarizing the book.
2. A list of 3 to 10 bullet points highlighting key themes, insights, or takeaways.

Use this format:
Title: [Book Title]

Summary:
[Detailed 3+ sentence paragraph]

Key Points:
• ...
• ...
• (3 to 10 bullet points)

Book title: {user_input}
"""
    return jsonify({"result": call_openai(prompt)})

# Quiz Generator
@app.route("/quiz", methods=["POST"])
def quiz():
    user_input = request.json["text"]
    prompt = f"""
You are an educational assistant that creates quizzes based on a topic.

Create at least 5 quiz questions related to the following topic. Questions should be a mix of multiple choice and short answer.

Topic: {user_input}

Quiz:
1.
2.
3.
4.
5.
"""
    return jsonify({"result": call_openai(prompt)})

# Idea Generator
@app.route("/ideas", methods=["POST"])
def ideas():
    user_input = request.json["text"]
    prompt = f"""
You are a creative assistant who generates useful and original ideas.

Generate at least 5 creative and practical ideas based on the following topic. Each idea should be 1–2 sentences long.

Topic: {user_input}

Ideas:
1.
2.
3.
4.
5.
"""
    return jsonify({"result": call_openai(prompt)})

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
