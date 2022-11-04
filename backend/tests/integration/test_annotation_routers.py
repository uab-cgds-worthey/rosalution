"""Routes dedicated for annotation within the system"""

from ..test_utils import read_test_fixture


def test_get_annotations_by_gene(client, mock_access_token, mock_repositories):
    """Testing that the annotations by gene endpoint returns the annotations correctly"""

    gene_annotations_fixture = read_test_fixture("annotations-VMA21.json")
    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_annotations_fixture
    response = client.get(
        "annotate/gene/VMA21",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert len(response.json()) == 2


def test_get_annotations_by_hgvs_variant(client, mock_access_token, mock_repositories):
    """Testing that the annotations by HGVS variant endpoint returns the annotations correctly"""

    variant_annotations_fixture = read_test_fixture("annotations-HGVS-Variant.json")
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_annotations_fixture
    response = client.get(
        "annotate/hgvsVariant/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    response_annotations = response.json()
    assert len(response_annotations['transcripts']) == 2
    assert response_annotations['ClinVar_Variantion_Id'] == "581244"
    assert response_annotations['ClinVar_variant_url'] == "https://www.ncbi.nlm.nih.gov/clinvar/variation/581244"
