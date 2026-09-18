from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Career Selection Page
@app.route("/career")
def career():
    return render_template("career.html")


# Assessment Page
@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


# Dashboard Page
@app.route("/dashboard", methods=["POST"])
def dashboard():

    skills = ["python", "sql", "numpy", "pandas", "ml"]

    score = 0
    missing = []

    for skill in skills:

        if request.form[skill] == "Yes":
            score += 20

        else:
            missing.append(skill.upper())

    return render_template(
        "dashboard.html",
        score=score,
        missing=missing
    )


if __name__ == "__main__":
    app.run(debug=True)