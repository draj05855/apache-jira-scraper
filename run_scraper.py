import argparse, json, os, time, logging
from tqdm import tqdm
import orjson

from scraper.client import JiraClient
from scraper.normalizer import normalize_issue
from scraper.checkpoint import Checkpoint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_jsonl_line(fp, obj):
    fp.write(orjson.dumps(obj).decode() + "\n")

def run(project_key, out_dir="out", page_size=50, resume=True, max_pages=None):
    os.makedirs(out_dir, exist_ok=True)
    client = JiraClient()
    checkpoint = Checkpoint(os.path.join(out_dir, "state.json"))
    state = checkpoint.get(project_key) if resume else None
    start_at = state.get("start_at", 0) if state else 0

    out_path = os.path.join(out_dir, f"{project_key}.jsonl")
    with open(out_path, "a", encoding="utf-8") as fout:
        page_count = 0
        while True:
            if max_pages and page_count >= max_pages:
                break
            jql = f'project = {project_key} ORDER BY created ASC'
            resp = client.search_issues(jql, start_at=start_at, max_results=page_size)
            issues = resp.get("issues", [])
            total = resp.get("total", 0)
            if not issues:
                break
            for issue in tqdm(issues, desc=f"{project_key} issues"):
                try:
                    full_issue = client.get_issue(issue["key"], fields="*all")
                    norm = normalize_issue(full_issue)
                    write_jsonl_line(fout, norm)
                except Exception as e:
                    logger.error("Error processing issue %s: %s", issue.get("key"), e)
                finally:
                    start_at += 1
                    checkpoint.set(project_key, {"start_at": start_at, "last_updated": time.time()})
            page_count += 1
            if start_at >= total:
                break
    logger.info("Completed project %s", project_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project key, e.g., HADOOP")
    parser.add_argument("--out_dir", default="out")
    parser.add_argument("--page_size", type=int, default=50)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max_pages", type=int, default=None)
    args = parser.parse_args()
    run(args.project, out_dir=args.out_dir, page_size=args.page_size, resume=args.resume, max_pages=args.max_pages)
