from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape definition from Oxford Learner's Dictionary
def get_definition(word):
    try:
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "Definition not found."

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the first definition
        definition_div = soup.find("span", class_="def")
        if definition_div:
            return definition_div.text.strip()

        return "Definition not found."
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    word = ""
    definition = ""
    
    if request.method == "POST":
        word = request.form["word"].strip().lower()
        if word:
            definition = get_definition(word)

    return render_template("index.html", word=word, definition=definition)

# if __name__ == "__main__":
#     app.run(debug=True)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
