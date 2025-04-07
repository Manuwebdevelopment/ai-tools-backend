from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

# Load OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Call OpenAI helper
def call_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=800,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Home route
@app.route("/")
def home():
    return "AI Tools Backend is running"

# Book Summary tool
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

# Quiz Generator tool
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

# Idea Generator tool
@app.route("/ideas", methods=["POST"])
def ideas():
    user_input = request.json["text"]
    prompt = f"""
You are a creative assistant who generates useful and original ideas.

Generate at least 5 creative and practical ideas based on the following topic. Each idea should be 1-2 sentences long.

Topic: {user_input}

Ideas:
1.
2.
3.
4.
5.
"""
    return jsonify({"result": call_openai(prompt)})

# Run the app with dynamic port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
