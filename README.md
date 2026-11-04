# Data analytics portfolio: three Year Up capstones

Abdiel Picado. Three capstone projects from the Year Up United data analytics track (2025), cleaned
up and extended in 2026 so each one can be run, inspected and explained from this repo.

| # | Project | Question | Tools | What survived |
|---|---|---|---|---|
| 1 | [Hospital operations dashboard](01-hospital-operations-dashboard/) | How busy is the clinic, who carries the load, where do patients come from? | MySQL, SQL, Power BI | The 13-table schema (no data). Power BI file and report being recovered. |
| 2 | [Retail sales analysis](02-retail-sales-analysis/) | What drove ~$3.4M of revenue across 240 transactions, Jan to Aug 2024, and what should the business do? | Excel, data storytelling | Nothing yet. Workbook, memo and deck being recovered from the Year Up account. |
| 3 | [Salary prediction](03-salary-prediction/) | How much does a year of experience add to salary, and how sure can we be? | Python, pandas, statsmodels, matplotlib | Dataset, full original code, capstone slides. |

## How to read the labels

Every file in every project is one of three things, and the folder it sits in says which:

| Label | Folder | Meaning |
|---|---|---|
| **Original** | `original/` | Produced during the capstone. Unchanged. |
| **Reconstruction** | `reconstruction/` | Rebuilt in 2026 from recovered evidence (IPython history, the schema, the project proposal, the slides). The logic matches the original work; the file itself is new and says so in its header. |
| **Portfolio improvement** | `improvements/` | New work added in 2026 to take the project further than the capstone did. Not part of what was graded. Labeled in each file. |

`docs/` holds charts, the plain-English walkthrough and the talking points for each project.

Why the labels: the originals were stored in my Year Up Microsoft account, which was closed when the
program ended, and the local copies in Downloads are gone. Where I could recover the exact work
(salary project) it is reproduced and verified against the capstone slides. Where I could not
(retail), nothing is faked.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Salary model: tests, CLI, notebooks
pytest 03-salary-prediction
python 03-salary-prediction/improvements/predict.py --years 5

# Hospital: synthetic data -> SQLite -> dashboard queries (stock Python, no MySQL needed)
python 01-hospital-operations-dashboard/improvements/generate_synthetic_data.py
python 01-hospital-operations-dashboard/improvements/build_sqlite.py

# Notebooks (already executed, outputs render on GitHub)
jupyter notebook
```

## Privacy

- No real patient, employee or customer data anywhere in this repo.
- Hospital rows are synthetic: SSNs in the never-issued 900 series, 555-01xx phones, "City, ST" addresses.
- The salary dataset is the public 30-row Kaggle teaching set.
- Year Up course materials, assignment briefs and rubrics are not included.
- `incoming/` is a gitignored drop folder for recovered originals; nothing moves from there into a project without a privacy check first.
