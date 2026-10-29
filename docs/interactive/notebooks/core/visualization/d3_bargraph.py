import json

from .utils import d3_plot_viz

def d3_bar_graph_example(data) -> str:
    experiment_style_text = """.bar { fill: #4f46e5; transition: fill 0.2s; }
.bar:hover { fill: #4338ca; }
.axis-label { font-family: sans-serif; font-size: 12px; }"""
    d3_json_code = """const data = $data_payload;

    const container = d3.select("#$dom_id");
            
    const margin = {top: 20, right: 20, bottom: 40, left: 40};
    const width = 400 - margin.left - margin.right;
    const height = 200 - margin.top - margin.bottom;

    const svg = container.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    console.log(svg)
    const x = d3.scaleBand()
        .domain(data.map(d => d.category))
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([height, 0]);

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.category))
        .attr("width", x.bandwidth())
        .attr("y", d => y(d.value))
        .attr("height", d => height - y(d.value));

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .attr("class", "axis-label");

    svg.append("g")
        .call(d3.axisLeft(y))
        .attr("class", "axis-label");"""
    plot_template = d3_plot_viz(experiment_style_text, d3_json_code)
    plot_dom_id = "sankey_plot"

    return plot_template.safe_substitute(
        data_payload=json.dumps(data),
        dom_id=plot_dom_id
    )