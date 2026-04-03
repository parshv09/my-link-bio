from flask import Flask, redirect, render_template, request, url_for
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f"https://{url}"

        # A browser-like user agent helps avoid some sites returning blocked/minimal HTML.
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # Support common Open Graph variants across sites:
        # - property="og:*"
        # - name="og:*"
        og_title = soup.select_one('meta[property="og:title"], meta[name="og:title"]')
        og_description = soup.select_one(
            'meta[property="og:description"], meta[name="og:description"]'
        )
        og_image = soup.select_one('meta[property="og:image"], meta[name="og:image"]')

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


def normalize_url(url):
    """Ensure URLs include a scheme."""
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return url

    return f"https://{url}"


@app.route("/")
def index():
    return render_template("index.html", links=links)


@app.route("/add", methods=["POST"])
def add_link():
    site_name = request.form.get("site_name", "").strip()
    url = request.form.get("url", "").strip()

    if site_name and url:
        normalized_url = normalize_url(url)
        metadata = get_open_graph_metadata(normalized_url)
        links.append(
            {
                "name": site_name,
                "url": normalized_url,
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
            normalized_url = normalize_url(url)
            link["name"] = site_name
            link["url"] = normalized_url
            metadata = get_open_graph_metadata(normalized_url)
            link["title"] = metadata["title"]
            link["description"] = metadata["description"]
            link["image_url"] = metadata["image_url"]

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
