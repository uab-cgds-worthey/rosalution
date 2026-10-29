from core.visualization.utils import d3_plot_viz

def test_creating_d3_html_template():
    styling = """.bar { fill: #4f46e5; transition: fill 0.2s; }
.bar:hover { fill: #4338ca; }"""
    d3_code = """const fake = d3 code here;
    fake.run_thing()
    print($test_data)
    print('id="$dom_id"')"""

    actual_template = d3_plot_viz(styling, d3_code)
    expected_template = """<style>
.bar { fill: #4f46e5; transition: fill 0.2s; }
.bar:hover { fill: #4338ca; }
</style>

<div id="$dom_id"></div>

<script type="module">
(async () => {
    const d3 = await import("https://cdn.skypack.dev/d3");

    const fake = d3 code here;
    fake.run_thing()
    print($test_data)
    print('id="$dom_id"')
})();
</script>"""

    assert actual_template.template == expected_template

   