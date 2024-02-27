"""Routes dedicated for annotation within the system"""


def test_get_annotations_by_gene(client, mock_access_token, mock_repositories, gene_vma21_annotations_json):
    """Testing that the annotations by gene endpoint returns the annotations correctly"""

    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_vma21_annotations_json
    response = client.get(
        "annotation/gene/VMA21",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert len(response.json()) == 2


def test_get_annotations_by_hgvs_variant(
    client, mock_access_token, mock_repositories, variant_nm001017980_3_c_164g_t_annotations_json
):
    """Testing that the annotations by HGVS variant endpoint returns the annotations correctly"""
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_nm001017980_3_c_164g_t_annotations_json
    response = client.get(
        "annotation/hgvsVariant/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    response_annotations = response.json()
    assert len(response_annotations['transcripts']) == 2
    assert response_annotations['ClinVar_Variantion_Id'] == "581244"
    assert response_annotations['ClinVar_variant_url'] == "https://www.ncbi.nlm.nih.gov/clinvar/variation/581244"
