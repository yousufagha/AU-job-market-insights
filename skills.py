"""Skill extraction for the ITW601 job market dataset.

The first version matched skills as plain substrings, so "Go" matched
"good", "SSIS" matched "assist", "Scala" matched "scalable" and "Excel"
matched "excellent". This module matches whole words only.

Run it directly to re-derive the Skills and skill_count columns of
cleaned_data.csv from the Description column:

    python skills.py
"""
import re
import sys

import pandas as pd

KEYWORDS = [
    "Python", "SQL", "Java", "JavaScript", "C++", "C#", "C Programming", "R Programming",
    "Scala", "Go", "Ruby", "PHP", "Shell", "PowerShell", "Bash", "TypeScript",
    "HTML", "CSS", "T-SQL", "VBA", "MATLAB", "Node.js", "React", "Angular",
    "Vue.js", "Express", "Next.js", "Flask", "Django", "ASP.NET", "Spring", "jQuery",
    "Laravel", "Symfony", "Ruby on Rails", "FastAPI", "Phoenix", "AWS", "Azure", "GCP",
    "IBM Cloud", "Oracle", "Firebase", "Redshift", "Snowflake", "DataBricks", "BigQuery", "Digital Ocean",
    "OpenStack", "Colocation", "Watson", "VMware", "Heroku", "SQL Server", "MySQL", "PostgreSQL",
    "Cassandra", "MongoDB", "ElasticSearch", "DynamoDB", "Redis", "DB2", "Neo4j", "MariaDB",
    "CouchDB", "Couchbase", "SQLite", "Firestore", "Power BI", "Tableau", "Looker", "Excel",
    "Word", "SAP", "SAS", "SPSS", "Qlik", "SSIS", "SSRS", "Alteryx",
    "MicroStrategy", "Google Sheets", "Spreadsheets", "DAX", "Outlook", "Visio", "MS Access", "DataRobot",
    "Splunk", "Jira", "Confluence", "Linux", "Linux Shell", "Zsh", "Windows Server", "Active Directory",
    "Group Policy", "Networking", "Switching", "Routing", "Firewalls", "VPN", "Remote Desktop", "TensorFlow",
    "PyTorch", "NumPy", "Pandas", "Scikit-learn", "Keras", "Jupyter", "Matplotlib", "Seaborn",
    "NLTK", "OpenCV", "GraphQL", "Airflow", "Spark", "Kafka", "Hadoop", "Hive",
    "ETL", "DevOps", "CI/CD", "Git", "GitHub", "Bitbucket", "Terraform", "Ansible",
    "Jenkins", "Bamboo", "Nagios", "Prometheus", "Grafana", "New Relic", "Datadog", "Logstash",
    "Snort", "Wireshark", "OAuth", "SSO", "SAML", "LDAP", "IT Support", "Service Desk",
    "Help Desk", "Desktop Support", "Machine Learning", "Deep Learning", "NLP", "Microservices", "RESTful Services", "SOAP",
    "Rest API", "Salesforce", "Zoho", "HubSpot", "Dynamics 365", "Shopify", "WordPress", "WooCommerce",
    "Magento", "Bootstrap", "Tailwind", "Webpack", "Agile", "Scrum", "Kanban", "ITIL",
]

# Short or common-word skills only count when written with their usual
# capitalisation ("Go", not "go"; "Excel", not "excel at").
CASE_SENSITIVE = {"Go", "R", "Excel", "Spark", "Hive", "Shell"}

# Phrases that look like a skill but are not one.
EXCLUDE_AFTER = {"Go": r"(?!\s+to\b)(?!-live)"}


def _pattern(skill):
    flags = 0 if skill in CASE_SENSITIVE else re.IGNORECASE
    body = r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9+#])"
    return re.compile(body + EXCLUDE_AFTER.get(skill, ""), flags)


PATTERNS = {skill: _pattern(skill) for skill in KEYWORDS}


def extract_skills(text):
    """Return a sorted, comma-separated string of skills found in text."""
    text = str(text) if text is not None else ""
    found = sorted(skill for skill, pat in PATTERNS.items() if pat.search(text))
    return ", ".join(found)


def rebuild(path="cleaned_data.csv"):
    df = pd.read_csv(path)
    before = df["Skills"].fillna("").str.split(", ").explode()
    df["Skills"] = df["Description"].apply(extract_skills)
    df["skill_count"] = df["Skills"].apply(lambda s: len(s.split(", ")) if s else 0)
    df["Skills"] = df["Skills"].replace("", pd.NA)
    df.to_csv(path, index=False)
    after = df["Skills"].dropna().str.split(", ").explode()
    print(f"Rebuilt {path}: {len(df)} rows")
    print("Top skills before:", before[before != ""].value_counts().head(8).to_dict())
    print("Top skills after: ", after.value_counts().head(8).to_dict())


if __name__ == "__main__":
    rebuild(*sys.argv[1:])
