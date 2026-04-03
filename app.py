from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

# In-memory link store for the current process.
links = [
    "https://github.com",
    "https://www.linkedin.com",
    "https://x.com",
]


@app.route("/")
def index():
    return render_template("index.html", links=links)


@app.route("/delete/<int:link_index>", methods=["POST"])
def delete_link(link_index):
    if 0 <= link_index < len(links):
        links.pop(link_index)

    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
