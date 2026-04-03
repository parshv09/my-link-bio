from flask import Flask, redirect, render_template, request

app = Flask(__name__)

# In-memory storage for links (reset when app restarts).
links = [
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com"},
    {"name": "X", "url": "https://x.com"},
]


@app.route("/")
def index():
    return render_template("index.html", links=links)


@app.route("/add", methods=["POST"])
def add_link():
    site_name = request.form.get("site_name", "").strip()
    url = request.form.get("url", "").strip()

    if site_name and url:
        links.append({"name": site_name, "url": url})

    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
