
import json

import plotly.graph_objects as go
from string import Template


from collections import defaultdict
from ..enums import NAMESPACE_MAPPING, MODEL_SYSTEM_PHENOTYPE_ONTOLOGY_MAPPING

from .utils import hex_to_rgba, d3_plot_viz


def sankey_hpo_to_upheno_system_to_animal_model_systems(analysis_name: str):
    if not analysis_name:
        return "Rosalution Analysis HPO Terms → Monarch UPHENO Phenotype System Terms → Modelable Animal Model Systems (Toggle Terms On/Off)"
    
    return f"Rosalution '{analysis_name}' HPO Terms → Monarch UPHENO Phenotype System Terms → Modelable Animal Model Systems (Toggle Terms On/Off)"

def sankey_homologous_phenotype_terms_model_system(analysis_name: str):
    if not analysis_name:
        return "Rosalution Analysis HPO Term → Closest Homologous Term Ancestor → Animal Model System"

    return f"Rosalution '{analysis_name}' HPO Term → Closest Homologous Term Ancestor → Animal Model System"


def sankey_phenotype_system_modelsystem(data, analysis_name: str = ""):
    # colors to use for the upheno phenotype terms used to represent systems
    system_colors = {
        "nervous system phenotype": "rgba(214,39,40,0.8)",
        "musculature phenotype": "rgba(31,119,180,0.8)",
        "digestive system phenotype": "rgba(44,160,44,0.8)",
        "growth phenotype": "rgba(255,127,14,0.8)",
        "skeletal system phenotype": "rgba(148,103,189,0.8)",
        "craniocervical region phenotype": "rgba(140,86,75,0.8)",
        "integument phenotype": "rgba(160,227,183,0.8)",
        "genitourinary system phenotype": "rgba(17,105,102,0.8)",
        "connective tissue phenotype": "rgba(90,196,248,0.8)",
        "immune system phenotype": "rgba(28,53,183,0.8)",
        "breast phenotype": "rgba(159,216,65,0.8)",
        "eyeball of camera-type eye phenotype": "rgba(126,38,64,0.8)",
        "endocrine system phenotype": "rgba(253,156,186,0.8)",
        "hematopoietic system phenotype": "rgba(114,142,36,0.8)",
        "respiratory system phenotype": "rgba(56,240,172,0.8)",
        "Abnormality of the ear": "rgba(42,83,138,0.8)",
        "Abnormality of metabolism/homeostasis": "rgba(172,159,253,0.8)",
        "Neoplasm": "rgba(169,96,237,0.8)",
        "late embryo phenotype": "rgba(101,241,18,0.8)",
    }

    model_set = { *MODEL_SYSTEM_PHENOTYPE_ONTOLOGY_MAPPING.keys()}

    # mappings to match hpo phenotype terms to uphen phenotype system terms
    # and the upheno phenotype system terms to animal model systems
    # for nodes
    term_system_map = {}
    term_to_system = defaultdict(int)
    system_to_model = defaultdict(int)

    for record in data:
        system = record["system"]

        for term in record["terms"]:
            term = term.strip()
            term_system_map[term] = system
            term_to_system[(term, system)] += 1

        for model in record["modelsystem"]:
            system_to_model[(system, model)] += 1

    def build_sankey(include_terms=True):

        labels = set()
        sources, targets, values, link_colors = [], [], [], []

        # Phenotype term to Upheno System
        if include_terms:
            for (term, system), value in term_to_system.items():
                labels.update([term, system])

                sources.append(term)
                targets.append(system)
                values.append(value)

                link_colors.append(system_colors.get(system, "gray"))

        # Upheno phenotype system to model system -----
        for (system, model), value in system_to_model.items():
            labels.update([system, model])

            sources.append(system)
            targets.append(model)
            values.append(value)

            color = system_colors.get(system, "gray").replace("0.8", "0.25")
            link_colors.append(color)

        # indexing for the plotly sankey plot
        labels = list(labels)
        label_index = {l: i for i, l in enumerate(labels)}

        sources = [label_index[s] for s in sources]
        targets = [label_index[t] for t in targets]

        # Setting the node colors and positions;
        # Upheno phenotype systems colors and labels
        node_colors = []
        x_positions = []

        for label in labels:
            if label in model_set:
                node_colors.append("lightgray")
                x_positions.append(1)

            elif label in system_colors:
                node_colors.append(system_colors[label])
                x_positions.append(0.5)

            else:
                system = term_system_map.get(label)
                node_colors.append(system_colors.get(system, "lightblue"))
                x_positions.append(0 if include_terms else None)

        # Used to hide phenotype term labels
        def clean(label):
            return label.replace(" phenotype", "").title()

        display_labels = [
            clean(label) if label in system_colors else
            MODEL_SYSTEM_PHENOTYPE_ONTOLOGY_MAPPING[label] if label in model_set else
            (label if include_terms else "")   # show terms only when expanded
            for label in labels
        ]

        return dict(
            node=dict(
                label=display_labels,
                color=node_colors,
                x=x_positions if include_terms else None,
                pad=20,
                thickness=30,
                line=dict(color="black", width=0.5),
                hovertemplate='%{label}<extra></extra>'
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=link_colors
            )
        )

    # Building two plots, one with hpo terms shown and another with just systems
    sankey_with_terms = build_sankey(include_terms=True)
    sankey_no_terms = build_sankey(include_terms=False)

    fig = go.Figure(go.Sankey(**sankey_with_terms))

    # Updates the figure to have options to switch which plot to show
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.5,
                y=1.15,
                showactive=True,
                buttons=[
                    dict(
                        label="Show Terms",
                        method="update",
                        args=[{
                            "node": sankey_with_terms["node"],
                            "link": sankey_with_terms["link"]
                        }]
                    ),
                    dict(
                        label="Hide Terms",
                        method="update",
                        args=[{
                            "node": sankey_no_terms["node"],
                            "link": sankey_no_terms["link"]
                        }]
                    )
                ]
            )
        ],
        title=sankey_hpo_to_upheno_system_to_animal_model_systems(analysis_name),
        font=dict(size=11)
    )

    return fig

