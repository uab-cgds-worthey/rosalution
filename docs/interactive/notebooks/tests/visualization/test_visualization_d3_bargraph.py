from core.visualization.d3_bargraph import d3_bar_graph_example

def test_creating_d3_bargraph_html_template_plot():
    mock_app_data = [
        {"category": "A", "value": 30},
        {"category": "B", "value": 80},
        {"category": "C", "value": 45},
        {"category": "D", "value": 60}
    ]

    plot_html = d3_bar_graph_example(mock_app_data)
    assert 'id="sankey_plot"' in plot_html
