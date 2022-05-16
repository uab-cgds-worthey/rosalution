"""Analysis Routes Intergration test"""

def test_get_analyses(client):
    """Testing that the correct number of analyses were returned and in the right order"""
    # database_collections['analysis'].find()
    # database_collections['analysis'].find.return_value = {'trash': 'json'}

    response = client.get('/analysis/')
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[2]['name'] == 'CPAM0053'


def test_get_analysis_summary(client):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    response = client.get('/analysis/summary')
    assert len(response.json()) == 5
