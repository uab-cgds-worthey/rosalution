"""Routes dedicated for annotation within the system"""

import pytest


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_get_annotations_by_gene_in_analysis(client, mock_access_token):
    """Testing that the annotations by gene endpoint returns the annotations correctly"""

    response = await client.get(
        "/analysis/CPAM0002/gene/VMA21", headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200
    assert len(response.json()) == 6


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_get_annotations_by_hgvs_varian_in_analysis(client, mock_access_token):
    """Testing that the annotations by HGVS variant endpoint returns the annotations correctly"""

    response = await client.get(
        "/analysis/CPAM0002/hgvsVariant/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert response.status_code == 200

    response_annotations = response.json()
    assert len(response_annotations['transcripts']) == 2
    assert response_annotations['ClinVar_Variation_Id'] == "581244"
    assert response_annotations['ClinVar_variant_url'] == "https://www.ncbi.nlm.nih.gov/clinvar/variation/581244"
