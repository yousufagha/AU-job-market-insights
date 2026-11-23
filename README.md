# Job Market Insights: entry-level IT roles in Australia

A team project for ITW601 (Torrens University) that scrapes 9,000 Australian IT job ads from Jora, extracts the skills each one asks for, and presents the results in an interactive Plotly Dash dashboard.

I was the team lead: I scraped all of the data and wrote most of the code (scraper, cleaning, skill extraction and dashboard).

## What it answers

- Which states and cities are hiring for entry-level IT roles
- Which skills employers ask for most, overall and by city
- How much experience the ads expect
- Which companies post the most roles

## Repository

| File | What it does |
| --- | --- |
| `multipage_main.ipynb` | Selenium scraper that pages through Jora results and saves the raw ads |
| `main.ipynb` | Earlier single-page version of the scraper |
| `enriched_jora_jobs_9000.csv` | Raw scraped data (9,000 ads) |
| `data_cleaning.ipynb` | Cleans the raw data and adds `job_level`, `desc_length` and `Experience_log` |
| `skills.py` | Whole-word skill extraction; also rebuilds the `Skills` column |
| `cleaned_data.csv` | Cleaned dataset the dashboard reads |
| `data_analysis.ipynb`, `dataset_analysis.ipynb` | Exploratory analysis and KMeans clustering of job titles |
| `dashboard.py` | Plotly Dash dashboard |

## Run it

```bash
pip install -r requirements.txt
python dashboard.py
```

Then open http://127.0.0.1:8050.

To re-derive the skills in `cleaned_data.csv` from the job descriptions:

```bash
python skills.py
```

## Skill extraction fix (November 2026)

The first version matched skills as plain substrings, which inflated several counts: "Go" matched "good" (841 ads tagged, 42 genuine), "SSIS" matched "assist", "Scala" matched "scalable" and "Excel" matched "excellent". `skills.py` now matches whole words, keeps short skills such as Go and R case-sensitive, and ignores phrases like "Go to". `cleaned_data.csv` has been rebuilt with it.

Top skills after the fix: AWS, Azure, Python, SQL, Agile, React, IT Support, Networking.

`enriched_jora_jobs_9000.csv` is left as scraped, so its `Skills` column still has the old substring matches.

## Licence

See [LICENSE](LICENSE).
