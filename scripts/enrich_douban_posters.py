#!/usr/bin/env python3
"""Resolve film posters from Douban's subject-suggest endpoint.

The endpoint returns the official Douban subject and its poster image.  We keep
the resolved URL and subject URL in the data so the browser never has to guess
which image belongs to a film.
"""
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from urllib.request import Request, urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {"User-Agent": "Mozilla/5.0 (Xiaohua Universe poster index)"}

def lookup(row):
    for query in (row.get("filmEn"), row.get("filmZh")):
        if not query:
            continue
        try:
            url = "https://movie.douban.com/j/subject_suggest?q=" + quote(query)
            with urlopen(Request(url, headers=HEADERS), timeout=5) as response:
                items = json.loads(response.read().decode("utf-8"))
            movies = [x for x in items if x.get("type") == "movie" and x.get("img")]
            if not movies:
                continue
            exact = [x for x in movies if str(row.get("year", "")) == str(x.get("year", ""))]
            item = (exact or movies)[0]
            return row, {
                "posterUrl": item["img"].replace("\\/", "/").replace("http://", "https://"),
                "doubanUrl": item.get("url", "").replace("\\/", "/"),
                "doubanId": item.get("id", ""),
            }
        except Exception:
            continue
    return row, {}

def main():
    path = ROOT / "data/records.json"
    rows = json.loads(path.read_text())
    found = 0
    with ThreadPoolExecutor(max_workers=32) as pool:
        futures = [pool.submit(lookup, row) for row in rows]
        for future in as_completed(futures):
            row, result = future.result()
            row.update(result)
            found += bool(result.get("posterUrl"))
    payload = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    path.write_text(payload)
    (ROOT / "public/data/records.json").write_text(payload)
    print(f"resolved {found}/{len(rows)} Douban posters")

if __name__ == "__main__":
    main()
