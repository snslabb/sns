from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    username = request.form.get("username")
    password = request.form.get("password")
    _2fa = request.form.get("2fa")
    private = request.form.get("private")

    fields_to_check = ["priv_activity", "priv_pfp", "priv_bio", "priv_call"]
    privacy_values = {field: request.form.get(field) for field in fields_to_check}

    security_level = sum([
        len(password) >= 8,
        bool(re.compile(r'[^a-zA-Z0-9\s]').search(password)),
        bool(re.compile(r'\d').search(password)),
        bool(_2fa),
    ])

    privacy_level = sum([
        bool(private),
        sum(2 if value == "nobody" else 1 for value in privacy_values.values() if value == "nobody"),
        sum(1 for value in privacy_values.values() if value == "friends"),
    ])

    sec_ratio = "{:.2f}/10".format((security_level / 4) * 10)
    priv_ratio = "{:.2f}/10".format((privacy_level / 9) * 10)

    data = {
        "username": username,
        "sec_ratio": sec_ratio,
        "priv_ratio": priv_ratio
    }

    return render_template("detected_result.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
