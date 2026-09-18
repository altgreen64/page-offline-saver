#!/usr/bin/env python3
"""Pobiera pojedynczą stronę wraz z grafikami/CSS/JS do przeglądania offline."""
import sys
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScrapeBot/1.0)"}


def sanitize_filename(name):
    return re.sub(r"[^\w\-.]", "_", name) or "asset"


def download_asset(url, out_dir, session):
    try:
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  ! nie udało się pobrać {url}: {e}")
        return None

    parsed = urlparse(url)
    filename = sanitize_filename(os.path.basename(parsed.path)) or "asset"
    if "." not in filename:
        ctype = resp.headers.get("Content-Type", "")
        ext = ctype.split("/")[-1].split(";")[0] if "/" in ctype else "bin"
        filename += f".{ext}"

    local_path = os.path.join(out_dir, filename)
    base, ext = os.path.splitext(local_path)
    counter = 1
    while os.path.exists(local_path):
        local_path = f"{base}_{counter}{ext}"
        counter += 1

    with open(local_path, "wb") as f:
        f.write(resp.content)

    return os.path.basename(local_path)


def scrape_page(url):
    session = requests.Session()
    print(f"Pobieram: {url}")
    resp = session.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, "html.parser")

    domain = urlparse(url).netloc.replace(":", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(os.getcwd(), f"scrape_{domain}_{timestamp}")
    assets_dir = os.path.join(out_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    targets = [
        ("img", "src"),
        ("img", "data-src"),
        ("link", "href"),
        ("script", "src"),
    ]

    downloaded = 0
    for tag_name, attr in targets:
        for tag in soup.find_all(tag_name):
            src = tag.get(attr)
            if not src or src.startswith("data:"):
                continue
            full_url = urljoin(url, src)
            local_name = download_asset(full_url, assets_dir, session)
            if local_name:
                tag[attr] = f"assets/{local_name}"
                downloaded += 1
                print(f"  + {full_url} -> assets/{local_name}")

    style_pattern = re.compile(r"url\((['\"]?)(.*?)\1\)")
    for tag in soup.find_all(style=True):
        style = tag["style"]
        for _, bg_url in style_pattern.findall(style):
            if bg_url.startswith("data:"):
                continue
            full_url = urljoin(url, bg_url)
            local_name = download_asset(full_url, assets_dir, session)
            if local_name:
                style = style.replace(bg_url, f"assets/{local_name}")
                downloaded += 1
        tag["style"] = style

    html_path = os.path.join(out_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"\nGotowe! Pobrano {downloaded} plików graficznych/zasobów.")
    print(f"Strona zapisana w: {html_path}")
    print(f"Otwórz w przeglądarce: file://{html_path}")
    return out_dir


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Podaj URL strony do zescrapowania: ").strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    scrape_page(url)


if __name__ == "__main__":
    main()
