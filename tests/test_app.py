import app


def test_header_is_present(dash_duo):
    dash_duo.start_server(app.app)

    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel Sales Visualiser" in header.text


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app.app)

    dash_duo.wait_for_element("#sales-line", timeout=10)
    # Graph renders plotly div inside the graph container
    plot = dash_duo.find_element("#sales-line .js-plotly-plot")
    assert plot is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app.app)

    dash_duo.wait_for_element("#region-radio", timeout=10)
    radio = dash_duo.find_element("#region-radio")
    assert radio is not None
