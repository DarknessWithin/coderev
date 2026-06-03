import json
import requests
import re

from config import OPENROUTER_API_KEY

URL = "https://openrouter.ai/api/v1/chat/completions"


SYSTEM_PROMPT = """
You are an expert pull request reviewer.

Review ONLY the provided git diff.

STRICT RULES:
- ONLY report issues that are explicitly visible in the diff.
- DO NOT assume surrounding code or missing context.
- DO NOT hallucinate functions, imports, or behavior.
- ONLY comment on lines that are directly shown in the diff.
- DO NOT comment on unchanged code.

Allowed issue types:
- runtime bugs
- logic errors
- security issues
- unsafe type conversions
- missing edge case handling

NOT allowed:
- style issues
- naming issues
- formatting issues
- hypothetical problems
- suggestions without clear evidence in diff

VERY IMPORTANT RULES:
- Each issue MUST be tied to a specific line shown in the diff.
- The "line" field MUST correspond exactly to the line number in the diff context.
- If unsure about the exact line, DO NOT include the issue.
- Do NOT guess line numbers.
- Before reporting an issue, verify that the code shown in the diff does not already handle that case.
- Do not report API design preferences as bugs.

Line type rules:
- "NEW" = lines starting with '+'
- "OLD" = lines starting with '-'

SELF-CHECK BEFORE RESPONDING:
1. Every issue must be directly visible in the diff
2. No assumption outside diff
3. Line number must exist in provided diff context
4. JSON must be valid

Return ONLY raw JSON.
Do NOT use markdown.
Do NOT explain anything.
Do NOT add extra keys.

FORMAT (MUST NOT CHANGE):
[
  {
    "file": "app.py",
    "line": 10,
    "line_type": "NEW",
    "severity": "MEDIUM",
    "category": "bug",
    "comment": "float(amount) may raise ValueError for invalid input."
  }
]
"""
def preprocess_diff(diff_text):
    """
    Keeps original format but adds structure hints
    without changing output schema.
    """

    lines = diff_text.splitlines()
    result = []

    for line in lines:
        # keep file headers
        if line.startswith("diff --git"):
            result.append(f"\nFILE: {line}")
            continue

        # keep hunk headers (VERY important for line grounding)
        if line.startswith("@@"):
            result.append(f"HUNK: {line}")
            continue

        # preserve original diff lines (do NOT reformat structure heavily)
        result.append(line)

    return "\n".join(result)
def clean_json_response(content):
    if not content:
        return []

    content = content.strip()

    # remove markdown fences if any
    content = re.sub(r"^```(json)?", "", content)
    content = re.sub(r"```$", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return []
def review_code(diff_text: str):
    processed_diff = preprocess_diff(diff_text)
    prompt = f"""
    Review this git diff carefully.

    You must ONLY use information visible in the diff.
    Do not assume missing context.
    
    Git diff:
    ```diff
    {processed_diff}
"""

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "temperature": 0.05,
        "top_p": 0.95,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(URL, headers=headers, json=payload)
    r.raise_for_status()

    data = r.json()
    content = data["choices"][0]["message"]["content"]

    print("\nRAW LLM RESPONSE:\n", content)

    return clean_json_response(content)
