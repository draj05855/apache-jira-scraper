# 🐍 Apache JIRA Scraper

This project is a **data scraping and transformation pipeline** that extracts public issue data from Apache’s Jira instance (https://issues.apache.org/jira/) and converts it into structured JSON files suitable for further analysis or training Large Language Models (LLMs).

---

## 🧠 Overview

The goal of this project is to:
- Scrape issues from Apache JIRA for multiple open-source projects (e.g., Hadoop, Spark, Kafka).
- Handle pagination and rate limiting efficiently.
- Store results in structured JSON files.
- Support checkpointing for resuming interrupted scrapes.

The scraper uses the **JIRA REST API** to collect issue details such as:
- Issue ID  
- Title  
- Reporter and Assignee  
- Status and Priority  
- Creation and Update Timestamps  
- Description and Comments  

---

## ⚙️ Environment Setup

Follow these steps to set up and run the scraper locally:

```bash
# Clone the repository
git clone https://github.com/<your-username>/apache-jira-scraper.git
cd apache-jira-scraper

# Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate      # On macOS/Linux
myenv\Scripts\activate         # On Windows

# Install dependencies
pip install -r requirements.txt
