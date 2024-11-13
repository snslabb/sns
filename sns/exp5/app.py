from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

user_data = {
    "luffy": {"name": "Monkey D. Luffy", "role": "Captain", "goal": "King of pirates"},
    "zoro": {"name": "Roronoa Zoro", "role": "Swordsman", "goal": "World's greatest swordsman"},
    "nami": {"name": "Nami", "role": "Navigator", "goal": "Map the entire world"},
    "usopp": {"name": "Usopp", "role": "Sniper", "goal": "Brave warrior of the sea"},
    "sanji": {"name": "Sanji", "role": "Chef", "goal": "Find the All Blue"},
    "chopper": {"name": "Tony Tony Chopper", "role": "Doctor", "goal": "Cure any disease"},
    "robin": {"name": "Nico Robin", "role": "Archaeologist", "goal": "Learn the true history"},
    "franky": {"name": "Franky", "role": "Shipwright", "goal": "Build the best ship"},
    "brook": {"name": "Brook", "role": "Musician", "goal": "Reunite with Laboon"},
    "jinbe": {"name": "Jinbe", "role": "Helmsman", "goal": "Achieve true justice"},
}

def query_sanitizer(query):
    sanitized_query = re.sub(r'[^\w\s]', '', query.strip()) or "query"
    return sanitized_query

@app.route("/")
def index():
    return render_template("index.html", users=user_data.items())

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("search_query")
    return redirect(url_for("search_results", query=query_sanitizer(query)))

@app.route("/search/<query>")
def search_results(query):
    results = [(key, user) for key, user in user_data.items() if query.lower() in user['name'].lower()]
    return render_template("search_results.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
