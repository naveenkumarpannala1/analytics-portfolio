# Analytics Portfolio - Naveenkumar Pannala

Three independent case studies using synthetic data. No employer or customer data is included.

Live portfolio: https://naveen-analytics-portfolio.ochreiris32.chatgpt.site

## Projects
- Checkout & conversion: SQL funnel analysis, simulated experiment, confidence interval, and QA.
- Revenue operations: mature-cohort channel efficiency, grain-safe spend joins, and CRM flags.
- Banking Power BI: embedded synthetic CSVs, dimensional model, eleven DAX measures, and three report pages.

## Review the evidence
Each project includes a README describing metric definitions and limitations. Checkout and revenue contain analysis.sql; the linked data bundles include analysis.sqlite for running queries independently with SQLite. Banking contains validate_source.py and validation_results.json.

## Reproduce
Use Python 3 with the requirements in requirements.txt. Running `python build_projects.py` regenerates the checkout and revenue synthetic datasets, readmes, analysis databases, and dashboard aggregates with a fixed seed. It writes web assets to ../dist. Run in a disposable copy if you want to preserve the original outputs. Banking uses frozen CSV snapshots embedded in M and is independent of this generator.

Run `python Banking_PowerBI/validate_source.py` for embedded-data and structural checks. It does not execute DAX/M or render visuals. See Banking_PowerBI/DESKTOP_CHECKLIST.md for native checks.

## Project status and contribution
Project scaffolding, analysis code, and presentation were developed with AI assistance. Review the code and assumptions before adapting or presenting them. Professional experience described on the portfolio is separate from these synthetic case studies. Native Power BI refresh and rendering remain pending; no validated PBIX is included.

## Datasets and downloads

Large raw data snapshots and SQLite databases are downloadable from the live case studies. The source generator regenerates checkout and revenue snapshots.

- [Checkout data, SQL and SQLite](https://naveen-analytics-portfolio.ochreiris32.chatgpt.site/assets/checkout-conversion.zip)
- [Revenue operations data, SQL and SQLite](https://naveen-analytics-portfolio.ochreiris32.chatgpt.site/assets/revenue-operations.zip)
- [Complete portable Power BI source](https://naveen-analytics-portfolio.ochreiris32.chatgpt.site/assets/Banking_PowerBI_Project.zip)
- [Guided project walkthroughs](https://naveen-analytics-portfolio.ochreiris32.chatgpt.site/walkthrough.html)
