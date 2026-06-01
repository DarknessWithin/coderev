import requests
from fastapi import FastAPI, Request
from requests.auth import HTTPBasicAuth

from bitbucket import (
    get_pr_diff,
    post_inline_comment
)

from reviewer import review_code

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    EMAIL = "112005tani@gmail.com"
    TOKEN = "ATATT3xFfGF04MTorFR_14Qml4Y-ChBQp9m7vsmrTh8PVaE_UU-Soc77_U2hD9Y1cd58c_MRmt5h0NkCo_Lb403KxPeU5gveWEv9n3N86-l2DXM42OQMkDnZ6XYYCMZWFvnQFyhfKFu4C_C7bzLZHVrOezUfMGDRLSPyO-k1zpIi0EHY21hQeGE=06075101"

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