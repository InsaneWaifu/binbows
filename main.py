from bs4 import BeautifulSoup
import httpx
import urllib.parse
import json
import random
from bottle import *
from homepage import home


with open("entries.json") as f:
    entries = json.load(f)

def search(query):
    res = httpx.get(f"https://engine.presearch.org/search?q={urllib.parse.quote_plus(query)}")
    soup = BeautifulSoup(res.text, features="lxml")
    results = []
    for result in soup.find_all("div", "ml-4 mb-4 md:mb-6 max-w-2xl pr-4"):
        result_entry = {}
        result_entry["title"] = result.find("div").find("h3").find("a").text
        result_entry["url"] = result.find("div").find("h3").find_next_sibling("div").find("a")["href"]
        result_entry["text"] = result.find("div", "text-gray-800 dark:text-gray-400").text
        results.append(result_entry)
    return results

@get("/")
def index():
    if not request.query:
        return template("./template.html", randomterm=random.choice(entries), results=home)
    return template("./template.html", randomterm=random.choice(entries), results=search(request.query.get("Search")))

@get("/assets/<asset>")
def assets(asset):
    return static_file("/assets/" + asset, ".")

@get("/list")
def list():
    return template("./list.html", entries=entries)


@post("/list")
def list():
    entries.append(request.forms.get('Term'))
    with open("entries.json", "w") as f:
        json.dump(entries, f)
    return redirect("/list")

run(host="0.0.0.0", port=8282)
