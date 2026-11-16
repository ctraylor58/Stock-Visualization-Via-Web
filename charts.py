import pygal


def build_chart(rows, symbol, chart_type, series_label, start, end):
    """Build a Pygal chart and return it for display in the Flask page."""
    chart_class = pygal.Bar if chart_type == "Bar" else pygal.Line
    chart = chart_class(
        title=f"Stock Data for {symbol}: {start} to {end} ({series_label})",
        x_label_rotation=35,
        x_labels_major_count=12,
        show_minor_x_labels=False,
        legend_at_bottom=True,
        width=1100,
        height=600,
    )
    chart.x_labels = [timestamp for timestamp, _ in rows]
    for field in ("open", "high", "low", "close"):
        chart.add(field.capitalize(), [values[field] for _, values in rows])
    return chart
