"""Analysis Routes Integration test"""

import pytest

from ..test_utils import read_test_fixture

@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
async def test_get_analyses(client, mock_access_token):
    """Testing that the correct number of analyses were returned and in the right order"""

    response = await client.get("/analysis", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 2

    actual_analyses = [ analysis["name"] for analysis in response.json() ]
    assert "CPAM0047" in actual_analyses


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
async def test_get_analysis_summary(client, mock_access_token):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    response = await client.get("/analysis/summary", headers={"Authorization": "Bearer " + mock_access_token})
    assert len(response.json()) == 2


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_get_summary_by_name(client, mock_access_token):
    """Tests the summary_by_name endpoint"""
    response = await client.get("/analysis/CPAM0002/summary", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert response.json()["name"] == "CPAM0002"


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_get_genomic_units_success(client, mock_access_token):
    """ Testing the get genomic units endpoint """

    response = await client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    expected_genomic_unit_response = {
        "genes": {"VMA21": ["NM_001017980.3:c.164G>T(p.Gly55Val)"]},
        "variants": ["NM_001017980.3:c.164G>T(p.Gly55Val)"]
    }

    assert response.status_code == 200
    assert response.json() == expected_genomic_unit_response


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_get_genomic_units_analysis_does_not_exist(client, mock_access_token):
    """ Testing the get genomic units endpoint """

    response = await client.get("/analysis/CPAM12345/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


@pytest.mark.usefixtures("mock_security_get_project_authorization")
@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
async def test_get_genomic_units_does_not_exist(client, mock_access_token):
    """ Testing the get genomic units endpoint """

    response = await client.get("/analysis/CPAM12345/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_attach_third_party_link(client, mock_access_token):
    """ Testing the attach third party link endpoint """

    response = await client.put(
        "/analysis/CPAM0002/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "https://monday.com"}
    )

    assert response.status_code == 200

    analysis = response.json()
    assert "third_party_links" in analysis

    link_types = [ link["type"] for link in analysis["third_party_links"] ]
    assert "monday_com" in link_types


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_attach_third_party_link_analysis_does_not_exist(client, mock_access_token):
    """ Testing the attach third party link endpoint """

    response = await client.put(
        "/analysis/CPAM12345/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 409


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_attach_third_party_link_invalid_enum(client, mock_access_token):
    """ Testing the attach third party link endpoint """
    response = await client.put(
        "/analysis/CPAM0002/attach/BAD_ENUM",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 422


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_mark_ready(client, mock_access_token):
    """ Testing the update analysis event endpoint """

    response = await client.put("/analysis/CPAM0002/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200

    analysis = response.json()
    events = [ event["event"] for event in analysis["timeline"] ]
    assert "ready" in events


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_mark_ready_analysis_does_not_exist(client, mock_access_token):
    """ Testing the mark ready endpoint """

    response = await client.put("/analysis/CPAM2222/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 409
    assert response.json() == {'detail': 'Analysis with name CPAM2222 does not exist.'}


@pytest.fixture(name="exported_new_analysis_to_import_json")
def fixture_new_analysis_import():
    """Returns a new analysis json fixture"""
    return read_test_fixture("new-analysis-import.json")
