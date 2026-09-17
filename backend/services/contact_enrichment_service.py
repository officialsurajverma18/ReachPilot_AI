"""Web-contact enrichment adapted from the legacy email_finder workflow.

Only public pages belonging to a lead's own website are fetched. It does not
attempt login-gated sources or directory pages and never sends messages.
"""
import html
import re
from urllib.parse import urljoin, urlparse
import requests

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
BAD_DOMAINS = {"example.com", "wixpress.com", "sentry.io", "googleapis.com"}


def _emails(text):
    found = []
    for address in EMAIL_RE.findall(html.unescape(text or "")):
        address = address.strip(".,;:()[]{}<>").lower()
        if address.split("@")[-1] not in BAD_DOMAINS and address not in found:
            found.append(address)
    return found


def find_public_email(website):
    if not website:
        return []
    if not website.startswith(("http://", "https://")):
        website = "https://" + website
    parsed = urlparse(website)
    headers = {"User-Agent": "ReachPilotAI/1.0 (college project contact enrichment)"}
    try:
        home = requests.get(website, headers=headers, timeout=8)
        home.raise_for_status()
    except requests.RequestException:
        return []
    result = _emails(home.text)
    # The legacy app checks a small, focused set of public contact paths.
    for path in ("/contact", "/contact-us", "/about"):
        if result:
            break
        try:
            candidate = urljoin(f"{parsed.scheme}://{parsed.netloc}", path)
            page = requests.get(candidate, headers=headers, timeout=6)
            if page.ok:
                result.extend(address for address in _emails(page.text) if address not in result)
        except requests.RequestException:
            continue
    return result[:3]
