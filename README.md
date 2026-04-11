# Energy DBT AI Model

This project is a personal endeavour to learn and research energy-market relevant data engineering product. 

## Data Sources
* Texas RRC
* EIA
* EPA GHGRP 

## Stack
### Ingestion & Orchestration

* **Python** (requests, pandas, httpx) for API pulls and file ingestion
* **Apache Airflow** (local via Docker) or just scheduled Python scripts to start — don't overcomplicate orchestration early
* Raw data lands in **PostgreSQL** staging schemas

### Transformation Layer

* **dbt Core** (local, free) — this is the right call. You define your staging → intermediate → mart layers here. Version controlled, tested, documented.

### AI/ML

* **Python**: scikit-learn, XGBoost, PyTorch or LightGBM depending on the use case
* Optionally: **MLflow** (local) for experiment tracking — adds a lot of credibility to the project

### Analytics / Reporting

* **Plotly Dash** (Python, local, free) — much better for a data engineering project than Tableau since it stays fully in-code and you can embed model outputs directly. 

## Schedule
**Project Start:** April 3, 2026

**Project End (Est.):** June 5

----

This project will occur over an eight-week duration: 

**Week 1**: Environment setup (Postgres, dbt init, Airflow/scripts). Ingest RRC + EIA raw files. Audit/master log table.

**Week 2**: Ingest EPA GHGRP. Staging layer + data profiling/EDA. Operator name reconciliation. Document data quality findings.

**Week 3**: Intermediate dbt models. Dim tables (well, operator, formation, geography). dbt tests written in parallel.

**Week 4**: Fact tables + data mart. Economics mart (breakeven, LOE/BOE). Finalize dbt documentation.

**Week 5**: Feature engineering + model selection. Decline curve fitting, EUR distribution, anomaly detection. MLflow tracking.

**Week 6**: Model validation, retraining pipeline on data refresh cadence. Finalize advanced analytics narrative.

**Week 7**: Plotly Dash dashboard build. Map view, operator benchmarking, model output overlays.

**Week 8**: Polish, dbt docs site, README, Docker Compose packaging, publishing to GitHub and gain traction online (Reddit, Medium posts).

# References 

https://www.eia.gov/opendata/documentation.php#Understandingreturneder || Rate limit of 5000 rows in JSON format for EIA API call