from neo4j import GraphDatabase

from .rosalution import Rosalution

class MonarchKnowledgeGraph:
    uri = "neo4j+s://neo4j.monarchinitiative.org:7687"
    auth= ("", "")
    upheno_terms_systems = [
        "UPHENO:0002964",
        "UPHENO:0004523",
        "UPHENO:0002764",
        "UPHENO:0002635",
        "UPHENO:0003020",
        "UPHENO:0080362",
        "HP:0001939",
        "UPHENO:0002642",
        "UPHENO:0002833",
        "HP:0002664",
        "UPHENO:0004459",
        "UPHENO:0002948",
        "UPHENO:0003116",
        "UPHENO:0002816",
        "UPHENO:0004536",
        "HP:0000598",
        "UPHENO:0002712",
        "UPHENO:0075949",
        "UPHENO:0049874",
        "UPHENO:0003013"
    ]

    @staticmethod
    def orthologous_phenotypic_systems(hpo_terms: list):
        with GraphDatabase.driver(MonarchKnowledgeGraph.uri, auth=MonarchKnowledgeGraph.auth) as driver:
            result = driver.execute_query("""
                MATCH (subjectHpo:`biolink:PhenotypicFeature`)
                WHERE subjectHpo.id IN $hpoTerms
                CALL(subjectHpo) {
                    MATCH path = (subjectHpo)-[:`biolink:subclass_of`*0..]->(ancestor)
                    WHERE ancestor.id IN $phenotypicSystems
                    RETURN
                        path,
                        ancestor,
                        length(path) AS distance
                    ORDER BY distance ASC
                    LIMIT 1
                }
                CALL (ancestor) {
                    MATCH descendantPath = (ancestor)<-[:`biolink:subclass_of`]-(descendant)
                    WHERE descendant.namespace <> "UPHENO"
                    RETURN descendantPath, descendant
                }
                RETURN  DISTINCT collect(DISTINCT subjectHpo.name) AS terms, ancestor.name AS system, ancestor.namespace AS system_source, collect(DISTINCT descendant.namespace) AS modelsystem
            """, hpoTerms=hpo_terms, phenotypicSystems=MonarchKnowledgeGraph.upheno_terms_systems, database_="neo4j")
            
            return [ record.data() for record in result.records ]

    # Final version of the query includes the target species namespaces in the knowledge graph to filter out animal models that are not
    # being included in our analysis
    @staticmethod
    def homologous_phenotypic_terms_by_model_systems(hpo_terms: list):
        with GraphDatabase.driver(MonarchKnowledgeGraph.uri, auth=MonarchKnowledgeGraph.auth) as driver:
            result = driver.execute_query("""
                MATCH (subjectHpo:`biolink:PhenotypicFeature`)
                WHERE subjectHpo.id IN $hpoTerms
                WITH subjectHpo, ['MP', 'XPO', 'WBPhenotype', 'ZP'] AS homologousNamespaces
                UNWIND homologousNamespaces as homologousNamespace
                CALL(subjectHpo, homologousNamespace) {
                    MATCH path = (subjectHpo)-[:`biolink:subclass_of`*0..]->(closest_ancestor)<-[:`biolink:homologous_to`]-(homologous_to_ancestor {namespace: homologousNamespace})
                    RETURN
                        path,
                        closest_ancestor,
                        homologous_to_ancestor,
                        length(path) AS distance
                    ORDER BY distance ASC
                    LIMIT 1
                }
                RETURN  DISTINCT collect(subjectHpo.name) AS terms, distance, homologous_to_ancestor.name AS closeHomologousTerm, collect(DISTINCT homologous_to_ancestor.namespace) AS homologousModelSystem
            """, hpoTerms=hpo_terms, database_="neo4j")

            return [ record.data() for record in result.records ]

    @staticmethod
    def no_homologous_phenotypic_terms_by_model_systems(hpo_terms: list):
        with GraphDatabase.driver(MonarchKnowledgeGraph.uri, auth=MonarchKnowledgeGraph.auth) as driver:
            result = driver.execute_query("""
                MATCH (subjectHpo:`biolink:PhenotypicFeature`)
                WHERE subjectHpo.id IN $hpoTerms
                WITH subjectHpo, ['MP', 'XPO', 'WBPhenotype', 'ZP'] AS homologousNamespaces
                UNWIND homologousNamespaces as homologousNamespace
                OPTIONAL CALL(subjectHpo, homologousNamespace) {
                    MATCH path = (subjectHpo)-[:`biolink:subclass_of`*0..]->(closest_ancestor)<-[:`biolink:homologous_to`]-(homologous_to_ancestor {namespace: homologousNamespace})
                    RETURN
                        path,
                        closest_ancestor,
                        homologous_to_ancestor,
                        length(path) AS distance
                    ORDER BY distance ASC
                    LIMIT 1
                }
                WITH subjectHpo, count(path) as pathsFound
                WHERE pathsFound = 0
                RETURN collect(subjectHpo.name) AS terms
            """, hpoTerms=hpo_terms, database_="neo4j")

            return [ term for record in result.records for term in record.data()['terms'] if 'terms' in record.data() and len(record.data()['terms']) ]

    @staticmethod
    def orthologous_gene_expression_of_tissue(gene_hgnc_id: str):
        with GraphDatabase.driver(MonarchKnowledgeGraph.uri, auth=MonarchKnowledgeGraph.auth) as driver:
            result = driver.execute_query("""
                MATCH (g:`biolink:Gene` {id: $hgncId})-[relationship:`biolink:orthologous_to`]-(g2:`biolink:Gene`)
                -[p_relationship:`biolink:expressed_in`]->(t)-[:`biolink:subclass_of`]-(anatomy {namespace: "UBERON"})
                WHERE NOT g2.namespace IN ["PomBase", "FB", "SGD", "NCBIGene"]
                RETURN DISTINCT g2.namespace as orthologous_gene_namesapce, g2.id as orthologous_gene_id, g2.name as orthologous_gene_name, t.namespace as tissue_namespace, t.name as tissue_name, COLLECT(DISTINCT anatomy.name) as anatomy
            """, hgncId=gene_hgnc_id, database_="neo4j")
            data = {}
            for record in result.records:
                key = (record["orthologous_gene_namesapce"], record["orthologous_gene_id"], record["orthologous_gene_name"])
                
                entry = {(record["tissue_namespace"], record["tissue_name"]): record["anatomy"]};
                data.setdefault(key, []).append(entry)
            return data

            # return [ record.data() for record in result.records ]
            # return [ term for record in result.records for term in record.data()['terms']) ]

    @staticmethod
    def gene_expression_across_orthologous_genes(gene_hgnc_id: str):
        with GraphDatabase.driver(MonarchKnowledgeGraph.uri, auth=MonarchKnowledgeGraph.auth) as driver:
            result = driver.execute_query("""
                MATCH (g:`biolink:Gene` {id: $hgncId})-[relationship:`biolink:orthologous_to`]-(g2:`biolink:Gene`)
                -[p_relationship:`biolink:expressed_in`]->(s)-[:`biolink:subclass_of`]-(u {namespace:'UBERON'})
                RETURN DISTINCT u.id + "-" + u.name AS terms
            """, hgncId=gene_hgnc_id, database_="neo4j")

            return [ record.data()['terms'] for record in result.records ]
            # return [ term for record in result.records for term in record.data()['terms']) ]

class RosalutionMonarch(object):
    def __init__(self, rosalution_analysis: Rosalution):
        self.analysis = rosalution_analysis

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return True

    def rosalution_orthologous_phenotypic_systems(self):
        terms = self.analysis.get_analysis_hpo_terms()
        if len(terms) == 0:
            return []
        return MonarchKnowledgeGraph.orthologous_phenotypic_systems(terms)

    def rosalution_homologous_phenotypic_terms(self):
        terms = self.analysis.get_analysis_hpo_terms()
        if len(terms) == 0:
            return []
        return MonarchKnowledgeGraph.homologous_phenotypic_terms_by_model_systems(terms)

    def rosalution_no_homologous_phenotypic_terms(self):
        terms = self.analysis.get_analysis_hpo_terms()
        if len(terms) == 0:
            return []
        return MonarchKnowledgeGraph.no_homologous_phenotypic_terms_by_model_systems(terms)