def sankey_homologous_phenotypes_and_modelsystem_close_only(data, analysis_name: str = ""):
    close_subset_data = [ record for record in data if record["distance" ] <= 4 ]
    return sankey_homologous_phenotypes_and_modelsystem(close_subset_data, analysis_name)

def sankey_homologous_phenotypes_and_modelsystem(data, analysis_name: str = ""):
    def distance_to_opacity(distance):
        min_d = 0
        max_d = 10

        # 2 -> 1.0
        # 6 -> 0.3

        return 1.0 - ((distance - min_d) / (max_d - min_d)) * 0.7

    # Color definitions
    MODEL_COLORS = {
        "Mammalian Phenotype": "#1f77b4",                        # blue
        "Xenopus Phenotype": "#2ca02c",                         # green
        "Worm Phenotype Ontology": "#ff7f0e",                   # orange
        "Zebrafish Phenotype": "#9467bd",                        # purple
        "FlyBase Controlled Vocabulary": "#e377c2",              # pink
        "Dictyostelium Discoideum Phenotype Ontology": "#FFEF00",# yellow
        "Pathogen-Host Interaction Phenotype Ontology": " #dc143c" #red
    }

    # Build node list
    nodes = set()

    for record in data:

        # phenotype nodes
        for term in record["terms"]:
            nodes.add(term)

        # homologous term nodes
        if record["closeHomologousTerm"]:
            nodes.add(record["closeHomologousTerm"])

        # model system nodes
        for model in record["homologousModelSystem"]:
            nodes.add(MODEL_SYSTEM_PHENOTYPE_ONTOLOGY_MAPPING[model])

    nodes = sorted(nodes)

    node_map = {
        node: node_index
        for node_index, node in enumerate(nodes)
    }

    # Build links
    sources = []
    targets = []
    values = []
    colors = []
    hover_text = []

    for record in data:

        if not record["closeHomologousTerm"]:
            continue
        homolog = record["closeHomologousTerm"]
        distance = record["distance"]

        alpha = distance_to_opacity(distance)

        # Human Phenotype Term to Homologous Phenotype Term
        for phenotype in set(record["terms"]):

            sources.append(node_map[phenotype])
            targets.append(node_map[homolog])
            values.append(1)

            # neutral gray link with opacity by distance
            colors.append(f"rgba(120,120,120,{alpha:.2f})")

            hover_text.append(
                f"{phenotype}<br>"
                f"→ {homolog}<br>"
                f"Distance: {distance}"
            )

        # Homologous Phenotype Term to Model System Phenotype Ontology
        for model in record["homologousModelSystem"]:
            mapped_model_name = MODEL_SYSTEM_PHENOTYPE_ONTOLOGY_MAPPING[model]

            sources.append(node_map[homolog])
            targets.append(node_map[mapped_model_name])
            values.append(1)

            # colors by animal model system with opacity by distance
            colors.append(hex_to_rgba(MODEL_COLORS[mapped_model_name],alpha))

            hover_text.append(
                f"{homolog}<br>"
                f"→ {mapped_model_name}<br>"
                f"Distance: {distance}"
            )

    # Node colors
    node_colors = []

    for node in nodes:

        if node in MODEL_COLORS:
            node_colors.append(MODEL_COLORS[node])
        else:
            node_colors.append("#BFBFBF")

    # Create Sankey
    fig = go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=20,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=node_colors,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors,
                customdata=hover_text,
                hovertemplate="%{customdata}<extra></extra>",
            ),
        )
    )

    fig.update_layout(
        title={
            "text": sankey_homologous_phenotype_terms_model_system(analysis_name),
            "x": 0.5,
        },
        font=dict(size=12),
        height=800,
    )
    return fig

def sankey_d3_homologous_phenotypes_and_modelsystem_template(data) -> str:
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