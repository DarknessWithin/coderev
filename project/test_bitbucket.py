import requests
from requests.auth import HTTPBasicAuth

EMAIL = "112005tani@gmail.com"
TOKEN = "ATATT3xFfGF04MTorFR_14Qml4Y-ChBQp9m7vsmrTh8PVaE_UU-Soc77_U2hD9Y1cd58c_MRmt5h0NkCo_Lb403KxPeU5gveWEv9n3N86-l2DXM42OQMkDnZ6XYYCMZWFvnQFyhfKFu4C_C7bzLZHVrOezUfMGDRLSPyO-k1zpIi0EHY21hQeGE=06075101"

workspace = "tanishq_sh"
repo_slug = "tsr"
pr_id = 2

url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/diff"

r = requests.get(
    url,
    auth=HTTPBasicAuth(EMAIL, TOKEN)
)

print(r.status_code)
print(r.text[:3000])