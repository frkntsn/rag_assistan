import requests


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
HEADERS = {
    "User-Agent": "BLG483E-Local-RAG-Assistant/1.0 (educational project)",
    "Accept": "application/json",
}


def _build_session() -> requests.Session:
    session = requests.Session()
    # Some environments set proxy variables that break Wikipedia access.
    session.trust_env = False
    session.headers.update(HEADERS)
    return session


def fetch_wikipedia_extract(title: str) -> str:
    session = _build_session()
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
        "titles": title,
    }
    try:
        response = session.get(WIKIPEDIA_API, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", [])
        page = pages[0] if pages else {}
        extract = page.get("extract", "").strip()
        if extract:
            return extract
    except requests.RequestException:
        pass

    # Fallback endpoint for environments where API query may fail.
    safe_title = title.replace(" ", "_")
    fallback_url = WIKIPEDIA_SUMMARY_API.format(title=safe_title)
    response = session.get(fallback_url, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("extract", "").strip()
