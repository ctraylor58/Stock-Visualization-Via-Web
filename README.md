# Stock Data Visualizer — Project 3A

A Flask web version of the Project 3 stock visualizer. It uses the existing Alpha Vantage API workflow and Pygal charts, and includes Docker support.

## S&P 500 stock list

The supplied `stocks.csv` has been included in `data/stocks.csv`. It contains 500 rows and uses the headers `Symbol`, `Name`, and `Sector`. The app reads the `Symbol` column to populate the stock dropdown.

## 1. Set up the API key

1. Copy `.env.example` to a file named `.env`.
2. Replace the placeholder with your Alpha Vantage API key:

   `ALPHAVANTAGE_API_KEY=your_actual_key`

Do not commit `.env` to GitHub. The `.gitignore` and `.dockerignore` files exclude it.

## 2. Run locally

Use Python 3.11 or newer.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Start Flask:

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## 3. Run with Docker Compose

After creating `.env` and replacing the starter CSV:

```bash
docker compose up --build
```

Open `http://localhost:5000`. Stop the app with `Ctrl+C`, or run `docker compose down`.

## Included files

- `app.py`: Flask web application
- `api.py`: Alpha Vantage requests and date filtering
- `charts.py`: Pygal chart creation
- `inputs.py`, `main.py`: original-style command-line interface from Project 3
- `templates/index.html`: browser form and chart display
- `data/stocks.csv`: starter ticker file; replace with the full class CSV
- `Dockerfile`, `docker-compose.yml`: container configuration

## Notes

- The dropdown reads ticker symbols from `data/stocks.csv`.
- Supported chart types: Bar and Line.
- Supported data intervals: Intraday (60 min), Daily, Weekly, Monthly.
- Alpha Vantage may enforce API request limits or return informational messages; the app displays those as errors.
- This starter package has not been tested with your instructor's exact CSV or your personal API key. Verify those before submission.
