from flask import Flask, redirect, render_template, request, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# In-memory storage for links (reset when app restarts).
links = [
    {
        "name": "GitHub",
        "url": "https://github.com",
        "title": "Not Available",
        "description": "Not Available",
        "image_url": "Not Available",
    },
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com",
        "title": "Not Available",
        "description": "Not Available",
        "image_url": "Not Available",
    },
    {
        "name": "X",
        "url": "https://x.com",
        "title": "Not Available",
        "description": "Not Available",
        "image_url": "Not Available",
    },
]


def get_open_graph_metadata(url):
    """Fetch Open Graph metadata from a URL."""
    default_value = "Not Available"
    metadata = {
        "title": default_value,
        "description": default_value,
        "image_url": default_value,
    }

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")

        if og_title and og_title.get("content"):
            metadata["title"] = og_title["content"].strip() or default_value

        if og_description and og_description.get("content"):
            metadata["description"] = og_description["content"].strip() or default_value

        if og_image and og_image.get("content"):
            metadata["image_url"] = og_image["content"].strip() or default_value
    except requests.RequestException:
        # Keep defaults if URL can't be fetched.
        pass

    return metadata


@app.route("/")
def index():
    return render_template("index.html", links=links)


@app.route("/add", methods=["POST"])
def add_link():
    site_name = request.form.get("site_name", "").strip()
    url = request.form.get("url", "").strip()

    if site_name and url:
        metadata = get_open_graph_metadata(url)
        links.append(
            {
                "name": site_name,
                "url": url,
                "title": metadata["title"],
                "description": metadata["description"],
                "image_url": metadata["image_url"],
            }
        )

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
