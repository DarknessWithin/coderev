import requests
from requests.auth import HTTPBasicAuth

from config import (
    BITBUCKET_EMAIL,
    BITBUCKET_API_TOKEN
)

BASE_URL = "https://api.bitbucket.org/2.0"


def get_pr_diff(workspace, repo_slug, pr_id):
    url = f"{BASE_URL}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/diff"

    r = requests.get(
        url,
        auth=HTTPBasicAuth(
            BITBUCKET_EMAIL,
            BITBUCKET_API_TOKEN
        )
    )

    r.raise_for_status()

    return r.text


import requests

from requests.auth import HTTPBasicAuth

from config import (
    BITBUCKET_EMAIL,
    BITBUCKET_API_TOKEN
)

BASE_URL = "https://api.bitbucket.org/2.0"


def post_inline_comment(
    workspace,
    repo_slug,
    pr_id,
    file_path,
    line_number,
    message,
    line_type="NEW"
):
    url = (
        f"{BASE_URL}/repositories/"
        f"{workspace}/{repo_slug}/pullrequests/{pr_id}/comments"
    )

    inline_data = {
        "path": file_path
    }

    if line_type == "OLD":
        inline_data["from"] = line_number
    else:
        inline_data["to"] = line_number

    payload = {
        "content": {
            "raw": message
        },
        "inline": inline_data
    }

    r = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(
            BITBUCKET_EMAIL,
            BITBUCKET_API_TOKEN
        )
    )

    print("BITBUCKET RESPONSE:")
    print(r.status_code)
    print(r.text)

    r.raise_for_status()

    return r.json()