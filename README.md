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

# References 

https://www.eia.gov/opendata/documentation.php#Understandingreturneder || Rate limit of 5000 rows in JSON format for EIA API call

### Next Steps: 

Pivoting off of integrating multiple data-sources, instead will focus on building a prototype with EIA data. And initial data modelling and ML application.

- Build out DBT model for ML and for 

### Progress Notes: 
- Load data: WTI Crude Spot Price (Daily), Natural Gas Spot Price (Henry Hub, daily), Weekly Crude Inventory (US Total Stocks)
- Will need to look into natural-gas/prod/ngpl, where some values for datetime were of invalid format and could not be transformed, need to address this issue with a function that looks through datetime values and will default to a value

- Need to make functions into one class and create a new obj of the class whenever you want to injest via a route of EIA API call -> call it EIALoader obj

### Modelling: 

To bring in best-in-class modelling techniques, refrencing academic papers and published Kaggle models will be the most efficient way to adopt best-practices and academic standard modelling techniques. 

