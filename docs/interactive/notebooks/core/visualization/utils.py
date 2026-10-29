from string import Template

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r},{g},{b},{alpha:.2f})"

def d3_plot_viz(styles, d3_javascript) -> Template:
    html_template_string = f"""<style>
{styles}
</style>

<div id="$dom_id"></div>

<script type="module">
(async () => {{
    const d3 = await import("https://cdn.skypack.dev/d3");

    {d3_javascript}
}})();
</script>"""

    return Template(html_template_string)
