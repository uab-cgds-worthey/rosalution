import plotly.graph_objects as go
from collections import defaultdict

from .utils import hex_to_rgba

def sankey_gene_expressed_in_anatomy_plot(analysis_name: str):
    if not analysis_name:
        return "Rosalution Analysis Orthologous Gene → Expressed In → Animal Model Tissues"

    return f"Rosalution '{analysis_name}' Orthologous Gene → Expressed In → Animal Model Tissues"

def sankey_gene_to_expressed_in_anatomy(data: dict, analysis_name: str = ""):
    # Colors
    MODEL_COLORS = {
        "MGI": "#1f77b4",                        # blue
        "EMAPA": "#2ca02c",                         # green
        "WB": "#ff7f0e",                   # orange
        "ZFIN": "#9467bd",                        # purple
        "Zebrafish Phenotype": "#9467bd",                        # purple
        "FlyBase Controlled Vocabulary": "#e377c2",              # pink
        "Dictyostelium Discoideum Phenotype Ontology": "#FFEF00",# yellow
        "Pathogen-Host Interaction Phenotype Ontology": "#dc143c", #red
        "NCBIGene": "#ADD8E6"
    }

    # Build node list
    nodes = set()

    gene_label_text = lambda namesapce, name: f"{namesapce}-{name}"

    for gene, expressed_in in data.items():
        gene_namespace, gene_id, gene_name = gene
        # print(gene)
        # print(expressed_in)

        # phenotype nodes
        # for term in record["terms"]:
        nodes.add(gene_label_text(gene_namespace, gene_name))

        # homologous term nodes
        for tissue in expressed_in:
            # print(tissue)
            for tissue_key, anatomy in tissue.items():
                tissue_namespace, tissue_name = tissue_key
                # nodes.add(tissue_namespace)
                # print(anatomy)

                for anatomy_entry in anatomy:
                    nodes.add(anatomy_entry)

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

    print('building source and targets')
    for gene, expressed_in in data.items():
        gene_namespace, gene_id, gene_name = gene

        # Orthologous Gene to expressed in tissue
        for tissue in expressed_in:
            for tissue_key, anatomy in tissue.items():
                tissue_namesapce, tissue_name = tissue_key

                # Tissue to Model System Tissues
                for anatomy_entry in anatomy:
                    sources.append(node_map[gene_label_text(gene_namespace, gene_name)])
                    targets.append(node_map[anatomy_entry])
                    values.append(1)

                    # colors by animal model system with opacity by distance
                    colors.append(hex_to_rgba(MODEL_COLORS[gene_namespace],1.0))

                    hover_text.append(
                        f"{gene_namespace}<br>"
                        f"→ {anatomy_entry}"
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
            "text": sankey_gene_expressed_in_anatomy_plot(analysis_name),
            "x": 0.5,
        },
        font=dict(size=12),
        height=800,
    )
    return fig
