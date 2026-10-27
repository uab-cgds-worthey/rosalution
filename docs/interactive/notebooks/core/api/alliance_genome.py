import requests

class AllianceGenome:
    base_url = "https://www.alliancegenome.org/api"
    
    @staticmethod
    def orthologs(gene_human_hgnc_id: str):
        url = f"{AllianceGenome.base_url}/gene/{gene_human_hgnc_id}/orthologs?filter.stringency=stringent&limit=20&page=1"
        response = requests.get(
            url,
            verify=False,
            timeout=5,
        )
        
        ortholog_list = []
        response_json = response.json()

        for result in response_json['results']:
            generated_orthology = result.get('geneToGeneOrthologyGenerated', None)
            if not generated_orthology:
                continue
            target_ortholog_id = generated_orthology['objectGene']['primaryExternalId']
            ortholog_list.append(target_ortholog_id)
        
        return ortholog_list
    
    @staticmethod
    def has_models(model_system_id: str) -> bool:
        url = f"{AllianceGenome.base_url}/gene/{model_system_id}/models?asc=true&limit=20&page=1&sortBy=geneName"
        response = requests.get(
            url,
            verify=False,
            timeout=5,
        )

        response_json = response.json()
        return response_json['total'] > 0
