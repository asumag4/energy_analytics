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

## Deployment -> Installable Application 

Planning on adding a main.py where it will initialize all the requirements for the app to work on anyone else's machines locally. Interactive through the CLI, and maybe through a Streamlit app as a later rendition. 

## Engineering: uv 

To run jupyter notebooks, make sure to start a kernel through uv: 

`uv run python -m ipykernel install --user --name energy-dbt-ai --display-name "energy-dbt-ai"`

Then select this kernel as the runtime for a jupyter-notebook's executions

# References 

https://www.eia.gov/opendata/documentation.php#Understandingreturneder || Rate limit of 5000 rows in JSON format for EIA API call

https://github.com/antoniodagnino/Oil-Gas-Drilling-Activity-Prediction.git || Oil-Gas-Drilling-Activity-Prediction

### Future Work

- [ ] Employ production model into main, save everything else into a dev/test branch (notebooks)
- [ ] Use Airflow
- [ ] Use Docker to make project deployable into other environments -> make command-line interface to produce analytics, statistical outputs and graphs
- [ ] Include Petrinex data

