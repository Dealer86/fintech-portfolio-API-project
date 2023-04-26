# Fintech Portfolio API

The Fintech Portfolio API is a web server with a REST API that allows you to keep track of your different financial assets and compare their evolution over time.

![API Screenshot](/finance-project/api2.jpg)

## Deployment Instructions

### Windows
1. Clone the git repository using `<git_repo_url>`
2. Navigate to the `cd finance-project` directory
3. Create a new virtual environment by running `python -m venv env/`
4. Activate the virtual environment by running `.\env\Scripts\activate`
5. Upgrade pip by running `python.exe -m pip install --upgrade pip`
6. Install the required dependencies by running `pip install -r requirements.txt`

### Linux
1. Clone the git repository using `<git_repo_url>`
2. Navigate to the `cd finance-project` directory
3. Create a new virtual environment by running `python3 -m venv env/`
4. Activate the virtual environment by running `source env/bin/activate`
5. Upgrade pip by running `pip install --upgrade pip`
6. Install the required dependencies by running `pip install -r requirements.txt`

## Technology Stack
This project uses the following technologies:
* FastAPI - a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints
* Uvicorn - a lightning-fast ASGI server, built on top of the asyncio event loop
* Yahooquery - a Python library that allows you to query Yahoo Finance data in a simple and efficient way
* Yfinance - a Python library that provides a simple way to download historical market data from Yahoo Finance
* Matplotlib - a Python library for creating static, animated, and interactive visualizations in Python

## Resources
For more information about FastAPI, visit their [official documentation](https://fastapi.tiangolo.com/).

For more information about yahooquery, visit their [official documentation](https://yahooquery.dpguthrie.com/).

For more information about yfinance, visit their [official documentation](https://pypi.org/project/yfinance/).

For more information about Matplotlib, visit their [official documentation](https://matplotlib.org/stable/index.html)