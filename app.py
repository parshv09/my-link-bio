from flask import Flask, redirect, render_template, request, url_for

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

    return redirect(url_for("index"))


@app.route("/edit/<int:link_index>", methods=["GET", "POST"])
def edit_link(link_index):
    if not 0 <= link_index < len(links):
        return redirect(url_for("index"))

    link = links[link_index]

    if request.method == "POST":
        site_name = request.form.get("site_name", "").strip()
        url = request.form.get("url", "").strip()

        if site_name and url:
            link["name"] = site_name
            link["url"] = url

        return redirect(url_for("index"))

    return render_template("edit.html", link=link, link_index=link_index)


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
