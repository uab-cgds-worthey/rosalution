import requests

from ..enums import ANIMAL_MODEL_TAXONOMY_ID_MAPPING

class Diopt:
    animal_model_taxonomy_id_mapping = ANIMAL_MODEL_TAXONOMY_ID_MAPPING
    base_url = "https://www.flyrnai.org/tools/diopt/web/diopt_api/v9/get_orthologs_from_entrez/9606"

    @staticmethod
    def best_score(geneEntrezId: str):
        models = ', '.join(str(model_key) for model_key in Diopt.animal_model_taxonomy_id_mapping.keys())
        url = f"{Diopt.base_url}/{geneEntrezId}/{models}/best"
        response = requests.get(
            url,
            verify=False,
            timeout=20,
        )
        return response.json()
