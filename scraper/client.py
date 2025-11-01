import time, requests, logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import RequestException, HTTPError

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {"Accept": "application/json"}

class JiraClient:
    def __init__(self, base_url="https://issues.apache.org/jira", timeout=15):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.timeout = timeout

    def _build(self, path):
        return f"{self.base_url}{path}"

    @retry(retry=retry_if_exception_type(RequestException),
           wait=wait_exponential(multiplier=1, min=2, max=60),
           stop=stop_after_attempt(6))
    def get(self, path, params=None):
        url = self._build(path)
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "10")
                wait = int(retry_after)
                logger.warning("429 Too Many Requests, sleeping for %s seconds", wait)
                time.sleep(wait)
                raise RequestException("Rate limit")
            resp.raise_for_status()
            return resp.json()
        except HTTPError as e:
            if 500 <= e.response.status_code < 600:
                raise RequestException(f"Server error {e.response.status_code}")
            raise

    def search_issues(self, jql, start_at=0, max_results=50, fields="*all"):
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": fields
        }
        return self.get("/rest/api/2/search", params=params)

    def get_issue(self, issue_key, fields="*all", expand=None):
        params = {"fields": fields}
        if expand:
            params["expand"] = expand
        return self.get(f"/rest/api/2/issue/{issue_key}", params=params)
