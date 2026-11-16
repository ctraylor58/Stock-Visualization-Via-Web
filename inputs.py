from datetime import datetime

CHART_TYPES = {"1": "Bar", "2": "Line"}
TIME_SERIES = {
    "1": ("TIME_SERIES_INTRADAY", "Intraday (60 min)"),
    "2": ("TIME_SERIES_DAILY", "Daily"),
    "3": ("TIME_SERIES_WEEKLY", "Weekly"),
    "4": ("TIME_SERIES_MONTHLY", "Monthly"),
}


def get_symbol():
    while True:
        symbol = input("Enter the stock symbol (e.g. IBM): ").strip().upper()
        if symbol and len(symbol) <= 10 and all(c.isalnum() or c in ".-" for c in symbol):
            return symbol
        print("Invalid symbol. Enter a valid ticker, e.g. AAPL or BRK.B.")


def _choose(title, options):
    print(f"\n{title}")
    print("-" * len(title))
    for key, value in options.items():
        label = value[1] if isinstance(value, tuple) else value
        print(f"{key}. {label}")
    while True:
        choice = input("Enter your choice: ").strip()
        if choice in options:
            return options[choice]
        print(f"Please enter one of: {', '.join(options)}")


def get_chart_type():
    return _choose("Chart types", CHART_TYPES)


def get_time_series():
    return _choose("Select the time series", TIME_SERIES)


def _get_date(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, e.g. 2024-03-15.")


def get_date_range():
    start = _get_date("Enter the begin date (YYYY-MM-DD): ")
    while True:
        end = _get_date("Enter the end date (YYYY-MM-DD): ")
        if end >= start:
            return start, end
        print("The end date cannot be before the begin date.")
