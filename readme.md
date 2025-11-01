# 🐍 Apache JIRA Scraper

A robust, fault-tolerant, and scalable **data scraping pipeline** that extracts issue data from [Apache’s public JIRA instance](https://issues.apache.org/jira/), normalizes it, and transforms it into a structured format suitable for analytical tasks or Large Language Model (LLM) training.

---

## 🧱 1. Setup Instructions & Environment Configuration

### 📦 Clone the Repository
```bash
git clone https://github.com/draj05855/apache-jira-scraper.git
cd apache-jira-scraper
🐍 Create a Virtual Environment
bash
Copy code
python -m venv env
source env/bin/activate       # Mac/Linux
env\Scripts\activate          # Windows
📚 Install Dependencies
bash
Copy code
pip install -r requirements.txt
🚀 Run the Scraper
bash
Copy code
python run_scraper.py --project HADOOP --out_dir data/hadoop --max_pages 5
python run_scraper.py --project SPARK --out_dir data/spark --max_pages 5
python run_scraper.py --project KAFKA --out_dir data/kafka --max_pages 5
Each run:

Scrapes issues from the specified project via JIRA REST API

Stores results as structured JSON files in the /data folder

Resumes automatically if interrupted (checkpointing)

🧠 2. Architecture Overview & Design Reasoning
🏗️ High-Level Architecture
pgsql
Copy code
┌──────────────────────────────┐
│        run_scraper.py        │  <-- Entry point
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Scraper             │
│  (client.py)                 │
│ - Handles API calls          │
│ - Manages pagination         │
│ - Respects rate limits       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Normalizer           │
│  (normalizer.py)             │
│ - Cleans JSON data           │
│ - Extracts key fields        │
│ - Handles nulls & formatting │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Checkpointing         │
│  (checkpoint.py)             │
│ - Saves progress             │
│ - Enables resume on failure  │
└──────────────────────────────┘
⚙️ Design Principles
API-Driven Scraping:
Instead of brittle HTML scraping, this system uses the official JIRA REST API, ensuring reliable, structured data retrieval.

Modular Design:
Each module (scraper, normalizer, checkpoint) handles one responsibility → easy to extend or replace.

Scalable and Fault-Tolerant:

Automatic retry on transient API failures

Checkpoint-based resume mechanism

Graceful handling of rate limits

LLM-Ready Output Format:
Data is cleaned and normalized into JSON fields that can directly feed NLP or fine-tuning pipelines.

⚖️ 3. Edge Cases & Handling
Edge Case	Description	Handling Strategy
Missing fields	Some issues lack reporters, assignees, or descriptions	Replaced with null to maintain schema consistency
API rate limit	Apache JIRA rate-limits requests per IP	Added controlled delay and retry mechanism
Pagination limit	Each page returns limited issues	Implemented looping pagination via JIRA’s startAt parameter
Network errors	Timeouts or dropped connections	Retry with exponential backoff
Long text bodies	Issue descriptions can exceed token limits	Truncated and cleaned safely before saving
Interrupted runs	System crashes or network failure mid-run	Checkpoint saves current index → resumes automatically

This ensures zero data corruption, no duplication, and resumable scrapes.

⚡ 4. Optimization Decisions & Future Improvements
✅ Current Optimizations
Checkpointing System – resumes scraping from the last successful page.

Batch Writes – writes data in chunks to minimize I/O overhead.

Backoff & Retry Logic – efficiently handles transient failures.

Minimal Dependencies – lightweight, easy to deploy anywhere.

🚀 Future Improvements
Asynchronous Requests – use aiohttp to speed up scraping.

Caching Layer – skip already downloaded pages.

Database Integration – push to MongoDB or SQLite for large-scale data management.

Metadata Enrichment – auto-generate summaries or extract Q&A pairs from descriptions.

CLI Interface – allow dynamic project selection and configuration.

🧾 Sample Output (JSON)
json
Copy code
{
  "id": "HADOOP-8",
  "project": "HADOOP",
  "title": "NDFS DataNode advertises localhost as it's address",
  "reporter": "Peter Sandström",
  "assignee": null,
  "status": "Closed",
  "priority": "Major",
  "created_at": "2005-07-24T23:46:18.000+0000",
  "updated_at": "2015-05-18T04:15:07.118+0000",
  "description": "Fixes the problem by connecting to the NameNode and using the bound address.",
  "comments": [
    {
      "author": "Doug Cutting",
      "body": "Perhaps this could use NetworkInterfaces.getInetAddresses() ...",
      "created": "2006-02-24T08:00:04.000+0000"
    }
  ]
}
🧩 Deliverables
✅ Complete, working codebase hosted here: Apache JIRA Scraper

✅ Comprehensive documentation (this README)

✅ Environment setup instructions & architecture explanation

✅ Edge cases and optimizations covered

✅ Public access granted to:

https://github.com/Naman-Bhalla/

https://github.com/raun/

👨‍💻 Author
Raj Kumar
B.Tech – Computer Science Engineering
Bennett University
GitHub: @draj05855
