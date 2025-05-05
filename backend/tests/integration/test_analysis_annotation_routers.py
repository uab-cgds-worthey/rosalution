"""Routes dedicated for annotation within the system"""


def test_get_annotations_by_gene_in_analysis(
    client, mock_access_token, mock_repositories, gene_vma21_annotations_json, cpam0002_analysis_json
):
    """Testing that the annotations by gene endpoint returns the annotations correctly"""

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_vma21_annotations_json
    response = client.get(
        "/analysis/CPAM0002/gene/VMA21",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_annotations_by_hgvs_varian_in_analysis(
    client, mock_access_token, mock_repositories, variant_nm001017980_3_c_164g_t_annotations_json,
    cpam0002_analysis_json
):
    """Testing that the annotations by HGVS variant endpoint returns the annotations correctly"""

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_nm001017980_3_c_164g_t_annotations_json
    response = client.get(
        "/analysis/CPAM0002/hgvsVariant/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    response_annotations = response.json()
    assert response.status_code == 200
    assert len(response_annotations['transcripts']) == 2
    assert response_annotations['ClinVar_Variation_Id'] == "581244"
    assert response_annotations['ClinVar_variant_url'] == "https://www.ncbi.nlm.nih.gov/clinvar/variation/581244"
