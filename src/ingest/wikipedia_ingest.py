import time

import requests


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
HEADERS = {
    "User-Agent": "BLG483E-Local-RAG-Assistant/1.0 (educational project)",
    "Accept": "application/json",
}
MAX_RETRIES = 3
BACKOFF_SECONDS = 1.0


def _build_session() -> requests.Session:
    session = requests.Session()
    # Some environments set proxy variables that break Wikipedia access.
    session.trust_env = False
    session.headers.update(HEADERS)
    return session


def _request_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict | None = None,
    timeout: int = 30,
) -> requests.Response:
    last_exc: requests.RequestException | None = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = session.get(url, params=params, timeout=timeout)
            if response.status_code == 429 and attempt < MAX_RETRIES:
                sleep_seconds = BACKOFF_SECONDS * (2**attempt)
                time.sleep(sleep_seconds)
                continue
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_exc = exc
            if attempt >= MAX_RETRIES:
                raise
            sleep_seconds = BACKOFF_SECONDS * (2**attempt)
            time.sleep(sleep_seconds)

    if last_exc is not None:
        raise last_exc
    raise requests.RequestException("Unknown Wikipedia request failure")


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
        response = _request_with_retry(session, WIKIPEDIA_API, params=params, timeout=30)
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
    response = _request_with_retry(session, fallback_url, timeout=30)
    data = response.json()
    return data.get("extract", "").strip()
