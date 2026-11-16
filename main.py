"""Command-line version from Project 3; the Project 3A web app uses app.py."""
import api
import charts
import inputs


def main():
    print("Stock Data Visualizer")
    print("---------------------")
    while True:
        symbol = inputs.get_symbol()
        chart_type = inputs.get_chart_type()
        function, series_label = inputs.get_time_series()
        start, end = inputs.get_date_range()

        try:
            series = api.fetch_stock_data(symbol, function)
            rows = api.filter_by_date(series, start, end)
        except api.StockDataError as exc:
            print(f"\nError: {exc}\n")
        else:
            chart = charts.build_chart(
                rows, symbol, chart_type, series_label, start, end
            )
            path = "stock_chart.svg"
            chart.render_to_file(path)
            print(f"\nChart saved as {path}.")

        again = input("\nView more stock data? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
