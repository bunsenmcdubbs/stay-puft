# stay-puft
HackTech 2017

## Project Layout
1. Gather Data
2. Populate Database
3. Visualize Data

## Getting Started
1. (optional, recommended) Make a Python (3.6) virtual environment
2. `pip install -r requirements.txt`
3. Create/start a MySQL database and set up the database configuration (`cp config.json.example config.json` and edit)
4. Initialize the database `mysql -u $MYSQL_USERNAME -p $MYSQL_SCHEMA < data/schema/XX-SQL_SCRIPT.sql`
5. `cd data/collect`
6. Load hackathons from hackalist.org `python hackalist.py YEAR MONTH`
7. Scrape projects from devpost `python devpost.py`


See Kenneth Reitz's description for [this workflow utilizing](https://www.kennethreitz.org/essays/a-better-pip-workflow)
`requirements.txt` and `requirements-to-freeze.txt`
