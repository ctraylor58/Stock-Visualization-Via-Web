import csv
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request

import api
import charts

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
STOCK_FILE = BASE_DIR / "data" / "stocks.csv"

CHART_TYPES = ["Bar", "Line"]
TIME_SERIES = {
    "Intraday (60 min)": "TIME_SERIES_INTRADAY",
    "Daily": "TIME_SERIES_DAILY",
    "Weekly": "TIME_SERIES_WEEKLY",
    "Monthly": "TIME_SERIES_MONTHLY",
}


def load_stocks():
    """Read ticker symbols from data/stocks.csv (Symbol or Ticker column)."""
    try:
        with STOCK_FILE.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("The stocks.csv file is empty or has no header.")

            symbol_column = next(
                (
                    name for name in reader.fieldnames
                    if name and name.strip().lower() in {"symbol", "ticker"}
                ),
                None,
            )
            if symbol_column is None:
                raise ValueError(
                    "stocks.csv must contain a column named 'Symbol' or 'Ticker'."
                )

            symbols = sorted({
                (row.get(symbol_column) or "").strip().upper()
                for row in reader
                if (row.get(symbol_column) or "").strip()
            })
            if not symbols:
                raise ValueError("No stock symbols were found in stocks.csv.")
            return symbols
    except (OSError, csv.Error) as exc:
        raise ValueError(f"Could not read {STOCK_FILE}: {exc}") from exc


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    chart_html = None
    try:
        stocks = load_stocks()
    except ValueError as exc:
        stocks = []
        error = str(exc)

    selected_stock = ""
    selected_chart = "Line"
    selected_series = "Daily"
    start_date = ""
    end_date = ""

    if request.method == "POST" and not error:
        selected_stock = request.form.get("stock", "").strip().upper()
        selected_chart = request.form.get("chart_type", "")
        selected_series = request.form.get("time_series", "")
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()

        try:
            if selected_stock not in stocks:
                raise ValueError("Please choose a stock from the dropdown.")
            if selected_chart not in CHART_TYPES:
                raise ValueError("Please choose Bar or Line for the chart type.")
            if selected_series not in TIME_SERIES:
                raise ValueError("Please choose a valid time series.")
            if not start_date or not end_date:
                raise ValueError("Please enter both a start date and an end date.")

            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end < start:
                raise ValueError("The end date cannot be before the start date.")

            function = TIME_SERIES[selected_series]
            series = api.fetch_stock_data(selected_stock, function)
            rows = api.filter_by_date(series, start, end)
            chart = charts.build_chart(
                rows, selected_stock, selected_chart,
                selected_series, start, end
            )
            chart_html = chart.render().decode("utf-8")

        except (ValueError, api.StockDataError) as exc:
            error = str(exc)
        except Exception:
            app.logger.exception("Unexpected application error")
            error = "Something went wrong. Check the application log and try again."

    return render_template(
        "index.html",
        stocks=stocks,
        chart_types=CHART_TYPES,
        time_series=list(TIME_SERIES.keys()),
        selected_stock=selected_stock,
        selected_chart=selected_chart,
        selected_series=selected_series,
        start_date=start_date,
        end_date=end_date,
        chart=chart_html,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
