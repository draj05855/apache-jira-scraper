from bs4 import BeautifulSoup

def html_to_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    return soup.get_text(separator="\n").strip()

def normalize_issue(issue_json):
    fields = issue_json.get("fields", {})
    key = issue_json.get("key")
    desc_html = fields.get("description") or ""
    description = html_to_text(desc_html)
    comments = fields.get("comment", {}).get("comments", []) if fields.get("comment") else []

    comments_list = []
    for c in comments:
        comments_list.append({
            "author": c.get("author", {}).get("displayName"),
            "body": html_to_text(c.get("body", "")),
            "created": c.get("created")
        })

    return {
        "id": key,
        "project": fields.get("project", {}).get("key"),
        "title": fields.get("summary"),
        "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "status": fields.get("status", {}).get("name") if fields.get("status") else None,
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "labels": fields.get("labels") or [],
        "created_at": fields.get("created"),
        "updated_at": fields.get("updated"),
        "description": description,
        "comments": comments_list,
        "derived": {
            "summary": (description[:240] + "...") if len(description) > 240 else description,
            "qna": []
        }
    }
