import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from requests.auth import HTTPBasicAuth
import os
load_dotenv()
from bitbucket import (
    get_pr_diff,
    post_inline_comment
)

from reviewer import review_code

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    EMAIL = os.getenv("BITBUCKET_EMAIL")
    TOKEN = os.getenv("BITBUCKET_API_TOKEN")

    payload = await request.json()
    event = request.headers.get("X-Event-Key")

    print("EVENT:", event)

    if event not in [
        "pullrequest:created",
        "pullrequest:updated"
    ]:
        return {"message": "ignored"}

    pullrequest = payload["pullrequest"]

    pr_id = pullrequest["id"]

    repo = payload["repository"]

    full_name = repo["full_name"]

    workspace, repo_slug = full_name.split("/")

    print("Workspace:", workspace)
    print("Repo:", repo_slug)
    print("PR:", pr_id)

    diff = get_pr_diff(
        workspace,
        repo_slug,
        pr_id
    )

    issues = review_code(diff)

    for issue in issues:
        post_inline_comment(
            workspace=workspace,
            repo_slug=repo_slug,
            pr_id=pr_id,
            file_path=issue["file"],
            line_number=issue["line"],
            message=issue["comment"],
            line_type=issue["line_type"]
        )
    return {
        "status": "success"
    }
