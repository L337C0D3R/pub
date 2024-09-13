import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Example usage for a POST request:
url = "https://api.example.com/resource"
headers = {
    "Authorization": "Bearer your_token",
    "Content-Type": "application/json"
}
cookies = {
    "session_id": "your_session_id"
}
body = {
    "key1": "value1",
    "key2": "value2"
}

try:
    response = requests_retry_session().post(
        url,
        headers=headers,
        cookies=cookies,
        json=body  # For JSON payloads, use `json=body`
    )
    response.raise_for_status()  # Raises HTTPError if the response was an error
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
else:
    print(response.content)
