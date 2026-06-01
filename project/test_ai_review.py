from bitbucket import get_pr_diff
from reviewer import review_code

workspace = "tanishq_sh"
repo_slug = "tsr"
pr_id = 3

diff = get_pr_diff(workspace, repo_slug, pr_id)

review = review_code(diff)

print(review)