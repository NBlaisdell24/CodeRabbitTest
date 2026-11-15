
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

DEFAULT_PORTS = {"http": 80, "https": 443}
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
}


class URLNormalizer:
    def normalize(self, url: str) -> str:
        p = urlparse(url.strip())
        scheme = p.scheme.lower()
        host = (p.hostname or "").lower()

        netloc = host
        if p.port and p.port != DEFAULT_PORTS.get(scheme):
            netloc = f"{host}:{p.port}"

        path = p.path or "/"
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/")

        query_pairs = [
            (k, v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS
        ]
        query = urlencode(sorted(query_pairs))

        return urlunparse((scheme, netloc, path, "", query, ""))

    def dedupe(self, urls: list[str]) -> list[str]:
        #Return URLs with duplicates removed, keeping order
        seen = set()
        result = []
        for url in urls:
            key = self.normalize(url)
            if key not in seen:
                seen.add(key)
                result.append(key)
        return result
